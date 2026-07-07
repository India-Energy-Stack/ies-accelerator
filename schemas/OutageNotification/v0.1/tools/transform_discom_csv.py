#!/usr/bin/env python3
"""Transform a DISCOM-style planned-shutdown CSV into OutageNotification JSON.

Mirrors the columns of a typical DISCOM "Detail of Planned Shutdown" sheet
and emits an array of OutageNotification objects (IES OutageNotification v0.1).

Grouping: rows sharing a `group_id` become ONE notice (one substation +
window + reason), with each feeder as an entry in `affectedAssets[]`. The
feeder smart-meter number maps to `affectedAssets[].meterRef`
(scheme METER_SERIAL) — the 1:1 feeder<->meter link.

Language: the CSV is read and the JSON written as UTF-8 with
ensure_ascii=False, so Hindi (Devanagari) `reason` / `consumer_area` text is
preserved verbatim in `cause.text`, `affectedArea.text` and
`publicInfo.description`; `publicInfo.language` is set to "hi" when Devanagari
is present, else "en".

Usage:
  python3 transform_discom_csv.py discom_planned_shutdown.csv -o out.json
  python3 transform_discom_csv.py discom_planned_shutdown.csv          # stdout
"""
import argparse
import csv
import json
import sys
from collections import OrderedDict
from datetime import datetime

CONTEXT = "https://india-energy-stack.github.io/ies-accelerator/schemas/OutageNotification/v0.1/context.jsonld"
TZ = "+05:30"  # Asia/Kolkata

# DISCOM "Feeder Type" -> schema consumerCategory enum; others -> OTHER.
CONSUMER_CATEGORY = {
    "URBAN": "URBAN", "RURAL": "RURAL", "AGRICULTURE": "AGRICULTURE",
    "INDUSTRIAL": "INDUSTRIAL", "MIXED": "MIXED",
}

# Keywords (English + Hindi) that indicate construction/new-build rather than
# routine maintenance -> IEEE 1782 §4.5 PLANNED subcategory.
NEW_CONSTRUCTION_KEYS = [
    "construction", "new ", "shifting", "underground",
    "निर्माण", "नई", "नया", "पोल लगाने", "ट्रांसफार्मर", "लाइन",
]


def has_devanagari(text):
    return any("ऀ" <= ch <= "ॿ" for ch in (text or ""))


def consumer_category(value):
    return CONSUMER_CATEGORY.get((value or "").strip().upper(), "OTHER")


def cause_subcategory(reason):
    r = (reason or "").lower()
    return "NEW_CONSTRUCTION" if any(k in r for k in NEW_CONSTRUCTION_KEYS) else "MAINTENANCE"


def iso_duration(from_time, to_time):
    f = datetime.strptime(from_time.strip(), "%H:%M")
    t = datetime.strptime(to_time.strip(), "%H:%M")
    minutes = int((t - f).total_seconds() // 60)
    if minutes < 0:
        minutes += 24 * 60  # window crossing midnight
    h, m = divmod(minutes, 60)
    out = "PT" + (f"{h}H" if h else "") + (f"{m}M" if m else "")
    return out if out != "PT" else "PT0M"


def to_datetime(date_str, time_str):
    d = datetime.strptime(date_str.strip(), "%d-%m-%Y")
    hh, mm = time_str.strip().split(":")
    return f"{d:%Y-%m-%d}T{int(hh):02d}:{int(mm):02d}:00{TZ}"


def build_notice(group_id, rows):
    r0 = rows[0]
    reason = (r0.get("reason") or "").strip()
    area = (r0.get("consumer_area") or "").strip()
    substation = (r0.get("substation") or "").strip()
    lang = "hi" if has_devanagari(reason) or has_devanagari(area) else "en"

    assets = []
    for r in rows:
        asset = OrderedDict()
        asset["id"] = {"scheme": "FEEDER", "value": (r.get("feeder") or "").strip()}
        asset["assetLevel"] = "FEEDER"
        asset["voltageLevel"] = "11kV"
        asset["consumerCategory"] = consumer_category(r.get("feeder_type"))
        meter = (r.get("feeder_smart_meter") or "").strip()
        if meter:  # the 1:1 feeder<->smart-meter link
            asset["meterRef"] = {"scheme": "METER_SERIAL", "value": meter}
        assets.append(asset)

    network = OrderedDict()
    for col in ("zone", "circle", "division"):
        v = (r0.get(col) or "").strip()
        if v:
            network[col] = v
    if substation:
        network["substation"] = {"scheme": "SUBSTATION", "value": substation}

    notice = OrderedDict()
    notice["@context"] = CONTEXT
    notice["@type"] = "OutageNotification"
    notice["objectType"] = "OUTAGE_NOTIFICATION"
    notice["id"] = {"scheme": "OTHER", "value": f"DISCOM-PSD-{group_id}", "namespace": "outages.discom.example"}
    notice["outageClass"] = "PLANNED"
    notice["status"] = "SCHEDULED"
    notice["msgType"] = "ALERT"
    notice["category"] = "MAINTENANCE"
    notice["cause"] = {"category": "PLANNED", "subcategory": cause_subcategory(reason), "text": reason}
    notice["forceMajeure"] = False
    notice["issuedBy"] = {"name": "the DISCOM", "contact": "1912"}
    notice["issuedAt"] = to_datetime(r0["date"], "00:00")
    if network:
        notice["network"] = network
    notice["affectedAssets"] = assets
    if area:
        notice["affectedArea"] = {"text": area}
    notice["timing"] = {"period": {
        "start": to_datetime(r0["date"], r0["from_time"]),
        "duration": iso_duration(r0["from_time"], r0["to_time"]),
    }}
    public = OrderedDict()
    public["language"] = lang
    public["headline"] = (
        f"Planned shutdown — {substation}, {r0['date'].strip()} "
        f"{r0['from_time'].strip()}-{r0['to_time'].strip()}"
    )
    if reason:
        public["description"] = reason  # verbatim; Hindi preserved
    notice["publicInfo"] = public
    notice["extensions"] = {"discom": {"groupId": group_id, "downType": "FEEDER"}}
    return notice


def transform(csv_path):
    groups = OrderedDict()
    with open(csv_path, encoding="utf-8") as f:
        for row in csv.DictReader(f):
            gid = (row.get("group_id") or "").strip()
            groups.setdefault(gid, []).append(row)
    return [build_notice(gid, rows) for gid, rows in groups.items()]


def main():
    ap = argparse.ArgumentParser(description="Transform DISCOM planned-shutdown CSV to OutageNotification JSON.")
    ap.add_argument("csv_path")
    ap.add_argument("-o", "--output", help="write JSON here (default: stdout)")
    args = ap.parse_args()

    notices = transform(args.csv_path)
    text = json.dumps(notices, ensure_ascii=False, indent=2)
    if args.output:
        with open(args.output, "w", encoding="utf-8") as f:
            f.write(text + "\n")
        print(f"Wrote {len(notices)} OutageNotification(s) to {args.output}", file=sys.stderr)
    else:
        print(text)


if __name__ == "__main__":
    main()
