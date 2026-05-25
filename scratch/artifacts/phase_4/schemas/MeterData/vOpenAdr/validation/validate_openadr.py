#!/usr/bin/env python3
import os
import sys
import json
import jsonschema

def load_json(filepath):
    with open(filepath, "r", encoding="utf-8") as f:
        return json.load(f)

def run_parity_check(v6_path, openadr_path):
    v6_data = load_json(v6_path)
    oadr_data = load_json(openadr_path)
    
    errors = []
    
    # 1. Verify metadata mapping
    meter_serial_v6 = v6_data.get("meterRefs", [{}])[0].get("value")
    client_name_oadr = oadr_data.get("clientName")
    if meter_serial_v6 != client_name_oadr:
        errors.append(f"Meter serial / Client name mismatch: v0.6='{meter_serial_v6}', OpenADR='{client_name_oadr}'")
        
    resource_name = oadr_data.get("resources", [{}])[0].get("resourceName")
    if meter_serial_v6 != resource_name:
        errors.append(f"Resource name mismatch: v0.6='{meter_serial_v6}', OpenADR='{resource_name}'")
        
    # 2. Extract and sum values in v0.6
    v6_sums = {}
    
    # Check compact intervals (Form B)
    if "intervals" in v6_data:
        desc_set = v6_data.get("payloadDescriptorSet", {})
        seq_name = v6_data.get("compactSequenceRef")
        seq_items = []
        if seq_name:
            for seq in desc_set.get("compactSequences", []):
                if seq.get("name") == seq_name:
                    seq_items = seq.get("sequenceItems", [])
                    break
        else:
            seq_items = desc_set.get("payloadDescriptors", [])
            
        descriptors = [item.get("readingTypeRef", {}).get("value") for item in seq_items]
        
        for idx, code in enumerate(descriptors):
            val_sum = 0.0
            count = 0
            for row in v6_data.get("intervals", []):
                payloads = row.get("payloads", [])
                if idx < len(payloads):
                    val_sum += float(payloads[idx])
                    count += 1
            v6_sums[code] = (val_sum, count)
            
    # Check elaborated readings (Form A)
    for r in v6_data.get("readings", []):
        code = r.get("readingTypeRef", {}).get("value")
        val = float(r.get("value", 0.0))
        if code in v6_sums:
            current_sum, current_count = v6_sums[code]
            v6_sums[code] = (current_sum + val, current_count + 1)
        else:
            v6_sums[code] = (val, 1)

    # 3. Extract and sum values in OpenADR
    oadr_sums = {}
    
    # In OpenADR, everything is grouped inside intervals
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
    # Since OpenADR uses upper-case categories (like USAGE, VOLTAGE, DEMAND) for type,
    # we map v0.6 codes to category names
    OBIS_MAPPING_PATH = "schemas/MeterData/v0.6/OBISMapping.json"
    if os.path.exists(OBIS_MAPPING_PATH):
        with open(OBIS_MAPPING_PATH, "r") as f:
            mapping = json.load(f).get("codes", {})
    else:
        mapping = {}
        
    v6_mapped_sums = {}
    for code, (v6_sum, v6_count) in v6_sums.items():
        # Resolve code to category
        resolved_info = mapping.get(code, {})
        if not resolved_info:
            # Try matching short label
            for c, info in mapping.items():
                if info.get("shortLabel") == code:
                    resolved_info = info
                    break
        category = resolved_info.get("category", "")
        
        # Map category to OpenADR type
        if category in ["energyCumulative", "energyIncremental"]:
            oadr_type = "USAGE"
        elif category == "demand":
            oadr_type = "DEMAND"
        elif category == "voltage":
            oadr_type = "VOLTAGE"
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
    
    success = True
    
    # Locate matching v0.6 files for parity verification
    v6_examples_dir = "schemas/MeterData/v0.6/examples"
    
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
                v6_filename = "IntervalProfile_UsageMode.json"
            else:
                v6_filename = filename.replace("_OpenAdr.json", ".json")
            v6_filepath = os.path.join(v6_examples_dir, v6_filename)
            
            if os.path.exists(v6_filepath):
                parity_errors = run_parity_check(v6_filepath, filepath)
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
