import json
import os

def generate_billing():
    base_dir = "schemas/MeterData/v0.6/examples"
    mdm_path = os.path.join(base_dir, "MDM_MonthlyProfile.json")
    
    with open(mdm_path, "r") as f:
        mdm_data = json.load(f)
        
    billing_data = []
    
    # Keep the descriptor and make it USAGE centric
    descriptor = None
    profiles = []
    for item in mdm_data:
        if item.get("profileType") == "DESCRIPTOR":
            import copy
            descriptor = copy.deepcopy(item)
            # Make all energy registers USAGE
            for pds in descriptor.get("payloadDescriptorSets", []):
                for pd in pds.get("payloadDescriptors", []):
                    if pd.get("reportedMode") == "READING" and "energy" in pd.get("name", "").lower():
                        pd["reportedMode"] = "USAGE"
            billing_data.append(descriptor)
        elif item.get("profileType") == "MONTHLY":
            import copy
            profiles.append(copy.deepcopy(item))
            
    # Mock Customer Database
    customer_db = {
        "BESCOM-SM-2025-654321": {"scheme": "CONSUMER_NUMBER", "value": "RR-1234"},
        "BESCOM-SM-2025-999999": {"scheme": "CONSUMER_NUMBER", "value": "RR-5678"}
    }
            
    for p in profiles:
        meter_serial = None
        for m in p.get("meterRefs", []):
            if m.get("scheme") == "METER_SERIAL":
                meter_serial = m.get("value")
                break
                
        # Add customer ref
        if meter_serial in customer_db:
            p["customerRefs"] = [customer_db[meter_serial]]
            
        # Transform readings to be USAGE centric
        for r in p.get("readings", []):
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
