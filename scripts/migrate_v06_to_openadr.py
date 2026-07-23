#!/usr/bin/env python3
import json
import os
import sys

# Load global mapping
OBIS_MAPPING_PATH = "schemas/MeterData/v0.6/IES codes.json"
if os.path.exists(OBIS_MAPPING_PATH):
    with open(OBIS_MAPPING_PATH, "r", encoding="utf-8") as f:
        codes_data = json.load(f).get("codes", [])
else:
    codes_data = []

OBIS_MAPPING = {}
for item in codes_data:
    OBIS_MAPPING[item["obis"]] = item
    if "shortLabel" in item:
        OBIS_MAPPING[item["shortLabel"]] = item

def get_obis_info(ref_val):
    info = OBIS_MAPPING.get(ref_val, {})
    return ref_val, info

def map_payload_type(category):
    if category in ["energyCumulative", "energyIncremental"]:
        return "USAGE"
    if category == "demand":
        return "DEMAND"
    if category == "voltage":
        return "VOLTAGE"
    if category == "current":
        return "CURRENT"
    if category == "power":
        return "POWER"
    return category.upper() if category else "USAGE"

def map_reading_type(mode, category):
    if category == "demand":
        return "PEAK"
    if mode == "READING":
        return "DIRECT_READ"
    if mode == "USAGE":
        return "SUM"
    return "DIRECT_READ"

def migrate_v06_file_to_openadr(v6_filepath):
    with open(v6_filepath, "r", encoding="utf-8") as f:
        v6_data = json.load(f)
        
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
        print(f"Warning: No data profiles found in {v6_filepath}")
        return None
        
    # We take metadata from the first profile
    first_profile = data_profiles[0]
    p_type = first_profile.get("profileType", "UNKNOWN")
    meter_serial = first_profile.get("meterRefs", [{}])[0].get("value", "UNKNOWN_METER")
    
    report = {
        "id": f"report-{p_type.lower()}-{meter_serial}",
        "createdDateTime": "2026-05-25T00:00:00Z",
        "modificationDateTime": "2026-05-25T00:00:00Z",
        "objectType": "REPORT",
        "clientID": f"client-{meter_serial}",
        "eventID": "event-000",
        "clientName": meter_serial,
        "reportName": f"{p_type}_Report",
        "payloadDescriptors": [],
        "resources": []
    }
    
    global_descriptors = []
    
    for profile in data_profiles:
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
            
        resolved_desc_info = []
        for idx, item in enumerate(seq_items):
            ref_val = item.get("readingType")
            _, info = get_obis_info(ref_val)
            category = info.get("category", "")
            
            # Find reportedMode in payloadDescriptors
            reported_mode = "READING"
            for pd in desc_set.get("payloadDescriptors", []):
                if pd.get("readingType") == ref_val:
                    reported_mode = pd.get("reportedMode", "READING")
                    break
            
            p_type_mapped = map_payload_type(category)
            r_type_mapped = map_reading_type(reported_mode, category)
            unit = info.get("unit", "KWH").upper()
            if not unit:
                unit = "KWH"
            
            desc_obj = {
                "objectType": "REPORT_PAYLOAD_DESCRIPTOR",
                "payloadType": p_type_mapped,
                "readingType": r_type_mapped,
                "units": unit
            }
            if desc_obj not in global_descriptors:
                global_descriptors.append(desc_obj)
                
            resolved_desc_info.append((p_type_mapped, ref_val, info))
            
        readings = profile.get("readings", [])
        elaborated_desc_info = []
        for idx, r in enumerate(readings):
            ref_val = r.get("readingType")
            _, info = get_obis_info(ref_val)
            category = info.get("category", "")
            
            reported_mode = "READING"
            for pd in desc_set.get("payloadDescriptors", []):
                if pd.get("readingType") == ref_val:
                    reported_mode = pd.get("reportedMode", "READING")
                    break
                    
            p_type_mapped = map_payload_type(category)
            r_type_mapped = map_reading_type(reported_mode, category)
            unit = info.get("unit", "KWH").upper()
            if not unit:
                unit = "KWH"
            
            desc_obj = {
                "objectType": "REPORT_PAYLOAD_DESCRIPTOR",
                "payloadType": p_type_mapped,
                "readingType": r_type_mapped,
                "units": unit
            }
            if desc_obj not in global_descriptors:
                global_descriptors.append(desc_obj)
                
            elaborated_desc_info.append((p_type_mapped, r_type_mapped))
            
        # Build resource intervals
        res_intervals = []
        
        # Map compact intervals (Form B)
        v6_intervals = profile.get("intervals", [])
        for row in v6_intervals:
            row_id = row.get("id")
            payloads = row.get("payloads", [])
            
            openadr_payloads = []
            for idx, val in enumerate(payloads):
                if idx < len(resolved_desc_info):
                    p_type_mapped, _, _ = resolved_desc_info[idx]
                    openadr_payloads.append({
                        "type": p_type_mapped,
                        "values": [str(val)]
                    })
                    
            int_obj = {
                "id": row_id,
                "payloads": openadr_payloads
            }
            
            # Map overrides to intervalPeriod if occurredAt is present
            if "overrides" in row:
                for ov in row["overrides"]:
                    if "occurredAt" in ov:
                        int_obj["intervalPeriod"] = {
                            "start": ov["occurredAt"],
                            "duration": "PT0S"
                        }
            res_intervals.append(int_obj)
            
        # Map elaborated readings if present (Form A)
        for idx, r in enumerate(readings):
            p_type_mapped, r_type_mapped = elaborated_desc_info[idx]
            val = r.get("value")
            
            int_obj = {
                "id": len(res_intervals) + idx,
                "payloads": [
                    {
                        "type": p_type_mapped,
                        "values": [str(val)]
                    }
                ]
            }
            
            # Determine timePeriod for this reading
            start_time = r.get("occurredAt") or profile.get("timestamp") or "2026-05-25T00:00:00Z"
            duration = r.get("integrationPeriod") or "PT0S"
            int_obj["intervalPeriod"] = {
                "start": start_time,
                "duration": duration
            }
            res_intervals.append(int_obj)
            
        res_meter_serial = profile.get("meterRefs", [{}])[0].get("value", "UNKNOWN_METER")
        resource_block = {
            "resourceName": res_meter_serial,
            "intervals": res_intervals
        }
        
        # Setup intervalPeriod default
        v6_period = profile.get("intervalPeriod") or profile.get("timePeriod")
        if v6_period:
            resource_block["intervalPeriod"] = {
                "start": v6_period["start"],
                "duration": v6_period["duration"]
            }
            
        report["resources"].append(resource_block)
        
    report["payloadDescriptors"] = global_descriptors
    return report

def main():
    v6_mappings = [
        ("schemas/MeterData/v0.6/examples/IntervalProfile.json", "IntervalProfile_OpenAdr.json"),
        ("schemas/MeterData/v0.6/examples/DailyProfile_ReadingMode.json", "DailyProfile_ReadingMode_OpenAdr.json"),
        ("schemas/MeterData/v0.6/examples/BillingProfile.json", "BillingProfile_OpenAdr.json")
    ]
    
    out_dir = "schemas/MeterData/vOpenAdr/examples"
    os.makedirs(out_dir, exist_ok=True)
    
    # Clean up outdated example files first
    stale_files = ["BillingProfile_Elaborated_OpenAdr.json", "IntervalProfile_UsageMode_OpenAdr.json"]
    for sf in stale_files:
        p = os.path.join(out_dir, sf)
        if os.path.exists(p):
            os.remove(p)
            print(f"Cleaned up stale file: {p}")
            
    for f, out_name in v6_mappings:
        if not os.path.exists(f):
            print(f"Warning: v0.6 example '{f}' not found.")
            continue
            
        print(f"Migrating {f} to OpenADR report...")
        openadr_report = migrate_v06_file_to_openadr(f)
        
        if openadr_report:
            out_path = os.path.join(out_dir, out_name)
            with open(out_path, "w", encoding="utf-8") as file:
                json.dump(openadr_report, file, indent=2, ensure_ascii=False)
            print(f"✅ Converted OpenADR report saved to: {out_path}")
            
            # Also save IntervalProfile to vOpenAdr_Example.json
            if out_name == "IntervalProfile_OpenAdr.json":
                example_path = os.path.join(out_dir, "vOpenAdr_Example.json")
                with open(example_path, "w", encoding="utf-8") as file:
                    json.dump(openadr_report, file, indent=2, ensure_ascii=False)
                print(f"✅ Converted OpenADR report example saved to: {example_path}")
        
    print("OpenADR migration complete!")

if __name__ == "__main__":
    main()
