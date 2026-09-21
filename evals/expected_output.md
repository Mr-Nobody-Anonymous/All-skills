# ADR-0001: Select PostgreSQL as Primary Relational Database

## Status
Accepted

## Context and Problem Statement
Our multi-tenant SaaS application requires a reliable primary relational database to store tenant user accounts, organization workspaces, and billing metadata.
Requirements include:
- Strict multi-table ACID transaction support.
- Native semi-structured JSON querying for tenant-specific configuration dictionaries.
- Streaming read replication for reporting workloads.
- First-class migration and type safety via Prisma ORM.

## Decision Drivers
* **ACID Transactions**: Required for zero-data-loss tenant operations.
* **JSON Query Capabilities**: Native JSONB indexing to avoid external document stores.
* **ORM Compatibility**: Robust integration with Prisma ORM.
* **Operational Maturity**: High availability on managed cloud providers (AWS RDS / Aurora).

## Considered Options
* **Option 1: PostgreSQL 16**
* **Option 2: MySQL 8.0**

## Decision Outcome
Chosen option: **PostgreSQL 16**, because its JSONB data type offers superior indexing (GIN/BTREE) and JSON path operators compared to MySQL's JSON implementation, while providing full ACID guarantees and best-in-class Prisma integration.

### Positive Consequences
* Single database tier handles structured schemas and dynamic tenant configuration.
* Strong typing and ecosystem support with Prisma migrations.

### Negative Consequences / Trade-offs
* Requires PgBouncer connection pooling for serverless execution environments.
