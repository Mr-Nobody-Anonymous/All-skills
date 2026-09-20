---
name: lakehouse
description: "Data lakehouse architecture: Delta Lake, Apache Iceberg, Apache Hudi, ACID transactions, time travel, and schema evolution"
category: data-engineering
version: 1.0.0
disable-model-invocation: false
risk: low
source: "https://github.com/Mr-Nobody-Anonymous/All-skills"
source_repository: "Mr-Nobody-Anonymous/All-skills"
source_path: "awesome_skills/data-engineering/lakehouse/SKILL.md"
license: "MIT"
imported_at: "2026-09-20"
---

# Data Lakehouse & Table Formats

## Scope
Lakehouse architectures combine the flexibility, cost-efficiency, and scale of cloud object storage (S3, GCS) with the ACID transaction guarantees and performance of data warehouses.

## Open Table Formats
- **Apache Iceberg / Delta Lake / Apache Hudi**:
  - Metadata Tree: Manifest lists and manifest files decoupling file storage from table metadata.
  - ACID Transactions: Multi-version concurrency control (MVCC) and optimistic concurrency control (OCC).
  - Time Travel: Querying table state at specific historical snapshots or timestamps.
  - In-Place Partition Evolution: Updating partitioning schemes without rewriting existing data.
  - Compaction: Merging small files into optimal size ($128-512\text{ MB}$) Parquet files.

## Tools & Standards
- **Software**: Apache Iceberg, Databricks Delta Lake, Trino, Dremio, DuckDB.
