#!/usr/bin/env python3
import json
import glob
import os
import sys

# Load global mapping
OBIS_MAPPING_PATH = "schemas/MeterData/v0.6/IES codes.json"
if os.path.exists(OBIS_MAPPING_PATH):
    with open(OBIS_MAPPING_PATH, "r") as f:
        OBIS_MAPPING = json.load(f).get("codes", {})
else:
    OBIS_MAPPING = {}

def get_obis_info(ref_val):
    for code, info in OBIS_MAPPING.items():
        if code == ref_val or info.get("shortLabel") == ref_val:
            return code, info
    return ref_val, {}

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

def migrate_profile_to_openadr(profile):
    p_type = profile.get("profileType")
    meter_serial = profile.get("meterRefs", [{}])[0].get("value", "UNKNOWN_METER")
    
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
    
    # 1. Process Descriptors
    descriptors = []
    desc_set = profile.get("payloadDescriptorSet", {})
    seq_name = profile.get("compactSequenceRef")
    
    # Identify sequence items
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
        ref_val = item.get("readingTypeRef", {}).get("value")
        code, info = get_obis_info(ref_val)
        category = info.get("category", "")
        mode = item.get("reportedMode", "READING")
        
        p_type_mapped = map_payload_type(category)
        r_type_mapped = map_reading_type(mode, category)
        unit = info.get("unit", "KWH").upper()
        
        descriptors.append({
            "objectType": "REPORT_PAYLOAD_DESCRIPTOR",
            "payloadType": p_type_mapped,
            "readingType": r_type_mapped,
            "units": unit
        })
        resolved_desc_info.append((p_type_mapped, code, info))
        
    # Also handle elaborated readings if present (Billing / Instantaneous)
    readings = profile.get("readings", [])
    elaborated_desc_info = []
    for idx, r in enumerate(readings):
        ref_val = r.get("readingTypeRef", {}).get("value")
        code, info = get_obis_info(ref_val)
        category = info.get("category", "")
        mode = r.get("reportedMode", "READING")
        
        p_type_mapped = map_payload_type(category)
        r_type_mapped = map_reading_type(mode, category)
        unit = info.get("unit", "KWH").upper()
        
        # Avoid duplicate descriptors
        desc_exists = False
        for d in descriptors:
            if d["payloadType"] == p_type_mapped and d["readingType"] == r_type_mapped:
                desc_exists = True
                break
        if not desc_exists:
            descriptors.append({
                "objectType": "REPORT_PAYLOAD_DESCRIPTOR",
                "payloadType": p_type_mapped,
                "readingType": r_type_mapped,
                "units": unit
            })
        elaborated_desc_info.append((p_type_mapped, r_type_mapped))
        
    report["payloadDescriptors"] = descriptors

    # 2. Build Resource Payload
    res_intervals = []
    
    # 2a. Map flat intervals if present (Form B)
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
        
    # 2b. Map elaborated readings if present (Form A)
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
        
    # Build resources block
    resource_block = {
        "resourceName": meter_serial,
        "intervals": res_intervals
    }
    
    # Setup intervalPeriod default
    v6_period = profile.get("intervalPeriod") or profile.get("timePeriod")
    if v6_period:
        resource_block["intervalPeriod"] = {
            "start": v6_period["start"],
            "duration": v6_period["duration"]
        }
        
    report["resources"] = [resource_block]
    
    return report

def main():
    v6_examples = [
        "schemas/MeterData/v0.6/examples/IntervalProfile_UsageMode.json",
        "schemas/MeterData/v0.6/examples/DailyProfile_ReadingMode.json",
        "schemas/MeterData/v0.6/examples/BillingProfile_Elaborated.json"
    ]
    
    out_dir = "schemas/MeterData/vOpenAdr/examples"
    os.makedirs(out_dir, exist_ok=True)
    
    for f in v6_examples:
        if not os.path.exists(f):
            print(f"Warning: v0.6 example '{f}' not found.")
            continue
            
        basename = os.path.basename(f)
        print(f"Migrating {basename} to OpenADR report...")
        
        with open(f, "r") as file:
            data = json.load(file)
            
        openadr_report = migrate_profile_to_openadr(data)
        
        out_name = basename.replace(".json", "_OpenAdr.json")
        out_path = os.path.join(out_dir, out_name)
        
        with open(out_path, "w") as file:
            json.dump(openadr_report, file, indent=2)
            
        print(f"✅ Converted OpenADR report saved to: {out_path}")
        
        if basename == "IntervalProfile_UsageMode.json":
            example_path = os.path.join(out_dir, "vOpenAdr_Example.json")
            with open(example_path, "w") as file:
                json.dump(openadr_report, file, indent=2)
            print(f"✅ Converted OpenADR report example saved to: {example_path}")
        
    print("OpenADR migration complete!")

if __name__ == "__main__":
    main()
