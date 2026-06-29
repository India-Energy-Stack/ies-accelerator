#!/usr/bin/env python3
import os
import sys
import json
import yaml

def convert_refs(obj):
    """
    Recursively updates $ref paths from components/schemas/ to $defs/
    """
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
    elif isinstance(obj, str):
        if obj.startswith("#/components/schemas/"):
            return obj.replace("#/components/schemas/", "#/$defs/")
    return obj

def resolve_properties(schema_def, all_schemas):
    """
    Resolve properties of a schema, including those inherited via allOf and $ref.
    """
    properties = {}
    if not isinstance(schema_def, dict):
        return properties
        
    # 1. Handle allOf composition
    if "allOf" in schema_def:
        for subschema in schema_def["allOf"]:
            properties.update(resolve_properties(subschema, all_schemas))
            
    # 2. Handle direct $ref
    if "$ref" in schema_def:
        ref_path = schema_def["$ref"]
        if ref_path.startswith("#/components/schemas/"):
            ref_name = ref_path.split("/")[-1]
            ref_def = all_schemas.get(ref_name, {})
            properties.update(resolve_properties(ref_def, all_schemas))
            
    # 3. Handle direct properties (local definitions override inherited ones)
    if "properties" in schema_def:
        properties.update(schema_def["properties"])
        
    return properties

def get_property_type(prop_schema):
    """
    Determine xsd type or reference type for JSON-LD mapping
    """
    if "$ref" in prop_schema:
        return "@id"
    
    p_type = prop_schema.get("type")
    p_format = prop_schema.get("format")
    
    if p_type == "string":
        if p_format == "date-time":
            return "xsd:dateTime"
        elif p_format == "date":
            return "xsd:date"
        elif p_format == "duration":
            return "xsd:string"  # Duration is represented as string in XSD
        elif p_format == "uri":
            return "@id"
        return "xsd:string"
    elif p_type == "number":
        return "xsd:decimal"
    elif p_type == "integer":
        return "xsd:integer"
    elif p_type == "boolean":
        return "xsd:boolean"
    elif p_type == "array":
        return "@id"  # Arrays of objects map to @id references
    elif p_type == "object":
        return "@id"
    return "xsd:string"

def generate_context_mapping(schema_name, schema_def, all_schemas):
    """
    Generate nested JSON-LD context mapping for an object schema
    """
    properties = resolve_properties(schema_def, all_schemas)
    if not properties:
        return None
        
    ctx = {
        "@version": 1.1,
        "@protected": True
    }
    
    for prop_name, prop_schema in properties.items():
        # Handle standard vocabulary terms or x-jsonld override
        x_jsonld = prop_schema.get("x-jsonld", {}) if isinstance(prop_schema, dict) else {}
        if isinstance(x_jsonld, dict) and "@id" in x_jsonld:
            prop_id = x_jsonld["@id"]
        else:
            vocab_prefix = "ies"
            if prop_name in ["name", "manufacturer"]:
                vocab_prefix = "schema"
            prop_id = f"{vocab_prefix}:{prop_name}"
        
        # Check if the property type is array
        if isinstance(prop_schema, dict) and prop_schema.get("type") == "array":
            items = prop_schema.get("items", {})
            val = {
                "@id": prop_id,
                "@type": "@id",
                "@container": "@set"
            }
            # If the array is of referenced objects, we can nest the context
            if "$ref" in items:
                ref_name = items["$ref"].split("/")[-1]
                ref_def = all_schemas.get(ref_name, {})
                nested = generate_context_mapping(ref_name, ref_def, all_schemas)
                if nested:
                    val["@context"] = nested["@context"]
            ctx[prop_name] = val
        elif isinstance(prop_schema, dict) and "$ref" in prop_schema:
            ref_name = prop_schema["$ref"].split("/")[-1]
            ref_def = all_schemas.get(ref_name, {})
            val = {
                "@id": prop_id,
                "@type": "@id"
            }
            nested = generate_context_mapping(ref_name, ref_def, all_schemas)
            if nested:
                val["@context"] = nested["@context"]
            ctx[prop_name] = val
        elif isinstance(prop_schema, dict) and prop_schema.get("type") == "object" and "properties" in prop_schema:
            # Inline object definition
            val = {
                "@id": prop_id,
                "@type": "@id"
            }
            nested = generate_context_mapping(prop_name, prop_schema, all_schemas)
            if nested:
                val["@context"] = nested["@context"]
            ctx[prop_name] = val
        else:
            ctx[prop_name] = {
                "@id": prop_id,
                "@type": get_property_type(prop_schema) if isinstance(prop_schema, dict) else "xsd:string"
            }
            
    return {"@id": f"ies:{schema_name}", "@type": "@id", "@context": ctx}

def camel_to_spaced(name):
    """Convert camelCase/PascalCase to spaced sentence case"""
    import re
    spaced = re.sub(r'(?<!^)(?=[A-Z])', ' ', name)
    return spaced.strip()

def main():
    if len(sys.argv) < 2:
        print("Usage: python generate_schema_permissive.py <schema_directory>")
        sys.exit(1)
        
    schema_dir = sys.argv[1]
    attributes_path = os.path.join(schema_dir, "attributes.yaml")
    
    if not os.path.exists(attributes_path):
        print(f"Error: {attributes_path} does not exist.")
        sys.exit(1)
        
    print(f"Loading {attributes_path}...")
    with open(attributes_path, "r", encoding="utf-8") as f:
        try:
            data = yaml.safe_load(f)
        except Exception as e:
            print(f"Error parsing YAML: {e}")
            sys.exit(1)
            
    norm_path = os.path.normpath(schema_dir)
    version_folder = os.path.basename(norm_path)
    schema_name = version_folder
    if version_folder.startswith("v") and version_folder[1:].replace(".", "").isdigit():
        parent_dir = os.path.dirname(norm_path)
        schema_name = os.path.basename(parent_dir)
    else:
        version_folder = "v0.5"
    print(f"Compiling schemas for '{schema_name}' ({version_folder})...")
    
    components = data.get("components", {})
    all_schemas = components.get("schemas", {})
    
    if not all_schemas:
        print("Error: No schemas found in components.schemas")
        sys.exit(1)
        
    # --- 1. COMPILE schema.json ---
    root_def = all_schemas.get(schema_name)
    if not root_def:
        print(f"Warning: Root component matching folder name '{schema_name}' not found. Using first component as root.")
        first_key = list(all_schemas.keys())[0]
        root_def = all_schemas[first_key]
        
    schema_json = {
        "$schema": "https://json-schema.org/draft/2020-12/schema",
        "$id": root_def.get("$id", f"https://raw.githubusercontent.com/India-Energy-Stack/ies-accelerator/main/schemas/{schema_name}/{version_folder}/schema.json"),
        "title": root_def.get("title", schema_name),
        "description": root_def.get("description", ""),
    }
    
    # Copy root properties except metadata fields
    for k, v in root_def.items():
        if k not in ["$id", "title", "description", "x-jsonld", "x-tags"]:
            schema_json[k] = convert_refs(v)
            
    # Add other schemas into $defs
    defs = {}
    for name, s_def in all_schemas.items():
        if name == schema_name:
            continue
        defs[name] = convert_refs(s_def)
        
    if defs:
        schema_json["$defs"] = defs
        
    schema_output = os.path.join(schema_dir, "schema.json")
    with open(schema_output, "w", encoding="utf-8") as f:
        json.dump(schema_json, f, indent=2, ensure_ascii=False)
    print(f"✅ Generated {schema_output}")
    
    # --- 2. COMPILE context.jsonld ---
    context_json = {
        "@context": {
            "@version": 1.1,
            "@protected": True,
            "id": "@id",
            "type": "@type",
            "schema": "https://schema.org/",
            "xsd": "http://www.w3.org/2001/XMLSchema#",
            "deg": "https://schema.beckn.io/deg/EnergyCredential/v2.0/",
            "ies": "https://raw.githubusercontent.com/India-Energy-Stack/ies-accelerator/main/schemas/ies#",
        }
    }
    
    # Map each object-type schema
    for name, s_def in all_schemas.items():
        if s_def.get("type") == "object" or "allOf" in s_def:
            mapping = generate_context_mapping(name, s_def, all_schemas)
            if mapping:
                # Add class context
                context_json["@context"][name] = {
                    "@id": f"ies:{name}",
                    "@context": mapping["@context"]
                }
                
    context_output = os.path.join(schema_dir, "context.jsonld")
    with open(context_output, "w", encoding="utf-8") as f:
        json.dump(context_json, f, indent=4, ensure_ascii=False)
    print(f"✅ Generated {context_output}")
    
    # --- 3. COMPILE vocab.jsonld ---
    vocab_json = {
        "@context": {
            "@version": 1.1,
            "ies": "https://raw.githubusercontent.com/India-Energy-Stack/ies-accelerator/main/schemas/ies/",
            "rdf": "http://www.w3.org/1999/02/22-rdf-syntax-ns#",
            "rdfs": "http://www.w3.org/2000/01/rdf-schema#",
            "xsd": "http://www.w3.org/2001/XMLSchema#",
            "schema": "https://schema.org/"
        },
        "@graph": []
    }
    
    # Add root class
    vocab_json["@graph"].append({
        "@id": f"ies:{schema_name}",
        "@type": "rdfs:Class",
        "rdfs:label": camel_to_spaced(schema_name),
        "rdfs:comment": root_def.get("description", "").strip()
    })
    
    # Add classes for all schemas
    unique_properties = {}
    for name, s_def in all_schemas.items():
        if s_def.get("type") == "object" or "allOf" in s_def:
            if name != schema_name:
                vocab_json["@graph"].append({
                    "@id": f"ies:{name}",
                    "@type": "rdfs:Class",
                    "rdfs:label": camel_to_spaced(name),
                    "rdfs:comment": s_def.get("description", "").strip()
                })
            
            # Record properties for properties definitions
            properties = resolve_properties(s_def, all_schemas)
            for prop_name, prop_schema in properties.items():
                desc = prop_schema.get("description", "").strip() if isinstance(prop_schema, dict) else ""
                if prop_name not in unique_properties:
                    unique_properties[prop_name] = desc
                elif desc and not unique_properties[prop_name]:
                    unique_properties[prop_name] = desc
                    
    # Add property nodes to vocabulary graph
    for prop_name, desc in unique_properties.items():
        # Check if the property has a custom x-jsonld mapping to a different namespace
        custom_id = None
        for name, s_def in all_schemas.items():
            props = resolve_properties(s_def, all_schemas)
            if prop_name in props:
                x_jsonld = props[prop_name].get("x-jsonld", {}) if isinstance(props[prop_name], dict) else {}
                if isinstance(x_jsonld, dict) and "@id" in x_jsonld:
                    custom_id = x_jsonld["@id"]
                    break
        
        if custom_id and ":" in custom_id:
            prefix = custom_id.split(":")[0]
            if prefix != "ies":
                # Skip defining external properties in our vocab
                continue
                
        prefix = "ies"
        if prop_name in ["name", "manufacturer"]:
            prefix = "schema"
            
        vocab_json["@graph"].append({
            "@id": f"{prefix}:{prop_name}",
            "@type": "rdf:Property",
            "rdfs:label": camel_to_spaced(prop_name),
            "rdfs:comment": desc
        })
        
    vocab_output = os.path.join(schema_dir, "vocab.jsonld")
    with open(vocab_output, "w", encoding="utf-8") as f:
        json.dump(vocab_json, f, indent=4, ensure_ascii=False)
    print(f"✅ Generated {vocab_output}")
    print("🎉 All compilation tasks completed successfully!")

if __name__ == "__main__":
    main()
