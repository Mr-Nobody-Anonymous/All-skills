---
name: spark
description: "Apache Spark: Resilient Distributed Datasets (RDD), DataFrames, Catalyst optimizer, Tungsten execution engine, and PySpark"
category: data-engineering
version: 1.0.0
disable-model-invocation: false
risk: low
source: "https://github.com/Mr-Nobody-Anonymous/All-skills"
source_repository: "Mr-Nobody-Anonymous/All-skills"
source_path: "awesome_skills/data-engineering/spark/SKILL.md"
license: "MIT"
imported_at: "2026-09-20"
---

# Apache Spark Distributed Computing

## Scope
Apache Spark provides unified distributed data processing, in-memory computing, and petabyte-scale transformations across large compute clusters.

## Optimization Engines & Architecture
- **Catalyst Optimizer**: Analysis $\to$ Logical Plan $\to$ Optimized Logical Plan (predicate pushdown, constant folding) $\to$ Physical Plan.
- **Tungsten Engine**: Off-heap memory management avoiding JVM garbage collection overhead; whole-stage code generation compiling query plans to Java bytecode.
- **Partition Tuning & Shuffling**:
  - Shuffle operations (`groupBy`, `join`) exchange data across cluster nodes over network.
  - Broadcast Hash Join: Broadcasing small tables ($<10\text{ MB}$) to all executors avoiding wide shuffle exchanges.
  - Sizing: Ideal partition size $100-200\text{ MB}$.

## Tools & Standards
- **APIs**: PySpark, Spark SQL, Spark Structured Streaming, GraphX.
