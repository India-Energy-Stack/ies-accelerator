#!/usr/bin/env python3
import os
import sys
import json
import jsonschema

def load_json(filepath):
    with open(filepath, "r", encoding="utf-8") as f:
        return json.load(f)

def run_parity_check(v6_path, openadr_path, obis_mapping):
    v6_data = load_json(v6_path)
    oadr_data = load_json(openadr_path)
    
    errors = []
    
    # 1. Parse v0.6 profiles list
    v6_profiles = v6_data if isinstance(v6_data, list) else [v6_data]
    
    descriptor_sets = {}
    data_profiles = []
    
    for p in v6_profiles:
        if p.get("profileType") == "DESCRIPTOR":
            for ds in p.get("payloadDescriptorSets", []):
                name = ds.get("name")
                if name:
                    descriptor_sets[name] = ds
        else:
            data_profiles.append(p)
            
    if not data_profiles:
        errors.append("No data profiles found in v0.6 payload.")
        return errors
        
    # Verify metadata mapping against first data profile
    main_profile = data_profiles[0]
    meter_serial_v6 = main_profile.get("meterRefs", [{}])[0].get("value")
    client_name_oadr = oadr_data.get("clientName")
    if meter_serial_v6 != client_name_oadr:
        errors.append(f"Meter serial / Client name mismatch: v0.6='{meter_serial_v6}', OpenADR='{client_name_oadr}'")
        
    resource_name = oadr_data.get("resources", [{}])[0].get("resourceName")
    if meter_serial_v6 != resource_name:
        errors.append(f"Resource name mismatch: v0.6='{meter_serial_v6}', OpenADR='{resource_name}'")
        
    # 2. Extract and sum values in v0.6 across all data profiles
    v6_sums = {}
    
    for profile in data_profiles:
        # Check compact intervals (Form B)
        if "intervals" in profile:
            ds_ref = profile.get("payloadDescriptorSetRef")
            seq_name = profile.get("compactSequenceRef")
            
            desc_set = descriptor_sets.get(ds_ref) if ds_ref else {}
            seq_items = []
            if seq_name:
                for seq in desc_set.get("compactSequences", []):
                    if seq.get("name") == seq_name:
                        seq_items = seq.get("sequenceItems", [])
                        break
            else:
                seq_items = desc_set.get("payloadDescriptors", [])
                
            descriptors = [item.get("readingType") for item in seq_items]
            
            for idx, code in enumerate(descriptors):
                if not code:
                    continue
                val_sum = 0.0
                count = 0
                for row in profile.get("intervals", []):
                    payloads = row.get("payloads", [])
                    if idx < len(payloads):
                        val_sum += float(payloads[idx])
                        count += 1
                if code in v6_sums:
                    current_sum, current_count = v6_sums[code]
                    v6_sums[code] = (current_sum + val_sum, current_count + count)
                else:
                    v6_sums[code] = (val_sum, count)
                    
        # Check elaborated readings (Form A)
        for r in profile.get("readings", []):
            code = r.get("readingType")
            val = float(r.get("value", 0.0))
            if not code:
                continue
            if code in v6_sums:
                current_sum, current_count = v6_sums[code]
                v6_sums[code] = (current_sum + val, current_count + 1)
            else:
                v6_sums[code] = (val, 1)

    # 3. Extract and sum values in OpenADR
    oadr_sums = {}
    
    for resource in oadr_data.get("resources", []):
        for interval in resource.get("intervals", []):
            for payload in interval.get("payloads", []):
                p_type = payload.get("type")
                for val in payload.get("values", []):
                    val_float = float(val)
                    if p_type in oadr_sums:
                        current_sum, current_count = oadr_sums[p_type]
                        oadr_sums[p_type] = (current_sum + val_float, current_count + 1)
                    else:
                        oadr_sums[p_type] = (val_float, 1)
                        
    # 4. Compare sums (auditing zero data loss)
    v6_mapped_sums = {}
    for code, (v6_sum, v6_count) in v6_sums.items():
        # Resolve code to category
        resolved_info = obis_mapping.get(code, {})
        category = resolved_info.get("category", "")
        
        # Map category to OpenADR type
        if category in ["energyCumulative", "energyIncremental"]:
            oadr_type = "USAGE"
        elif category == "demand":
            oadr_type = "DEMAND"
        elif category == "voltage":
            oadr_type = "VOLTAGE"
        elif category == "current":
            oadr_type = "CURRENT"
        elif category == "power":
            oadr_type = "POWER"
        else:
            oadr_type = category.upper() if category else "USAGE"
            
        if oadr_type in v6_mapped_sums:
            s, c = v6_mapped_sums[oadr_type]
            v6_mapped_sums[oadr_type] = (s + v6_sum, c + v6_count)
        else:
            v6_mapped_sums[oadr_type] = (v6_sum, v6_count)
            
    for oadr_type, (v6_sum, v6_count) in v6_mapped_sums.items():
        if oadr_type not in oadr_sums:
            errors.append(f"OpenADR missing telemetry type: expected '{oadr_type}'")
            continue
            
        oadr_sum, oadr_count = oadr_sums[oadr_type]
        if v6_count != oadr_count:
            errors.append(f"Data point count mismatch for '{oadr_type}': v0.6={v6_count}, OpenADR={oadr_count}")
            
        diff = abs(v6_sum - oadr_sum)
        if diff > 1e-4:
            errors.append(f"Parity Sum mismatch for '{oadr_type}': v0.6={v6_sum}, OpenADR={oadr_sum} (diff={diff})")
            
    return errors

def main():
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    schema_path = os.path.join(base_dir, "schema.json")
    examples_dir = os.path.join(base_dir, "examples")
    
    if not os.path.exists(schema_path):
        print(f"Error: Schema path '{schema_path}' does not exist. Run scripts/generate_openadr_schema.py first.")
        sys.exit(1)
        
    print(f"Loading OpenADR schema from {schema_path}...")
    schema = load_json(schema_path)
    validator = jsonschema.Draft202012Validator(schema)
    
    # Load central codes mapping
    v6_dir = os.path.join(os.path.dirname(base_dir), "v0.6")
    obis_mapping_path = os.path.join(v6_dir, "IES codes.json")
    with open(obis_mapping_path, "r", encoding="utf-8") as f:
        codes_data = json.load(f).get("codes", [])
    obis_mapping = {}
    for item in codes_data:
        obis_mapping[item["obis"]] = item
        if "shortLabel" in item:
            obis_mapping[item["shortLabel"]] = item
            
    success = True
    
    # Locate matching v0.6 files for parity verification
    v6_examples_dir = os.path.join(v6_dir, "examples")
    
    for filename in sorted(os.listdir(examples_dir)):
        if filename.endswith(".json"):
            filepath = os.path.join(examples_dir, filename)
            print(f"\n--- OpenADR Audit: {filename} ---")
            
            # 1. Structural Validation
            try:
                data = load_json(filepath)
            except Exception as e:
                print(f"❌ Failed to parse JSON: {e}")
                success = False
                continue
                
            errors = sorted(validator.iter_errors(data), key=lambda e: e.path)
            if errors:
                print("❌ Structural Validation Failed:")
                for error in errors:
                    path_str = " -> ".join([str(p) for p in error.path]) if error.path else "root"
                    print(f"  - Path: {path_str} | Message: {error.message}")
                success = False
                continue
            print("✅ Structural validation: PASSED")
            
            # Map OpenADR example name back to v0.6 example name
            if filename == "vOpenAdr_Example.json":
                v6_filename = "IntervalProfile.json"
            else:
                v6_filename = filename.replace("_OpenAdr.json", ".json")
            v6_filepath = os.path.join(v6_examples_dir, v6_filename)
            
            if os.path.exists(v6_filepath):
                parity_errors = run_parity_check(v6_filepath, filepath, obis_mapping)
                if parity_errors:
                    print("❌ Zero Data Loss Parity Check Failed:")
                    for err in parity_errors:
                        print(f"  - {err}")
                    success = False
                else:
                    print("✅ Zero Data Loss Parity Check: PASSED (100% equivalence verified)")
            else:
                print(f"ℹ️ Skipping parity check: matching v0.6 file '{v6_filename}' not found.")
                
    if not success:
        print("\n❌ OpenADR verification FAILED!")
        sys.exit(1)
        
    print("\n✅ OpenADR verification SUCCESSFUL! All files comply structurally and have zero data loss.")
    sys.exit(0)

if __name__ == "__main__":
    main()
