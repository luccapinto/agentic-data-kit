# Medallion Architecture

The Medallion Architecture logically organizes data in a Lakehouse into three overarching layers, progressively increasing structure and quality.

## 🥉 Bronze (Raw)
- **Concept:** Unaltered, raw data loaded precisely as it arrived from the source. 
- **Format:** Parquet, JSON, Delta.
- **Rules:**
  - APPEND ONLY. No updates or deletes.
  - Maintain historical truth. 
  - Add loading metadata (e.g., `_ingest_time`, `_source_file_name`).

## 🥈 Silver (Cleansed & Conformed)
- **Concept:** Filtered, cleaned, and augmented data.
- **Format:** Delta Lake / Iceberg.
- **Rules:**
  - Apply data types and schema validation.
  - Deduplicate records.
  - Standardize formats (e.g., date formats, casing).
  - Serve as the "Enterprise Source of Truth" for ad-hoc querying or data science tasks.

## 🥇 Gold (Curated & Modeled)
- **Concept:** Business-level aggregates, dimensional models, and feature tables.
- **Format:** Delta Lake / RDBMS.
- **Rules:**
  - Modeled often as Star Schema (Facts and Dimensions).
  - Heavy business logic and pre-aggregations applied here.
  - Strictly governed and permissions-controlled for end-user BI (Power BI, Tableau) consumption.
