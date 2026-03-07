---
name: tmdl-modeling
description: Standards and syntax for writing and structuring Tabular Model Definition Language (TMDL) files in Power BI projects. Covers tables, relationships, DAX measures, and model architecture.
---

# TMDL Modeling

This skill governs the creation and modification of Semantic Models using Tabular Model Definition Language (TMDL). TMDL is a YAML-like syntax designed for human readability and version control.

## 🧠 Core Philosophy

TMDL is the source of truth for the Power BI Semantic Model. It is where logic, relationships, security, and metadata reside. If a business rule can be codified in TMDL, it should not exist in the visual layer.

## 🏗️ Structure of a TMDL Project

In a `.pbip` project, the semantic model is stored in the `\Dataset\` folder. The root file is `model.tmdl`, which references other files, typically organized by object type (e.g., tables, roles).

-   `\Dataset\model.tmdl` -> The root definition, containing cultures and references.
-   `\Dataset\tables\{TableName}.tmdl` -> Individual file for each table, containing its columns, measures, partitions, and hierarchies.
-   `\Dataset\roles\{RoleName}.tmdl` -> Definitions for Row-Level Security (RLS).
-   `\Dataset\expressions.tmdl` -> Shared expressions/Power Query parameters.

## ✍️ TMDL Syntax & Best Practices

TMDL relies heavily on significant whitespace (indentation) to define scope, similar to Python.

### 1. Table Definitions

Every table file should clearly define its partitions (usually M queries), columns, and measures.

```tmdl
table DimCustomer
    lineageTag: a1b2c3d4-e5f6-7890-1234-567890abcdef

    column CustomerKey
        dataType: int64
        isHidden
        formatString: 0
        sourceColumn: CustomerKey

    column CustomerName
        dataType: string
        sourceColumn: FullName
        description: The full name of the customer.

    partition DimCustomer-Partition = m
        mode: import
        expression:
            let
                Source = Sql.Database("Server", "Database"),
                dbo_DimCustomer = Source{[Schema="dbo",Item="DimCustomer"]}[Data]
            in
                dbo_DimCustomer
```

**Rules:**
-   Always hide surrogate keys (`isHidden`).
-   Provide `description` properties for business-facing columns.
-   Explicitly declare `dataType` and `formatString`.

### 2. Measure Definitions (DAX)

Measures are defined within the `table` scope, usually in a dedicated `_Measures` table or attached to the relevant fact table.

```tmdl
table FactSales

    measure 'Total Revenue' =
        VAR _Base = SUM(FactSales[SalesAmount])
        VAR _Discount = SUM(FactSales[DiscountAmount])
        RETURN
            _Base - _Discount
        formatString: \$#,0.00;(\$#,0.00);\$#,0.00
        displayFolder: "Revenue Metrics"
        description: Total revenue after discounts have been applied.
```

**Rules:**
-   **Multiline DAX is Mandatory:** Complex DAX functions must span multiple lines and be properly indented. Single-line DAX for complex logic is strictly forbidden.
-   **Variables (`VAR`):** Use variables aggressively for readability and performance.
-   **Display Folders:** Always categorize measures using the `displayFolder` property.
-   **Formatting:** Explicitly set the `formatString`.

### 3. Relationships

Relationships are defined in the `model.tmdl` file, not in the individual table files.

```tmdl
relationship 'FactSales-DimDate'
    fromColumn: FactSales.OrderDateKey
    toColumn: DimDate.DateKey
    crossFilteringBehavior: singleDirection
```

**Rules:**
-   Always explicitly define `crossFilteringBehavior`.
-   Avoid `both` (bidirectional) cross-filtering unless absolutely required for a specific, documented many-to-many scenario. Default to `singleDirection`.

### 4. Row-Level Security (RLS)

RLS is defined in the `\roles\` directory.

```tmdl
role 'Regional Managers'
    modelPermission: read

    tablePermission DimGeography =
        [Region] = USERPRINCIPALNAME()
```

## 🛠️ Execution Protocol

When asked to update the Semantic Model via TMDL:

1.  **Locate the File:** Find the correct `.tmdl` file in the `\Dataset\tables\` or `\Dataset\roles\` directory.
2.  **Respect Indentation:** Ensure your edits use the exact same indentation level as the surrounding code (typically tabs or 4 spaces; match the existing file).
3.  **Validate DAX:** Ensure any DAX written within the TMDL string is syntactically correct.
4.  **Save:** Overwrite the file.

## ❌ Pitfalls to Avoid

-   **Indentation Errors:** TMDL breaks if indentation is inconsistent. This is the #1 cause of corruption.
-   **Missing Lineage Tags:** While Power BI can often regenerate them, try to preserve existing `lineageTag` properties when modifying existing columns/measures to prevent breaking visual bindings.
-   **Syntax Mismatches:** Remember that TMDL uses `= m` for Power Query M expression partitions, but assigns DAX directly with `=` for measures.
