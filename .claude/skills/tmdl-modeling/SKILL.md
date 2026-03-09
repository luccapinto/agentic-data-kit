---
name: tmdl-modeling
description: Standards and syntax for writing and structuring Tabular Model Definition Language (TMDL) files in Power BI projects. Covers tables, relationships, DAX measures, and model architecture.
---

# TMDL Modeling

This skill governs the creation and modification of Semantic Models using Tabular Model Definition Language (TMDL). TMDL is an indentation-based, human-readable format for defining the Tabular Object Model (TOM), designed for version control.

> **Official Docs:** [TMDL Overview](https://learn.microsoft.com/en-us/analysis-services/tmdl/tmdl-overview) | [PBIP SemanticModel folder](https://learn.microsoft.com/en-us/power-bi/developer/projects/projects-dataset)

## 🧠 Core Philosophy

TMDL is the **source of truth** for the Power BI Semantic Model. Logic, relationships, security, and metadata reside here. Business rules must **not** exist in the visual layer.

---

## 🏗️ TMDL Folder Structure (PBIP)

In a `.pbip` project, the semantic model lives in the `{ProjectName}.SemanticModel\` folder.

```
{ProjectName}.SemanticModel/
├── definition.pbism              # Core settings + format declaration (TMDL or TMSL)
├── .pbi/
│   ├── localSettings.json        # LOCAL ONLY — add to .gitignore
│   └── cache.abf                 # LOCAL ONLY — add to .gitignore
└── definition/                   # TMDL folder (replaces model.bim)
    ├── database.tmdl             # compatibilityLevel
    ├── model.tmdl                # Root: culture, ref ordering, relationships, annotations
    ├── expressions.tmdl          # Shared M expressions / parameters (optional)
    └── tables/
    │   └── {TableName}.tmdl     # Columns, measures, partitions, hierarchies per table
    ├── roles/
    │   └── {RoleName}.tmdl      # Row-Level Security definitions
    └── cultures/
        └── {locale}.tmdl        # Linguistic schema / translations
```

> ⚠️ **`definition\` folder only exists in TMDL format.** If the project uses TMSL, the model is stored as a single `model.bim` JSON file instead. Check `definition.pbism` to confirm the format.

---

## ⚡ CRITICAL: The Two Delimiters

TMDL has **only two** ways to assign a value. Confusing them is the **#1 cause of parser errors**.

| Delimiter | Symbol | Used For |
|-----------|--------|----------|
| **Colon** | `:` | All simple (non-expression) **property values** |
| **Equals** | `=` | **Expressions** and **default properties** (DAX, M, RLS) |

### Use `=` (equals) for:
- Measure definitions (DAX): `measure Sales = SUM(...)`
- Partition sources (M query): `source = let ... in ...`
- Partition expressions (calculated/DAX): `expression = DATATABLE(...)`
- Table permissions (RLS DAX filter): `tablePermission DimGeo = [Region] = "BR"`
- Annotations: `annotation PBI_ProTooling = ["DevMode"]`

### Use `:` (colon) for:
- All other properties: `dataType:`, `formatString:`, `mode:`, `sourceColumn:`, `lineageTag:`, `crossFilteringBehavior:`, `sortByColumn:`, `culture:`, `fromColumn:`, `toColumn:`, `isActive:`, `displayFolder:`, `isHidden`, etc.

> ❌ **`expression:` or `source:` with a colon will crash the parser with `Property has no value specified!`**

---

## ✍️ TMDL Syntax & Indentation

TMDL uses **strict single-tab indentation** (default). Each object has 3 levels:
1. **Level 1** — Object declaration: `table`, `column`, `measure`, `partition`
2. **Level 2** — Object properties at one tab deeper
3. **Level 3** — Multi-line expression body (DAX/M) at two tabs deeper

> ⚠️ **Mixing tabs and spaces corrupts the file silently.** Always match the indentation character of the existing file.

Database, model, tables, roles, cultures, and perspectives do **not** need to be indented because they are implicitly nested under root Model/Database.

---

### 1. Table & Column Definitions

```tmdl
/// Dim table with customer data
table DimCustomer
	lineageTag: a1b2c3d4-e5f6-7890-1234-567890abcdef

	/// Surrogate key — hidden from report
	column CustomerKey
		dataType: int64
		isHidden
		formatString: 0
		sourceColumn: CustomerKey

	/// Full name of the customer
	column CustomerName
		dataType: string
		sourceColumn: FullName
		sortByColumn: CustomerName

	partition DimCustomer-Partition = m
		mode: import
		source =
			let
				Source = Sql.Database("Server", "Database"),
				dbo_DimCustomer = Source{[Schema="dbo",Item="DimCustomer"]}[Data]
			in
				dbo_DimCustomer
```

**Rules:**
- `isHidden` is a boolean shortcut — `true` is implied when declared alone.
- `sourceColumn` maps to the column name in the partition query result.
- Use `summarizeBy: none` on non-numeric columns to prevent implicit aggregation.
- Always declare `dataType` and `formatString` explicitly.

---

### 2. Calculated Tables (DAX Partitions)

Use `partition ... = calculated` with `expression =` (equals, never colon):

```tmdl
table dCalendario
	lineageTag: a1b2c3d4-0002-0002-0002-000000000001

	column Data
		dataType: dateTime
		formatString: dd/MM/yyyy
		sourceColumn: Data
		isKey
		summarizeBy: none
		lineageTag: b1b2c3d4-0002-0002-0002-000000000001

	partition dCalendario = calculated
		mode: import
		expression =
			VAR _Cal = CALENDAR(DATE(2025,1,1), DATE(2025,12,31))
			RETURN
				ADDCOLUMNS(_Cal, "Data", [Date], "Ano", YEAR([Date]))
```

> ⚠️ **Columns in `calculated` partitions do NOT support inline `description:` properties.** Use `///` triple-slash comments instead.

---

### 3. Measure Definitions (DAX)

Properties like `formatString:` and `displayFolder:` go **after** the DAX expression body, at the **property level** (Level 2), not inside the expression (Level 3):

```tmdl
/// Total revenue after discounts
measure 'Total Revenue' =
		VAR _Base = SUM(FactSales[SalesAmount])
		VAR _Discount = SUM(FactSales[DiscountAmount])
		RETURN
			_Base - _Discount
	formatString: R$ #,0.00
	displayFolder: Financeiro
	lineageTag: c1b2c3d4-0001-0001-0001-000000000001
```

**Rules:**
- Use `VAR` aggressively for readability and performance.
- Always set `displayFolder` to categorize measures into logical groups.
- Always set `formatString` explicitly.
- Multi-line DAX is mandatory for complex logic.

---

### 4. Descriptions (`///` Triple-Slash)

TMDL uses `///` triple-slash as first-class description syntax (not `description:` property):

```tmdl
/// This is a table-level description
table Sales

	/// Revenue from all channels after discounts
	measure 'Total Revenue' =
			SUM(Sales[Amount])
		formatString: $ #,##0

	/// Unique surrogate key - do not expose in reports
	column CustomerKey
		dataType: int64
		isHidden
```

**Rules:**
- `///` must appear **immediately above** the object — no blank lines between comment and object.
- Multiple consecutive `///` lines are supported for long descriptions.
- Works on: `table`, `column`, `measure`, `relationship`, `role`, `hierarchy`, etc.
- **For `calculated` partition columns:** `description:` property is NOT supported — use `///` instead.

---

### 5. Relationships (defined in `model.tmdl`)

```tmdl
model Model
	culture: pt-BR
	defaultPowerBIDataSourceVersion: powerBI_V3

ref table dCalendario
ref table fVoos

relationship fVoos_DataVoo_dCalendario
	fromColumn: fVoos.DataVoo
	toColumn: dCalendario.Data
	crossFilteringBehavior: oneDirection

relationship fVoos_DestinoID_dAeroportos
	isActive: false
	fromColumn: fVoos.DestinoID
	toColumn: dAeroportos.AeroportoID
	crossFilteringBehavior: oneDirection
```

**Rules:**
- Always explicitly define `crossFilteringBehavior`. Valid values: `oneDirection`, `bothDirections`, `automatic`.
- ❌ **`singleDirection` is INVALID.** Use `oneDirection`.
- Use `isActive: false` for inactive relationships (activated via `USERELATIONSHIP()` in DAX).
- `fromColumn` / `toColumn` use **dot notation**: `TableName.ColumnName`.
- Name relationships descriptively: `{FactTable}_{FKColumn}_{DimTable}`.

---

### 6. The `ref` Keyword (Ordering)

`ref` entries in `model.tmdl` define the **serialization order** of objects. Without them, new tables are appended at the end (non-deterministic). This is critical for clean git diffs:

```tmdl
model Model
	culture: pt-BR

ref table Calendar
ref table Sales
ref table Product
ref culture pt-BR
ref role 'Regional Managers'
```

> Objects referenced in TMDL but without a matching file are **ignored**. Objects with a file but no `ref` are **appended to the end**.

---

### 7. Row-Level Security (RLS)

RLS is defined in `roles\{RoleName}.tmdl`:

```tmdl
role 'Regional Managers'
	modelPermission: read

	tablePermission DimGeography =
		[Region] = USERPRINCIPALNAME()
```

---

### 8. Object Naming Rules

Object names **must** be enclosed in single quotes (`'`) if they contain a dot (`.`), equals (`=`), colon (`:`), single quote (`'`), or whitespace:

```tmdl
measure 'Sales Amount' = SUM(...)       // Spaces → requires quotes
measure SimpleMetric = COUNT(...)       // No special chars → no quotes needed
column 'Customer''s Name'              // Escaped single quote → double them
```

---

### 9. Backtick Enclosure (Verbatim Expressions)

To force verbatim parsing (preserve trailing whitespace, blank lines):

```tmdl
measure Measure1 = ```
	var myVar = Today()
	return result
```
```

Use backticks only when strictly needed (e.g., expressions with intentional trailing blank lines).

---

## 🛠️ Execution Protocol

When asked to create or update via TMDL:

1. **Locate the File:** Find the `.tmdl` file in `{ProjectName}.SemanticModel\definition\tables\` or `...\roles\`.
2. **Match Indentation:** Use the **exact same** indentation character (tab). Mixing tabs and spaces corrupts the model.
3. **Use Correct Delimiters:** `=` for expressions (DAX/M/RLS), `:` for all other properties.
4. **Preserve Lineage Tags:** Keep existing `lineageTag` values to avoid breaking visual bindings.
5. **Update `model.tmdl`:** If adding a new table, add a `ref table {Name}` entry. If adding relationships, define them inline in `model.tmdl`.
6. **Validate DAX/M:** Ensure expressions are syntactically correct before saving.

---

## ❌ Critical Pitfalls

| Calculated partition (`DATATABLE`) table used in relationships | `invalid column ID N` — **model fails to load** |
| `expression:` instead of `expression =` | `Property has no value specified!` |
| `source:` instead of `source =` | `Property has no value specified!` |
| `crossFilteringBehavior: singleDirection` | `InvalidValueFormat` |
| `description:` on calculated table columns | `UnknownKeyword` |
| Mixed tabs and spaces | Silent corruption or parser error |
| Removing `lineageTag` from existing objects | Breaks visual bindings in reports |
| Adding a table file without `ref table` in `model.tmdl` | Table appended at end (non-deterministic order) |
| Double quotes for object names | Parser error (use single quotes `'`) |

> 🔴 **RULE: Calculated partitions (`partition T = calculated`) MUST NOT be used for tables involved in relationships.**
> The TOM engine assigns column IDs to calculated table columns **only after model processing**. At load time, those IDs are undefined/stale, causing `PFE_TM_RELATIONSHIP_END_COLUMN_INVALID`.
> **Fix:** Use `partition T = m` with Power Query `Table.FromRows(...)` inline data instead. M partition columns have stable metadata at load time.


---

## 📋 Cheat Sheet

```
USE : (colon)                    USE = (equals)
─────────────────                ──────────────────────────────
dataType: int64                  measure Sales = SUM(...)
formatString: #,0                expression = DATATABLE(...)
sourceColumn: Name               source = let ... in ...
mode: import                     tablePermission T = [X] = "Y"
crossFilteringBehavior: oneDir.  annotation Key = "Value"
lineageTag: guid
isHidden                   ← boolean shortcut (true implied)
sortByColumn: OtherCol
displayFolder: Finance
isActive: false
```
