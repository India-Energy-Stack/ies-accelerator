#!/usr/bin/env python3
import os
import sys
import json
import jsonschema

# Global constants for telemetry mode support
CATEGORY_MODES = {
    "energyCumulative": ["READING", "USAGE"],
    "energyIncremental": ["USAGE"],
    "energyToU": ["READING", "USAGE"],
    "demand": ["USAGE"],
    "voltage": ["READING"],
    "current": ["READING"],
    "power": ["READING"],
    "general": ["READING"],
    "identification": ["READING"],
    "programmable": ["READING"]
}

def load_obis_mapping(mapping_path):
    if not os.path.exists(mapping_path):
        print(f"Error: OBIS mapping file {mapping_path} not found.")
        sys.exit(1)
    with open(mapping_path, "r", encoding="utf-8") as f:
        return json.load(f).get("codes", {})

def resolve_reading_type(reading_type_ref, obis_mapping):
    scheme = reading_type_ref.get("scheme")
    value = reading_type_ref.get("value")
    
    if scheme == "OBIS":
        if value in obis_mapping:
            return value, obis_mapping[value]
    elif scheme == "SHORT_CODE":
        for code, info in obis_mapping.items():
            if info.get("shortLabel") == value:
                return code, info
    return None, None

def get_meter_categories(directory_path):
    """
    Search for customer profiles in the directory to build a map of meter serial -> category
    """
    meter_map = {}
    if not os.path.isdir(directory_path):
        return meter_map
        
    for filename in os.listdir(directory_path):
        if filename.endswith(".json") and filename != "OBISMapping.json":
            filepath = os.path.join(directory_path, filename)
            try:
                with open(filepath, "r", encoding="utf-8") as f:
                    data = json.load(f)
                
                # Check list or single dict
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

def validate_profile_semantics(profile, obis_mapping, meter_categories_map):
    errors = []
    p_type = profile.get("profileType")
    
    # Extract meter ID to check categories if possible
    meter_ids = [ref.get("value") for ref in profile.get("meterRefs", [])]
    meter_category = None
    for m_id in meter_ids:
        if m_id in meter_categories_map:
            meter_category = meter_categories_map[m_id]
            break

    # 1. Resolve payloadDescriptorSet and check compact sequences
    descriptor_set = profile.get("payloadDescriptorSet", {})
    compact_seq_ref = profile.get("compactSequenceRef")
    
    resolved_seq = None
    if compact_seq_ref:
        sequences = descriptor_set.get("compactSequences", [])
        for seq in sequences:
            if seq.get("name") == compact_seq_ref:
                resolved_seq = seq
                break
        if not resolved_seq:
            errors.append(f"compactSequenceRef '{compact_seq_ref}' not found in payloadDescriptorSet compactSequences.")
            
    # Resolve all descriptors to check capabilities
    resolved_descriptors = []
    for idx, desc in enumerate(descriptor_set.get("payloadDescriptors", [])):
        ref = desc.get("readingTypeRef")
        code, info = resolve_reading_type(ref, obis_mapping)
        if not code:
            errors.append(f"PayloadDescriptor index {idx}: readingTypeRef {ref} could not be resolved in OBISMapping.json")
            continue
            
        reported_mode = desc.get("reportedMode", "READING")
        category = info.get("category", "")
        allowed_modes = CATEGORY_MODES.get(category, ["READING"])
        
        if reported_mode not in allowed_modes:
            errors.append(f"PayloadDescriptor index {idx} ({code}): Mode '{reported_mode}' not supported for category '{category}'. Allowed: {allowed_modes}")
            
        # Physical check: meterCategory compatibility
        if meter_category:
            supported_categories = info.get("meterCategories", [])
            if meter_category not in supported_categories:
                errors.append(f"PayloadDescriptor index {idx} ({code}): Code is only supported for meter categories {supported_categories}, but meter is category '{meter_category}'")

    # 2. Check strict arity in compact arrays
    if resolved_seq:
        seq_items = resolved_seq.get("sequenceItems", [])
        expected_len = len(seq_items)
        
        # Resolve sequence items and check modes
        resolved_seq_info = []
        for idx, item in enumerate(seq_items):
            ref = item.get("readingTypeRef")
            code, info = resolve_reading_type(ref, obis_mapping)
            if code:
                reported_mode = item.get("reportedMode", "READING")
                resolved_seq_info.append((code, info, reported_mode))
            else:
                resolved_seq_info.append((None, {}, "READING"))
        
        intervals = profile.get("intervals", [])
        last_id = -1
        
        # Prepare cumulative columns to check monotonicity
        cumulative_cols = []
        for idx, (code, info, mode) in enumerate(resolved_seq_info):
            if code and info.get("accumulationBehaviour") == "CUMULATIVE" and mode == "READING":
                cumulative_cols.append(idx)

        last_cumulative_values = {}
        
        for idx, interval in enumerate(intervals):
            int_id = interval.get("id", 0)
            payloads = interval.get("payloads", [])
            
            # Sequence sorting check
            if int_id <= last_id:
                errors.append(f"Interval index {idx}: id {int_id} is not strictly increasing. Last: {last_id}")
            last_id = int_id
            
            # Arity check
            if len(payloads) != expected_len:
                errors.append(f"Interval id {int_id}: value count {len(payloads)} does not match compact sequence arity {expected_len}")
                
            # Monotonicity check
            for col_idx in cumulative_cols:
                if col_idx < len(payloads):
                    val = payloads[col_idx]
                    if val is not None:
                        if val < 0:
                            errors.append(f"Interval id {int_id}: Cumulative value for column {col_idx} cannot be negative: {val}")
                        if col_idx in last_cumulative_values:
                            prev_val = last_cumulative_values[col_idx]
                            if val < prev_val:
                                # Look for a potential reset flag/override if we wanted to allow resets
                                errors.append(f"Interval id {int_id}: Cumulative value for column {col_idx} decreased from {prev_val} to {val} (Monotonicity violation)")
                        last_cumulative_values[col_idx] = val

            # Check individual interval overrides
            for override in interval.get("overrides", []):
                desc_idx = override.get("descriptorIndex", 0)
                if desc_idx < 0 or desc_idx >= expected_len:
                    errors.append(f"Interval id {int_id} Override: descriptorIndex {desc_idx} out of range [0, {expected_len-1}]")

    # 3. Validate elaborated Readings lists
    readings = profile.get("readings", [])
    for idx, r in enumerate(readings):
        ref = r.get("readingTypeRef")
        code, info = resolve_reading_type(ref, obis_mapping)
        if not code:
            errors.append(f"Reading index {idx}: readingTypeRef {ref} could not be resolved in OBISMapping.json")
            continue
            
        reported_mode = r.get("reportedMode", "READING")
        category = info.get("category", "")
        allowed_modes = CATEGORY_MODES.get(category, ["READING"])
        if reported_mode not in allowed_modes:
            errors.append(f"Reading index {idx} ({code}): Mode '{reported_mode}' not supported for category '{category}'. Allowed: {allowed_modes}")
            
        # Mathematical proof for opening/closing values in USAGE mode
        if reported_mode == "USAGE":
            val = r.get("value")
            opening = r.get("openingValue")
            closing = r.get("closingValue")
            if opening is not None and closing is not None and val is not None:
                expected_val = closing - opening
                if abs(val - expected_val) > 1e-5:
                    errors.append(f"Reading index {idx} ({code}): Usage mathematical inconsistency. closing ({closing}) - opening ({opening}) = {expected_val}, but value is {val}")

    return errors

def main():
    if len(sys.argv) < 2:
        print("Usage: python validate_v06.py <target_json_or_directory>")
        sys.exit(1)
        
    target_path = sys.argv[1]
    
    # Locate OBISMapping.json relative to script or workspace
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    obis_mapping_path = os.path.join(base_dir, "OBISMapping.json")
    obis_mapping = load_obis_mapping(obis_mapping_path)
    
    # Gather meter categories from context directory
    dir_to_search = os.path.dirname(target_path) if os.path.isfile(target_path) else target_path
    meter_categories = get_meter_categories(dir_to_search)
    
    # First compile v0.6 schema to run structural validation
    schema_path = os.path.join(base_dir, "schema.json")
    if not os.path.exists(schema_path):
        print(f"Error: compiled schema.json at {schema_path} does not exist. Run scripts/generate_schema.py first.")
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
        items = data if isinstance(data, list) else [data]
        struct_ok = True
        for idx, item in enumerate(items):
            errors = sorted(validator.iter_errors(item), key=lambda e: e.path)
            if errors:
                struct_ok = False
                print(f"❌ Structural Validation Failed:")
                for error in errors:
                    path_str = f"[{idx}] -> " + (" -> ".join([str(p) for p in error.path]) if error.path else "root")
                    print(f"  - Path: {path_str} | Message: {error.message}")
                    
        if not struct_ok:
            success = False
            continue
        print("✅ Structural validation: PASSED")
        
        # 2. Semantic Rules Validation
        semantic_errors = []
        for idx, item in enumerate(items):
            profile_errors = validate_profile_semantics(item, obis_mapping, meter_categories)
            for err in profile_errors:
                semantic_errors.append(f"Item {idx}: {err}")
                
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
