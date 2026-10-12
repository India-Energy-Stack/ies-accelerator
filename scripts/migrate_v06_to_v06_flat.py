#!/usr/bin/env python3
import json
import glob
import os
import re

# Load global mapping for category checking
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

def determine_mode(profile_type, obis_code, info):
    category = info.get("category", "")
    accumulation = info.get("accumulationBehaviour", "")
    
    if profile_type in ["DAILY", "BILLING"]:
        if accumulation == "CUMULATIVE" or "cumulative" in info.get("name", "").lower():
            return "READING"
    if profile_type == "INTERVAL":
        if accumulation == "DELTA" or "block" in info.get("name", "").lower():
            return "USAGE"
        if accumulation == "CUMULATIVE":
            return "READING"
    if profile_type == "INSTANTANEOUS":
        return "READING"
    
    if category in ["voltage", "current", "power", "general", "identification"]:
        return "READING"
    if category in ["energyIncremental", "demand"]:
        return "USAGE"
    
    return "READING"

def migrate_node(node):
    if not isinstance(node, dict):
        return node

    profile_type = node.get("profileType", "")
    node.pop("readingPurpose", None)  # Clean up deprecated field

    # 1. Convert readings if present
    if "readings" in node:
        new_readings = []
        for r in node["readings"]:
            r.pop("unit", None)
            r.pop("phase", None)
            r.pop("accumulationBehaviour", None)
            
            ref_val = r.get("readingTypeRef", {}).get("value", "")
            code, info = get_obis_info(ref_val)
            r["reportedMode"] = determine_mode(profile_type, code, info)
            new_readings.append(r)
        node["readings"] = new_readings

    # 2. Convert touBuckets if present
    if "touBuckets" in node:
        for bucket in node["touBuckets"]:
            if "readings" in bucket:
                new_bucket_readings = []
                for r in bucket["readings"]:
                    r.pop("unit", None)
                    r.pop("phase", None)
                    r.pop("accumulationBehaviour", None)
                    
                    ref_val = r.get("readingTypeRef", {}).get("value", "")
                    code, info = get_obis_info(ref_val)
                    r["reportedMode"] = determine_mode(profile_type, code, info)
                    new_bucket_readings.append(r)
                bucket["readings"] = new_bucket_readings

    # 3. Convert intervalBlocks to flat intervalPeriod and intervals
    if "intervalBlocks" in node:
        blocks = node.pop("intervalBlocks")
        if blocks:
            # We assume single block for simplicity of existing examples
            block = blocks[0]
            
            # Setup intervalPeriod
            block_period = block.get("timePeriod") or block.get("intervalPeriod")
            if block_period:
                node["intervalPeriod"] = {
                    "start": block_period["start"],
                    "duration": block_period.get("duration") or "PT30M"
                }
            
            # Build PayloadDescriptorSet
            descriptors = []
            seq_items = []
            for d in block.get("payloadDescriptors", []):
                ref_val = d.get("readingTypeRef", {}).get("value", "")
                code, info = get_obis_info(ref_val)
                mode = determine_mode(profile_type, code, info)
                
                desc = {
                    "readingTypeRef": d["readingTypeRef"],
                    "reportedMode": mode
                }
                if "powerOfTenMultiplier" in d:
                    desc["powerOfTenMultiplier"] = d["powerOfTenMultiplier"]
                if "touZone" in d:
                    desc["touZone"] = d["touZone"]
                descriptors.append(desc)
                
                seq_item = {
                    "readingTypeRef": d["readingTypeRef"],
                    "reportedMode": mode
                }
                if "powerOfTenMultiplier" in d:
                    seq_item["powerOfTenMultiplier"] = d["powerOfTenMultiplier"]
                seq_items.append(seq_item)
                
            set_name = f"{profile_type.capitalize()}LoadSurveySet"
            seq_name = f"{profile_type.capitalize()}EnergySeq"
            
            node["payloadDescriptorSet"] = {
                "name": set_name,
                "payloadDescriptors": descriptors,
                "compactSequences": [
                    {
                        "name": seq_name,
                        "sequenceItems": seq_items
                    }
                ]
            }
            node["compactSequenceRef"] = seq_name
            
            # Convert intervals and overrides
            new_intervals = []
            block_overrides = block.get("overrides") or block.get("qualityOverrides") or []
            
            for row in block.get("intervals", []):
                interval_id = row["id"]
                int_overrides = []
                for ov in block_overrides:
                    if ov.get("intervalId") == interval_id:
                        ov_clean = {
                            "intervalId": ov["intervalId"],
                            "descriptorIndex": ov.get("descriptorIndex", 0)
                        }
                        for k, v in ov.items():
                            if k not in ["intervalId", "descriptorIndex", "unit", "phase", "accumulationBehaviour"]:
                                ov_clean[k] = v
                        int_overrides.append(ov_clean)
                
                new_int = {
                    "id": interval_id,
                    "payloads": row.get("values") or row.get("payloads") or []
                }
                if int_overrides:
                    new_int["overrides"] = int_overrides
                new_intervals.append(new_int)
                
            node["intervals"] = new_intervals

    # Reorder keys
    order = [
        "@context", "@type", "profileType", "customerRefs", "meterRefs",
        "serviceDeliveryPointRefs", "timestamp", "billNumber", "billDate",
        "dueDate", "currency", "amountDue", "payloadDescriptorSet", "compactSequenceRef",
        "intervalPeriod", "readings", "touBuckets", "intervals", "events"
    ]
    new_node = {}
    for k in order:
        if k in node:
            new_node[k] = node[k]
    for k, v in node.items():
        if k not in new_node:
            new_node[k] = v
            
    return new_node

def compact_json_formatting(text):
    def collapse_payloads(m):
        return '"payloads": [' + ', '.join(x.strip() for x in m.group(1).split(',')) + ']'
    text = re.sub(r'"payloads"\s*:\s*\[([^\]]*)\]', collapse_payloads, text)
    
    def collapse_reading_type(m):
        return '"readingTypeRef": { ' + ' '.join(x.strip() for x in m.group(1).split('\n')) + ' }'
    text = re.sub(r'"readingTypeRef"\s*:\s*\{([^\}]*)\}', collapse_reading_type, text)
    
    def collapse_interval_period(m):
        return '"intervalPeriod": { ' + ' '.join(x.strip() for x in m.group(1).split('\n')) + ' }'
    text = re.sub(r'"intervalPeriod"\s*:\s*\{([^\}]*)\}', collapse_interval_period, text)

    def collapse_ident(m):
        cleaned = re.sub(r'\s+', ' ', m.group(0))
        return cleaned
    text = re.sub(r'\{\s*"scheme"\s*:\s*"[^"]+"\s*,\s*"value"\s*:\s*"[^"]+"\s*\}', collapse_ident, text)
    
    return text

def main():
    v6_files = glob.glob("schemas/MeterData/v0.6/examples/*.json")
    
    for f in v6_files:
        basename = os.path.basename(f)
        
        # Skip the newly created target files which are already flat
        if basename in [
            "DailyProfile_ReadingMode.json", 
            "IntervalProfile_UsageMode.json", 
            "BillingProfile_Elaborated.json",
            "vOpenAdr_Example.json"
        ]:
            continue
            
        print(f"Migrating {basename} in-place in v0.6 examples...")
        with open(f, "r") as file:
            data = json.load(file)
            
        if isinstance(data, list):
            data = [migrate_node(item) for item in data]
        else:
            data = migrate_node(data)
            
        out = json.dumps(data, indent=2)
        out = compact_json_formatting(out)
        
        with open(f, "w") as file:
            file.write(out + "\n")
            
    print("In-place migration of existing v0.6 examples complete!")

if __name__ == "__main__":
    main()
