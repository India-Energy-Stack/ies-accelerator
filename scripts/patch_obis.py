import json
import sys

def patch_obis():
    with open('schemas/MeterData/v0.6/OBISMapping.json', 'r') as f:
        data = json.load(f)
        
    for c in data['codes']:
        allowed = ["value"]
        cat = c.get("category", "")
        short = c.get("shortLabel", "")
        name = c.get("name", "").lower()
        
        # Energy registers usually support opening/closing value when used in READING mode (delta derivation)
        # Even if used as USAGE, they might just report 'value'. 
        if "energy" in name or "block" in name.lower() or "tz" in name.lower() or cat in ["energy", "cumulative_energy"]:
            allowed.extend(["openingValue", "closingValue"])
            
        # Maximum demand
        if "maximum demand" in name or "md " in short.lower():
            allowed.extend(["occurredAt", "integrationPeriod"])
            
        # Add 'validationStatus', 'changeMethod', 'failCode', 'source' as generally applicable metadata
        allowed.extend(["validationStatus", "source", "changeMethod", "failCode"])
        
        c["allowedAttributes"] = allowed
        
    with open('schemas/MeterData/v0.6/OBISMapping.json', 'w') as f:
        json.dump(data, f, indent=2)
        
if __name__ == "__main__":
    patch_obis()
