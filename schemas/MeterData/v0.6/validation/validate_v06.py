#!/usr/bin/env python3
import os
import sys
import json
import jsonschema

def load_obis_mapping(mapping_path):
    if not os.path.exists(mapping_path):
        print(f"Error: OBIS mapping file {mapping_path} not found.")
        sys.exit(1)
    with open(mapping_path, "r", encoding="utf-8") as f:
        data = json.load(f).get("codes", [])
        return {item["obis"]: item for item in data}

def resolve_reading_type(reading_type_value, obis_mapping):
    if not reading_type_value:
        return None, None
        
    # Check if it's an OBIS code directly
    if reading_type_value in obis_mapping:
        return reading_type_value, obis_mapping[reading_type_value]
        
    # Check if it's a short code
    for code, info in obis_mapping.items():
        if info.get("shortLabel") == reading_type_value:
            return code, info
            
    return None, None

def get_meter_categories(directory_path):
    meter_map = {}
    if not os.path.isdir(directory_path):
        return meter_map
        
    for filename in os.listdir(directory_path):
        if filename.endswith(".json") and filename != "OBISMapping.json":
            filepath = os.path.join(directory_path, filename)
            try:
                with open(filepath, "r", encoding="utf-8") as f:
                    data = json.load(f)
                
                # Check root
                if isinstance(data, dict) and "data" in data:
                    items = data["data"]
                else:
                    items = data if isinstance(data, list) else [data]
                    
                for item in items:
                    if item.get("profileType") == "CUSTOMER" and "meters" in item:
                        for meter in item["meters"]:
                            m_id = meter.get("id", {}).get("value")
                            cat = meter.get("meterCategory")
                            if m_id and cat:
                                meter_map[m_id] = cat
            except Exception:
                pass
    return meter_map

def validate_dataset_semantics(dataset, obis_mapping, meter_categories_map):
    errors = []
    
    descriptor_sets = dataset.get("payloadDescriptorSets", [])
    descriptor_map = {ds.get("name"): ds for ds in descriptor_sets if "name" in ds}
    
    # Check inline descriptors consistency against OBIS
    for idx, ds in enumerate(descriptor_sets):
        for p_idx, desc in enumerate(ds.get("payloadDescriptors", [])):
            rt = desc.get("readingType")
            code, info = resolve_reading_type(rt, obis_mapping)
            if code:
                # Check optional obis field matches
                inline_obis = desc.get("obis")
                if inline_obis and inline_obis != code:
                    errors.append(f"Descriptor '{rt}' obis mismatch: Inline '{inline_obis}', Canonical '{code}'")
                    
                # Check properties if they exist
                if "unit" in desc and "unit" in info and desc["unit"] != info["unit"]:
                    errors.append(f"Descriptor '{rt}' unit mismatch: Inline '{desc['unit']}', Canonical '{info['unit']}'")
                if "flowDirection" in desc and "flowDirection" in info and desc["flowDirection"] != info["flowDirection"]:
                    errors.append(f"Descriptor '{rt}' flowDirection mismatch: Inline '{desc['flowDirection']}', Canonical '{info['flowDirection']}'")
            else:
                errors.append(f"DescriptorSet index {idx}, Descriptor index {p_idx}: readingType '{rt}' could not be resolved in OBISMapping.json")
    
    profiles = dataset.get("data", [])
    
    for p_idx, profile in enumerate(profiles):
        p_type = profile.get("profileType")
        meter_ids = [ref.get("value") for ref in profile.get("meterRefs", [])]
        meter_category = None
        for m_id in meter_ids:
            if m_id in meter_categories_map:
                meter_category = meter_categories_map[m_id]
                break
                
        # Matrix Validation
        if p_type in ["INTERVAL", "DAILY"]:
            compact_seq_ref = profile.get("compactSequenceRef")
            if not compact_seq_ref:
                continue # Elaborated format, skip matrix validation
            resolved_seq = None
            for ds in descriptor_sets:
                for seq in ds.get("compactSequences", []):
                    if seq.get("name") == compact_seq_ref:
                        resolved_seq = seq
                        break
                if resolved_seq:
                    break
                    
            if not resolved_seq:
                errors.append(f"Profile {p_idx}: compactSequenceRef '{compact_seq_ref}' not found in any payloadDescriptorSets.")
                continue
                
            seq_items = resolved_seq.get("sequenceItems", [])
            expected_len = len(seq_items)
            
            resolved_seq_info = []
            for item in seq_items:
                rt = item.get("readingType")
                code, info = resolve_reading_type(rt, obis_mapping)
                if not code:
                    errors.append(f"Profile {p_idx} SeqItem: readingType '{rt}' could not be resolved.")
                resolved_seq_info.append({
                    "code": code,
                    "info": info or {},
                    "reportedMode": item.get("reportedMode", "READING"),
                    "attribute": item.get("attribute", "value")
                })
                
            intervals = profile.get("intervals", [])
            last_id = -1
            
            cumulative_cols = []
            for col_idx, sinfo in enumerate(resolved_seq_info):
                if sinfo["code"] and sinfo["info"].get("accumulationBehaviour") == "CUMULATIVE" and sinfo["reportedMode"] == "READING":
                    if sinfo["attribute"] == "value":
                        cumulative_cols.append(col_idx)
                        
            last_cumulative_values = {}
            
            for idx, interval in enumerate(intervals):
                int_id = interval.get("id", 0)
                payloads = interval.get("payloads", [])
                
                if int_id <= last_id:
                    errors.append(f"Profile {p_idx} Interval {idx}: id {int_id} is not strictly increasing. Last: {last_id}")
                last_id = int_id
                
                if len(payloads) != expected_len:
                    errors.append(f"Profile {p_idx} Interval id {int_id}: value count {len(payloads)} does not match sequence arity {expected_len}")
                    continue
                    
                # Type checking dynamically
                for col_idx, (val, sinfo) in enumerate(zip(payloads, resolved_seq_info)):
                    attr = sinfo["attribute"]
                    if attr == "value" and not isinstance(val, (int, float)):
                        errors.append(f"Profile {p_idx} Interval id {int_id} Col {col_idx}: expected number for 'value', got {type(val)}")
                    elif attr == "occurredAt" and not isinstance(val, str):
                        errors.append(f"Profile {p_idx} Interval id {int_id} Col {col_idx}: expected string for 'occurredAt', got {type(val)}")
                    elif attr in ["openingValue", "closingValue"] and not isinstance(val, (int, float)):
                        errors.append(f"Profile {p_idx} Interval id {int_id} Col {col_idx}: expected number for '{attr}', got {type(val)}")
                    elif attr == "validationStatus" and not isinstance(val, str):
                        errors.append(f"Profile {p_idx} Interval id {int_id} Col {col_idx}: expected string for '{attr}', got {type(val)}")
                        
                for col_idx in cumulative_cols:
                    val = payloads[col_idx]
                    if isinstance(val, (int, float)):
                        if val < 0:
                            errors.append(f"Profile {p_idx} Interval id {int_id}: Cumulative value for column {col_idx} negative: {val}")
                        if col_idx in last_cumulative_values:
                            prev_val = last_cumulative_values[col_idx]
                            if val < prev_val:
                                errors.append(f"Profile {p_idx} Interval id {int_id}: Cumulative column {col_idx} decreased from {prev_val} to {val}")
                        last_cumulative_values[col_idx] = val

        # Validate elaborated Readings lists
        if p_type in ["MONTHLY", "BILL_DETAILS", "INSTANTANEOUS", "ALARM"]:
            readings = profile.get("readings", [])
            for r_idx, r in enumerate(readings):
                rt = r.get("readingType")
                code, info = resolve_reading_type(rt, obis_mapping)
                if not code:
                    errors.append(f"Profile {p_idx} Reading {r_idx}: readingType '{rt}' could not be resolved.")
                    continue
                    
                reported_mode = r.get("reportedMode", "READING")
                if reported_mode == "USAGE":
                    val = r.get("value")
                    opening = r.get("openingValue")
                    closing = r.get("closingValue")
                    if opening is not None and closing is not None and val is not None:
                        expected_val = closing - opening
                        if abs(val - expected_val) > 1e-5:
                            errors.append(f"Profile {p_idx} Reading {r_idx} ({code}): Usage math inconsistency. closing ({closing}) - opening ({opening}) = {expected_val}, but value is {val}")

    return errors

def main():
    if len(sys.argv) < 2:
        print("Usage: python validate_v06.py <target_json_or_directory>")
        sys.exit(1)
        
    target_path = sys.argv[1]
    
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    obis_mapping_path = os.path.join(base_dir, "OBISMapping.json")
    obis_mapping = load_obis_mapping(obis_mapping_path)
    
    dir_to_search = os.path.dirname(target_path) if os.path.isfile(target_path) else target_path
    meter_categories = get_meter_categories(dir_to_search)
    
    schema_path = os.path.join(base_dir, "schema.json")
    if not os.path.exists(schema_path):
        print(f"Error: schema.json at {schema_path} does not exist.")
        sys.exit(1)
        
    with open(schema_path, "r", encoding="utf-8") as f:
        schema = json.load(f)
        
    validator = jsonschema.Draft202012Validator(schema)
    
    success = True
    
    files_to_validate = []
    if os.path.isdir(target_path):
        for filename in sorted(os.listdir(target_path)):
            if filename.endswith(".json") and filename != "OBISMapping.json":
                files_to_validate.append(os.path.join(target_path, filename))
    else:
        files_to_validate.append(target_path)
        
    for filepath in files_to_validate:
        basename = os.path.basename(filepath)
        print(f"\n--- Semantics Audit: {basename} ---")
        
        try:
            with open(filepath, "r", encoding="utf-8") as f:
                data = json.load(f)
        except Exception as e:
            print(f"❌ Failed to parse JSON: {e}")
            success = False
            continue
            
        # 1. Structural Schema Validation
        # (validator is already initialized with schema outside the loop)
        
        errors = sorted(validator.iter_errors(data), key=lambda e: e.path)
        if errors:
            success = False
            print(f"❌ Structural Validation Failed:")
            for error in errors:
                path_str = " -> ".join([str(p) for p in error.path]) if error.path else "root"
                print(f"  - Path: {path_str} | Message: {error.message}")
            continue
        print("✅ Structural validation: PASSED")
        
        # 2. Semantic Rules Validation
        semantic_errors = validate_dataset_semantics(data, obis_mapping, meter_categories)
        if semantic_errors:
            print(f"❌ Semantic Validation Failed:")
            for err in semantic_errors:
                print(f"  - {err}")
            success = False
        else:
            print("✅ Semantic validation: PASSED")
            
    if not success:
        print("\n❌ Semantics audit FAILED!")
        sys.exit(1)
        
    print("\n✅ Semantics audit SUCCESSFUL! All files conform to physical and mathematical constraints.")
    sys.exit(0)

if __name__ == "__main__":
    main()
