#!/usr/bin/env python3
"""
Idempotency Checker
Scans SQL and Python pipelines to enforce "no-repeat-side-effect" rules:
- Warns against bare INSERTs without OVERWRITE or MERGE
- Checks for TRUNCATE before INSERT patterns
"""

import sys
import re
from pathlib import Path

def check_idempotency(filepath: Path) -> list:
    issues = []
    
    try:
        content = filepath.read_text(encoding="utf-8")
        content_upper = content.upper()
        
        # 1. Check for raw INSERTS without OVERWRITE or MERGE (SQL/Spark SQL)
        # We look for "INSERT INTO" and warn if there is no TRUNCATE or MERGE logic nearby
        if "INSERT INTO" in content_upper and "MERGE INTO" not in content_upper and "TRUNCATE" not in content_upper:
            # In Databricks, INSERT OVERWRITE is preferred for idempotency
            if "INSERT OVERWRITE" not in content_upper:
                issues.append(f"Found 'INSERT INTO' without 'OVERWRITE', 'MERGE', or 'TRUNCATE'. This operation may not be idempotent and could duplicate data on retry.")
                
        # 2. Check for PySpark append mode without partition overwrite
        if ".MODE('APPEND')" in content_upper.replace('"', "'") or ".MODE(\"APPEND\")" in content_upper.replace('"', "'"):
             if "REPLACEWHERE" not in content_upper:
                 issues.append(f"Found Spark DataFrame write in 'append' mode without 'replaceWhere' or partition overwrite. This may duplicate data on pipeline rerun.")

    except Exception as e:
        issues.append(f"Error parsing {filepath}: {e}")
        
    return issues

def main():
    target = Path(sys.argv[1] if len(sys.argv) > 1 else ".")
    print(f"\n🔁 Idempotency Checker running on: {target}\n")
    
    files_to_check = []
    if target.is_file() and target.suffix in ['.sql', '.py']:
        files_to_check.append(target)
    elif target.is_dir():
        files_to_check.extend(target.rglob("*.sql"))
        files_to_check.extend(target.rglob("*.py"))
        
    total_issues = 0
    checked_files = 0
    for file in files_to_check:
        issues = check_idempotency(file)
        checked_files += 1
        if issues:
            print(f"📄 {file.name}:")
            for issue in issues:
                print(f"   ❌ {issue}")
            total_issues += len(issues)
            print()
            
    if checked_files == 0:
        print("ℹ️ No SQL or Python files found to check.")
        sys.exit(0)
    elif total_issues == 0:
        print("✅ No idempotency anti-patterns detected!")
        sys.exit(0)
    else:
        print(f"⚠️ Found {total_issues} operations that might violate idempotency rules.")
        sys.exit(1)

if __name__ == "__main__":
    main()
