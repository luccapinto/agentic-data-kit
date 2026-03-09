# Batch vs Streaming

Data pipelines generally process data in one of two paradigms: Batch processing or Streaming processing. Choosing the correct one is driven largely by the SLA required by the business.

## 🕒 Batch Processing (Default)
Processing data at scheduled intervals (e.g., daily at 2:00 AM, hourly).

- **Use Cases:** EOD Financial reporting, daily marketing aggregations, model training.
- **Tools:** Apache Airflow, dbt, Apache Spark, Snowflake.
- **Trade-offs:** 
  - **Pros:** Cheaper, easier to build, easier to backfill and debug, high throughput.
  - **Cons:** High latency, "thundering herd" resource usage at scheduled times.

## ⚡ Streaming Processing
Processing data continuously as it is generated.

- **Use Cases:** Fraud detection, real-time dashboards, IoT monitoring, personalization.
- **Tools:** Apache Kafka, Flink, Spark Structured Streaming, Kinesis.
- **Trade-offs:**
  - **Pros:** Lowest latency, constant resource usage.
  - **Cons:** Significantly higher cost, complex state management, difficult to backfill, handles late-arriving data poorly without advanced windowing.

## 🔄 Micro-Batching (The Middle Ground)
Processing data in very small, frequent batches (every 1, 5, or 15 minutes).
A practical compromise for most "near-real-time" requirements that don't literally need sub-second latency.

## Architecture Patterns

### Lambda Architecture
Maintains two separate paths: a cold batch layer (historically accurate) and a hot speed layer (real-time but potentially inexact). The serving layer merges both.
*Pros: Robust. Cons: Maintaining two separate codebases for the same logic.*

### Kappa Architecture
A single stream processing layer handles both real-time data and reprocessing of historical data using tools like Kafka with infinite retention or Flink.
*Pros: Single codebase. Cons: Harder to manage large backfills efficiently compared to pure batch.*
