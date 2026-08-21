import json
import glob
import sys
import os

KEY_ORDER = [
    "@context", "@type", "profileType", "id", "customerRefs", "serviceDeliveryPointRefs", "meterRefs",
    "payloadDescriptorSetRef", "intervalPeriod", "timePeriod",
    "payloadDescriptorSets", "name", "payloadDescriptors", "compactSequences",
    "sequenceItems", "readingType", "attribute", "unit", "flowDirection", "reportedMode", "category",
    "intervals", "id", "payloads", "readings", "occurredAt", "value", "openingValue", "closingValue"
]

def order_keys(obj):
    if isinstance(obj, dict):
        ordered = {}
        # Known keys first
        for k in KEY_ORDER:
            if k in obj:
                ordered[k] = order_keys(obj[k])
        # Then other keys
        for k, v in obj.items():
            if k not in ordered:
                ordered[k] = order_keys(v)
        return ordered
    elif isinstance(obj, list):
        return [order_keys(v) for v in obj]
    else:
        return obj

def format_custom(obj, level=0):
    indent = "  " * level
    if isinstance(obj, dict):
        if len(obj) == 0:
            return "{}"
        
        # Heuristic for one-line objects: small number of keys, no nested structures except simple lists
        is_small = len(obj) <= 5 and not any(isinstance(v, (dict, list)) for v in obj.values())
        if is_small:
            items = []
            for k, v in obj.items():
                items.append(f'"{k}": {json.dumps(v)}')
            return "{ " + ", ".join(items) + " }"
        
        items = []
        for k, v in obj.items():
            items.append(f'{indent}  "{k}": {format_custom(v, level + 1)}')
        return "{\n" + ",\n".join(items) + f"\n{indent}}}"
    elif isinstance(obj, list):
        if len(obj) == 0:
            return "[]"
        
        # Check if list of primitives
        if all(not isinstance(v, (dict, list)) for v in obj):
            # One line for primitives if not too long
            items = [json.dumps(v) for v in obj]
            line = "[ " + ", ".join(items) + " ]"
            if len(line) < 80:
                return line
                
        items = []
        for v in obj:
            items.append(f"{indent}  {format_custom(v, level + 1)}")
        return "[\n" + ",\n".join(items) + f"\n{indent}]"
    else:
        return json.dumps(obj)

def main():
    target_dir = sys.argv[1] if len(sys.argv) > 1 else "."
    
    for filepath in glob.glob(os.path.join(target_dir, "*.json")):
        try:
            with open(filepath, 'r') as f:
                data = json.load(f)
            
            data = order_keys(data)
            out_str = format_custom(data)
            # Remove trailing space
            out_str = out_str.replace("} ", "}")
            
            with open(filepath, 'w') as f:
                f.write(out_str + "\n")
                
            print(f"Formatted {filepath}")
        except Exception as e:
            print(f"Error formatting {filepath}: {e}")

if __name__ == "__main__":
    main()
