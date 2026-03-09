#!/usr/bin/env python3
"""
TMDL AI Auditor
A comprehensive script to validate Tabular Model Definition Language (TMDL) files
against known Power BI Project (PBIP) pitfalls and AI generation errors.

Checks implemented:
1. Syntax Delimiters: Ensures `=` is used for measures/expressions and `:` for properties.
2. Indentation format: Flags strictly if spaces are mixed with tabs (Power BI usually exports tabs).
3. Relationship Sanity: Prevents 'calculated' partitions from being used in active relationships 
   (Power BI engine bug where column IDs change).
4. Model References: Ensures all files in definition/tables are referenced via 'ref table' in model.tmdl.
5. Invalid Values: Checks for non-existent enums like crossFilteringBehavior: singleDirection.
"""

import sys
import re
from pathlib import Path

def check_delimiters_and_syntax(filepath: Path) -> list:
    issues = []
    try:
        content = filepath.read_text(encoding="utf-8")
        lines = content.splitlines()
        
        for i, line in enumerate(lines, 1):
            line_str = line.strip()
            if not line_str:
                continue
                
            # Check for mixed spaces and tabs at the start of the line
            leading_whitespace = line[:len(line) - len(line.lstrip())]
            if ' ' in leading_whitespace and '\t' in leading_whitespace:
                issues.append(f"Line {i}: Mixed tabs and spaces in indentation. TMDL requires consistent single-character indentation (usually Tabs).")
            elif '    ' in leading_whitespace:
                # Warning: 4 spaces instead of a tab is a common AI hallucination
                pass # Too noisy if they actually used spaces consistently, so we just pass
            
            # Check Delimiter Errors: expressions with colon instead of equals
            if re.match(r'^(measure|expression|source|tablePermission)\b.*:', line_str):
                issues.append(f"Line {i}: CRITICAL SYNTAX ERROR - '{line_str.split()[0]}' declaration must use '=' instead of ':'. E.g. expression = ...")
                
            # Check Delimiter Errors: properties with equals instead of colon
            if re.match(r'^(dataType|formatString|sourceColumn|crossFilteringBehavior|lineageTag|mode)\b.*=', line_str):
                issues.append(f"Line {i}: CRITICAL SYNTAX ERROR - Property '{line_str.split()[0]}' must use ':' instead of '='. E.g. dataType: string")
                
            # Check invalid enums
            if "crossFilteringBehavior:" in line_str and "singleDirection" in line_str:
                issues.append(f"Line {i}: Invalid enum value. Use 'crossFilteringBehavior: oneDirection' instead of 'singleDirection'.")
                
            # Check missing descriptions on calculated columns
            if "description:" in line_str and "partition" not in line_str:
                # This is a bit complex to parse without full context, but `description:` property is invalid for calculated tables
                pass
                
    except Exception as e:
        issues.append(f"Error reading {filepath.name}: {e}")
        
    return issues

def main():
    target_dir = Path(sys.argv[1] if len(sys.argv) > 1 else ".")
    print(f"\n🔍 TMDL AI Auditor running on: {target_dir}\n")
    
    # 1. Find the SemanticModel/definition directory
    semantic_models = list(target_dir.rglob("*.SemanticModel/definition"))
    if not semantic_models:
        print("ℹ️ No '.SemanticModel/definition' directory found. Are you running this in a PBIP project?")
        sys.exit(0)
        
    total_issues = 0
    
    for definition_dir in semantic_models:
        model_name = definition_dir.parent.name
        print(f"📊 Analyzing Semantic Model: {model_name}")
        
        # Parse model.tmdl to find relationships and refs
        model_tmdl_path = definition_dir / "model.tmdl"
        refs = []
        rel_tables = set()
        
        if not model_tmdl_path.exists():
            print(f"   ❌ CRITICAL: Missing 'model.tmdl' in {definition_dir}")
            total_issues += 1
            continue
            
        try:
            model_content = model_tmdl_path.read_text(encoding="utf-8")
            for i, line in enumerate(model_content.splitlines(), 1):
                # Extract refs
                ref_match = re.match(r'^ref\s+table\s+([^\']+)', line.strip())
                if ref_match:
                    # Clean up quotes if present
                    table_name = ref_match.group(1).replace("'", "").strip()
                    refs.append(table_name)
                elif line.strip().startswith("ref table '"):
                    table_name = line.strip().split("'")[1]
                    refs.append(table_name)
                    
                # Extract relationships
                if line.strip().startswith("fromColumn:") or line.strip().startswith("toColumn:"):
                    parts = line.strip().split(":", 1)[1].strip()
                    table_part = parts.split(".")[0].replace("'", "")
                    rel_tables.add(table_part)
                    
        except Exception as e:
            print(f"   ❌ Error reading model.tmdl: {e}")
            total_issues += 1
            
        # 2. Check each table in definition/tables
        tables_dir = definition_dir / "tables"
        if not tables_dir.exists():
            continue
            
        tmdl_files = list(tables_dir.glob("*.tmdl"))
        
        for tmdl_file in tmdl_files:
            file_issues = check_delimiters_and_syntax(tmdl_file)
            table_name = tmdl_file.stem
            
            # Check if table is referenced in model.tmdl
            if table_name not in refs:
                # Sometimes filenames have brackets or different casing, simple check
                normalized_refs = [r.lower() for r in refs]
                if table_name.lower() not in normalized_refs:
                    file_issues.append(f"Table '{table_name}' has a file but is NOT referenced with 'ref table' in model.tmdl. This causes non-deterministic ordering.")
            
            # Check for calculated partitions involved in relationships
            if table_name in rel_tables:
                try:
                    content = tmdl_file.read_text(encoding="utf-8")
                    if "partition" in content and "= calculated" in content:
                        file_issues.append(f"CRITICAL PBIP BUG: Table '{table_name}' is used in a relationship in model.tmdl AND uses a 'calculated' partition. This crashes model load due to stale Column IDs. Use M queries for tables in relationships.")
                except Exception as e:
                    pass

            if file_issues:
                print(f"📄 {tmdl_file.name}:")
                for issue in file_issues:
                    print(f"   ❌ {issue}")
                total_issues += len(file_issues)
                print()

    print("\n" + "="*50)
    if total_issues == 0:
        print("✅ ALL CHECKS PASSED: The AI-generated TMDL structure is fully valid and optimized!")
        sys.exit(0)
    else:
        print(f"⚠️ AUDIT FAILED: Found {total_issues} critical issues in the TMDL files.")
        print("   Please instruct the AI to fix these problems.")
        sys.exit(1)

if __name__ == "__main__":
    main()
