---
name: db-inspector
description: Inspect database schemas and queries read-only by default and explain performance or safety risks.
category: media_and_utilities
aliases: [database, db, schema, query, inspect, mysql, postgres]
triggers:
  - Check database schema
  - Inspect this database
  - Run a query
  - Database structure
  - Explain this query
keywords: [database, sql, schema, query, inspect, mysql, postgres, mongodb]
required_tools: [database-client]
risk: medium
version: 1.0.0
source: openclawskills.net
enabled: true
metadata:
  openclaw:
    requires:
      env: []
      bins: []
    primaryEnv: null
---

# Database Query Inspector

## Purpose

Inspect database schemas, run queries, and explain execution plans with read-only
defaults and clear risk indicators. The skill helps developers understand database
structure and optimize queries while preventing accidental modifications.

## When to Use

- Exploring database schema and structure
- Understanding table relationships
- Optimizing slow queries
- Verifying data in development
- Troubleshooting database issues

## When NOT to Use

- For production data modification (use explicit migration tools)
- Without proper database credentials
- For bulk operations without review

## Capabilities

- Schema inspection (tables, columns, indexes, constraints)
- Query execution with EXPLAIN
- Query performance analysis
- Data sampling (LIMIT results)
- Connection testing
- Index recommendations
- Safety risk assessment

## Inputs

- `action` (required) â€” one of: schema, query, explain, sample
- `connection` (required) â€” database connection string or alias
- `query` (required for query/explain) â€” SQL or query language
- `limit` (optional) â€” result limit (default: 100)

## Workflow

1. **Connect** â€” Establish database connection
2. **Validate** â€” Check connection and permissions
3. **Execute** â€” Run inspection or query
4. **Explain** â€” Provide execution plan if requested
5. **Assess** â€” Flag any safety concerns
6. **Present** â€” Format results clearly

## Safety

- ALWAYS use read-only mode by default
- ALWAYS warn before any write operation
- Require explicit confirmation for DELETE, UPDATE, DROP
- Never expose connection credentials
- Limit result sets to prevent memory issues
- Log all queries for audit

## Examples

**User:** "Show me the users table schema"
**Response:**
```
Table: users
Columns:
- id (UUID, PK, NOT NULL)
- email (VARCHAR(255), UNIQUE, NOT NULL)
- created_at (TIMESTAMP, NOT NULL)
- updated_at (TIMESTAMP)
Indexes:
- idx_email (B-tree, UNIQUE)
- idx_created_at (B-tree)

Related tables: posts(user_id), sessions(user_id)
```

## Source

Auto-generated from openclawskills.net description.

## Pairs Well With

- `docker-manager` (database container management)
- `api-mock-generator` (mock database responses)
- `security-scanner` (scan for sensitive data)
