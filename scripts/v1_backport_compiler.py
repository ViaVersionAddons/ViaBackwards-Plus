"""
ViaBackwards v1 Resource Pack Compiler

This script automates the backporting of new items for the legacy (v1) resource pack branch, 
which relies on OptiFine CIT and Chime to assign textures to NBT-tagged items.

FUTURE UPDATE GUIDE (e.g., for 26.3):
1. First, set up the standard v2 overlays (e.g., `backport_to_26_2` folder) with all the raw assets and carrier models.
2. Ensure the Mappings repository has been updated with the new `mapping-26.3to26.2.json` and registry files.
3. Update `VERSION_STEPS` in this script to include ("26.3", "26.2").
4. Add "26.3" to the `targeted_transitions` list.
5. Run this script! It will safely append the new Chime and CIT overrides without overwriting older backported assets.

WORKSPACE REQUIREMENTS:
By default, this script assumes:
- You are running it from the root of the `ViaBackwards-Plus` repository.
- The `Mappings` repository (https://github.com/ViaVersion/Mappings) is cloned as a sibling directory (e.g., `../Mappings`).
You can override these paths using the MAPPINGS_DIR and VBACK_DIR environment variables for CI/CD usage.
"""

import json
import os
import shutil
from pathlib import Path

# Paths (Overrideable via environment variables for CI/CD portability)
# Default assumes script is run from ViaBackwards-Plus root, and Mappings is a sibling directory.
MAPPINGS_DIR = Path(os.environ.get("MAPPINGS_DIR", "../Mappings/mappings")).resolve()
V2_SOURCE_DIR = Path(os.environ.get("V2_SOURCE_DIR", "../ViaBackwards-Plus")).resolve()
V1_TARGET_DIR = Path(os.environ.get("V1_TARGET_DIR", "../v1-branch")).resolve()

# Descending list of version transitions to follow
VERSION_STEPS = [
    ("26.2", "26.1"),
    ("26.1", "1.21.11"),
    ("1.21.11", "1.21.9"),
    ("1.21.9", "1.21.7"),
    ("1.21.7", "1.21.6"),
    ("1.21.6", "1.21.5"),
    ("1.21.5", "1.21.4"),
    ("1.21.4", "1.21.2"),
    ("1.21.2", "1.21"),
    ("1.21", "1.20.5"),
    ("1.20.5", "1.20.3"),
    ("1.20.3", "1.20.2"),
    ("1.20.2", "1.20"),
    ("1.20", "1.19.4"),
    ("1.19.4", "1.19.3"),
    ("1.19.3", "1.19"),
    ("1.19", "1.18"),
    ("1.18", "1.17"),
    ("1.17", "1.16.2"),
    ("1.16.2", "1.16")
]

def load_json(path):
    if not path.exists():
        return {}
    with open(path, 'r', encoding='utf-8') as f:
        return json.load(f)

def save_json(path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=2)

def get_protocol_name(v_from, v_to):
    v_from_str = v_from.replace(".", "_")
    v_to_str = v_to.replace(".", "_")
    return f"Protocol{v_from_str}To{v_to_str}"

def resolve_path(namespace_str, asset_type):
    if namespace_str.startswith("minecraft:"):
        namespace_str = namespace_str[len("minecraft:"):]
    
    if asset_type == "model":
        return Path("models") / f"{namespace_str}.json"
    elif asset_type == "texture":
        return Path("textures") / f"{namespace_str}.png"
    return None

def extract_models(node, target_item_with_ns, item_name, current_nbt=None, is_matched=False):
    if current_nbt is None:
        current_nbt = {}
    if not isinstance(node, dict):
        return []
        
    mtype = node.get("type")
    results = []
    
    if mtype == "minecraft:select":
        prop = node.get("property")
        
        if is_matched:
            if prop == "minecraft:display_context":
                for case in node.get("cases", []):
                    when_val = case.get("when")
                    if isinstance(when_val, list) and "gui" in when_val:
                        results.extend(extract_models(case.get("model"), target_item_with_ns, item_name, current_nbt, True))
                        return results
                    elif isinstance(when_val, str) and when_val == "gui":
                        results.extend(extract_models(case.get("model"), target_item_with_ns, item_name, current_nbt, True))
                        return results
                results.extend(extract_models(node.get("fallback"), target_item_with_ns, item_name, current_nbt, True))
                return results
                
            elif prop == "minecraft:trim_material":
                for case in node.get("cases", []):
                    when_val = case.get("when")
                    if isinstance(when_val, str):
                        new_nbt = current_nbt.copy()
                        new_nbt["Trim"] = {"material": when_val}
                        results.extend(extract_models(case.get("model"), target_item_with_ns, item_name, new_nbt, True))
                results.extend(extract_models(node.get("fallback"), target_item_with_ns, item_name, current_nbt, True))
                return results
                
            else:
                results.extend(extract_models(node.get("fallback"), target_item_with_ns, item_name, current_nbt, True))
                return results
                
        else:
            if prop == "minecraft:custom_model_data":
                for case in node.get("cases", []):
                    when_val = case.get("when")
                    is_match = False
                    if isinstance(when_val, str) and when_val == target_item_with_ns:
                        is_match = True
                    elif isinstance(when_val, list) and target_item_with_ns in when_val:
                        is_match = True
                    
                    if is_match:
                        results.extend(extract_models(case.get("model"), target_item_with_ns, item_name, current_nbt, True))
                        return results
                        
                results.extend(extract_models(node.get("fallback"), target_item_with_ns, item_name, current_nbt, False))
                return results
                
            elif prop == "minecraft:component" and node.get("component") == "minecraft:custom_name":
                for case in node.get("cases", []):
                    when_val = case.get("when")
                    if isinstance(when_val, dict):
                        text = when_val.get("text", "").lower().replace(" ", "_")
                        if item_name in text:
                            results.extend(extract_models(case.get("model"), target_item_with_ns, item_name, current_nbt, True))
                            return results
                            
                results.extend(extract_models(node.get("fallback"), target_item_with_ns, item_name, current_nbt, False))
                return results
                
            else:
                results.extend(extract_models(node.get("fallback"), target_item_with_ns, item_name, current_nbt, False))
                return results
            
    elif mtype == "minecraft:model":
        if is_matched:
            model_str = node.get("model")
            if model_str:
                results.append((model_str, current_nbt))
        return results
        
    elif mtype == "minecraft:condition":
        results.extend(extract_models(node.get("on_true"), target_item_with_ns, item_name, current_nbt, is_matched))
        return results
        
    elif mtype == "minecraft:range_dispatch":
        results.extend(extract_models(node.get("fallback"), target_item_with_ns, item_name, current_nbt, is_matched))
        return results
        
    return results

def extract_model_for_item_from_carrier(carrier_path, item_name):
    if not carrier_path.exists():
        return []
    data = load_json(carrier_path)
    target_item_with_ns = f"minecraft:{item_name}"
    return extract_models(data.get("model"), target_item_with_ns, item_name, None, False)

def main():
    print("Loading mapping data and registries...")
    registries = {}
    diffs = {}
    
    all_versions = set()
    for v_from, v_to in VERSION_STEPS:
        all_versions.add(v_from)
        all_versions.add(v_to)
        
    for v in all_versions:
        reg_path = MAPPINGS_DIR / f"mapping-{v}.json"
        if reg_path.exists():
            data = load_json(reg_path)
            items_list = data.get("items", [])
            registries[v] = {item: idx for idx, item in enumerate(items_list)}
            print(f"Loaded registry for {v}: {len(items_list)} items")
            
    for v_from, v_to in VERSION_STEPS:
        diff_path = MAPPINGS_DIR / "diff" / f"mapping-{v_from}to{v_to}.json"
        if diff_path.exists():
            diffs[(v_from, v_to)] = load_json(diff_path).get("items", {})
            print(f"Loaded diff {v_from} to {v_to}: {len(diffs[(v_from, v_to)])} mapped items")
            
    targeted_transitions = [step for step in VERSION_STEPS if step[0] in ["26.2", "26.1", "1.21.11", "1.21.9", "1.21.7", "1.21.6", "1.21.5"]]
    
    compiled_items = []
    
    for v_from, v_to in targeted_transitions:
        items_map = diffs.get((v_from, v_to), {})
        protocol_name = get_protocol_name(v_from, v_to)
        
        for new_item, carrier in items_map.items():
            if v_from not in registries or new_item not in registries[v_from]:
                print(f"Warning: {new_item} not found in registry {v_from}")
                continue
                
            origin_id = registries[v_from][new_item]
            
            carriers_chain = []
            curr = carrier
            if curr.endswith("["):
                curr = curr[:-1]
            carriers_chain.append(curr)
            
            start_index = VERSION_STEPS.index((v_from, v_to)) + 1
            for step_from, step_to in VERSION_STEPS[start_index:]:
                step_diff = diffs.get((step_from, step_to), {})
                if curr in step_diff:
                    next_carrier = step_diff[curr]
                    if next_carrier.endswith("["):
                        next_carrier = next_carrier[:-1]
                    if next_carrier not in carriers_chain:
                        carriers_chain.append(next_carrier)
                    curr = next_carrier
                    
            compiled_items.append({
                "item": new_item,
                "protocol": protocol_name,
                "origin_id": origin_id,
                "carriers": carriers_chain,
                "first_carrier": carrier.split("[")[0],
                "final_carrier": curr,
                "v_to": v_to
            })
            
    print(f"Resolved {len(compiled_items)} item definitions to backport.")
    
    for item_data in compiled_items:
        new_item = item_data["item"]
        protocol = item_data["protocol"]
        origin_id = item_data["origin_id"]
        carriers = item_data["carriers"]
        first_carrier = item_data["first_carrier"]
        v_to_folder = item_data["v_to"].replace(".", "_")
        
        print(f"Processing: {new_item} (Protocol: {protocol}, ID: {origin_id}, Carriers: {carriers})")
        
        # Determine the source model path from the v2 item carrier definition
        # Dynamically discover and sort overlay folders (descending order)
        def parse_version(folder_name):
            parts = folder_name.replace("backport_to_", "").split("_")
            return [int(p) if p.isdigit() else 0 for p in parts]
            
        all_dirs = [d.name for d in V2_SOURCE_DIR.iterdir() if d.is_dir() and d.name.startswith("backport_to_")]
        possible_folders = sorted(all_dirs, key=parse_version, reverse=True)
        
        carrier_json_path = None
        target_model_id = None
        
        for folder in possible_folders:
            test_dir = V2_SOURCE_DIR / folder / "assets" / "minecraft"
            test_path = test_dir / "items" / f"{first_carrier}.json"
            if test_path.exists():
                target = extract_model_for_item_from_carrier(test_path, new_item)
                if target:
                    carrier_json_path = test_path
                    target_model_id = target
                    break
                    
        if not target_model_id:
            target_model_id = [(f"minecraft:item/{new_item}", {})]
            
        # 1. CHIME OVERRIDES INJECTIONS (we do this first to prep the data)
        predicate_tag = f"VB|{protocol}|id"
        
        for carrier in carriers:
            chime_file = V1_TARGET_DIR / "assets" / "minecraft" / "overrides" / "item" / f"{carrier}.json"
            if chime_file.exists():
                chime_data = load_json(chime_file)
            else:
                chime_data = {"overrides": []}
            if "overrides" not in chime_data:
                chime_data["overrides"] = []
                
            for t_model_id, t_nbt in target_model_id:
                if t_model_id.startswith("minecraft:"):
                    t_model_id = t_model_id[10:]
                    
                exists = False
                for override in chime_data["overrides"]:
                    pred = override.get("predicate", {}).get("nbt", {})
                    is_match = True
                    if pred.get(predicate_tag) != origin_id:
                        is_match = False
                    
                    for k, v in t_nbt.items():
                        if pred.get(k) != v:
                            is_match = False
                            
                    if is_match and len(pred) == len(t_nbt) + 1:
                        print(f"DEBUG: Overwriting existing override {predicate_tag}={origin_id} from {override.get('model')} to {t_model_id}")
                        override["model"] = t_model_id
                        exists = True
                        break
                        
                        
                if not exists:
                    new_override = {
                        "predicate": {
                            "nbt": {
                                predicate_tag: origin_id
                            }
                        },
                        "model": t_model_id
                    }
                    for k, v in t_nbt.items():
                        new_override["predicate"]["nbt"][k] = v
                    chime_data["overrides"].append(new_override)
                        
            save_json(chime_file, chime_data)

        # 2. ASSET COPY & OPTIFINE CIT
        def resolve_src(rel_path):
            for folder in possible_folders:
                test_src = V2_SOURCE_DIR / folder / "assets" / "minecraft" / rel_path
                if test_src.exists():
                    return test_src
            return None

        def copy_asset(rel_path):
            src = resolve_src(rel_path)
            if not src:
                return False
            dst = V1_TARGET_DIR / "assets" / "minecraft" / rel_path
            dst.parent.mkdir(parents=True, exist_ok=True)
            if not dst.exists():
                if rel_path.suffix == ".json":
                    raw_model_data = load_json(src)
                    sanitized_model = {}
                    for key in ["parent", "textures", "display", "elements", "gui_light", "ambientocclusion"]:
                        if key in raw_model_data:
                            sanitized_model[key] = raw_model_data[key]
                    save_json(dst, sanitized_model)
                else:
                    shutil.copy2(src, dst)
            return True

        def crawl_model(rel_path):
            src = resolve_src(rel_path)
            if not src: return
            copy_asset(rel_path)
            model_data = load_json(src)
            if "parent" in model_data:
                parent_val = model_data["parent"]
                if not parent_val.startswith("builtin/"):
                    parent_rel = resolve_path(parent_val, "model")
                    if parent_rel: crawl_model(parent_rel)
            if "textures" in model_data:
                for tex_val in model_data["textures"].values():
                    if isinstance(tex_val, str) and not tex_val.startswith("#"):
                        tex_rel = resolve_path(tex_val, "texture")
                        if tex_rel: copy_asset(tex_rel)

        for t_model_id, t_nbt in target_model_id:
            if t_model_id.startswith("minecraft:"):
                t_model_id = t_model_id[10:]
            print(f"  Resolved model path: {t_model_id} with NBT {t_nbt}")
            
            # CIT GENERATION
            match_items_str = " ".join(carriers)
            cit_dir = V1_TARGET_DIR / "assets" / "minecraft" / "optifine" / "cit" / "backports" / new_item
            cit_dir.mkdir(parents=True, exist_ok=True)
            
            nbt_suffix = ""
            if "Trim" in t_nbt:
                trim_mat = t_nbt["Trim"]["material"].replace("minecraft:", "")
                nbt_suffix = f"_{trim_mat}_trim"
                
            nbt_lines = f"nbt.VB|{protocol}|id={origin_id}\n"
            if "Trim" in t_nbt:
                nbt_lines += f"nbt.Trim.material={t_nbt['Trim']['material']}\n"
                
            properties_content = f"type=item\nmatchItems={match_items_str}\nmodel={t_model_id}\n{nbt_lines}"
            with open(cit_dir / f"{new_item}{nbt_suffix}.properties", "w", encoding="utf-8") as f:
                f.write(properties_content)
                
            model_rel = Path("models") / f"{t_model_id}.json"
            crawl_model(model_rel)
                                
    print("Sorting Chime overrides to prioritize newer protocols...")
    protocol_indices = {}
    for i, step in enumerate(VERSION_STEPS):
        protocol_indices[get_protocol_name(step[0], step[1])] = i

    def get_override_index(override):
        pred = override.get("predicate", {}).get("nbt", {})
        proto_idx = 999
        for key in pred.keys():
            if key.startswith("VB|") and key.endswith("|id"):
                proto = key.split("|")[1]
                if proto in protocol_indices:
                    proto_idx = protocol_indices[proto]
        # Return a tuple: higher protocol index (newer) first, then more keys first.
        # Since reverse=True, we use (999 - proto_idx) to make proto 0 the largest value,
        # so proto 0 (newest) appears at the top.
        return (999 - proto_idx, len(pred.keys()))
        
    overrides_dir = V1_TARGET_DIR / "assets" / "minecraft" / "overrides" / "item"
    if overrides_dir.exists():
        for filepath in overrides_dir.glob("*.json"):
            data = load_json(filepath)
            if "overrides" in data and isinstance(data["overrides"], list):
                data["overrides"].sort(key=get_override_index, reverse=True)
                save_json(filepath, data)

    print("CIT and Chime compilation finished successfully!")

if __name__ == "__main__":
    main()
