import json
import glob
import os

def cleanup_examples():
    base_dir = "schemas/MeterData/v0.6/examples"
    
    # We want to clean up manually maintained files, not elaborated ones.
    for filepath in glob.glob(os.path.join(base_dir, "*.json")):
        if "Elaborated" in filepath:
            continue
            
        with open(filepath, 'r') as f:
            data = json.load(f)
            
        modified = False
        
        def process_readings(readings):
            mod = False
            for r in readings:
                if "reportedMode" in r:
                    del r["reportedMode"]
                    mod = True
                
                # if not MD, remove occurredAt
                rt = r.get("readingType", "")
                if "MD " not in rt and "1.0.1.6" not in rt and "occurredAt" in r:
                    del r["occurredAt"]
                    mod = True
            return mod
            
        if isinstance(data, list):
            for item in data:
                if "readings" in item:
                    if process_readings(item["readings"]):
                        modified = True
                if "alarms" in item:
                    for a in item["alarms"]:
                        if "reportedMode" in a:
                            del a["reportedMode"]
                            modified = True
                if "events" in item:
                    for e in item["events"]:
                        if "reportedMode" in e:
                            del e["reportedMode"]
                            modified = True
                if "touBuckets" in item:
                    for t in item["touBuckets"]:
                        if "readings" in t:
                            if process_readings(t["readings"]):
                                modified = True
        elif isinstance(data, dict):
            if "readings" in data:
                if process_readings(data["readings"]):
                    modified = True
            if "alarms" in data:
                for a in data["alarms"]:
                    if "reportedMode" in a:
                        del a["reportedMode"]
                        modified = True
            if "events" in data:
                for e in data["events"]:
                    if "reportedMode" in e:
                        del e["reportedMode"]
                        modified = True
            if "touBuckets" in data:
                for t in data["touBuckets"]:
                    if "readings" in t:
                        if process_readings(t["readings"]):
                            modified = True
                        
        if modified:
            with open(filepath, 'w') as f:
                json.dump(data, f, indent=2)
            print(f"Cleaned {filepath}")

if __name__ == "__main__":
    cleanup_examples()
