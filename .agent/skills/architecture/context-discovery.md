# Context Discovery for Data Systems

> Before suggesting any data pipeline or modeling architecture, gather context.

## Question Hierarchy (Ask User FIRST)

1. **Volume & Velocity (The 3 Vs)**
   - How much data per day/month? (MB, GB, TB, PB)
   - How fast does it arrive? (Streaming, hourly batches, daily dumps)
   - What is the structure? (Structured SQL, Semi-structured JSON/XML, Unstructured logs)

2. **Latency & SLAs**
   - When does the business NEED the data? (Real-time, near-real-time, D+1)
   - What happens if the data is 1 hour late?

3. **Consumers & Access**
   - Who will use this data? (BI Dashboards, ML Models, operational APIS)
   - What tools will they use? (Power BI, Python, direct SQL)
   - Concurrency: How many users querying simultaneously?

4. **Source Systems**
   - What are the upstream sources? (APIs, CDC from Postgres, Flat files in S3/ADLS)
   - Do they support incremental extraction? (Watermarks, UpdatedAt columns)

5. **Governance & Compliance**
   - Is there PII/LGPD/GDPR data?
   - Do we need row-level or column-level security?
   - Data retention policies?

## Project Classification Matrix

```
                     Ad-Hoc/BI        Lakehouse        Data Mesh
┌─────────────────────────────────────────────────────────────┐
│ Volume       │ < 100GB       │ 100GB - 50TB │ 50TB+        │
│ Ingestion    │ Batch Daily   │ Hourly/CDC   │ Streaming+CDC│
│ Consumer     │ 1 Dept        │ Company-wide │ Cross-Domain │
│ Pipeline     │ ETL (Simple)  │ Medallion    │ Federated    │
│ Target       │ RDBMS/Mart    │ Databricks   │ Multi-Lake   │
└─────────────────────────────────────────────────────────────┘
```
