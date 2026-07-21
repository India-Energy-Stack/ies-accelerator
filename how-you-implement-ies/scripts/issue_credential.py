#!/usr/bin/env python3
"""Issue an ElectricityCredential v1.2 via a local/remote OpenCred issuer.

Mirrors the curl walkthrough in `how-you-implement-ies/issue-credentials.md`
(§2.6). The credential is **revocable by default**: the script embeds a
`revocationRegistryUrl`, so OpenCred stamps a `credentialStatus` block onto
the credential (and its signed JWT payload) that verifiers can check.

Environment:
  OPENCRED_API_KEY          (required) issuer API key
  OPENCRED_BASE             OpenCred base URL   (default http://localhost:3100)
  OPENCRED_DEDI_NAMESPACE   DeDi namespace used to build the revocation
                            registry URL        (default discom.example)
  ISSUER_DID                issuer DID; if unset, read from /v1/keys

Usage:
  python3 issue_credential.py                 # revocable (default)
  python3 issue_credential.py --no-revocation # bearer-style, no credentialStatus
  python3 issue_credential.py -o credential.json

To issue *without* revocation, pass --no-revocation (or unset the namespace):
the `revocationRegistryUrl` field is dropped and the issued credential carries
no `credentialStatus` — nothing points a verifier at a revocation registry, so
the credential cannot be revoked. Use this only for demos or bearer-style flows.
"""
import argparse
import json
import os
import sys
import urllib.request

BASE = os.environ.get("OPENCRED_BASE", "http://localhost:3100")
NAMESPACE = os.environ.get("OPENCRED_DEDI_NAMESPACE", "discom.example")

# The whole-registry ("query") URL passed at issue. OpenCred writes back the
# per-credential ("lookup") URL into credentialStatus.id on the issued VC.
REVOCATION_REGISTRY_URL = (
    f"https://api.dedi.global/dedi/query/{NAMESPACE}/vc-revocation-registry"
)


def _api_key() -> str:
    key = os.environ.get("OPENCRED_API_KEY")
    if not key:
        sys.exit("Set OPENCRED_API_KEY (the issuer API key).")
    return key


def _request(method: str, path: str, payload: dict | None = None) -> dict:
    data = json.dumps(payload).encode() if payload is not None else None
    headers = {"Authorization": f"Bearer {_api_key()}"}
    if data is not None:
        headers["Content-Type"] = "application/json"
    req = urllib.request.Request(f"{BASE}{path}", data=data, headers=headers, method=method)
    with urllib.request.urlopen(req) as resp:
        return json.load(resp)


def issuer_did() -> str:
    return os.environ.get("ISSUER_DID") or _request("GET", "/v1/keys")["keys"][0]["id"].split("#")[0]


def build_payload(revocable: bool) -> dict:
    payload = {
        "schemaId": "ies/electricity-credential/v1.2",
        "issuerDid": issuer_did(),
        "proofFormat": "vc-jwt",
        "validFrom": "2026-04-01T00:00:00+05:30",
        "validUntil": "2031-04-01T00:00:00+05:30",
        "credentialSubject": {
            "customerProfile": {
                "customerNumber": "DISCOM-2025-00987654",
                "energyResources": [
                    {
                        "id": "did:web:example.discom.in:assets:meter:MET-IMPORT-001",
                        "type": "METER",
                        "attributes": {"meterCapability": "AMI", "energyDirection": "Forward"},
                    }
                ],
                "consumptionProfiles": [
                    {
                        "meterId": "did:web:example.discom.in:assets:meter:MET-IMPORT-001",
                        "sanctionedLoad": {"value": 10, "unit": "kW"},
                        "tariffCategoryCode": "DS-I",
                        "premisesType": "Residential",
                        "connectionType": "Single-phase",
                    }
                ],
            },
            "customerDetails": {
                "fullName": "Arjun Mehra",
                "installationAddress": {
                    "geo": {"type": "Point", "coordinates": [77.5946, 12.9716]},
                    "address": {
                        "streetAddress": "12, 4th Cross, Indiranagar",
                        "addressLocality": "Bengaluru",
                        "addressRegion": "Karnataka",
                        "postalCode": "560038",
                        "addressCountry": "IND",
                    },
                },
                "serviceConnectionDate": "2018-07-15T00:00:00+05:30",
            },
        },
    }
    if revocable:
        # >>> the one field that makes the credential revocable <<<
        payload["revocationRegistryUrl"] = REVOCATION_REGISTRY_URL
    return payload


def main() -> None:
    parser = argparse.ArgumentParser(description="Issue an ElectricityCredential v1.2 via OpenCred.")
    parser.add_argument(
        "--no-revocation",
        action="store_true",
        help="Omit revocationRegistryUrl (bearer-style, no credentialStatus — cannot be revoked).",
    )
    parser.add_argument("-o", "--out", help="Write the signed credential JSON to this file.")
    args = parser.parse_args()

    revocable = not args.no_revocation
    credential = _request("POST", "/v1/credentials/issue", build_payload(revocable))["credential"]

    if args.out:
        with open(args.out, "w") as fh:
            json.dump(credential, fh, indent=2)
        print(f"Wrote {args.out}")

    status = credential.get("credentialStatus")
    if revocable:
        if not status:
            sys.exit("ERROR: expected a credentialStatus but none was returned.")
        print("Revocable credential issued. credentialStatus:")
        print(json.dumps(status, indent=2))
    else:
        print("Bearer-style credential issued (no credentialStatus — not revocable).")


if __name__ == "__main__":
    main()
