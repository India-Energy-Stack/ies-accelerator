#!/usr/bin/env python3
import os
import re
import sys

def check_markdown_links():
    root_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "schemas", "MeterData", "v0.6"))
    markdown_files = []
    
    # Walk directory to find all markdown files, excluding venv, .git, and scratch
    for dirpath, _, filenames in os.walk(root_dir):
        if any(p in dirpath for p in [".git", "venv", "scratch"]):
            continue
        for filename in filenames:
            if filename.endswith(".md"):
                markdown_files.append(os.path.join(dirpath, filename))
                
    link_pattern = re.compile(r'\[([^\]]+)\]\(([^)]+)\)')
    broken_links_count = 0
    checked_links_count = 0
    
    print("Checking markdown documentation links...")
    
    for filepath in sorted(markdown_files):
        rel_filepath = os.path.relpath(filepath, root_dir)
        file_dir = os.path.dirname(filepath)
        
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()
            
        matches = link_pattern.findall(content)
        for text, url in matches:
            # Clean up URL (remove anchors and query params)
            clean_url = url.split("#")[0].split("?")[0]
            
            # Skip external web links and mailto links
            if clean_url.startswith(("http://", "https://", "mailto:")):
                continue
                
            # Handle file:/// absolute/relative scheme if present
            if clean_url.startswith("file:///"):
                # Clean up to absolute path
                target_path = clean_url.replace("file://", "")
            else:
                # URL is relative to the file it resides in
                # Unquote URL space characters (e.g. %20 -> ' ')
                import urllib.parse
                clean_url = urllib.parse.unquote(clean_url)
                target_path = os.path.abspath(os.path.join(file_dir, clean_url))
                
            checked_links_count += 1
            
            if not os.path.exists(target_path):
                print(f"❌ Broken link in [{rel_filepath}]: [{text}]({url}) -> Target not found: {target_path}")
                broken_links_count += 1
                
    print(f"\nLink check summary: Checked {checked_links_count} links. Found {broken_links_count} broken links.")
    
    if broken_links_count > 0:
        sys.exit(1)
    else:
        print("✅ Link validation SUCCESSFUL!")
        sys.exit(0)

if __name__ == "__main__":
    check_markdown_links()
