#!/usr/bin/env python3
"""
Medallion Architecture Drift Checker
Scans project files to ensure layered architecture rules are respected:
- Gold models should not read directly from Bronze (they must read from Silver)
- Silver models should read from Bronze or other Silver
- Bronze models should read from source/raw, not other Bronze
"""

import sys
import re
from pathlib import Path

def check_medallion_rules(filepath: Path) -> list:
    issues = []
    
    # Simple heuristic to determine the layer of the current file
    filename = filepath.name.lower()
    path_str = str(filepath).lower()
    
    layer = "unknown"
    if "bronze" in filename or "bronze" in path_str:
        layer = "bronze"
    elif "silver" in filename or "silver" in path_str:
        layer = "silver"
    elif "gold" in filename or "gold" in path_str or "mart" in filename or "mart" in path_str:
        layer = "gold"
        
    if layer == "unknown":
        return issues
        
    try:
        content = filepath.read_text(encoding="utf-8").lower()
        
        # Look for ref() or source() calls commonly used in dbt or sql files
        refs = re.findall(r"ref\s*\(\s*['\"]([^'\"]+)['\"]\s*\)", content)
        # also look for direct table references (heuristic)
        direct_refs = re.findall(r"from\s+([a-zA-Z0-9_\.]+)", content)
        
        all_referenced_models = refs + direct_refs
        
        for ref_model in all_referenced_models:
            ref_model_lower = ref_model.lower()
            
            # Rule 1: Gold reading from Bronze
            if layer == "gold" and "bronze" in ref_model_lower:
                issues.append(f"Gold layer model '{filename}' references Bronze model '{ref_model}'. Gold must consume from Silver.")
                
            # Rule 2: Silver reading from Gold (Reverse dependency)
            if layer == "silver" and ("gold" in ref_model_lower or "mart" in ref_model_lower):
                issues.append(f"Silver layer model '{filename}' references Gold model '{ref_model}'. Silver must consume from Bronze or Silver.")
                
            # Rule 3: Bronze reading from Silver/Gold (Reverse dependency)
            if layer == "bronze" and ("silver" in ref_model_lower or "gold" in ref_model_lower or "mart" in ref_model_lower):
                 issues.append(f"Bronze layer model '{filename}' references higher layer model '{ref_model}'. Bronze must only consume from raw sources.")
                 
    except Exception as e:
        issues.append(f"Error analyzing {filepath}: {e}")
        
    return issues

def main():
    target = Path(sys.argv[1] if len(sys.argv) > 1 else ".")
    print(f"\n🏅 Medallion Architecture Checker running on: {target}\n")
    
    files_to_check = []
    if target.is_file():
        files_to_check.append(target)
    elif target.is_dir():
        # Check SQL and Python files typically used for transformations
        files_to_check.extend(target.rglob("*.sql"))
        files_to_check.extend(target.rglob("*.py"))
        
    total_issues = 0
    for file in files_to_check:
        issues = check_medallion_rules(file)
        if issues:
            print(f"📄 {file.name}:")
            for issue in issues:
                print(f"   ❌ {issue}")
            total_issues += len(issues)
            print()
            
    if total_issues == 0:
        print("✅ No Medallion architecture drift detected.")
        sys.exit(0)
    else:
        print(f"⚠️ Found {total_issues} architecture violations.")
        sys.exit(1)

if __name__ == "__main__":
    main()
