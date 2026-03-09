#!/usr/bin/env python3
"""
DAX Best Practices Auditor
Looks for generic DAX patterns that cause performance bottlenecks:
- FILTER(Table, ...) instead of FILTER(Valid_Column, ...)
- Bi-directional cross-filtering functions (CROSSFILTER)
"""

import sys
import re
from pathlib import Path

def audit_dax_expressions(filepath: Path) -> list:
    issues = []
    try:
        content = filepath.read_text(encoding="utf-8")
        lines = content.splitlines()
        
        for i, line in enumerate(lines, 1):
            line_str = line.upper()
            
            # Simple heuristic matching: FILTER(Table) vs FILTER(Column)
            # This regex looks for FILTER( 'TableName' or FILTER( TableName
            if re.search(r'FILTER\s*\(\s*\'?[a-zA-Z0-9_]+\'?\s*,', line_str):
                # We can't know for sure if it's a table or column without the model,
                # but often filtering an entire table is a red flag.
                issues.append(f"Line {i}: 'FILTER(Table, ...)' detected. Consider filtering specific columns instead of the entire table for better performance.")
                
            if "CROSSFILTER" in line_str and "BOTH" in line_str:
                issues.append(f"Line {i}: 'CROSSFILTER(..., BOTH)' detected. Bi-directional filtering can cause severe performance issues and ambiguity.")

            if "ISERROR" in line_str or "IFERROR" in line_str:
                issues.append(f"Line {i}: Error-handling functions like ISERROR force the engine to work row-by-row on the storage engine. Use DIVIDE() for division by zero instead.")

    except Exception as e:
        issues.append(f"Error reading {filepath}: {e}")
        
    return issues

def main():
    target = Path(sys.argv[1] if len(sys.argv) > 1 else ".")
    print(f"\n📈 DAX Best Practices Auditor running on: {target}\n")
    
    files_to_check = []
    if target.is_file() and target.suffix in [".dax", ".tmdl"]:
        files_to_check.append(target)
    elif target.is_dir():
        files_to_check.extend(target.rglob("*.dax"))
        files_to_check.extend(target.rglob("*.tmdl"))
        
    total_issues = 0
    checked_files = 0
    for file in files_to_check:
        issues = audit_dax_expressions(file)
        checked_files += 1
        if issues:
            print(f"📄 {file.name}:")
            for issue in issues:
                print(f"   ❌ {issue}")
            total_issues += len(issues)
            print()
            
    if checked_files == 0:
        print("ℹ️ No .dax or .tmdl files found to check.")
        sys.exit(0)
    elif total_issues == 0:
        print("✅ No DAX anti-patterns found!")
        sys.exit(0)
    else:
        print(f"⚠️ Found {total_issues} potential DAX performance bottlenecks.")
        sys.exit(1)

if __name__ == "__main__":
    main()
