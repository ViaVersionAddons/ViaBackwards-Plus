# ViaBackwards-Plus v1 Maintenance

This workspace represents the legacy (`v1`) branch of the ViaBackwards-Plus resource pack, which is primarily targeted at legacy clients (like 1.20.1) mapping to newer servers (1.21.x+).

## 1. Core Philosophy (v1 vs v2)
*   **The v1 Rule**: DO NOT use vanilla `CustomModelData` by overwriting base models (e.g., `iron_axe.json`). Overwriting base carrier models destroys compatibility with other resource packs and server plugins. Instead, this branch relies exclusively on OptiFine CIT (`.properties`) and Chime (`overrides/item/` folder).
*   **The 1.21.4 Constraint**: Minecraft 1.21.4 introduced `minecraft:condition` to split item models for inventory vs. in-hand. Legacy 1.20 clients physically cannot support this split. Always fallback to using a single unified 3D JSON model containing a `"display": {"gui": ...}` block for inventory compatibility.

## 2. Missing Texture Troubleshooting Guide
If a newly backported asset shows up as a purple/black missing texture, follow these steps:
1.  **Check the Pipeline**: Did `v1_backport_compiler.py` run? Did it dynamically find the assets in the `backport_to_*` folders of the v2 repository?
2.  **Check the Model Mapping**: Verify the Chime override (`assets/minecraft/overrides/item/<carrier>.json`) or OptiFine CIT (`assets/minecraft/optifine/cit/backports/<item>.properties`). Do they point to the exact `target_model_id` path?
3.  **Check the NBT Tag**: Use `grep` to search for the `VB|Protocol<Version>To<Version>|id` NBT tag in the overrides to ensure the carrier hasn't mutated or the mapping ID hasn't shifted in the registry.
4.  **Check the Crawl**: The compiler's `crawl_model()` function is responsible for recursively parsing and copying `.png` files. If a texture is missing, check if the original 1.21.x asset pointed to a texture atlas path that the crawler missed.

## 3. Workspace Assumptions
*   **Mappings**: The compiler script assumes the `Mappings` repository (https://github.com/ViaVersion/Mappings) is available in a directory defined by the `MAPPINGS_DIR` environment variable (defaults to `../Mappings/mappings` relative to the repository root).
*   **Execution**: The script dynamically resolves fallback overlay folders. Run `python scripts/v1_backport_compiler.py` from the root of the repository to append new assets to this branch.
