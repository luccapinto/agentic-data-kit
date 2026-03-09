#!/usr/bin/env python3
"""
Checklist Format Verifier
Scans Markdown files (e.g. task.md) used by AI agents to ensure
the status checkboxes follow the standard: [ ], [/], [x].
Alerts if tasks are left in an invalid state.
"""

import sys
import re
from pathlib import Path

def verify_markdown_checklists(filepath: Path) -> list:
    issues = []
    
    try:
        content = filepath.read_text(encoding="utf-8")
        lines = content.splitlines()
        
        for i, line in enumerate(lines, 1):
            line_str = line.strip()
            
            # Simple heuristic for a markdown list item with some bracket content
            if re.match(r'^[-\*]\s+\[.*\]', line_str):
                # Check valid standard checkboxes
                if not (line_str.startswith("- [ ]") or 
                        line_str.startswith("- [/]") or 
                        line_str.startswith("- [x]") or 
                        line_str.startswith("- [X]") or
                        line_str.startswith("* [ ]") or 
                        line_str.startswith("* [/]") or 
                        line_str.startswith("* [x]") or 
                        line_str.startswith("* [X]")):
                    issues.append(f"Line {i}: Non-standard checkbox format found: '{line_str}'. Must be [ ], [/], or [x].")
                    
    except Exception as e:
        issues.append(f"Error parsing {filepath}: {e}")
        
    return issues

def main():
    target = Path(sys.argv[1] if len(sys.argv) > 1 else ".")
    print(f"\n✅ Checklist Format Verifier running on: {target}\n")
    
    files_to_check = []
    if target.is_file() and target.suffix == ".md":
        files_to_check.append(target)
    elif target.is_dir():
        # Focus mainly on active task/plan trackers
        for file in target.rglob("*.md"):
            if "task" in file.name.lower() or "plan" in file.name.lower() or "checklist" in file.name.lower():
                files_to_check.append(file)
                
    total_issues = 0
    checked_files = 0
    for file in files_to_check:
        issues = verify_markdown_checklists(file)
        checked_files += 1
        if issues:
            print(f"📄 {file.name}:")
            for issue in issues:
                print(f"   ❌ {issue}")
            total_issues += len(issues)
            print()
            
    if checked_files == 0:
        print("ℹ️ No relevant markdown checklist files found.")
        sys.exit(0)
    elif total_issues == 0:
        print("✅ Markdown task formatting is pristine!")
        sys.exit(0)
    else:
        print(f"⚠️ Found {total_issues} task formatting anomalies.")
        sys.exit(1)

if __name__ == "__main__":
    main()
