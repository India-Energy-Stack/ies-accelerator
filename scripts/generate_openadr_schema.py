#!/usr/bin/env python3
import os
import sys
import json
import yaml
import datetime

def convert_refs(obj):
    if isinstance(obj, list):
        return [convert_refs(i) for i in obj]
    elif isinstance(obj, dict):
        new_dict = {}
        for k, v in obj.items():
            if k == "$ref" and isinstance(v, str):
                if v.startswith("#/components/schemas/"):
                    new_dict[k] = v.replace("#/components/schemas/", "#/$defs/")
                else:
                    new_dict[k] = v
            else:
                new_dict[k] = convert_refs(v)
        return new_dict
    elif isinstance(obj, (datetime.datetime, datetime.date)):
        return obj.isoformat()
    return obj

def main():
    schema_dir = "schemas/MeterData/vOpenAdr"
    yaml_path = os.path.join(schema_dir, "openadr.yaml")
    
    if not os.path.exists(yaml_path):
        print(f"Error: {yaml_path} does not exist.")
        sys.exit(1)
        
    print(f"Loading {yaml_path}...")
    with open(yaml_path, "r", encoding="utf-8") as f:
        try:
            data = yaml.safe_load(f)
        except Exception as e:
            print(f"Error parsing YAML: {e}")
            sys.exit(1)
            
    components = data.get("components", {})
    all_schemas = components.get("schemas", {})
    
    if not all_schemas:
        print("Error: No schemas found in components.schemas")
        sys.exit(1)
        
    root_name = "report"
    root_def = all_schemas.get(root_name)
    if not root_def:
        print(f"Error: Root schema '{root_name}' not found in openadr.yaml")
        sys.exit(1)
        
    schema_json = {
        "$schema": "https://json-schema.org/draft/2020-12/schema",
        "$id": "https://raw.githubusercontent.com/India-Energy-Stack/ies-accelerator/main/schemas/MeterData/vOpenAdr/schema.json",
        "title": "OpenADR Report Payload",
        "description": root_def.get("description", "OpenADR 3.0 compatible report payload"),
    }
    
    # Copy root properties except metadata fields
    for k, v in root_def.items():
        if k not in ["$id", "title", "description"]:
            schema_json[k] = convert_refs(v)
            
    # Add other schemas into $defs
    defs = {}
    for name, s_def in all_schemas.items():
        if name == root_name:
            continue
        defs[name] = convert_refs(s_def)
        
    if defs:
        schema_json["$defs"] = defs
        
    schema_output = os.path.join(schema_dir, "schema.json")
    with open(schema_output, "w", encoding="utf-8") as f:
        json.dump(schema_json, f, indent=2, ensure_ascii=False)
    print(f"✅ Generated OpenADR JSON schema: {schema_output}")

if __name__ == "__main__":
    main()
