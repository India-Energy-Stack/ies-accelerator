import json
import glob
import os
import re
from datetime import datetime

def iso_duration(start_str, end_str):
    try:
        fmt = "%Y-%m-%dT%H:%M:%S%z"
        s = datetime.strptime(start_str, fmt)
        e = datetime.strptime(end_str, fmt)
        diff = e - s
        days = diff.days
        seconds = diff.seconds
        
        if days == 30 or days == 31 or (days >= 28 and e.day == s.day): return "P1M"
        if days > 0 and seconds == 0: return f"P{days}D"
        
        hours = seconds // 3600
        minutes = (seconds % 3600) // 60
        if days == 0:
            if hours > 0 and minutes == 0: return f"PT{hours}H"
            if hours == 0 and minutes > 0: return f"PT{minutes}M"
            if hours > 0 and minutes > 0: return f"PT{hours}H{minutes}M"
    except Exception as ex:
        pass
    return "P1D"

def reorder_keys(node):
    if not isinstance(node, dict):
        return node
    
    order = [
        '@context', '@type', 'profileType', 'readingPurpose', 'customerRefs', 'meterRefs', 
        'serviceDeliveryPointRefs', 'timePeriod', 'timestamp', 'billNumber', 'billDate', 
        'dueDate', 'currency', 'amountDue', 'readings', 'touBuckets', 'payloadDescriptors', 'intervals', 
        'overrides', 'events'
    ]
    
    new_node = {}
    for k in order:
        if k in node:
            new_node[k] = node[k]
    for k, v in node.items():
        if k not in new_node:
            new_node[k] = v
    return new_node

def process_node(node):
    if not isinstance(node, dict):
        return node
        
    if '@context' in node and 'v0.5' in node['@context']:
        node['@context'] = node['@context'].replace('v0.5', 'v0.6')

    for p_name in ['coveragePeriod', 'billingPeriod']:
        if p_name in node:
            p = node.pop(p_name)
            if 'end' in p:
                p['duration'] = iso_duration(p['start'], p['end'])
                p.pop('end')
            node['timePeriod'] = p
            
    if 'intervalPeriod' in node:
        ip = node.pop('intervalPeriod')
        il = node.pop('intervalLength', None)
        node['timePeriod'] = {
            'start': ip['start'],
            'duration': il if il else ip['duration']
        }

    # Extract _mdOccurredAt from intervals and move to overrides
    if 'intervals' in node:
        overrides = node.setdefault('overrides', [])
        for row in node['intervals']:
            if '_mdOccurredAt' in row:
                t = row.pop('_mdOccurredAt')
                overrides.append({
                    'intervalId': row['id'],
                    'descriptorIndex': 2,
                    'occurredAt': t
                })
        if not overrides:
            node.pop('overrides', None)

    # Strip _label and other custom _ prefix properties
    for k in list(node.keys()):
        if k.startswith('_'):
            node.pop(k)

    if 'capturedAt' in node:
        node['timestamp'] = node.pop('capturedAt')

    if 'qualityOverrides' in node:
        overrides = node.pop('qualityOverrides')
        for ov in overrides:
            if 'descriptorIndex' not in ov:
                ov['descriptorIndex'] = 0
        node['overrides'] = overrides

    for k in ['unit', 'phase', 'accumulationBehaviour']:
        if k in node:
            if k == 'accumulationBehaviour' and 'readingTypeRef' in node and 'id' not in node and 'value' not in node:
                pass
            else:
                node.pop(k)

    if node.get('@type') in ['BillingProfile', 'InstantaneousProfile', 'BILLING', 'INSTANTANEOUS'] or node.get('profileType') in ['BILLING', 'INSTANTANEOUS']:
        readings = []
        for k in ['totals', 'values']:
            if k in node:
                for t in node[k]:
                    t.pop('accumulationBehaviour', None)
                    t.pop('unit', None)
                    t.pop('phase', None)
                    readings.append(t)
                node.pop(k)
        if readings:
            node['readings'] = readings

        if 'touBuckets' in node:
            by_zone = {}
            for t in node['touBuckets']:
                zone = t.pop('zone', None)
                if zone is None:
                    continue
                t.pop('accumulationBehaviour', None)
                t.pop('unit', None)
                t.pop('phase', None)
                by_zone.setdefault(zone, []).append(t)
            
            tou_buckets = []
            for zone in sorted(by_zone.keys()):
                tou_buckets.append({
                    'zone': zone,
                    'readings': by_zone[zone]
                })
            node['touBuckets'] = tou_buckets

    for k, v in node.items():
        if isinstance(v, dict):
            node[k] = process_node(v)
        elif isinstance(v, list):
            node[k] = [process_node(item) for item in v]
            
    return reorder_keys(node)

def compact_json(text):
    # 1. Collapse values arrays safely (e.g. "values": [ 1, 2 ])
    def collapse_values(m):
        return '"values": [' + ', '.join(x.strip() for x in m.group(1).split(',')) + ']'
    text = re.sub(r'"values"\s*:\s*\[([^\]]*)\]', collapse_values, text)
    
    # 2. Collapse simple readingTypeRef objects: { "readingTypeRef": { "scheme": "...", "value": "..." } }
    def collapse_reading_type(m):
        return '"readingTypeRef": { ' + ' '.join(x.strip() for x in m.group(1).split('\n')) + ' }'
    text = re.sub(r'"readingTypeRef"\s*:\s*\{([^\}]*)\}', collapse_reading_type, text)
    
    # 3. Collapse simple timePeriod objects: { "timePeriod": { "start": "...", "duration": "..." } }
    def collapse_time_period(m):
        return '"timePeriod": { ' + ' '.join(x.strip() for x in m.group(1).split('\n')) + ' }'
    text = re.sub(r'"timePeriod"\s*:\s*\{([^\}]*)\}', collapse_time_period, text)

    # 4. Collapse simple scheme-value identifier dicts inside arrays:
    # { "scheme": "...", "value": "..." }
    def collapse_ident(m):
        cleaned = re.sub(r'\s+', ' ', m.group(0))
        return cleaned
    text = re.sub(r'\{\s*"scheme"\s*:\s*"[^"]+"\s*,\s*"value"\s*:\s*"[^"]+"\s*\}', collapse_ident, text)
    
    return text

files = glob.glob('schemas/MeterData/v0.6/examples/*.json')
for f in files:
    print(f"Migrating {f}...")
    with open(f, 'r') as file:
        data = json.load(file)
        
    if isinstance(data, list):
        data = [process_node(item) for item in data]
    else:
        data = process_node(data)
        
    out = json.dumps(data, indent=2)
    out = compact_json(out)
    
    with open(f, 'w') as file:
        file.write(out + '\n')
print("Migration and formatting completed successfully.")
