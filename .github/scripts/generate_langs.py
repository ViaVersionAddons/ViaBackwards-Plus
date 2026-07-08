import os
import re
import json
import zipfile
import io
import urllib.request
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor

# ==========================================
# Configuration Constants
# ==========================================
# Read from environment variables (set by GitHub Actions), fallback to defaults for local execution
MIN_VERSION = os.environ.get("MIN_VERSION", "1.21.4")

MAX_VERSION = os.environ.get("MAX_VERSION", None)
if MAX_VERSION == "None" or MAX_VERSION == "":
    MAX_VERSION = None

OUTPUT_DIR = "assets/minecraft/lang"

# API and CDN URLs
VERSION_MANIFEST_URL = "https://piston-meta.mojang.com/mc/game/version_manifest_v2.json"
RESOURCES_CDN_URL = "https://resources.download.minecraft.net"

# ==========================================
# Version Parsing and Helpers
# ==========================================
def parse_version(v_str):
    """Parses a version string into a list of integers (e.g. '1.20.5' -> [1, 20, 5])"""
    cleaned = re.sub(r'[^0-9.]', '', v_str)
    return [int(x) for x in cleaned.split('.') if x]

def resolve_mappings_dir():
    """Resolves the path to the Mappings repository mappings/ directory."""
    env_dir = os.environ.get("MAPPINGS_DIR")
    if env_dir:
        print(f"Using MAPPINGS_DIR from environment: {env_dir}")
        return Path(env_dir)
    
    # Try common local development/CI layout paths
    project_root = Path(__file__).resolve().parents[2]
    candidates = [
        project_root.parent / "Mappings" / "mappings",
        project_root / "Mappings" / "mappings"
    ]
    for cand in candidates:
        if cand.exists():
            print(f"Discovered Mappings directory: {cand}")
            return cand
            
    # Default fallback
    print(f"Defaulting to mappings path candidate: {candidates[0]}")
    return candidates[0]

# ==========================================
# Phase A: Discovering Backported Assets

# ==========================================
def discover_backported_ids(mappings_dir, min_ver_str, max_ver_str):
    """Scans diff mappings and returns a tuple of (item_ids, entity_ids, resolved_max_version)"""
    diff_dir = mappings_dir / "diff"
    if not diff_dir.exists():
        raise FileNotFoundError(f"Diff directory does not exist: {diff_dir}")
        
    min_ver = parse_version(min_ver_str)
    max_ver = parse_version(max_ver_str) if max_ver_str else None
    
    # First, list all versions to find the highest if auto-detecting
    all_versions = []
    for filename in os.listdir(diff_dir):
        m = re.match(r'mapping-(.+)to(.+)\.json', filename)
        if m:
            v_from_str, v_to_str = m.groups()
            try:
                all_versions.append((v_from_str, parse_version(v_from_str)))
                all_versions.append((v_to_str, parse_version(v_to_str)))
            except ValueError:
                continue
                
    if not all_versions:
        raise ValueError(f"No valid mapping diff files found in {diff_dir}")
        
    # Find highest mapped version in diffs
    all_versions.sort(key=lambda x: x[1])
    highest_ver_str, highest_ver = all_versions[-1]
    
    resolved_max_ver = max_ver if max_ver else highest_ver
    resolved_max_ver_str = max_ver_str if max_ver_str else highest_ver_str
    
    if resolved_max_ver < min_ver:
        raise ValueError(
            f"MAX_VERSION ({resolved_max_ver_str}) must be greater than "
            f"MIN_VERSION ({min_ver_str}). Please check your configuration."
        )
    
    item_ids = set()
    entity_ids = set()
    custom_model_data_ids = set()  # Items that have a custom_model_data number assigned
    
    # Process files matching within range
    for filename in os.listdir(diff_dir):
        m = re.match(r'mapping-(.+)to(.+)\.json', filename)
        if m:
            v_from_str, v_to_str = m.groups()
            try:
                v_from = parse_version(v_from_str)
                v_to = parse_version(v_to_str)
            except ValueError:
                continue
                
            # Only process new-to-old (backwards) diffs
            if (v_from > v_to and
                v_from >= min_ver and v_from <= resolved_max_ver and
                v_to >= min_ver and v_to <= resolved_max_ver):
                file_path = diff_dir / filename
                print(f"Scanning diff mappings in {filename}...")
                with open(file_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    
                    # Extract items
                    for k in data.get("items", {}).keys():
                        k_clean = k.split('[')[0] if '[' in k else k
                        item_ids.add(k_clean)
                        
                    # Extract entities
                    for k in data.get("entities", {}).keys():
                        entity_ids.add(k)
                        
                    # Extract items that have a custom_model_data number assigned —
                    # these are genuinely new items, not just vanilla renames
                    for k in data.get("custom_model_data", {}).keys():
                        custom_model_data_ids.add(k)
                        
    return item_ids, entity_ids, custom_model_data_ids, resolved_max_ver_str

# ==========================================
# Phase B: Retrieving Translations from Mojang
# ==========================================
def fetch_json(url):
    """Helper to fetch JSON from a URL with standard user agent."""
    req = urllib.request.Request(
        url, 
        headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
    )
    with urllib.request.urlopen(req) as r:
        return json.loads(r.read().decode('utf-8'))

def resolve_mojang_version(version_str):
    """Locates the metadata URL for the target Mojang version.
    
    Matches the resolved MAX_VERSION (e.g. '26.3') against the Mojang manifest,
    first by exact ID, then by prefix (e.g. '26.3' -> '26.3-snapshot-3').
    """
    print("Fetching Mojang version manifest...")
    manifest = fetch_json(VERSION_MANIFEST_URL)
    
    # Exact match first
    for v in manifest['versions']:
        if v['id'] == version_str:
            return v['id'], v['url']
    # Prefix match: '26.3' matches '26.3-snapshot-3'
    for v in manifest['versions']:
        if v['id'].startswith(version_str):
            return v['id'], v['url']
    raise ValueError(
        f"Mojang version matching '{version_str}' not found in manifest. "
        f"Check that MAX_VERSION corresponds to a real Mojang release."
    )

def extract_en_us(client_jar_url):
    """Downloads Mojang's client JAR and extracts en_us.json."""
    print(f"Downloading client JAR to extract en_us.json ({client_jar_url})...")
    req = urllib.request.Request(
        client_jar_url, 
        headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
    )
    with urllib.request.urlopen(req) as r:
        jar_data = r.read()
        
    print("Extracting assets/minecraft/lang/en_us.json from client JAR...")
    with zipfile.ZipFile(io.BytesIO(jar_data)) as z:
        with z.open('assets/minecraft/lang/en_us.json') as f:
            return json.loads(f.read().decode('utf-8'))

def download_lang_file(lang_key, obj_info, version_id, cache_dir):
    """Downloads a single translation file from Mojang CDN, or returns from cache."""
    lang_code = lang_key.split('/')[-1].replace('.json', '')
    cache_file = cache_dir / version_id / f"{lang_code}.json"
    
    if cache_file.exists():
        try:
            with open(cache_file, 'r', encoding='utf-8') as f:
                return lang_code, json.load(f)
        except Exception:
            pass  # Fallback to downloading if cache read fails
            
    h = obj_info['hash']
    first_two = h[:2]
    url = f"{RESOURCES_CDN_URL}/{first_two}/{h}"
    
    try:
        req = urllib.request.Request(
            url, 
            headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
        )
        with urllib.request.urlopen(req, timeout=15) as r:
            content = r.read().decode('utf-8')
            data = json.loads(content)
            
        # Write to cache
        cache_file.parent.mkdir(parents=True, exist_ok=True)
        with open(cache_file, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False)
            
        return lang_code, data
    except Exception as e:
        print(f"Error downloading language file for '{lang_code}': {e}")
        return lang_code, None

def download_all_languages(asset_index, version_id, cache_dir):
    """Concurrent download of all non-English translation files."""
    lang_objects = {
        k: v for k, v in asset_index['objects'].items() 
        if k.startswith('minecraft/lang/') and k.endswith('.json')
    }
    print(f"Found {len(lang_objects)} language files in Mojang asset index.")
    
    langs_data = {}
    with ThreadPoolExecutor(max_workers=16) as executor:
        futures = {
            executor.submit(download_lang_file, k, v, version_id, cache_dir): k 
            for k, v in lang_objects.items()
        }
        for fut in futures:
            lang_code, data = fut.result()
            if data:
                langs_data[lang_code] = data
                
    return langs_data

# ==========================================
# Phase C: Remapping and Safe Write/Merge
# ==========================================
def map_and_merge_translations(item_ids, entity_ids, custom_model_data_ids, langs_data, output_dir):
    """Maps items/entities to the required keys and merges with existing files."""
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Only translate items that have a custom_model_data number in the diff mappings.
    # Items without one are vanilla renames (e.g. iron_chain) that the client already knows.
    excluded_items = item_ids - custom_model_data_ids
    allowed_item_ids = item_ids & custom_model_data_ids
    if excluded_items:
        print(f"Excluding {len(excluded_items)} items without custom_model_data (vanilla renames): {sorted(excluded_items)}")
    print(f"Writing translation files (for {len(allowed_item_ids)} items and {len(entity_ids)} entities) to {output_dir}...")
    
    mapped_count = 0
    for lang_code, translations in langs_data.items():
        mapped = {}
        
        # Map item/block IDs (only those with a custom_model_data assignment)
        for item_id in sorted(allowed_item_ids):
            item_key = f"item.minecraft.{item_id}"
            block_key = f"block.minecraft.{item_id}"
            
            # Check item translation, fallback to block translation
            translation_val = None
            if item_key in translations:
                translation_val = translations[item_key]
            elif block_key in translations:
                translation_val = translations[block_key]
                
            if translation_val is not None:
                if lang_code.lower() != 'en_us':
                    mapped[f"vb.item.{item_id}"] = translation_val
                mapped[item_key] = translation_val
                mapped[block_key] = translation_val
                
        # Map entity IDs
        for entity_id in sorted(entity_ids):
            entity_key = f"entity.minecraft.{entity_id}"
            if entity_key in translations:
                translation_val = translations[entity_key]
                if lang_code.lower() != 'en_us':
                    mapped[f"vb.entity.{entity_id}"] = translation_val
                mapped[entity_key] = translation_val
                
        if not mapped:
            continue
            
        out_file = output_dir / f"{lang_code.lower()}.json"
        
        # Safe Merge Protocol: load existing values if the file is already present
        existing = {}
        if out_file.exists():
            try:
                with open(out_file, 'r', encoding='utf-8') as f:
                    existing = json.load(f)
            except Exception as e:
                print(f"Warning: Failed to load existing translations from {out_file.name}: {e}")
                
        # Merge new mapped items into existing structure
        merged = {**existing, **mapped}
        
        # Write merged translations with 4-space indent
        with open(out_file, 'w', encoding='utf-8') as f:
            json.dump(merged, f, indent=4, ensure_ascii=False)
        mapped_count += 1
        
    print(f"Finished remapping and writing/merging {mapped_count} translation files.")

# ==========================================
# Main Execution Flow
# ==========================================
def main():
    # Resolve project root and paths
    project_root = Path(__file__).resolve().parents[2]
    mappings_dir = resolve_mappings_dir()
    output_dir = project_root / OUTPUT_DIR
    cache_dir = project_root / ".cache" / "lang"
    
    # 1. Discover backported items and entities
    print("--- Phase 1: Discovering Backported Assets ---")
    item_ids, entity_ids, custom_model_data_ids, resolved_max_ver = discover_backported_ids(mappings_dir, MIN_VERSION, MAX_VERSION)
    print(f"Discovered {len(item_ids)} backported items/blocks, {len(entity_ids)} backported entities, and {len(custom_model_data_ids)} with custom_model_data.")
    
    if not item_ids and not entity_ids:
        print("No items or entities found in the configured version range. Exiting.")
        return
        
    # 2. Retrieve Mojang version details and assets
    print("\n--- Phase 2: Resolving Mojang Translations ---")
    # Always derive the translation source from MAX_VERSION — no separate override needed.
    version_id, version_url = resolve_mojang_version(resolved_max_ver)
    print(f"Resolved Mojang translation source version: {version_id}")
    
    version_meta = fetch_json(version_url)
    
    # Download all translations (English from JAR, others from CDN)
    langs_data = {}
    
    # A. English (en_us) from Client JAR
    try:
        client_jar_url = version_meta['downloads']['client']['url']
        en_us_translations = extract_en_us(client_jar_url)
        langs_data['en_us'] = en_us_translations
    except Exception as e:
        print(f"Warning: Could not fetch/extract en_us.json from client JAR: {e}")
        
    # B. Other languages from asset index
    asset_index_url = version_meta['assetIndex']['url']
    asset_index = fetch_json(asset_index_url)
    
    non_english_langs = download_all_languages(asset_index, version_id, cache_dir)
    langs_data.update(non_english_langs)
    
    # 3. Remap keys and merge save output
    print("\n--- Phase 3: Remapping & Merging Translations ---")
    map_and_merge_translations(item_ids, entity_ids, custom_model_data_ids, langs_data, output_dir)
    
    print("\nGeneration process complete!")

if __name__ == "__main__":
    main()
