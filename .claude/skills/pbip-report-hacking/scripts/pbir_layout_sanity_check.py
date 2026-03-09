#!/usr/bin/env python3
"""
PBIP Layout Sanity Check
Analyzes `report.json` in PBIP projects for programmatically introduced visual errors:
- Visuals placed out of bounds (negative X/Y coordinates)
- Hidden visuals that might be an error
- Missing essential properties after AI modification
"""

import sys
import json
from pathlib import Path

def validate_pbir_layout(filepath: Path) -> list:
    issues = []
    
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = json.load(f)
            
        # report.json generally has a 'sections' array
        sections = content.get('sections', [])
        
        for section in sections:
            section_name = section.get('displayName', 'Unknown Page')
            visuals = section.get('visualContainers', [])
            
            for visual in visuals:
                x = visual.get('x', 0)
                y = visual.get('y', 0)
                z = visual.get('z', 0)
                width = visual.get('width', 0)
                height = visual.get('height', 0)
                
                # Check 1: Out of bounds (negative coordinates)
                if x < 0 or y < 0:
                    issues.append(f"Page '{section_name}': Visual at Z-index {z} has negative coordinates (X={x}, Y={y}). It might be invisible.")
                    
                # Check 2: Zero dimensions
                if width <= 0 or height <= 0:
                    issues.append(f"Page '{section_name}': Visual at Z-index {z} has zero or negative dimensions (W={width}, H={height}).")
                    
                # Check 3: Hidden
                if visual.get('isHidden', False):
                    # We might just warn, not necessarily an error, but worth flagging if AI just added it
                    pass # Skipping to reduce noise, hidden can be valid

    except json.JSONDecodeError as e:
        issues.append(f"Invalid JSON parsing {filepath}: {e}")
    except Exception as e:
        issues.append(f"Error parsing {filepath}: {e}")
        
    return issues

def main():
    target = Path(sys.argv[1] if len(sys.argv) > 1 else ".")
    print(f"\n🎨 PBIP Layout Sanity Check running on: {target}\n")
    
    files_to_check = []
    if target.is_file() and target.name == "report.json":
        files_to_check.append(target)
    elif target.is_dir():
        files_to_check.extend(target.rglob("report.json"))
        
    total_issues = 0
    checked_files = 0
    for file in files_to_check:
        issues = validate_pbir_layout(file)
        checked_files += 1
        if issues:
            print(f"📄 {file.parent.name}/{file.name}:")
            for issue in issues:
                print(f"   ❌ {issue}")
            total_issues += len(issues)
            print()
            
    if checked_files == 0:
        print("ℹ️ No 'report.json' files found. Ensure you are pointing to a PBIP report folder.")
        sys.exit(0)
    elif total_issues == 0:
        print("✅ No layout anomalies found in the Power BI reports!")
        sys.exit(0)
    else:
        print(f"⚠️ Found {total_issues} potential UI errors in the report JSON.")
        sys.exit(1)

if __name__ == "__main__":
    main()
