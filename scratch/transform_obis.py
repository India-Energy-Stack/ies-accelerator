import json
import os

mapping_file = 'schemas/MeterData/v0.6/OBISMapping.json'

with open(mapping_file, 'r') as f:
    data = json.load(f)

for code in data['codes']:
    cat = code.get('category')
    
    if cat in ['voltage', 'current', 'power', 'general', 'identification', 'programmable', 'billing', 'tamper', 'eventLog', 'profile']:
        code['supportedModes'] = ['READING']
        code['defaultMode'] = 'READING'
    elif cat in ['demand']:
        code['supportedModes'] = ['USAGE']
        code['defaultMode'] = 'USAGE'
    elif cat in ['energyIncremental']:
        code['supportedModes'] = ['USAGE']
        code['defaultMode'] = 'USAGE'
    elif cat in ['energyCumulative', 'energyToU']:
        code['supportedModes'] = ['READING', 'USAGE']
        code['defaultMode'] = 'READING'
    else:
        # Fallback to READING
        code['supportedModes'] = ['READING']
        code['defaultMode'] = 'READING'

with open(mapping_file, 'w') as f:
    json.dump(data, f, indent=2)

print("OBISMapping.json updated successfully.")
