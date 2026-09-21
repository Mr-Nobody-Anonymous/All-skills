# ADR-0042: Adopt PostgreSQL as the Primary Data Store for Billing

## Status
Accepted

## Context and Problem Statement
Our billing and invoice processing subsystem has outgrown DynamoDB. Invoices require multi-table ACID transactions across Accounts, Invoices, LineItems, and PaymentLedgers. DynamoDB's multi-table transactions have incurred high consumed capacity unit costs, complex manual indexing, and lack ad-hoc analytical query capabilities for financial reconciliation.

## Decision Drivers
* **ACID Guarantees**: Strict multi-record transactional integrity is required for financial compliance (SOC1/SOC2).
* **Relational Joins**: Complex billing calculations require joins between organizations, subscriptions, and usage records.
* **Cost Predictability**: High query variance in billing reconciliation must not produce unpredictable serverless read spikes.
* **Ecosystem Maturity**: Native ORM (Prisma/Drizzle) migration and tooling support.

## Considered Options
* **Option 1: PostgreSQL 16 on AWS Aurora Serverless v2**
* **Option 2: MySQL 8.0 on AWS RDS**
* **Option 3: Keep DynamoDB with AWS AppSync & Lambda-managed transactions**

## Decision Outcome
Chosen option: **PostgreSQL 16 on AWS Aurora Serverless v2**, because it offers full ACID transactional guarantees, native JSONB support for variable invoice line-item metadata, and predictable cost ceilings through Aurora ACU limits.

### Positive Consequences
* Complete financial transactional integrity without distributed lock boilerplate.
* Ad-hoc SQL reporting eliminates custom ETL pipelines for monthly finance reviews.
* Reduced infrastructure development effort by using Prisma migrations.

### Negative Consequences / Trade-offs
* Requires connection pooling management (PgBouncer) between serverless Lambda handlers and Aurora.
* Team engineers must re-familiarize with relational schema indexing strategies after 2 years of NoSQL.

## Pros and Cons of the Options

### Option 1: PostgreSQL 16 (Chosen)
* Good: ACID compliant, robust JSONB support, mature window functions.
* Good: Aurora Serverless v2 provides automated auto-scaling for burst billing runs.
* Bad: Requires VPC configuration and PgBouncer connection proxy.

### Option 2: MySQL 8.0
* Good: Team has historic familiarity.
* Bad: Weaker JSON indexing capabilities compared to PostgreSQL JSONB; less mature vector/extension ecosystem.

### Option 3: DynamoDB
* Good: Zero connection pooling headaches; fully managed.
* Bad: Cross-partition transactions incur 2x write unit cost; ad-hoc financial audits require full table scans.
