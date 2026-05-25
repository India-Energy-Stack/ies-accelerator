import os
import sys
import json
import jsonschema

def load_obis_mapping(path):
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
    return {entry["obis"]: entry for entry in data.get("codes", [])}

def resolve_reading_type(reading_type, obis_mapping):
    if reading_type in obis_mapping:
        return reading_type, obis_mapping[reading_type]
    for code, info in obis_mapping.items():
        if info.get("shortLabel") == reading_type:
            return code, info
    return None, None

def get_meter_categories(target_dir):
    map_file = os.path.join(target_dir, "MeterCategories.json")
    if os.path.exists(map_file):
        with open(map_file, "r", encoding="utf-8") as f:
            data = json.load(f)
            return {m["id"]: m["category"] for m in data.get("meters", [])}
    return {}

def validate_semantics(data, obis_mapping, meter_categories_map):
    errors = []
    
    # Payload is either a list of profiles or a single profile
    profiles = data if isinstance(data, list) else [data]
    
    # 1. Extract Descriptor Sets from PayloadDescriptorProfiles
    descriptor_sets = {}
    for profile in profiles:
        if profile.get("profileType") == "DESCRIPTOR":
            for ds in profile.get("payloadDescriptorSets", []):
                name = ds.get("name")
                if name:
                    descriptor_sets[name] = ds
                    
    # 2. Check inline descriptors consistency against OBIS
    for ds_name, ds in descriptor_sets.items():
        for p_idx, desc in enumerate(ds.get("payloadDescriptors", [])):
            rt = desc.get("readingType")
            code, info = resolve_reading_type(rt, obis_mapping)
            if code:
                inline_obis = desc.get("obis")
                if inline_obis and inline_obis != code:
                    errors.append(f"DescriptorSet '{ds_name}' Descriptor '{rt}' obis mismatch: Inline '{inline_obis}', Canonical '{code}'")
                    
                # STRICT ENFORCEMENT: name, flowDirection, category must exactly match if present
                for prop in ["name", "flowDirection", "category", "unit"]:
                    if prop in desc and prop in info and desc[prop] != info[prop]:
                        errors.append(f"DescriptorSet '{ds_name}' Descriptor '{rt}' {prop} mismatch: Inline '{desc[prop]}', Canonical '{info[prop]}'")
            else:
                errors.append(f"DescriptorSet '{ds_name}', Descriptor '{rt}': readingType could not be resolved in IES codes.json")
                
    # 3. Validate Data Profiles
    for p_idx, profile in enumerate(profiles):
        p_type = profile.get("profileType")
        if p_type == "DESCRIPTOR":
            continue
            
        meter_ids = [ref.get("value") for ref in profile.get("meterRefs", [])]
        meter_category = None
        for m_id in meter_ids:
            if m_id in meter_categories_map:
                meter_category = meter_categories_map[m_id]
                break
                
        # Matrix Validation
        if p_type in ["INTERVAL", "DAILY"]:
            compact_seq_ref = profile.get("compactSequenceRef")
            ds_ref = profile.get("payloadDescriptorSetRef")
            
            if not compact_seq_ref:
                continue # Elaborated format, skip matrix validation
                
            if not ds_ref:
                errors.append(f"Profile {p_idx} missing payloadDescriptorSetRef for compactSequence '{compact_seq_ref}'")
                continue
                
            ds = descriptor_sets.get(ds_ref)
            if not ds:
                errors.append(f"Profile {p_idx} payloadDescriptorSetRef '{ds_ref}' not found in provided PayloadDescriptorProfiles.")
                continue
                
            resolved_seq = None
            for seq in ds.get("compactSequences", []):
                if seq.get("name") == compact_seq_ref:
                    resolved_seq = seq
                    break
                    
            if not resolved_seq:
                errors.append(f"Profile {p_idx}: compactSequenceRef '{compact_seq_ref}' not found in descriptor set '{ds_ref}'.")
                continue
                
            seq_items = resolved_seq.get("sequenceItems", [])
            expected_len = len(seq_items)
            
            resolved_seq_info = []
            for item in seq_items:
                rt = item.get("readingType")
                code, info = resolve_reading_type(rt, obis_mapping)
                if not code:
                    errors.append(f"Profile {p_idx} SeqItem: readingType '{rt}' could not be resolved.")
                
                # Fetch multiplier from descriptor if any
                multiplier = 1.0
                reported_mode = "READING"
                for desc in ds.get("payloadDescriptors", []):
                    if desc.get("readingType") == rt:
                        multiplier = desc.get("multiplier", 1.0)
                        reported_mode = desc.get("reportedMode", "READING")
                        break
                        
                resolved_seq_info.append({
                    "code": code,
                    "info": info or {},
                    "reportedMode": reported_mode,
                    "attribute": item.get("attribute", "value"),
                    "multiplier": multiplier
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
                            errors.append(f"Profile {p_idx} Interval id {int_id} Col {col_idx}: CUMULATIVE mode value {val} is negative.")
                        elif col_idx in last_cumulative_values and val < last_cumulative_values[col_idx]:
                            errors.append(f"Profile {p_idx} Interval id {int_id} Col {col_idx}: CUMULATIVE mode value {val} decreased from {last_cumulative_values[col_idx]}.")
                        last_cumulative_values[col_idx] = val
                        
        # General Readings Validation
        for reading in profile.get("readings", []):
            if "reportedMode" in reading:
                errors.append(f"Profile {p_idx} Reading: 'reportedMode' MUST NOT be present in elaborated reading objects. It belongs in the payload descriptor.")
                
            rt = reading.get("readingType")
            code, info = resolve_reading_type(rt, obis_mapping)
            if not code:
                errors.append(f"Profile {p_idx} Reading: readingType '{rt}' could not be resolved.")
                continue
                
            if meter_category and info:
                supported_cats = info.get("meterCategories", [])
                if supported_cats and meter_category not in supported_cats:
                    errors.append(f"Profile {p_idx} Reading '{rt}': Meter Category '{meter_category}' is not in supported categories {supported_cats}.")
            
            if info:
                # Resolve reportedMode from descriptor set or fall back to defaultMode
                ds_ref = profile.get("payloadDescriptorSetRef")
                ds = descriptor_sets.get(ds_ref) if ds_ref else None
                reported_mode = None
                if ds:
                    for desc in ds.get("payloadDescriptors", []):
                        desc_rt = desc.get("readingType")
                        desc_code, _ = resolve_reading_type(desc_rt, obis_mapping)
                        if desc_rt == rt or (desc_code and desc_code == code):
                            reported_mode = desc.get("reportedMode")
                            break
                if not reported_mode:
                    reported_mode = info.get("defaultMode", "READING")

                allowed_attrs = info.get("allowedAttributes", ["value"])
                allowed_attrs.extend(["readingType", "intervalPeriod", "reportedMode"])
                for attr in reading:
                    if attr not in allowed_attrs:
                        errors.append(f"Profile {p_idx} Reading '{rt}': attribute '{attr}' is not allowed for this reading type by OBISMapping. Allowed: {allowed_attrs}")
                
                # Check opening/closing value constraint:
                opening = reading.get("openingValue")
                closing = reading.get("closingValue")
                if opening is not None or closing is not None:
                    if reported_mode == "READING":
                        errors.append(f"Profile {p_idx} Reading '{rt}': 'openingValue'/'closingValue' are NOT permitted when reportedMode is READING.")
                    elif "openingValue" not in allowed_attrs:
                        errors.append(f"Profile {p_idx} Reading '{rt}': 'openingValue'/'closingValue' are NOT permitted for this reading type.")
                    
                    # Math consistency for cumulative readings
                    if info.get("accumulationBehaviour") == "CUMULATIVE":
                        val = reading.get("value")
                        if val is not None and opening is not None and closing is not None:
                            expected_val = closing - opening
                            if abs(val - expected_val) > 1e-5:
                                errors.append(f"Profile {p_idx} Reading ({code}): Usage math inconsistency. closing ({closing}) - opening ({opening}) = {expected_val}, but value is {val}")

    return errors

def main():
    if len(sys.argv) < 2:
        print("Usage: python validate_v06.py <target_json_or_directory>")
        sys.exit(1)
        
    target_path = sys.argv[1]
    
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    obis_mapping_path = os.path.join(base_dir, "IES codes.json")
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
            if filename.endswith(".json") and filename not in ["IES codes.json", "MeterCategories.json", "CustomerMapping.json"]:
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
            
        errors = sorted(validator.iter_errors(data), key=lambda e: e.path)
        if errors:
            success = False
            print("❌ Structural Validation Failed:")
            for error in errors:
                path = " -> ".join([str(p) for p in error.path]) if error.path else "Root"
                print(f"  - Path: {path} | Message: {error.message}")
        else:
            print("✅ Structural validation: PASSED")
            
        semantic_errors = validate_semantics(data, obis_mapping, meter_categories)
        if semantic_errors:
            success = False
            print("❌ Semantic Validation Failed:")
            for error in semantic_errors:
                print(f"  - {error}")
        else:
            print("✅ Semantic validation: PASSED")
            
    if success:
        print("\n✅ Semantics audit SUCCESSFUL! All files conform to physical and mathematical constraints.")
    else:
        print("\n❌ Semantics audit FAILED!")
        sys.exit(1)

if __name__ == "__main__":
    main()
