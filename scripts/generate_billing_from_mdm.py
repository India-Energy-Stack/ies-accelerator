import json
import os

def generate_billing():
    base_dir = "schemas/MeterData/v0.6/examples"
    mdm_path = os.path.join(base_dir, "MDM_MonthlyProfile.json")
    
    with open(mdm_path, "r") as f:
        mdm_data = json.load(f)
        
    billing_data = []
    
    # 1. Build a map of readingType -> (multiplier, accuracy) from the MDM descriptor
    desc_map = {}
    descriptor = None
    profiles = []
    
    for item in mdm_data:
        if item.get("profileType") == "DESCRIPTOR":
            import copy
            descriptor = copy.deepcopy(item)
            # Make all energy registers USAGE and set output multiplier to 1.0 (default)
            for pds in descriptor.get("payloadDescriptorSets", []):
                for pd in pds.get("payloadDescriptors", []):
                    rt = pd.get("readingType")
                    if rt:
                        desc_map[rt] = {
                            "multiplier": pd.get("multiplier", 1.0),
                            "accuracy": pd.get("accuracy", None)
                        }
                    if pd.get("reportedMode") == "READING" and "energy" in pd.get("name", "").lower():
                        pd["reportedMode"] = "USAGE"
                    # Resolve multiplier to 1.0 in output descriptor
                    pd["multiplier"] = 1.0
            billing_data.append(descriptor)
        elif item.get("profileType") == "MONTHLY":
            import copy
            profiles.append(copy.deepcopy(item))
            
    # 2. Load Customer Database from the externalized example file
    mapping_path = os.path.join(base_dir, "CustomerMapping.json")
    with open(mapping_path, "r") as f:
        customer_db = json.load(f)
            
    # 3. Transform profiles and resolve readings
    for p in profiles:
        meter_serial = None
        for m in p.get("meterRefs", []):
            if m.get("scheme") == "METER_SERIAL":
                meter_serial = m.get("value")
                break
                
        # Add customer ref from external mapping
        if meter_serial in customer_db:
            p["customerRefs"] = [customer_db[meter_serial]]
            
        # Transform readings to be USAGE centric and resolve multiplier & accuracy
        for r in p.get("readings", []):
            rt = r.get("readingType")
            desc_info = desc_map.get(rt, {"multiplier": 1.0, "accuracy": None})
            multiplier = desc_info["multiplier"]
            accuracy = desc_info["accuracy"]
            
            # Resolve value using multiplier and accuracy
            val = r.get("value")
            if val is not None:
                resolved_val = val * multiplier
                if accuracy is not None and accuracy > 0:
                    import math
                    if accuracy < 1:
                        decimals = int(round(-math.log10(accuracy)))
                        resolved_val = round(resolved_val, decimals)
                    else:
                        resolved_val = round(resolved_val)
                r["value"] = resolved_val
                
            # Remove opening/closing values since billing profiles are USAGE centric
            if "openingValue" in r:
                del r["openingValue"]
            if "closingValue" in r:
                del r["closingValue"]
        
        billing_data.append(p)
        
    out_path = os.path.join(base_dir, "Billing_MonthlyProfile.json")
    with open(out_path, "w") as f:
        json.dump(billing_data, f, indent=2)
        
    print(f"Generated {out_path} from MDM data.")

if __name__ == "__main__":
    generate_billing()
