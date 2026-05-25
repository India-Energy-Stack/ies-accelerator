#!/usr/bin/env python3
import os
import json

def main():
    pairs = [
        ("IntervalProfile_UsageMode.json", "IntervalProfile_UsageMode_OpenAdr.json"),
        ("DailyProfile_ReadingMode.json", "DailyProfile_ReadingMode_OpenAdr.json"),
        ("BillingProfile_Elaborated.json", "BillingProfile_Elaborated_OpenAdr.json")
    ]
    
    v6_dir = "schemas/MeterData/v0.6/examples"
    oadr_dir = "schemas/MeterData/vOpenAdr/examples"
    
    print("| Example Profile | v0.6 Size (Bytes) | vOpenAdr Size (Bytes) | Size Ratio (Oadr / v0.6) | % Difference |")
    print("| :--- | :---: | :---: | :---: | :---: |")
    
    for v6_name, oadr_name in pairs:
        v6_path = os.path.join(v6_dir, v6_name)
        oadr_path = os.path.join(oadr_dir, oadr_name)
        
        v6_size = os.path.getsize(v6_path)
        oadr_size = os.path.getsize(oadr_path)
        
        ratio = oadr_size / v6_size
        pct = (oadr_size - v6_size) / v6_size * 100
        
        print(f"| {v6_name.replace('.json', '')} | {v6_size} | {oadr_size} | {ratio:.2f}x | {pct:+.1f}% |")

if __name__ == "__main__":
    main()
