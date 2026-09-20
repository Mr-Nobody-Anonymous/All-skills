---
name: data-warehouse
description: "Dimensional modeling (Kimball), star/snowflake schemas, columnar storage, partition pruning, and clustering keys"
category: data-engineering
version: 1.0.0
disable-model-invocation: false
risk: low
source: "https://github.com/Mr-Nobody-Anonymous/All-skills"
source_repository: "Mr-Nobody-Anonymous/All-skills"
source_path: "awesome_skills/data-engineering/data-warehouse/SKILL.md"
license: "MIT"
imported_at: "2026-09-20"
---

# Data Warehouse Engineering

## Scope
Cloud data warehousing organizes historical enterprise data for rapid analytical reporting, business intelligence, and complex aggregation queries.

## Dimensional Modeling (Ralph Kimball)
- **Star Schema Architecture**:
  - Fact Tables: Additive, semi-additive, or non-additive numerical measurements of business processes (`fct_sales`).
  - Dimension Tables: Contextual descriptive attributes (`dim_customer`, `dim_product`, `dim_date`).
- **Columnar Storage & Compression**: Column-oriented storage (Parquet, ORC, Snowflake micro-partitions) with dictionary encoding and run-length encoding.
- **Optimization**: Clustering keys, partition pruning, materialized views, and caching layers.

## Tools & Standards
- **Platforms**: Snowflake, Google BigQuery, Amazon Redshift, ClickHouse.
