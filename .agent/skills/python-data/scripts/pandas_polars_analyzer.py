#!/usr/bin/env python3
"""
Pandas/Polars Performance Analyzer
Scans Python data code for inefficient Pandas operations and suggests Polars/vectorized alternatives.

Checks:
- iterrows(), itertuples()
- apply() syntax on large axes
"""

import sys
import re
from pathlib import Path

def analyze_python_data_file(filepath: Path) -> list:
    issues = []
    try:
        content = filepath.read_text(encoding="utf-8")
        lines = content.splitlines()
        
        for i, line in enumerate(lines, 1):
            line_str = line.strip()
            if line_str.startswith("#"):
                continue
                
            # 1. Inefficient iterations
            if ".iterrows(" in line_str:
                issues.append(f"Line {i}: Inefficient '.iterrows()' found. Use vectorized operations, .apply(), or migrate to Polars.")
            elif ".itertuples(" in line_str:
                issues.append(f"Line {i}: '.itertuples()' found. While faster than iterrows, vectorization is highly preferred.")
                
            # 2. apply with axis=1 (very slow)
            if re.search(r'\.apply\(.*axis\s*=\s*1\)', line_str):
                issues.append(f"Line {i}: '.apply(..., axis=1)' is extremely slow. Try to use vectorized series operations.")
                
            # 3. Chained indexing assignment
            if re.search(r'\]\[.*\]\s*=', line_str.replace(" ", "")):
                 issues.append(f"Line {i}: Potential SettingWithCopyWarning (chained indexing assignment). Use .loc[row_indexer, col_indexer] = value instead.")
                 
            # 4. inplace=True (often an anti-pattern in modern Pandas)
            if "inplace=True" in line_str.replace(" ", ""):
                issues.append(f"Line {i}: 'inplace=True' found. It's often better to reassign (df = df.method()) to enable method chaining, and Pandas 3.0 may deprecate it.")

    except Exception as e:
        issues.append(f"Error reading {filepath}: {e}")
        
    return issues

def main():
    target = Path(sys.argv[1] if len(sys.argv) > 1 else ".")
    print(f"\n🐼 Pandas/Polars Code Analyzer running on: {target}\n")
    
    files_to_check = []
    if target.is_file() and target.suffix == ".py":
        files_to_check.append(target)
    elif target.is_dir():
        files_to_check.extend(target.rglob("*.py"))
        
    total_issues = 0
    for file in files_to_check:
        # Check if it imports pandas or polars
        content = file.read_text(encoding="utf-8")
        if "pandas" not in content and "polars" not in content:
            continue
            
        issues = analyze_python_data_file(file)
        if issues:
            print(f"📄 {file.name}:")
            for issue in issues:
                print(f"   ❌ {issue}")
            total_issues += len(issues)
            print()
            
    if total_issues == 0:
        print("✅ No Pandas anti-patterns found!")
        sys.exit(0)
    else:
        print(f"⚠️ Found {total_issues} Python data anti-patterns to rewrite.")
        sys.exit(1)

if __name__ == "__main__":
    main()
