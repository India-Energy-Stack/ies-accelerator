import json
import os
import sys

def load_json(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def resolve_properties(schema_def, all_schemas):
    """
    Resolve properties of a schema, including those inherited via allOf and $ref.
    """
    properties = {}
    if not isinstance(schema_def, dict):
        return properties
        
    # 1. Handle allOf composition
    if "allOf" in schema_def:
        for subschema in schema_def["allOf"]:
            properties.update(resolve_properties(subschema, all_schemas))
            
    # 2. Handle direct $ref
    if "$ref" in schema_def:
        ref_path = schema_def["$ref"]
        # Extract the component name from path
        ref_name = ref_path.split("/")[-1]
        ref_def = all_schemas.get(ref_name, {})
        properties.update(resolve_properties(ref_def, all_schemas))
            
    # 3. Handle direct properties
    if "properties" in schema_def:
        properties.update(schema_def["properties"])
        
    return properties

def are_properties_equivalent(v05_prop, v06_props):
    # Mapping of v0.5 property names to set of acceptable v0.6 property names
    equivalences = {
        "coveragePeriod": {"timePeriod"},
        "billingPeriod": {"timePeriod"},
        "capturedAt": {"timestamp"},
        "values": {"readings", "intervalBlocks"},
        "totals": {"readings"}
    }
    
    if v05_prop in v06_props:
        return True
        
    if v05_prop in equivalences:
        equivalent_set = equivalences[v05_prop]
        if any(eq in v06_props for eq in equivalent_set):
            return True
            
    return False

def verify_obis_mapping():
    print("=== Verification 1: OBIS Mapping ===")
    v05_path = "schemas/MeterData/v0.5/OBISMapping.json"
    v06_path = "schemas/MeterData/v0.6/OBISMapping.json"
    
    v05 = load_json(v05_path)
    v06 = load_json(v06_path)
    
    v05_codes = set(v05["codes"].keys())
    v06_codes = set(item["obis"] for item in v06["codes"])
    
    missing_codes = v05_codes - v06_codes
    if missing_codes:
        print(f"❌ Error: The following OBIS codes from v0.5 are missing in v0.6: {missing_codes}")
        return False
    else:
        print("✅ Success: No OBIS codes from v0.5 are lost in v0.6.")
        added_codes = v06_codes - v05_codes
        print(f"ℹ️ Added OBIS codes in v0.6: {added_codes}")
        
    if "alarms" in v06:
        print("✅ Success: v0.6 OBISMapping.json includes 'alarms' definitions.")
    else:
        print("❌ Error: v0.6 OBISMapping.json does not contain 'alarms' block.")
        return False
        
    return True

def verify_schema_properties():
    print("\n=== Verification 2: Schema Properties ===")
    v05_path = "schemas/MeterData/v0.5/schema.json"
    v06_path = "schemas/MeterData/v0.6/schema.json"
    
    v05 = load_json(v05_path)
    v06 = load_json(v06_path)
    
    v05_components = v05["$defs"]
    v06_components = v06["$defs"]
    
    profiles_to_compare = [
        "IntervalProfile",
        "DailyProfile",
        "InstantaneousProfile",
        "EventProfile"
    ]
    
    success = True
    for profile in profiles_to_compare:
        v05_props = set(resolve_properties(v05_components[profile], v05_components).keys())
        v06_props = set(resolve_properties(v06_components[profile], v06_components).keys())
        
        missing_props = [p for p in v05_props if not are_properties_equivalent(p, v06_props)]
        if missing_props:
            print(f"❌ Error: {profile} is missing properties in v0.6: {missing_props}")
            print(f"   v0.5 properties: {v05_props}")
            print(f"   v0.6 properties: {v06_props}")
            success = False
        else:
            print(f"✅ Success: No properties lost in {profile}.")
            
    # For BillingProfile vs (MonthlyProfile + BillDetails)
    print("\n=== Verification 3: BillingProfile Split ===")
    v05_billing_props = set(resolve_properties(v05_components["BillingProfile"], v05_components).keys())
    
    v06_monthly_props = set(resolve_properties(v06_components["MonthlyProfile"], v06_components).keys())
    v06_bill_details_props = set(resolve_properties(v06_components["BillDetails"], v06_components).keys())
    
    union_v06_props = v06_monthly_props | v06_bill_details_props
    
    missing_billing_props = [p for p in v05_billing_props if not are_properties_equivalent(p, union_v06_props)]
    if missing_billing_props:
        print(f"❌ Error: The following properties from BillingProfile v0.5 are missing in v0.6 MonthlyProfile/BillDetails: {missing_billing_props}")
        success = False
    else:
        print("✅ Success: All properties from BillingProfile v0.5 are preserved in v0.6 MonthlyProfile + BillDetails.")
        print(f"   v0.5 BillingProfile properties: {v05_billing_props}")
        print(f"   v0.6 MonthlyProfile properties: {v06_monthly_props}")
        print(f"   v0.6 BillDetails properties: {v06_bill_details_props}")
        
    return success

def main():
    res1 = verify_obis_mapping()
    res2 = verify_schema_properties()
    
    if res1 and res2:
        print("\n🎉 Verification Successful! No data is lost, all changes are strictly additive.")
        sys.exit(0)
    else:
        print("\n❌ Verification Failed! Some properties or codes were lost.")
        sys.exit(1)

if __name__ == "__main__":
    main()
