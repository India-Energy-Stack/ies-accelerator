import json
import glob
import os

def migrate_file(filepath):
    with open(filepath, 'r') as f:
        data = json.load(f)

    def process_node(node, root_end=None):
        if not isinstance(node, dict):
            return node
            
        # Extract root end time if available
        if 'timePeriod' in node and 'end' in node['timePeriod']:
            root_end = node['timePeriod']['end']
        elif 'coveragePeriod' in node and 'end' in node['coveragePeriod']:
            root_end = node['coveragePeriod']['end']
        elif 'billingPeriod' in node and 'end' in node['billingPeriod']:
            root_end = node['billingPeriod']['end']

        # 1. Update Context
        if '@context' in node and 'v0.5' in node['@context']:
            node['@context'] = node['@context'].replace('v0.5', 'v0.6')

        # 2. Time Terminology
        if 'coveragePeriod' in node:
            node['timePeriod'] = node.pop('coveragePeriod')
        if 'billingPeriod' in node:
            node['timePeriod'] = node.pop('billingPeriod')
        if 'intervalPeriod' in node:
            node['timePeriod'] = node.pop('intervalPeriod')
        if 'capturedAt' in node:
            node['timestamp'] = node.pop('capturedAt')

        # Fix duration in timePeriod
        if 'timePeriod' in node and 'duration' in node['timePeriod']:
            node['timePeriod'].pop('duration')
            if 'end' not in node['timePeriod'] and root_end:
                node['timePeriod']['end'] = root_end

        # 3. Rename qualityOverrides
        if 'qualityOverrides' in node:
            node['overrides'] = node.pop('qualityOverrides')

        # 4. Remove redundant unit, phase, accumulationBehaviour
        for k in ['unit', 'phase', 'accumulationBehaviour']:
            if k in node:
                if k == 'accumulationBehaviour' and 'readingTypeRef' in node and 'id' not in node and 'value' not in node:
                    pass
                else:
                    node.pop(k)

        if node.get('@type') in ['BillingProfile', 'InstantaneousProfile', 'BILLING', 'INSTANTANEOUS'] or node.get('profileType') in ['BILLING', 'INSTANTANEOUS']:
            readings = []
            if 'totals' in node:
                for t in node['totals']:
                    t.pop('openingValue', None)
                    t.pop('closingValue', None)
                    t.pop('integrationPeriod', None)
                    readings.append(t)
                node.pop('totals')
            if 'touBuckets' in node:
                for t in node['touBuckets']:
                    readings.append(t)
                node.pop('touBuckets')
            if 'values' in node:
                for t in node['values']:
                    t.pop('accumulationBehaviour', None)
                    t.pop('unit', None)
                    t.pop('phase', None)
                    readings.append(t)
                node.pop('values')
            if readings:
                node['readings'] = readings

        # 6. Recurse
        for k, v in node.items():
            if isinstance(v, dict):
                node[k] = process_node(v, root_end)
            elif isinstance(v, list):
                node[k] = [process_node(item, root_end) for item in v]
        
        return node

    if isinstance(data, list):
        data = [process_node(item) for item in data]
    else:
        data = process_node(data)

    with open(filepath, 'w') as f:
        json.dump(data, f, indent=2)

files = glob.glob('schemas/MeterData/v0.6/examples/*.json')
# Need to reload original files to migrate cleanly because they are partially migrated
import subprocess
subprocess.run("git checkout schemas/MeterData/v0.6/examples/*.json", shell=True)

for f in files:
    migrate_file(f)
print("Migration completed.")
