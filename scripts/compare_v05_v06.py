import json
import glob
import os

DEPRECATED_KEYS = {
    'unit', 'phase', 'accumulationBehaviour', 
    'coveragePeriod', 'billingPeriod', 'intervalPeriod', 
    'intervalLength', 'capturedAt', 'qualityOverrides', 
    '_label', '_mdOccurredAt', 'openingValue', 'closingValue', 
    'integrationPeriod'
}

def diff_dict(d1, d2, path=""):
    diffs = []
    
    # Check if keys in d1 are in d2
    for k, v in d1.items():
        curr_path = f"{path}.{k}" if path else k
        
        # If it's a deprecated key, skip it
        if k in DEPRECATED_KEYS:
            continue
            
        if k not in d2:
            # Special check for renamed properties
            if k == 'totals' and 'readings' in d2:
                continue
            if k == 'values' and 'readings' in d2:
                # Instantaneous values mapped to readings
                continue
            diffs.append((curr_path, "missing_key", v, None))
            continue
            
        v2 = d2[k]
        
        if isinstance(v, dict) and isinstance(v2, dict):
            diffs.extend(diff_dict(v, v2, curr_path))
        elif isinstance(v, list) and isinstance(v2, list):
            if len(v) != len(v2):
                diffs.append((curr_path, "list_length_mismatch", len(v), len(v2)))
            else:
                for idx, (item1, item2) in enumerate(zip(v, v2)):
                    if isinstance(item1, dict) and isinstance(item2, dict):
                        diffs.extend(diff_dict(item1, item2, f"{curr_path}[{idx}]"))
                    elif item1 != item2:
                        diffs.append((f"{curr_path}[{idx}]", "value_mismatch", item1, item2))
        elif v != v2:
            # Special check for @context
            if k == '@context' and 'v0.6' in str(v2):
                continue
            diffs.append((curr_path, "value_mismatch", v, v2))
            
    return diffs

v5_dir = "schemas/MeterData/v0.5/examples"
v6_dir = "schemas/MeterData/v0.6/examples"

v5_files = glob.glob(os.path.join(v5_dir, "*.json"))

print("=== Starting Data Loss Audit (v0.5 vs v0.6) ===")
total_diffs = 0
for f5 in v5_files:
    basename = os.path.basename(f5)
    # Map AggregatedFeeder_Example to AggregatedFeeder
    if basename == "AggregatedFeeder_Example.json":
        basename = "AggregatedFeeder.json"
        
    f6 = os.path.join(v6_dir, basename)
    if not os.path.exists(f6):
        print(f"⚠️ Warning: {basename} does not exist in v0.6")
        continue
        
    with open(f5, 'r') as file5, open(f6, 'r') as file6:
        d5 = json.load(file5)
        d6 = json.load(file6)
        
    diffs = []
    if isinstance(d5, list) and isinstance(d6, list):
        if len(d5) != len(d6):
            diffs.append(("root", "list_length_mismatch", len(d5), len(d6)))
        else:
            for idx, (item5, item6) in enumerate(zip(d5, d6)):
                diffs.extend(diff_dict(item5, item6, f"[{idx}]"))
    elif isinstance(d5, dict) and isinstance(d6, dict):
        diffs.extend(diff_dict(d5, d6))
        
    if diffs:
        print(f"\nDifferences found in {basename}:")
        for path, diff_type, v1, v2 in diffs:
            print(f"  - {path} ({diff_type}):")
            print(f"      v0.5: {v1}")
            print(f"      v0.6: {v2}")
        total_diffs += len(diffs)
    else:
        print(f"✅ {basename}: 100% equivalent (no unexpected differences).")

print(f"\nAudit complete. Total unexpected differences: {total_diffs}")
