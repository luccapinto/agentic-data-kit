# Dimensional Modeling

Dimensional modeling (often associated with Ralph Kimball) is the predominant design technique for data delivery in a Data Warehouse (or the Gold layer of a Medallion architecture). 
It focuses on two things: performance for analytical queries and ease of understanding for business users.

## 🌟 Star Schema
The core of dimensional modeling is the Star Schema, where a central **Fact table** is surrounded by multiple **Dimension tables**.

### Fact Tables
- **Content:** Represents a business event or measurement (e.g., Sales, Clicks, Transactions).
- **Structure:** Contains quantitative metrics (Measures) and Foreign Keys pointing to Dimensions.
- **Granularity:** The most important decision. Define exactly what one row represents (e.g., "One item on a single invoice").
- **Types:**
  - **Transaction Fact:** One row per event.
  - **Periodic Snapshot Fact:** One row per time period (e.g., end-of-day balances).
  - **Accumulating Snapshot Fact:** Tracks a process with multiple well-defined milestones (e.g., Order Placed -> Shipped -> Delivered).

### Dimension Tables
- **Content:** The "Who, What, Where, When, Why, How" of the data (e.g., Customers, Products, Dates). Contains descriptive attributes.
- **Structure:** Wide tables with many string columns. Denormalized (no snowflakes unless strictly necessary).
- **Surrogate Keys:** Always use integer surrogate keys as the Primary Key instead of natural/business keys to handle changes over time.
- **Slowly Changing Dimensions (SCD):**
  - **Type 1:** Overwrite old values (no history).
  - **Type 2:** Add a new row with trackable valid date ranges (maintains history).

## Rules
- Avoid **Snowflaking** (normalizing dimensions) as it degrades query performance via multiple JOINs.
- Use **Conformed Dimensions** (e.g., a single shared `dim_date` or `dim_customer`) across multiple facts to allow for easy cross-functional reporting.
