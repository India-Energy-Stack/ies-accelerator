import os
import sys
import subprocess

def run_validator(filepath):
    # Runs the validator script against a file and returns (exit_code, output)
    val_script = os.path.join(os.path.dirname(__file__), "validator.py")
    res = subprocess.run(
        [sys.executable, "-X", "utf8", "-B", val_script, filepath],
        capture_output=True,
        text=True
    )
    return res.returncode, res.stdout + res.stderr

def main():
    test_cases_dir = os.path.join(os.path.dirname(__file__), "test_cases")
    
    tests = [
        {"file": "valid_request.json", "expected_pass": True},
        {"file": "invalid_request_mode_unsupported.json", "expected_pass": False, "expected_text": "Telemetry mode 'READING' is not supported"},
        {"file": "invalid_request_profile_mismatch.json", "expected_pass": False, "expected_text": "Register is not permitted in IntervalProfile profile"},
        {"file": "invalid_authorisation_expired.json", "expected_pass": False, "expected_text": "validUntil"}
    ]
    
    success = True
    print("Running MeterDataRequest v0.6 Validator Tests...")
    
    for test in tests:
        filepath = os.path.join(test_cases_dir, test["file"])
        if not os.path.exists(filepath):
            print(f"❌ Test file missing: {test['file']}")
            success = False
            continue
            
        code, out = run_validator(filepath)
        passed = (code == 0)
        
        reason_matched = test.get("expected_text") is None or test["expected_text"] in out
        if passed == test["expected_pass"] and reason_matched:
            print(f"✅ Test '{test['file']}' behaved as expected (passed: {passed})")
        else:
            print(f"❌ Test '{test['file']}' FAILED: expected pass: {test['expected_pass']}, got code {code}")
            if not reason_matched:
                print(f"❌ Expected diagnostic was absent: {test['expected_text']!r}")
            print(f"--- Output: ---\n{out}\n----------------")
            success = False
            
    if success:
        print("\n🎉 All MeterDataRequest v0.6 validator tests PASSED!")
        sys.exit(0)
    else:
        print("\n❌ Some MeterDataRequest v0.6 validator tests FAILED!")
        sys.exit(1)

if __name__ == "__main__":
    main()
