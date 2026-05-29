import os
import sys
import json
import jsonschema
import importlib.util

# Load MeterData/v0.6/validation/validator.py dynamically to share core logic without circular imports
core_validator_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../MeterData/v0.6/validation/validator.py"))
if not os.path.exists(core_validator_path):
    print(f"Error: Core validator not found at {core_validator_path}")
    sys.exit(1)

spec = importlib.util.spec_from_file_location("meter_data_validator", core_validator_path)
meter_data_validator = importlib.util.module_from_spec(spec)
sys.modules["meter_data_validator"] = meter_data_validator
try:
    spec.loader.exec_module(meter_data_validator)
except Exception as e:
    print(f"Error executing core validator module: {e}")
    sys.exit(1)

resolve_reading_type = meter_data_validator.resolve_reading_type
load_obis_mapping = meter_data_validator.load_obis_mapping
map_profile_type_to_registry = meter_data_validator.map_profile_type_to_registry

try:
    from referencing import Registry, Resource
    energy_cred_schema = {
        "$schema": "https://json-schema.org/draft/2020-12/schema",
        "type": "object"
    }
    energy_res_schema = {
        "$schema": "https://json-schema.org/draft/2020-12/schema",
        "type": "object"
    }
    registry = Registry().with_resources([
        ("https://schema.beckn.io/EnergyCredential/v2.0", Resource.from_contents(energy_cred_schema)),
        ("https://schema.beckn.io/EnergyResource/v2.0", Resource.from_contents(energy_res_schema))
    ])
except ImportError:
    registry = None

def get_all_capabilities(data):
    # Extracts all MeterDataCapabilities objects from a payload
    # Root payload can be a MeterDataRequest, a MeterDataAuthorisation, or a MeterDataCapabilities document.
    capabilities_list = []
    
    if not isinstance(data, dict):
        return capabilities_list
        
    # Check if root is Capabilities object
    if "profiles" in data and not ("capabilitiesRequested" in data or "capabilities" in data or "grantor" in data):
        capabilities_list.append(data)
        
    # Check if root is Request object
    if "capabilitiesRequested" in data:
        capabilities_list.append(data["capabilitiesRequested"])
    if "authorisation" in data:
        auth = data["authorisation"]
        if isinstance(auth, dict) and "capabilities" in auth:
            capabilities_list.append(auth["capabilities"])
            
    # Check if root is Authorisation object
    if "capabilities" in data and ("grantor" in data or "grantee" in data):
        capabilities_list.append(data["capabilities"])
        
    return capabilities_list

def map_request_profile_type(p_type):
    # Maps request schema ProfileCapability.profileType enum to IES codes profiles
    mapping = {
        "CustomerProfile": "CUSTOMER",
        "IntervalProfile": "INTERVAL",
        "DailyProfile": "DAILY",
        "MonthlyProfile": "MONTHLY",
        "BillDetails": "MONTHLY",
        "InstantaneousProfile": "INSTANTANEOUS",
        "EventProfile": "EVENT",
        "AlarmProfile": "ALARM"
    }
    return mapping.get(p_type)

def validate_semantics(data, obis_mapping):
    errors = []
    
    # 1. Authorisation Time Window Validation
    # Checks if validUntil is strictly after validFrom
    if isinstance(data, dict):
        auth_objects = []
        if "grantor" in data and "grantee" in data:
            auth_objects.append(data)
        if "authorisation" in data and isinstance(data["authorisation"], dict):
            auth_objects.append(data["authorisation"])
            
        for auth in auth_objects:
            v_from = auth.get("validFrom")
            v_until = auth.get("validUntil")
            if v_from and v_until:
                if v_until <= v_from:
                    errors.append(f"Authorisation time window invalid: validUntil ({v_until}) is not strictly after validFrom ({v_from})")

    # 2. ValueCapability Semantic Check
    capabilities = get_all_capabilities(data)
    for cap_idx, cap in enumerate(capabilities):
        profiles = cap.get("profiles", [])
        for p_idx, profile in enumerate(profiles):
            p_type = profile.get("profileType")
            reg_p_type = map_request_profile_type(p_type)
            
            readings = profile.get("readings", [])
            for r_idx, reading in enumerate(readings):
                val = reading.get("value")
                mode = reading.get("mode")
                
                code, info = resolve_reading_type(val, obis_mapping)
                if not code:
                    errors.append(f"Capabilities[{cap_idx}] Profile '{p_type}' Reading[{r_idx}] '{val}': Could not resolve readingType in IES codes.json")
                    continue
                    
                # Profile Compatibility Check
                reg_profiles = info.get("profiles", [])
                if reg_p_type and reg_p_type not in ["CUSTOMER"] and reg_p_type not in reg_profiles:
                    errors.append(f"Capabilities[{cap_idx}] Profile '{p_type}' Reading[{r_idx}] '{val}': Register is not permitted in {p_type} profile. Permitted: {reg_profiles}")
                    
                # Mode Check
                if mode and info:
                    supported_modes = info.get("supportedModes", [])
                    if mode not in supported_modes:
                        errors.append(f"Capabilities[{cap_idx}] Profile '{p_type}' Reading[{r_idx}] '{val}': Telemetry mode '{mode}' is not supported. Supported: {supported_modes}")
                        
    return errors

def main():
    if len(sys.argv) < 2:
        print("Usage: python validator.py <target_json_or_directory>")
        sys.exit(1)
        
    target_path = sys.argv[1]
    
    # Path setup
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    obis_mapping_path = os.path.abspath(os.path.join(base_dir, "../../MeterData/v0.6/IES codes.json"))
    
    if not os.path.exists(obis_mapping_path):
        print(f"Error: IES codes.json not found at {obis_mapping_path}")
        sys.exit(1)
        
    obis_mapping = load_obis_mapping(obis_mapping_path)
    
    schema_path = os.path.join(base_dir, "schema.json")
    if not os.path.exists(schema_path):
        print(f"Error: schema.json at {schema_path} does not exist.")
        sys.exit(1)
        
    with open(schema_path, "r", encoding="utf-8") as f:
        schema = json.load(f)
        
    if registry is not None:
        validator = jsonschema.Draft202012Validator(schema, registry=registry)
    else:
        validator = jsonschema.Draft202012Validator(schema)
        
    success = True
    
    files_to_validate = []
    if os.path.isdir(target_path):
        for filename in sorted(os.listdir(target_path)):
            if filename.endswith(".json"):
                files_to_validate.append(os.path.join(target_path, filename))
    else:
        files_to_validate.append(target_path)
        
    for filepath in files_to_validate:
        basename = os.path.basename(filepath)
        print(f"\n--- Semantics Audit: {basename} ---")
        
        try:
            with open(filepath, "r", encoding="utf-8") as f:
                data = json.load(f)
        except Exception as e:
            print(f"❌ Failed to parse JSON: {e}")
            success = False
            continue
            
        errors = sorted(validator.iter_errors(data), key=lambda e: e.path)
        if errors:
            success = False
            print("❌ Structural Validation Failed:")
            for error in errors:
                path = " -> ".join([str(p) for p in error.path]) if error.path else "Root"
                print(f"  - Path: {path} | Message: {error.message}")
        else:
            print("✅ Structural validation: PASSED")
            
        semantic_errors = validate_semantics(data, obis_mapping)
        if semantic_errors:
            success = False
            print("❌ Semantic Validation Failed:")
            for error in semantic_errors:
                print(f"  - {error}")
        else:
            print("✅ Semantic validation: PASSED")
            
    if success:
        print("\n✅ Semantics audit SUCCESSFUL! All requests conform to physical and authorization constraints.")
        sys.exit(0)
    else:
        print("\n❌ Semantics audit FAILED!")
        sys.exit(1)

if __name__ == "__main__":
    main()
