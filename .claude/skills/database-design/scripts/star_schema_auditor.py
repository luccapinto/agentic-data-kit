#!/usr/bin/env python3
"""
Star Schema Auditor
Audits data models (SQL DDL or dbt models) for Star Schema best practices:
- Proper prefixes/suffixes (dim_, fact_, brg_, map_)
- Proper surrogate key naming (sk_, _key, id)
"""

import sys
import re
from pathlib import Path

def audit_star_schema(filepath: Path) -> list:
    issues = []
    filename = filepath.stem.lower() # without extension
    
    allowed_prefixes = ('dim_', 'fact_', 'fct_', 'brg_', 'map_', 'agg_', 'stg_')
    
    # 1. Check Naming Convention
    if not filename.startswith(allowed_prefixes) and not any(infix in filename for infix in ['_dim_', '_fact_', '_fct_']):
         # If the file doesn't seem to be a dimensional model, we might skip or warn.
         # For this strict auditor, we assume it's checking mart/gold layer models.
         if filepath.parent.name.lower() in ('mart', 'marts', 'gold'):
             issues.append(f"Model '{filename}' in mart/gold layer missing standard prefix (dim_, fact_, etc.).")
    
    is_dim = filename.startswith('dim_') or '_dim' in filename
    is_fact = filename.startswith('fact_') or filename.startswith('fct_') or '_fact' in filename
    
    if not (is_dim or is_fact):
        return issues # Not explicitly a dim or fact, skip deep checks
        
    try:
        content = filepath.read_text(encoding="utf-8").lower()
        
        # Look for column definitions or selections
        # Very simplified heuristic for SQL SELECT statements or DDL
        columns = re.findall(r"([a-z0-9_]+)\s+as\s+([a-z0-9_]+)", content) 
        columns.extend(re.findall(r"select\s+([a-z0-9_]+)", content))
        
        all_cols = []
        for match in columns:
            if isinstance(match, tuple):
                all_cols.append(match[1]) # The alias
            else:
                all_cols.append(match)
                
        # 2. Check for Surrogate Key in Dimensions
        if is_dim:
            has_sk = any(col.endswith('_key') or col.endswith('_sk') or col == 'id' for col in all_cols)
            # In DDL we might look for PRIMARY KEY. Here we just look at names.
            if not has_sk and all_cols: # Only warn if we actually parsed columns
                 issues.append(f"Dimension '{filename}' appears to lack a surrogate key suffix (_key, _sk, or id).")
                 
        # 3. Check for Foreign Keys in Facts
        if is_fact:
            fks = [col for col in all_cols if col.endswith('_key') or col.endswith('_id') or col.endswith('_sk')]
            measures = [col for col in all_cols if col.startswith('amt_') or col.startswith('qty_') or col.startswith('is_')]
            
            if not fks and all_cols:
                issues.append(f"Fact table '{filename}' appears to lack dimension foreign keys.")

    except Exception as e:
        issues.append(f"Error parsing {filepath}: {e}")
        
    return issues

def main():
    target = Path(sys.argv[1] if len(sys.argv) > 1 else ".")
    print(f"\n⭐ Star Schema Auditor running on: {target}\n")
    
    files_to_check = []
    if target.is_file():
        files_to_check.append(target)
    elif target.is_dir():
        files_to_check.extend(target.rglob("*.sql"))
        
    total_issues = 0
    for file in files_to_check:
        issues = audit_star_schema(file)
        if issues:
            print(f"📄 {file.name}:")
            for issue in issues:
                print(f"   ❌ {issue}")
            total_issues += len(issues)
            print()
            
    if total_issues == 0:
        print("✅ No Star Schema violations detected.")
        sys.exit(0)
    else:
        print(f"⚠️ Found {total_issues} potential Star Schema design issues.")
        sys.exit(1)

if __name__ == "__main__":
    main()
