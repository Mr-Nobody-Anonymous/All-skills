---
name: dbt
description: "Data build tool: SQL compilation, Jinja templating, incremental models, snapshots (SCD Type 2), and automated testing"
category: data-engineering
version: 1.0.0
disable-model-invocation: false
risk: low
source: "https://github.com/Mr-Nobody-Anonymous/All-skills"
source_repository: "Mr-Nobody-Anonymous/All-skills"
source_path: "awesome_skills/data-engineering/dbt/SKILL.md"
license: "MIT"
imported_at: "2026-09-20"
---

# dbt (Data Build Tool) Modeling

## Scope
dbt enables analytics engineering by bringing software engineering best practices (modularity, version control, testing, CI/CD) to SQL transformations inside data warehouses.

## Core Features & Design
- **Lineage Graph (`ref` function)**: `SELECT * FROM {{ ref('stg_orders') }}` compiles dependencies into a directed acyclic execution graph.
- **Incremental Materialization**:
  ```sql
  {{ config(materialized='incremental', unique_key='event_id') }}
  SELECT * FROM {{ ref('stg_events') }}
  {% if is_incremental() %}
    WHERE event_timestamp > (SELECT MAX(event_timestamp) FROM {{ this }})
  {% endif %}
  ```
- **Snapshots (Slowly Changing Dimensions Type 2)**: Tracking historical state changes over time using valid-from and valid-to timestamps.

## Tools & Standards
- **Software**: dbt Core, dbt Cloud.
