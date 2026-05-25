import os
import sys
import json
import copy
import isodate
from datetime import timedelta

def resolve_reading_type(reading_type, obis_mapping):
    if reading_type in obis_mapping:
        return reading_type, obis_mapping[reading_type]
    for code, info in obis_mapping.items():
        if info.get("shortLabel") == reading_type:
            return code, info
    return None, None

def load_obis_mapping(path):
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
    return {entry["obis"]: entry for entry in data.get("codes", [])}

def parse_duration(duration_str):
    if not duration_str:
        return timedelta()
    return isodate.parse_duration(duration_str)

def expand_profile(profile, descriptor_sets, obis_mapping):
    p_type = profile.get("profileType")
    if p_type not in ["INTERVAL", "DAILY"]:
        return profile
        
    compact_seq_ref = profile.get("compactSequenceRef")
    ds_ref = profile.get("payloadDescriptorSetRef")
    
    if not compact_seq_ref or not ds_ref:
        return profile # Already elaborated or invalid
        
    ds = descriptor_sets.get(ds_ref)
    if not ds:
        return profile
        
    seq = None
    for s in ds.get("compactSequences", []):
        if s.get("name") == compact_seq_ref:
            seq = s
            break
            
    if not seq:
        return profile
        
    seq_items = seq.get("sequenceItems", [])
    
    # Pre-resolve information for each column
    col_info = []
    for item in seq_items:
        rt = item.get("readingType")
        attr = item.get("attribute", "value")
        
        # Look up descriptor to get reportedMode and multiplier
        reported_mode = "READING"
        multiplier = 1.0
        for desc in ds.get("payloadDescriptors", []):
            if desc.get("readingType") == rt:
                reported_mode = desc.get("reportedMode", "READING")
                multiplier = desc.get("multiplier", 1.0)
                break
                
        # Look up OBIS mapping to get accumulationBehaviour
        code, info = resolve_reading_type(rt, obis_mapping)
        acc_behaviour = info.get("accumulationBehaviour", "NONE") if info else "NONE"
        
        col_info.append({
            "readingType": rt,
            "attribute": attr,
            "reportedMode": reported_mode,
            "multiplier": multiplier,
            "accBehaviour": acc_behaviour
        })
        
    # Process intervals
    intervals = profile.get("intervals", [])
    overrides = profile.get("overrides", [])
    period_start = isodate.parse_datetime(profile["intervalPeriod"]["start"])
    period_duration = parse_duration(profile["intervalPeriod"]["duration"])
    
    readings = []
    
    # Build overrides map: (intervalId, descriptorIndex) -> override object
    overrides_map = {}
    for ov in overrides:
        overrides_map[(ov["intervalId"], ov["descriptorIndex"])] = ov
        
    # We need to track the last reading value for cumulative calculations
    last_values = {}
    
    elaborated = copy.deepcopy(profile)
    
    if "intervals" in elaborated:
        for interval in elaborated["intervals"]:
            int_id = interval.get("id", 0)
            payloads = interval.get("payloads", [])
            
            merged_readings = {}
            
            for col_idx, (val, sinfo) in enumerate(zip(payloads, col_info)):
                attr = sinfo["attribute"]
                rt = sinfo["readingType"]
                
                if rt not in merged_readings:
                    merged_readings[rt] = {
                        "readingType": rt
                    }
                
                reading = merged_readings[rt]
                reading[attr] = val
                    
                # Add override info if any
                ov = overrides_map.get((int_id, col_idx))
                if ov:
                    for k, v in ov.items():
                        if k not in ["intervalId", "descriptorIndex"]:
                            reading[k] = v
                            
            interval["readings"] = list(merged_readings.values())
            # Remove payloads and overrides
            if "payloads" in interval:
                del interval["payloads"]
            if "overrides" in interval:
                del interval["overrides"]
                
        # Remove compactSequenceRef
        if "compactSequenceRef" in elaborated:
            del elaborated["compactSequenceRef"]
    if "overrides" in elaborated:
        del elaborated["overrides"]
        
    return elaborated
    
def process_file(filepath, obis_mapping):
    with open(filepath, "r", encoding="utf-8") as f:
        data = json.load(f)
        
    profiles = data if isinstance(data, list) else [data]
    
    # Extract Descriptor Sets
    descriptor_sets = {}
    for profile in profiles:
        if profile.get("profileType") == "DESCRIPTOR":
            for ds in profile.get("payloadDescriptorSets", []):
                name = ds.get("name")
                if name:
                    descriptor_sets[name] = ds
                    
    elaborated_profiles = []
    has_elaborated = False
    
    for profile in profiles:
        if profile.get("profileType") in ["INTERVAL", "DAILY"] and "compactSequenceRef" in profile:
            elaborated = expand_profile(profile, descriptor_sets, obis_mapping)
            elaborated_profiles.append(elaborated)
            has_elaborated = True
        else:
            elaborated_profiles.append(copy.deepcopy(profile))
            
    if has_elaborated:
        out_path = filepath.replace(".json", "_Elaborated.json")
        with open(out_path, "w", encoding="utf-8") as f:
            json.dump(elaborated_profiles, f, indent=2)
        print(f"✅ Generated {os.path.basename(out_path)}")
    else:
        print(f"Skipped {os.path.basename(filepath)} (no compact sequences)")
        
def main():
    if len(sys.argv) < 2:
        print("Usage: python generate_elaborated_profiles.py <target_json_or_directory>")
        sys.exit(1)
        
    target_path = sys.argv[1]
    
    base_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "schemas", "MeterData", "v0.6")
    obis_mapping_path = os.path.join(base_dir, "OBISMapping.json")
    obis_mapping = load_obis_mapping(obis_mapping_path)
    
    files_to_process = []
    if os.path.isdir(target_path):
        for filename in sorted(os.listdir(target_path)):
            if filename.endswith(".json") and not filename.endswith("_Elaborated.json") and filename != "OBISMapping.json" and filename != "MeterCategories.json":
                files_to_process.append(os.path.join(target_path, filename))
    else:
        files_to_process.append(target_path)
        
    for filepath in files_to_process:
        process_file(filepath, obis_mapping)

if __name__ == "__main__":
    main()
