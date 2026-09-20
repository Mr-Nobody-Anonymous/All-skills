---
name: cdc
description: "Change Data Capture: database transaction log mining (Debezium), WAL replication, schema evolution, and real-time streaming"
category: data-engineering
version: 1.0.0
disable-model-invocation: false
risk: low
source: "https://github.com/Mr-Nobody-Anonymous/All-skills"
source_repository: "Mr-Nobody-Anonymous/All-skills"
source_path: "awesome_skills/data-engineering/cdc/SKILL.md"
license: "MIT"
imported_at: "2026-09-20"
---

# Change Data Capture (CDC)

## Scope
Change Data Capture captures row-level insert, update, and delete mutations directly from database transaction logs without query polling, streaming changes in real time.

## Mechanics & Architecture
- **Log-Based Mining**: Reading PostgreSQL Write-Ahead Logs (WAL) via `pgoutput` plugin, or MySQL binary logs (`binlog`).
- **Debezium CDC Architecture**: Debezium connector captures row changes $\to$ Kafka topic per table $\to$ consumers parse envelope (`before`, `after`, `op`, `ts_ms`).
- **Zero Impact on Production**: Avoids high-overhead `SELECT * WHERE updated_at` database polling.

## Tools & Standards
- **Software**: Debezium, Kafka Connect, AWS DMS.
