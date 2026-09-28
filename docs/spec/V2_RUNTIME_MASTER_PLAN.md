# 🚀 All-skills v2: Autonomous Agent Operating System Master Plan & Specification

> **Document Version**: 2.0.0  
> **Status**: Approved Architectural Master Plan  
> **Target Repository**: [Mr-Nobody-Anonymous/All-skills](https://github.com/Mr-Nobody-Anonymous/All-skills)  
> **Date**: September 20, 2026  

---

## Executive Summary

The foundational insight behind **All-skills** is that the value of an agent ecosystem is not determined simply by hoarding thousands of static `SKILL.md` markdown files. The true objective is building an **Agent Operating System and Capability Runtime** around them:
- **Intelligent multi-signal routing** and large-scale semantic retrieval.
- **Strict capability-based security**, quarantine barriers, and runtime sandboxing.
- **Empirical behavioral evaluation**, reproducible benchmarks, and evidence records.
- **Typed input/output interfaces** and declarative workflow composition.
- **Formal software supply-chain provenance** and cryptographic verification.
- **Autonomy classification levels (L0–L4)** with deterministic human confirmation gates.

This specification formalizes the **v2 Architecture Blueprint**, synthesizing the platform into **6 Core Operating Primitives**, defining the **6 Foundational Questions** every skill must answer, establishing the **20 Concrete Architectural Enhancements**, and mapping the **Top 10 Reference Repositories** directly into actionable subsystems.

---

## 1. The 6 Core Operating Primitives

The v2 platform architecture organizes all capabilities across six tightly integrated functional pillars:

```
                                ALL-SKILLS v2
                                      │
        ┌─────────────────────────────┼─────────────────────────────┐
        ▼                             ▼                             ▼
   1. REGISTRY                   2. ROUTER                     3. RUNTIME
   ├── Provenance Tracking       ├── Multi-Signal Routing      ├── Execution Isolation
   ├── Semantic Versioning       ├── Large-Scale Retrieval     ├── Least-Privilege Sandbox
   ├── Dependency Graphs         ├── Token Overlap & Aliases   ├── L0–L4 Autonomy Gates
   └── Package Distribution      └── Explainable Telemetry     └── Secret & Network Guardrails
        │                             │                             │
        └─────────────────────────────┼─────────────────────────────┘
                                      │
                                      ▼
                                 4. COMPOSER
                                 ├── Typed I/O Contracts
                                 ├── Sequential & Parallel Stages
                                 └── Resumable State Machine
                                      │
                                      ▼
                              5. WORKFLOW ENGINE
                                 ├── Human Approval Gates
                                 ├── Error Fingerprinting & Loops
                                 └── Deterministic Rollbacks
                                      │
                                      ▼
                               6. EVALUATION
                                 ├── Standardized Benchmarks
                                 ├── With-vs-Without Utility A/B
                                 ├── Adversarial Red-Teaming
                                 └── Telemetry Feedback Loops
```

---

## 2. The 6 Foundational Questions Every Skill Must Answer

In All-skills v2, a skill is not merely a collection of natural-language advice. Every canonical skill must provide machine-verifiable answers to six foundational questions:

| # | Question | Structural Manifest Mapping | Runtime Enforcement |
| :-: | :--- | :--- | :--- |
| **1** | **What does it do?** | `name`, `description`, `capabilities` | Declarative metadata & taxonomy classification |
| **2** | **When should it be selected?** | `triggers`, `aliases`, `keywords`, `intent_embeddings` | 9-signal routing engine & large-scale reranker |
| **3** | **What does it require?** | `requires.tools`, `requires.env`, `dependencies` | Pre-execution dependency resolution & capability checks |
| **4** | **What does it produce?** | `produces.artifacts`, `outputs.schema` | Semantic dataflow validation & artifact indexing |
| **5** | **What is it allowed to do?** | `autonomy_level` (L0–L4), `permissions`, `network` | Runtime sandbox isolation & human confirmation gates |
| **6** | **How do we know it works?** | `evidence.tests`, `evidence.benchmark_score`, `evidence.matrix` | Empirical regression evaluation & model test suites |

---

## 3. The 20 Concrete Architectural Enhancements

### 1. Skill Evaluation & Evidence Records
Replace subjective self-reported quality scores with cryptographically tied, reproducible **Evidence Records**:

```yaml
# Example: evidence record embedded in skill manifest or registry
evidence:
  evaluation_version: "2.0.0"
  functional_tests: 42
  integration_tests: 14
  benchmark_score: 0.94
  last_verified: "2026-09-20"
  model_compatibility:
    claude_code: "verified"
    codex_cli: "verified"
    cursor: "verified"
    antigravity: "verified"
  human_reviewed: true
  production_telemetry:
    total_runs: 1420
    success_rate: 0.965
    avg_latency_sec: 8.4
    avg_tokens: 3850
```

Every certified skill presents an empirical radar covering:
$$\text{Trust} = f(\text{Correctness}, \text{Reliability}, \text{Security}, \text{Freshness}, \text{Compatibility}, \text{Provenance})$$

---

### 2. Standardized Skill Benchmark Suite
A first-class benchmarking subsystem residing under `benchmarks/`:

```
benchmarks/
├── coding/          # Refactoring, algorithmic synthesis, test generation
├── debugging/       # Reproduction isolation, trace analysis, root cause
├── research/        # Paper synthesis, technical evaluation, comparison
├── security/        # SAST analysis, secret detection, exploit mitigation
├── browser/         # DOM navigation, headless interaction, scraping
├── databases/       # Migration safety, index optimization, query tuning
├── agents/          # Subagent delegation, context compaction, state sync
└── documents/       # PDF parsing, markdown synthesis, spec authoring
```

CLI commands:
```bash
allskills benchmark skill react-state-management
allskills benchmark category frontend
allskills benchmark compare skill-a skill-b
```

Outputs standardized metrics:
```
Skill Evaluation Matrix: react-state-management
────────────────────────────────────────────────────
Task Success Rate:         96.2%
Instruction Adherence:     98.5%
Hallucination Rate:         2.1%
Tool Efficiency:           91.4%
Regression Rate:            0.0%
Security Violations:           0
Average Token Spend:       4,210 tokens
Average Execution Time:     9.8s
```

---

### 3. Deep Semantic Skill Versioning
Explicit semantic versioning isolating identity, schema, and runtime contracts:
```yaml
name: api-designer
version: 2.3.1
schema_version: 1.2
runtime_compatibility:
  min_platform_version: "2.0.0"
  supported_engines: ["python>=3.10", "node>=18"]
dependencies:
  - id: database-design
    version_range: ">=1.4.0 <3.0.0"
```

Distinguishes:
1. **Skill Identity**: Canonical slug (`api-designer`).
2. **Skill Version**: Semantic release (`2.3.1`).
3. **Skill Schema Version**: Frontmatter contract format (`1.2`).
4. **Runtime Compatibility**: Model and platform minimum requirements.
5. **Dependency Versions**: Semver ranges for composable prerequisite skills.

---

### 4. Typed Skill Interfaces & Dataflow Contracts
Transform instructional chaining into strongly typed semantic dataflow:

```yaml
interface:
  inputs:
    - name: source_code
      type: "path[]"
      required: true
      description: "Paths to application source files."
    - name: target_framework
      type: "string"
      default: "react"
  outputs:
    - name: review_report
      type: "file:markdown"
      path: "artifacts/review.md"
    - name: severity_matrix
      type: "json"
      schema: "schemas/severity_matrix.json"
  requires:
    tools:
      - filesystem:read
      - git:diff
  produces:
    artifacts:
      - "artifacts/review.md"
```

Enables pipeline verification: Skill $B$ can only be scheduled after Skill $A$ if all required typed inputs of $B$ are produced by $A$.

---

### 5. Declarative Skill Composition Engine
Support both deterministic sequential pipelines and parallel multi-agent stages:

```yaml
workflow:
  name: fullstack-saas-feature
  description: "End-to-end autonomous feature engineering pipeline"
  timeout_seconds: 1800
  stages:
    - id: stage-requirements
      skill: requirements-analysis
      on_failure: abort

    - id: stage-design
      skill: architecture-design
      depends_on: [stage-requirements]

    - id: stage-parallel-reviews
      parallel:
        - skill: security-review
          inputs: { scope: "design" }
        - skill: database-design
          inputs: { scope: "entities" }
        - skill: api-designer
          inputs: { scope: "endpoints" }
      depends_on: [stage-design]

    - id: stage-implementation
      skill: tdd
      depends_on: [stage-parallel-reviews]
      checkpoint: true
      retry:
        max_attempts: 3
        backoff: exponential

    - id: stage-verification
      skill: verification-before-completion
      depends_on: [stage-implementation]
      human_approval_gate: required
```

---

### 6. Human Approval & Autonomy Levels (L0 to L4)
A formalized five-tier autonomy classification:

```
L0 — INFORMATIONAL  (Zero tool calls, advisory analysis, question answering)
L1 — READ-ONLY       (Read repository, search codebase, inspect logs, run AST linter)
L2 — LOCAL MUTATION  (Write local source code, add unit tests, run test suites locally)
L3 — EXTERNAL EFFECTS(Package install, push Git branch, execute external HTTP mutation)
L4 — PRODUCTION IMPACT(Cloud deployment, drop database table, modify production secrets)
```

Policy specification (`policies/high-risk.yaml`):
```yaml
risk:
  autonomy_level: L3
  requires_confirmation:
    - external_api_write
    - git_push_origin
    - package_installation
  strictly_blocked:
    - database_drop
    - recursive_deletion_outside_workspace
    - secret_key_exposure
```

---

### 7. Runtime Sandboxing & Execution Isolation
Static text analysis is insufficient to guarantee runtime safety. Implement containerized or OS-level bounded execution:

```
Skill Execution Environment
├── Filesystem: Bounded strictly to repo root (mount /scratch as isolated tempfs)
├── Network: Deny all by default, domain allowlist only
├── Subprocesses: Prohibit arbitrary shell execution; wrap CLI tools via strict arguments
├── Environment: Mask all secret patterns (AWS, GITHUB_TOKEN, OPENAI_KEY, SSH keys)
├── CPU Quotas: Maximum 4 threads, 5-minute timeout per stage
└── Memory Quotas: Maximum 2 GB RAM per worker process
```

---

### 8. Granular Network Policy per Skill
Declare explicit network access rules directly in skill definitions:

```yaml
network_policy:
  mode: allowlist
  allowed_hosts:
    - "api.github.com"
    - "registry.npmjs.org"
    - "pypi.org"
  blocked_ports:
    - 22
    - 25
    - 3389
```

Skills without an explicit network policy inherit the global default: `mode: deny`.

---

### 9. Provenance & Software Supply-Chain Bill of Materials (SBOM)
Every skill includes an end-to-end cryptographic audit trail:

```
UPSTREAM SOURCE REPO
        │
        ▼ (pinned commit SHA)
CRYPTOGRAPHIC DIGEST (SHA-256)
        │
        ▼
STATIC SCAN & AST VERIFICATION
        │
        ▼
EVIDENCE & BENCHMARK SCORE
        │
        ▼
PUBLISHED LOCKED ARTIFACT (`awesome_skills.lock`)
```

Marketplace representation:
```
┌────────────────────────────────────────────────────────┐
│ api-designer                                   v2.3.1  │
├────────────────────────────────────────────────────────┤
│ Source:      github.com/anthropics/skills             │
│ Commit:      a81f3d4... (verified)                    │
│ License:     MIT (Commercial-friendly)                │
│ Maintainer:  Anthropic AI                             │
│ SBOM Digest: sha256:7f4c91b8a...                      │
│ Security:    0 vulnerabilities (Passed OWASP/AST)      │
│ Benchmark:   94.8% Task Success Rate                  │
└────────────────────────────────────────────────────────┘
```

---

### 10. Formal 8-Stage Skill Lifecycle State Machine
A strictly gated finite state machine:

```
DRAFT ──► DISCOVERED ──► QUARANTINED ──► AUDITED ──► VERIFIED ──► PUBLISHED
                                                         │              │
                                                         ▼              ▼
                                                     DEPRECATED ──► ARCHIVED
```

**Gate Requirements**:
- `QUARANTINED ──► AUDITED`: Static AST scan passing, zero forbidden shell tokens, license whitelisted.
- `AUDITED ──► VERIFIED`: Schema frontmatter valid, dependency tree resolvable, unit tests $\ge 90\%$.
- `VERIFIED ──► PUBLISHED`: Live model evaluation passing, evidence record registered, SHA-256 pinned in lockfile.

---

### 11. Semantic Duplicate & Redundancy Detection
Eliminate catalogue bloat where nearly identical skills proliferate (`react-review`, `react-code-review`, `review-react-code`):

- **Embedding Cosine Similarity**: Flag skill pairs with text cosine similarity $> 0.90$.
- **Trigger/Capability Overlap**: Compute Jaccard index of trigger regexes and tool permissions.
- **Automated Differential Report**:
  ```
  Candidate Duplicates:
  [react-review] <──> [react-code-review] (Similarity: 94.2%)
  Recommendation: Merge into canonical `react-code-review` with alias `react-review`.
  ```

---

### 12. Skill Specialization & Taxonomy Trees
Enable semantic routing between generic and specialized capabilities:

```
code-review (generic router target)
 ├── security-review (specialized: OWASP, auth, cryptography)
 ├── performance-review (specialized: memory leaks, query optimization)
 ├── accessibility-review (specialized: WCAG 2.2, ARIA, screen readers)
 ├── database-review (specialized: schema indexes, locking, migrations)
 └── api-review (specialized: REST contracts, OpenAPI, rate limits)
```

The router dynamically selects the specialized skill if user intent indicates specific constraints, falling back to the generic parent if intent is broad.

---

### 13. Empirical Multi-Model Compatibility Matrix
Continuous behavioral testing across 11 major AI agent environments:

| Skill Discipline | Claude Code | Cursor | Codex CLI | GitHub Copilot | Antigravity | Windsurf | Cline | Roo | Goose |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: | :---: |
| **AST Transformation** | ✅ Verified | ✅ Verified | ✅ Verified | ✅ Verified | ✅ Verified | ✅ Verified | ✅ Verified | ✅ Verified | ✅ Verified |
| **Multi-Step Workflows**| ✅ Verified | ✅ Verified | ✅ Verified | ⚠️ Partial | ✅ Verified | ⚠️ Partial | ✅ Verified | ✅ Verified | ⚠️ Partial |
| **Dynamic Sandboxing**  | ✅ Verified | ⚠️ Partial | ⚠️ Partial | ❌ N/A | ✅ Verified | ❌ N/A | ⚠️ Partial | ⚠️ Partial | ❌ N/A |
| **MCP Tool Servers**    | ✅ Verified | ✅ Verified | ⚠️ Partial | ❌ N/A | ✅ Verified | ⚠️ Partial | ✅ Verified | ✅ Verified | ✅ Verified |

---

### 14. Privacy-Conscious Local Runtime Telemetry
Zero remote reporting; 100% local SQLite/JSON execution logs:
- `skill_id`: The invoked skill.
- `trigger_query`: Masked prompt intent.
- `execution_latency_ms`: Time from activation to completion.
- `tokens_consumed`: Prompt + completion token expenditure.
- `tool_call_count`: Number of tool invocations.
- `verification_verdict`: `PASS` or `FAIL`.
- `retry_count`: Number of automated recovery attempts.

Enables query analysis:
> *"Skill `docker-debug` is selected 85% of the time for container failures, but fails verification 40% of the time $\rightarrow$ triggers automated inspection alert."*

---

### 15. Execution-to-Routing Telemetry Feedback Loops
Close the loop between execution success and future routing:

```
USER PROMPT
    │
    ▼
ROUTER (Priors + Historical Win-Rate)
    │
    ▼
SKILL SELECTION
    │
    ▼
EXECUTION & VERIFICATION
    │
    ▼
LOCAL TELEMETRY (Success / Failure / Retries)
    │
    ▼
BAYESIAN ROUTER UPDATE (Increase/Decrease Score Weight)
```

Skills that consistently succeed for specific intent clusters receive elevated routing confidence, while skills that trigger frequent rollbacks are dynamically penalized.

---

### 16. Eight-Division Behavioral Test Taxonomy
Upgrade the test suite from purely structural validation to eight distinct tiers:

```
1. Schema Tests        (Frontmatter, types, required keys, YAML syntax)
2. Routing Tests       (Top-k accuracy, alias resolution, ambiguous disambiguation)
3. Security Tests      (Quarantine isolation, path traversal, forbidden commands)
4. Execution Tests     (Tool invocation, file write boundaries, state tracking)
5. Behavior Tests      (Instruction adherence, output format compliance)
6. Regression Tests    (Golden prompt datasets, deterministic outputs)
7. Compatibility Tests (Multi-agent harness symlink and directory resolution)
8. Adversarial Tests   (Prompt injection defense, tool poisoning resilience)
```

---

### 17. Adversarial Skill Testing (`skill-redteam`)
A dedicated automated security probe subsystem testing every imported skill against:
- **Prompt Injection**: Direct and indirect prompt hijacking vectors.
- **Instruction Contradictions**: Subversive instructions attempting to override global safety directives.
- **Path Traversal**: Exploiting tool inputs with `../../` to escape the workspace sandbox.
- **Tool Poisoning**: Overriding system tool definitions or simulating invalid confirmations.
- **Secret Exfiltration**: Prompts attempting to echo or write `.env` credentials to disk or network.
- **Confused-Deputy Vulnerabilities**: Tricking privileged skills into executing unvetted code.

---

### 18. Rich Marketplace Metadata Cards
Interactive CLI and web marketplace cards displaying verified trust signals:

```
┌────────────────────────────────────────────────────────────────────────┐
│  ⭐ TRUST CERTIFIED  │  🧪 96% TEST PASS  │  📊 0.94 BENCHMARK SCORE   │
├────────────────────────────────────────────────────────────────────────┤
│  Skill:       postgresql-query-optimizer                               │
│  Version:     1.4.0 (Semver Verified)                                  │
│  Autonomy:    L1 — Read-Only                                           │
│  Category:    database / performance                                   │
│  License:     Apache-2.0                                               │
│  Context:     ~2,100 tokens (Minimal Bloat)                            │
│  Tools:       postgresql:explain, filesystem:read                      │
│  Upstream:    github.com/microsoft/skills (commit b41e0a2)             │
│  Security:    0 High, 0 Medium, AST Clean                              │
└────────────────────────────────────────────────────────────────────────┘
```

---

### 19. Standardized Skill Package Format
Formalize every production skill as an exportable, self-contained, signed package:

```
skill-name/
├── SKILL.md             # Standard instructions and human-readable playbook
├── skill.yaml           # Machine-readable typed interface, permissions, and metadata
├── tests/               # Behavior, regression, and unit test suites
│   ├── test_behavior.py
│   └── fixtures/
├── benchmarks/          # Empirical tasks and gold output assertions
│   └── benchmark.json
├── scripts/             # Deterministic helper scripts and AST tools
├── references/          # Supporting specs, schemas, and documentation
└── LICENSE              # Open-source license text
```

CLI Packaging Suite:
```bash
allskills pack <skill-name>      # Compiles to tar.gz with cryptographic signature
allskills publish <skill-name>   # Submits package to local/remote registry
allskills install <skill>@2.1.0  # Resolves, validates, and installs into active harness
```

---

### 20. The Programmatic Skill SDK (`allskills-sdk`)
Empower developers to build and compose skills programmatically in Python and TypeScript:

```python
from allskills import skill, Registry, Context

@skill(
    id="database-review",
    version="1.2.0",
    autonomy="L1",
    capabilities=["database.read", "filesystem.read"],
    inputs={"connection_string": str, "schema_path": str},
    outputs={"report_path": str}
)
def review_database(ctx: Context) -> dict:
    """Analyze database schema and active indexes for query performance."""
    schema = ctx.fs.read(ctx.inputs["schema_path"])
    findings = ctx.analyze_indexes(schema)
    ctx.fs.write("artifacts/db_report.md", findings.to_markdown())
    return {"report_path": "artifacts/db_report.md"}
```

Client Runtime APIs:
```python
registry = Registry.load()
selected = registry.route("optimize slow Postgres queries")
execution = registry.execute(selected, context=current_context)
verification = registry.verify(execution)
```

---

## 4. Top 10 Reference Repositories Deep Dive

To realize this v2 architecture without reinventing existing wheels, All-skills establishes direct architectural synthesis with the top 10 external agent skill repositories:

| Priority | Repository | Architectural Domain | Core Pattern to Synthesize | Anti-Pattern to Avoid | Target Module in All-skills |
| :---: | :--- | :--- | :--- | :--- | :--- |
| **🔴 1** | **`NVIDIA/SkillEvaluator`** | Evaluation & Quality Gates | 3-tier validation (Tier 1 Validation $\rightarrow$ Tier 2 Deduplication $\rightarrow$ Tier 3 Live Agent Eval); PII scanning; synthetic test generation. | Excessive heavy cloud dependencies; focus on lightweight local runner. | `benchmarks/`, `scripts/run_evals.py` |
| **🔴 2** | **`zhengyanzhao1997/SkillRouter`** | Large-Scale Retrieval | Dual-stage retrieval (Bi-encoder candidate retrieval + Cross-encoder reranking) scaling to 80k+ skills. | Giant neural models requiring multi-GB GPU VRAM; use lightweight embeddings / BM25. | `scripts/skills/router.py` |
| **🔴 3** | **`oneal2000/SR-Agents` (SRA-Bench)** | Retrieval & Task Benchmarks | 5,400 evaluation instances; distractor skills; joint evaluation of retrieval accuracy + task success. | Rigid monolithic dataset; implement extensible JSONL benchmark format. | `benchmarks/tasks/` |
| **🔴 4** | **`SkillLens-AI/skilllens`** | Adversarial Security | Clean separation of Utility Probes vs Security Probes; agent trajectory inspection; LLM judge auditing. | Non-deterministic prompt judging; enforce deterministic AST assertions. | `scripts/scan_skills_security.py` |
| **🟠 5** | **`Aakash2512git/skillregistry`** | Semantic Indexing | Automated directory scanning; metadata extraction; Recall@K & MRR retrieval metrics. | Hard-coded local path dependencies; maintain universal relative path resolution. | `registry/`, `scripts/build_indexes.py` |
| **🟠 6** | **`nikships/skills-registry`** | Distribution & Packaging | Cross-agent installation CLI; TUI interface; lockfile synchronization. | Non-standard packaging manifests; adhere to canonical `SKILL.md` format. | `scripts/allskills.py`, `allskills.bat` |
| **🟠 7** | **`anthropics/skills`** | Format Specification | Progressive disclosure model; document extraction workflows; single-responsibility playbooks. | Agent lock-in; maintain multi-platform compatibility across 11 agent targets. | `skills/`, `.agents/skills/` |
| **🟠 8** | **`darkrishabh/agent-skills-eval`** | A/B Utility Evaluation | Empirical Delta Testing: Measuring task completion of *Agent with Skill* vs *Agent without Skill*. | Subjective grading; rely on automated unit/lint pass rates. | `scripts/benchmark_skills.py` |
| **🟡 9** | **`simota/agent-skills`** | Multi-Agent Orchestration | Nexus coordinator pattern; specialized agent persona recipes; cross-agent handoffs. | Unbounded multi-agent chatter; enforce structured message contracts. | `workflows/`, `scripts/manage_state.py` |
| **🟡 10** | **`open-agent-craft/awesome-agent-skills`** | Ecosystem Taxonomy | Broad domain classification index; community curation workflows. | Uncurated quality pollution; strictly enforce quarantine gate. | `awesome_skills/`, `sources/` |

---

## 5. Architectural Synthesis: The Unified Engine

```
                             ALL-SKILLS v2
                                  │
    ┌─────────────────────────────┼─────────────────────────────┐
    ▼                             ▼                             ▼
 REGISTRY                      ROUTER                        SECURITY
 [skillregistry]             [SkillRouter]                  [SkillLens]
 [nikships-registry]         [SR-Agents]                    [SkillEvaluator]
    │                             │                             │
    └─────────────────────────────┼─────────────────────────────┘
                                  │
                                  ▼
                               RUNTIME
                         [Least-Privilege]
                         [L0–L4 Autonomy]
                                  │
                                  ▼
                             COMPOSITION
                           [simota-nexus]
                           [anthropics]
                                  │
                                  ▼
                              EXECUTION
                                  │
                                  ▼
                             EVALUATION
                     [NVIDIA SkillEvaluator]
                     [agent-skills-eval A/B]
                                  │
                                  ▼
                          LOCAL TELEMETRY
                                  │
                                  ▼
                           DYNAMIC ROUTING
                             IMPROVEMENT
```

---

## 6. Single Source of Truth Metrics & Ecosystem Alignment

To ensure platform trustworthiness, all documentation, generated indexes, and CLI outputs strictly adhere to a synchronized single source of truth:

| Metric Category | Authoritative Value | Source of Truth Location | Description |
| :--- | :---: | :--- | :--- |
| **Canonical Skills** | **122** | `skills/` | Validated, core engineering skills |
| **Active Harness Skills** | **70** | `.agents/skills/` | Pre-loaded staff-engineer playbooks |
| **Manifest Skills** | **192** | `manifest.json` | Fully tool-mapped and verified skills |
| **Unique Skills** | **12,757** | `dependency_graph.json`, `stats.json` | Distinct capabilities across the platform |
| **Catalog Records** | **14,855** | `awesome_skills/CATALOG.md` | Domain-categorized skill entries |
| **Super-Domains** | **15** | `ontology/domains.json` | Top-level academic & industry domains |
| **Sub-Domains** | **251** | `awesome_skills/`, `ontology/domains.json` | Specialized subject categories |
| **Supported Platforms** | **11** | `platforms/platforms.yaml` | Claude, Cursor, Codex, Antigravity, etc. |
| **Passing Tests** | **94 / 94** | `scripts/skills/skills.py test` | Core runtime and routing unit tests |
| **Valid Frontmatters** | **192 / 192** | `scripts/validate_schema.py` | Validated YAML frontmatter schemas |

---

## 7. Implementation Roadmap & Rollout Sequence

1. **Phase 1 (Specification & Governance)**: Standardize v2 Master Plan, L0–L4 Autonomy hierarchies, evidence records, and reference sources registry. *(Completed)*
2. **Phase 2 (Evaluation & Benchmarks)**: Implement `benchmarks/` test runner and with-vs-without skill A/B harness (`agent-skills-eval` integration).
3. **Phase 3 (Large-Scale Router Scaling)**: Implement dense bi-encoder / BM25 reranking inspired by `SkillRouter` and `SR-Agents`.
4. **Phase 4 (Runtime Sandboxing & Network Policies)**: Enforce sub-process isolation, memory limits, and explicit domain allowlisting.
5. **Phase 5 (Skill Package SDK & CLI)**: Deliver `allskills-sdk` with `@skill` decorator and `allskills pack/publish/install` CLI workflows.
