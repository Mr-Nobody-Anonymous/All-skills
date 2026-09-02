---
name: api-mock-generator
description: Derive API mocks and contract tests from schemas or observed interfaces without inventing behavior.
category: media_and_utilities
aliases: [api, mock, test, contract, openapi, swagger]
triggers:
  - Generate API mocks
  - Create mock API
  - API testing
  - Mock endpoints
keywords: [api, mock, test, openapi, swagger, rest, contract]
required_tools: [test-framework]
risk: low
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

# API Mock & Contract Generator

## Purpose

Generate API mocks and contract tests from OpenAPI schemas or observed interfaces.
The skill ensures mocks accurately reflect the API contract without inventing
behavior beyond the specification.

## When to Use

- Setting up local development environments
- Writing contract tests
- Mocking external APIs for testing
- Generating API documentation examples

## When NOT to Use

- For production API implementations
- When a real API is available and accessible
- For security testing (use specialized tools)

## Capabilities

- OpenAPI/Swagger schema parsing
- JSON Schema to mock conversion
- Request/response example generation
- Contract test skeleton generation
- Mock server configuration
- Multi-format support (REST, GraphQL)
- Header and authentication simulation

## Inputs

- `source` (required) â€” OpenAPI file, JSON Schema, or HAR file
- `format` (optional) â€” mock-server, contract-tests, examples
- `framework` (optional) â€” jest, pytest, etc.
- `base_url` (optional) â€” for mock server

## Workflow

1. **Parse** â€” Load and analyze schema
2. **Generate** â€” Create mocks from definitions
3. **Validate** â€” Ensure mocks match schema
4. **Package** â€” Generate config files and tests
5. **Document** â€” Provide usage instructions

## Tools

- OpenAPI parsers
- Mock server tools (Prism, Prism, Mockoon)
- Test framework integration

## Examples

**User:** "Generate mocks from this OpenAPI spec"
**Response:**
```
Parsing openapi.yaml...
Found 15 endpoints, 45 schemas

Generated:
- mock-server.js (Prism mock server)
- contracts.test.js (Jest contract tests)
- examples.json (request/response examples)

Run: npx prism mock openapi.yaml
```

## Safety

- Never mock sensitive data
- Clearly label generated code as mocks
- Don't use mocks in place of real integration tests
- Validate mocks against schema

## Source

Auto-generated from openclawskills.net description.

## Pairs Well With

- `testing` (integration with test suite)
- `frontend-design` (frontend API development)
- `db-inspector` (backend data structures)
