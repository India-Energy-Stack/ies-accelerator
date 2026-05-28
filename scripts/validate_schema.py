#!/usr/bin/env python3
import os
import sys
import json
import jsonschema

try:
    from referencing import Registry, Resource
    energy_cred_schema = {
        "$schema": "https://json-schema.org/draft/2020-12/schema",
        "type": "object"
    }
    energy_res_schema = {
        "$schema": "https://json-schema.org/draft/2020-12/schema",
        "type": "object"
    }
    resources = [
        ("https://schema.beckn.io/EnergyCredential/v2.0", Resource.from_contents(energy_cred_schema)),
        ("https://schema.beckn.io/EnergyResource/v2.0", Resource.from_contents(energy_res_schema))
    ]
    # Dynamically register all local schema.json files under their raw.githubusercontent.com URLs
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "schemas"))
    for root, dirs, files in os.walk(base_dir):
        for file in files:
            if file == "schema.json":
                schema_path = os.path.join(root, file)
                rel_path = os.path.relpath(schema_path, base_dir)
                url = f"https://raw.githubusercontent.com/India-Energy-Stack/ies-accelerator/main/schemas/{rel_path}"
                try:
                    with open(schema_path, "r", encoding="utf-8") as sf:
                        local_schema = json.load(sf)
                    resources.append((url, Resource.from_contents(local_schema)))
                except Exception:
                    pass
    registry = Registry().with_resources(resources)
except ImportError:
    registry = None

def validate_json_file(schema, filepath):
    """
    Validates a single JSON file against the parsed schema.
    """
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            data = json.load(f)
    except Exception as e:
        print(f"❌ {os.path.basename(filepath)}: Failed to parse JSON: {e}")
        return False, [f"JSON Parse Error: {e}"]

    # We use Draft202012Validator because the output schema matches the dialect specified in attributes.yaml
    if registry is not None:
        validator = jsonschema.Draft202012Validator(schema, registry=registry)
    else:
        validator = jsonschema.Draft202012Validator(schema)
    schema_type = schema.get("type", "object")
    
    if isinstance(data, list) and schema_type == "object":
        all_ok = True
        err_msg = []
        for idx, item in enumerate(data):
            errors = sorted(validator.iter_errors(item), key=lambda e: e.path)
            if errors:
                all_ok = False
                print(f"❌ {os.path.basename(filepath)} [Item {idx}]: Failed validation.")
                for error in errors:
                    path_str = f"[{idx}] -> " + (" -> ".join([str(p) for p in error.path]) if error.path else "root")
                    print(f"  - Path: {path_str}")
                    print(f"    Message: {error.message}")
                    err_msg.append(f"Path '{path_str}': {error.message}")
        if all_ok:
            print(f"✅ {os.path.basename(filepath)}: 100% compliant (validated {len(data)} items).")
            return True, []
        else:
            return False, err_msg
    else:
        errors = sorted(validator.iter_errors(data), key=lambda e: e.path)
        if not errors:
            print(f"✅ {os.path.basename(filepath)}: 100% compliant.")
            return True, []
        else:
            print(f"❌ {os.path.basename(filepath)}: Failed validation.")
            err_msg = []
            for error in errors:
                path_str = " -> ".join([str(p) for p in error.path]) if error.path else "root"
                print(f"  - Path: {path_str}")
                print(f"    Message: {error.message}")
                err_msg.append(f"Path '{path_str}': {error.message}")
            return False, err_msg

def main():
    if len(sys.argv) < 3:
        print("Usage: python validate_schema.py <schema_json_path> <target_json_or_directory>")
        sys.exit(1)
        
    schema_path = sys.argv[1]
    target_path = sys.argv[2]
    
    if not os.path.exists(schema_path):
        print(f"Error: Schema path '{schema_path}' does not exist.")
        sys.exit(1)
        
    if not os.path.exists(target_path):
        print(f"Error: Target path '{target_path}' does not exist.")
        sys.exit(1)
        
    print(f"Loading schema from {schema_path}...")
    try:
        with open(schema_path, "r", encoding="utf-8") as f:
            schema = json.load(f)
    except Exception as e:
        print(f"❌ Failed to parse schema JSON: {e}")
        sys.exit(1)
        
    success = True
    
    if os.path.isdir(target_path):
        print(f"Auditing directory '{target_path}' for schema compliance...")
        files = sorted(os.listdir(target_path))
        for filename in files:
            if filename.endswith(".json"):
                if filename in ["IES codes.json", "CustomerMapping.json", "MeterCategories.json"]:
                    print(f"ℹ️ Skipping {filename} (lookup/mapping metadata)")
                    continue
                    
                filepath = os.path.join(target_path, filename)
                file_ok, _ = validate_json_file(schema, filepath)
                if not file_ok:
                    success = False
    else:
        file_ok, _ = validate_json_file(schema, target_path)
        if not file_ok:
            success = False
            
    if not success:
        print("\n❌ Verification Failed! Some JSON payloads are non-compliant.")
        sys.exit(1)
        
    print("\n✅ Verification Successful! All payloads are 100% compliant.")
    sys.exit(0)

if __name__ == "__main__":
    main()
