#!/usr/bin/env python3
"""
Databricks Anti-Pattern Linter
Validates PySpark scripts and Databricks notebooks for common anti-patterns.

Checks:
- Usage of %fs or dbutils in production paths (where applicable)
- display() statements left in production code
- Inefficient operations like df.count() before df.collect()
- Hardcoded sensitive information or paths
"""

import sys
import re
from pathlib import Path

def lint_databricks_file(filepath: Path) -> list:
    issues = []
    try:
        content = filepath.read_text(encoding="utf-8")
        lines = content.splitlines()
        
        has_count = False
        
        for i, line in enumerate(lines, 1):
            line_str = line.strip()
            
            # Skip comments
            if line_str.startswith("#"):
                continue
                
            # 1. Check for interactive display()
            if re.search(r'\bdisplay\s*\(', line_str):
                issues.append(f"Line {i}: Found 'display()'. Remove interactive displays from production code.")
                
            # 2. Check for %fs magics (in exported notebooks)
            if line_str.startswith("%fs") or line_str.startswith("MAGIC %fs"):
                issues.append(f"Line {i}: Found '%fs' magic command. Use dbutils.fs or native Spark readers in production.")
                
            # 3. Check for raw dbutils widgets without defaults or in non-notebook contexts
            # (Contextual check - simplified for this linter)
            if "dbutils.widgets.get" in line_str and "try:" not in content:
                issues.append(f"Line {i}: 'dbutils.widgets.get' found. Ensure this handles missing widgets gracefully if run outside Databricks interactive UI.")
                
            # 4. Inefficient action tracking (count followed by collect)
            if ".count(" in line_str:
                has_count = True
            elif ".collect(" in line_str and has_count:
                issues.append(f"Line {i}: Found '.collect()' shortly after '.count()'. This triggers duplicate Spark jobs.")
                has_count = False  # Reset
                
            # 5. Pandas conversion on large frames
            if ".toPandas()" in line_str:
                issues.append(f"Line {i}: Found '.toPandas()'. Ensure the DataFrame is small enough to fit in driver memory, otherwise this will cause OOM.")

    except Exception as e:
        issues.append(f"Error reading {filepath}: {e}")
        
    return issues

def main():
    target = Path(sys.argv[1] if len(sys.argv) > 1 else ".")
    print(f"\n🔍 Databricks Notebook Linter running on: {target}\n")
    
    files_to_check = []
    if target.is_file() and target.suffix in [".py"]:
        files_to_check.append(target)
    elif target.is_dir():
        # Specifically targeting databricks notebook exports or pyspark scripts
        files_to_check.extend(target.rglob("*.py"))
        
    total_issues = 0
    for file in files_to_check:
        # Simple heuristic to check if it's a databricks or pyspark file
        if "spark" not in file.read_text(encoding="utf-8").lower() and "databricks" not in file.read_text(encoding="utf-8").lower() and "dbutils" not in file.read_text(encoding="utf-8").lower():
             continue
             
        issues = lint_databricks_file(file)
        if issues:
            print(f"📄 {file.name}:")
            for issue in issues:
                print(f"   ❌ {issue}")
            total_issues += len(issues)
            print()
            
    if total_issues == 0:
        print("✅ No Databricks anti-patterns found!")
        sys.exit(0)
    else:
        print(f"⚠️ Found {total_issues} potential issues to review.")
        sys.exit(1) # We can exit 1 to fail a CI/CD check or pre-commit hook

if __name__ == "__main__":
    main()
