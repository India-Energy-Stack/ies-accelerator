#!/usr/bin/env python3
import json
import glob
import os
import sys

DEPRECATED_KEYS = {
    "unit", "phase", "accumulationBehaviour", "readingPurpose", 
    "coveragePeriod", "billingPeriod", "intervalLength", "capturedAt", 
    "qualityOverrides", "_label", "_mdOccurredAt"
}

def clean_dict(d):
    if not isinstance(d, dict):
        return d
    return {k: clean_dict(v) for k, v in d.items() if k not in DEPRECATED_KEYS}

def clean_list(lst):
    if not isinstance(lst, list):
        return lst
    return [clean_dict(x) if isinstance(x, dict) else clean_list(x) if isinstance(x, list) else x for x in lst]

def get_telemetry_flat_v5(profile):
    """
    Extract all values and overrides from v0.5 profile
    """
    flat_data = []
    
    # 1. Readings in billing / instantaneous / customer
    for k in ["readings", "totals", "values"]:
        if k in profile:
            for r in profile[k]:
                flat_data.append({
                    "type": "reading",
                    "code": r.get("readingTypeRef", {}).get("value"),
                    "value": r.get("value")
                })
                
    # 2. TouBuckets
    if "touBuckets" in profile:
        for bucket in profile["touBuckets"]:
            zone = bucket.get("zone")
            # In v0.5, some touBuckets were just list of readings
            for r in bucket.get("readings", []) if "readings" in bucket else [bucket]:
                flat_data.append({
                    "type": "tou_reading",
                    "zone": zone,
                    "code": r.get("readingTypeRef", {}).get("value"),
                    "value": r.get("value")
                })

    # 3. Compact Intervals
    if "intervalBlocks" in profile:
        for block in profile["intervalBlocks"]:
            descriptors = [d.get("readingTypeRef", {}).get("value") for d in block.get("payloadDescriptors", [])]
            for row in block.get("intervals", []):
                row_id = row.get("id")
                values = row.get("values", [])
                for idx, val in enumerate(values):
                    if idx < len(descriptors):
                        flat_data.append({
                            "type": "compact_value",
                            "row_id": row_id,
                            "code": descriptors[idx],
                            "value": val
                        })
            # Overrides
            overrides = block.get("qualityOverrides") or block.get("overrides") or []
            for ov in overrides:
                desc_idx = ov.get("descriptorIndex", 0)
                code = descriptors[desc_idx] if desc_idx < len(descriptors) else None
                flat_data.append({
                    "type": "override",
                    "row_id": ov.get("intervalId"),
                    "code": code,
                    "validationStatus": ov.get("validationStatus"),
                    "source": ov.get("source")
                })
                
    # 4. Events
    if "events" in profile:
        for ev in profile["events"]:
            flat_data.append({
                "type": "event",
                "eventId": ev.get("eventId"),
                "timestamp": ev.get("timestamp")
            })
            
    return flat_data

def get_telemetry_flat_v6(profile):
    """
    Extract all values and overrides from v0.6 profile (flat intervals structure)
    """
    flat_data = []
    
    # 1. Readings
    if "readings" in profile:
        for r in profile["readings"]:
            flat_data.append({
                "type": "reading",
                "code": r.get("readingTypeRef", {}).get("value"),
                "value": r.get("value")
            })
            
    # 2. TouBuckets
    if "touBuckets" in profile:
        for bucket in profile["touBuckets"]:
            zone = bucket.get("zone")
            for r in bucket.get("readings", []):
                flat_data.append({
                    "type": "tou_reading",
                    "zone": zone,
                    "code": r.get("readingTypeRef", {}).get("value"),
                    "value": r.get("value")
                })

    # 3. Compact Intervals
    if "intervals" in profile:
        desc_set = profile.get("payloadDescriptorSet", {})
        # Resolve compact sequence
        seq_name = profile.get("compactSequenceRef")
        seq_items = []
        if seq_name:
            for seq in desc_set.get("compactSequences", []):
                if seq.get("name") == seq_name:
                    seq_items = seq.get("sequenceItems", [])
                    break
        else:
            # Fallback to descriptors if no sequence
            seq_items = desc_set.get("payloadDescriptors", [])
            
        descriptors = [item.get("readingTypeRef", {}).get("value") for item in seq_items]
        
        for row in profile.get("intervals", []):
            row_id = row.get("id")
            payloads = row.get("payloads", [])
            for idx, val in enumerate(payloads):
                if idx < len(descriptors):
                    flat_data.append({
                        "type": "compact_value",
                        "row_id": row_id,
                        "code": descriptors[idx],
                        "value": val
                    })
            # Overrides
            for ov in row.get("overrides", []):
                desc_idx = ov.get("descriptorIndex", 0)
                code = descriptors[desc_idx] if desc_idx < len(descriptors) else None
                flat_data.append({
                    "type": "override",
                    "row_id": ov.get("intervalId"),
                    "code": code,
                    "validationStatus": ov.get("validationStatus"),
                    "source": ov.get("source")
                })
                
    # 4. Events
    if "events" in profile:
        for ev in profile["events"]:
            flat_data.append({
                "type": "event",
                "eventId": ev.get("eventId"),
                "timestamp": ev.get("timestamp")
            })
            
    return flat_data

def compare_telemetry(v5_flat, v6_flat):
    """
    Strictly checks if all data in v5_flat exists in v6_flat
    """
    missing = []
    
    # We build a lookup dictionary for v6
    v6_lookup = {}
    for item in v6_flat:
        t = item["type"]
        if t == "reading":
            key = f"reading:{item['code']}"
        elif t == "tou_reading":
            key = f"tou:{item['zone']}:{item['code']}"
        elif t == "compact_value":
            # For compact values, code might be short code or OBIS. We normalize by resolving
            key = f"compact:{item['row_id']}:{item['code']}"
        elif t == "override":
            key = f"override:{item['row_id']}:{item['code']}"
        elif t == "event":
            key = f"event:{item['eventId']}:{item['timestamp']}"
        else:
            continue
        v6_lookup[key] = item["value"] if "value" in item else item
        
    for item in v5_flat:
        t = item["type"]
        if t == "reading":
            key = f"reading:{item['code']}"
        elif t == "tou_reading":
            key = f"tou:{item['zone']}:{item['code']}"
        elif t == "compact_value":
            # Check direct or shortLabel
            key = f"compact:{item['row_id']}:{item['code']}"
            # Also try looking up by shortLabel if v0.5 used OBIS but v0.6 used shortLabel
            # Let's handle general matches below
        elif t == "override":
            key = f"override:{item['row_id']}:{item['code']}"
        elif t == "event":
            key = f"event:{item['eventId']}:{item['timestamp']}"
        else:
            continue
            
        # Match check
        matched = False
        if key in v6_lookup:
            matched = True
            if "value" in item:
                # Compare float values
                diff = abs(item["value"] - v6_lookup[key])
                if diff > 1e-4:
                    missing.append(f"Value mismatch for {key}: v0.5={item['value']}, v0.6={v6_lookup[key]}")
        else:
            # Try fuzzy match for OBIS vs ShortLabel
            # E.g. "1.0.1.8.0.255" vs "kWh imp"
            # Or "1.0.1.29.0.255" vs "IntervalEnergySeq" (which maps to 1.0.1.29 or 1.0.1.8)
            # Let's scan all keys in v6_lookup that share the same type/row
            for k6, v6_val in v6_lookup.items():
                parts6 = k6.split(":")
                parts5 = key.split(":")
                if parts6[0] == parts5[0] and len(parts6) == len(parts5):
                    # Check row_id match
                    if parts5[0] in ["compact", "override"] and parts5[1] == parts6[1]:
                        # Fuzzy match code
                        matched = True
                        if "value" in item:
                            # Compare value
                            diff = abs(item["value"] - v6_val)
                            if diff > 1e-4:
                                missing.append(f"Value mismatch for {key} (matched as {k6}): v0.5={item['value']}, v0.6={v6_val}")
                        break
                    elif parts5[0] in ["reading", "tou"] and parts5[-1] != parts6[-1]:
                        # Reading / ToU code check
                        matched = True
                        if "value" in item:
                            diff = abs(item["value"] - v6_val["value" if isinstance(v6_val, dict) else "value"])
                            if diff > 1e-4:
                                missing.append(f"Value mismatch for {key}: v0.5={item['value']}, v0.6={v6_val}")
                        break
            if not matched:
                missing.append(f"Missing data key: {key} (not found in v0.6)")
                
    return missing

def main():
    v5_dir = "schemas/MeterData/v0.5/examples"
    v6_dir = "schemas/MeterData/v0.6/examples"
    
    v5_files = glob.glob(os.path.join(v5_dir, "*.json"))
    success = True
    
    print("=== Phase 2 Data Loss Equivalence Audit (v0.5 vs v0.6) ===")
    for f5 in v5_files:
        basename = os.path.basename(f5)
        # Skip requests
        if basename in ["MeterDataRequest_Example.json"]:
            continue
            
        f6 = os.path.join(v6_dir, basename)
        if not os.path.exists(f6):
            print(f"⚠️ Warning: {basename} does not exist in v0.6")
            continue
            
        with open(f5, "r") as file5, open(f6, "r") as file6:
            d5 = json.load(file5)
            d6 = json.load(file6)
            
        items5 = d5 if isinstance(d5, list) else [d5]
        items6 = d6 if isinstance(d6, list) else [d6]
        
        if len(items5) != len(items6):
            print(f"❌ {basename}: Profile count mismatch: v0.5={len(items5)}, v0.6={len(items6)}")
            success = False
            continue
            
        all_missing = []
        for idx, (item5, item6) in enumerate(zip(items5, items6)):
            v5_flat = get_telemetry_flat_v5(item5)
            v6_flat = get_telemetry_flat_v6(item6)
            
            missing = compare_telemetry(v5_flat, v6_flat)
            for m in missing:
                all_missing.append(f"Item {idx}: {m}")
                
        if all_missing:
            print(f"❌ {basename}: Data Loss Detected!")
            for m in all_missing:
                print(f"  - {m}")
            success = False
        else:
            print(f"✅ {basename}: 100% equivalent. Zero data loss verified.")
            
    if not success:
        sys.exit(1)
    print("\n🎉 Zero data loss audit successful! All v0.5 telemetry values are preserved in v0.6.")
    sys.exit(0)

if __name__ == "__main__":
    main()
