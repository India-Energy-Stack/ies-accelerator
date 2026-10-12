import json
import glob
import os

def remove_customer_refs():
    mdm_files = [
        "IntervalProfile.json",
        "DailyProfile.json",
        "DailyProfile_ReadingMode.json",
        "MonthlyProfile.json",
        "MonthlyProfile_MultipleResets.json",
        "MultiMeterBulkDataset.json",
        "MultiMeterBulkDatasetShortCodes.json",
        "InstantaneousProfile.json",
        "AlarmProfile.json",
        "EventProfile.json"
    ]
    
    base_dir = "schemas/MeterData/v0.6/examples"
    
    for filename in mdm_files:
        filepath = os.path.join(base_dir, filename)
        if not os.path.exists(filepath):
            continue
            
        with open(filepath, 'r') as f:
            data = json.load(f)
            
        modified = False
        
        if isinstance(data, list):
            for item in data:
                if "customerRefs" in item:
                    del item["customerRefs"]
                    modified = True
        elif isinstance(data, dict):
            if "customerRefs" in data:
                del data["customerRefs"]
                modified = True
                
        if modified:
            with open(filepath, 'w') as f:
                json.dump(data, f, indent=2)
            print(f"Removed customerRefs from {filename}")

if __name__ == "__main__":
    remove_customer_refs()
