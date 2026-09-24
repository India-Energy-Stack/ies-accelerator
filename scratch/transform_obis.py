import json
import os

def main():
    filepath = "schemas/MeterData/v0.6/OBISMapping.json"
    with open(filepath, "r", encoding="utf-8") as f:
        data = json.load(f)

    # Dictionary mapping category to list of profile types
    category_to_profiles = {
        "identification": ["CUSTOMER"],
        "general": ["CUSTOMER", "INTERVAL", "DAILY", "MONTHLY", "INSTANTANEOUS", "EVENT"],
        "voltage": ["INSTANTANEOUS"],
        "current": ["INSTANTANEOUS"],
        "power": ["INSTANTANEOUS"],
        "energyCumulative": ["DAILY", "MONTHLY"],
        "energyIncremental": ["INTERVAL"],
        "energyToU": ["MONTHLY"],
        "demand": ["MONTHLY"],
        "programmable": ["CUSTOMER", "MONTHLY"],
        "profile": ["CUSTOMER", "DAILY", "MONTHLY", "INTERVAL", "EVENT"],
        "eventLog": ["EVENT"]
    }

    new_codes = []
    
    # Process existing codes
    for obis_code, details in data["codes"].items():
        record = {"obis": obis_code}
        for k, v in details.items():
            record[k] = v
        
        # Add list of profiles
        category = details.get("category", "")
        record["profiles"] = category_to_profiles.get(category, [])

        # Add attributes for maximum demand
        if category == "demand":
            record["attributes"] = [
                {
                    "name": "timestamp",
                    "unit": "time",
                    "description": "Timestamp of peak occurrence"
                }
            ]
        
        new_codes.append(record)

    # Add standard DLMS Alarm Register code
    alarm_reg_present = any(c["obis"] == "0.0.97.98.0.255" for c in new_codes)
    if not alarm_reg_present:
        new_codes.append({
            "obis": "0.0.97.98.0.255",
            "name": "Alarm register",
            "shortLabel": "Alarm Reg",
            "unit": "",
            "category": "general",
            "meterCategories": ["D1", "D2", "D3", "D4"],
            "profiles": ["ALARM"],
            "source": "IS 15959"
        })

    data["codes"] = new_codes

    # Add alarms block
    data["alarms"] = {
        "_description": "Smart meter alarm register definitions. Alarms represent active real-time conditions/states on the meter.",
        "ids": {
            "1": { "name": "Voltage Sag", "category": "voltage" },
            "2": { "name": "Voltage Swell", "category": "voltage" },
            "3": { "name": "Over Current", "category": "current" },
            "4": { "name": "Power Threshold Exceeded", "category": "power" },
            "5": { "name": "Magnetic Tamper", "category": "tamper" },
            "6": { "name": "Meter Cover Open", "category": "tamper" },
            "7": { "name": "Neutral Disturbance", "category": "voltage" },
            "8": { "name": "Low Prepayment Balance", "category": "billing" }
        }
    }

    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    print("OBISMapping.json transformed successfully with alarm definitions!")

if __name__ == "__main__":
    main()
