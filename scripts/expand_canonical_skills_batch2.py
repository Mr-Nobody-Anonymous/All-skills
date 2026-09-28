"""Batch 2 expansion for canonical skill suites: Programming, Cloud, FinOps, AI, Security, Observability, Product, Education, Finance/Business, Creative."""
from __future__ import annotations

import os
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(REPO_ROOT))

from typing import Dict, List, Tuple
from scripts.expand_canonical_skills import create_skill_markdown, SKILLS_ROOT

CANONICAL_DOMAIN_SPECS_BATCH2: Dict[str, List[Tuple[str, str, str, str, List[str], List[str]]]] = {
    "programming": [
        ("python-fundamentals", "Python Language Fundamentals & OOP", "Core Python semantics, object-oriented design, dunder methods, generators, and standard library patterns.", "procedural", ["python fundamentals", "python oop classes"], ["python", "oop", "dunder", "generators"]),
        ("python-idiomatic-style", "Idiomatic Python (Pythonic) Style", "Write clean, idiomatic Python adhering to PEP 8, list comprehensions, context managers, and type annotations.", "procedural", ["idiomatic python style", "pythonic code review"], ["python", "pep8", "pythonic", "typing"]),
        ("python-testing", "Python Testing with pytest & Hypothesis", "Comprehensive Python testing with pytest fixtures, parameterization, mocking, and property-based testing.", "procedural", ["pytest testing python", "python hypothesis tests"], ["pytest", "testing", "fixtures", "mock"]),
        ("python-security", "Python Secure Coding & Bandit Auditing", "Identify and remediate Python security vulnerabilities, unsafe deserialization, SQL injection, and AST linting.", "procedural", ["python secure coding", "bandit python security"], ["python", "security", "bandit", "vulnerability"]),
        ("python-async", "Python Asynchronous Programming & asyncio", "Master Python asynchronous I/O, asyncio event loops, coroutines, tasks, and async context managers.", "procedural", ["python asyncio coroutines", "async await python"], ["python", "asyncio", "async", "coroutines"]),
        ("typescript-fundamentals", "TypeScript Advanced Types & Generics", "Master TypeScript type algebra: conditional types, mapped types, template literals, and type narrowing.", "procedural", ["typescript advanced types", "typescript generics narrowing"], ["typescript", "types", "generics", "compiler"]),
        ("typescript-project-structure", "Enterprise TypeScript Architecture", "Structure large monorepos with TypeScript project references, path mappings, and tsconfig optimization.", "procedural", ["typescript monorepo structure", "tsconfig optimization"], ["typescript", "tsconfig", "monorepo", "architecture"]),
        ("typescript-testing", "TypeScript Testing with Vitest & Jest", "Unit and integration testing for TypeScript with Vitest, Jest, ts-jest, and coverage reporting.", "procedural", ["typescript vitest testing", "jest typescript mocks"], ["typescript", "vitest", "jest", "testing"]),
        ("rust-fundamentals", "Rust Language Ownership & Borrowing", "Master Rust ownership, borrowing rules, lifetimes, traits, pattern matching, and memory safety invariants.", "procedural", ["rust ownership borrowing", "rust lifetimes traits"], ["rust", "ownership", "borrowing", "lifetimes"]),
        ("rust-async", "Rust Asynchronous Programming with Tokio", "Build high-throughput async systems with Tokio runtime, Futures, async channels, and select macros.", "procedural", ["rust async tokio", "rust futures channels"], ["rust", "tokio", "async", "concurrency"]),
        ("rust-testing", "Rust Testing, Benchmarking & Miri", "Write unit, integration, and documentation tests, criterion benchmarks, and unsafe validation with Miri.", "procedural", ["rust testing criterion benchmark", "miri unsafe validation"], ["rust", "testing", "criterion", "miri"]),
        ("go-fundamentals", "Go Language Idioms & Interfaces", "Core Go programming: interfaces, structs, error handling patterns, slices, and standard library conventions.", "procedural", ["go language fundamentals", "golang interfaces errors"], ["go", "golang", "interfaces", "structs"]),
        ("go-concurrency", "Go Concurrency with Goroutines & Channels", "Design concurrent Go systems using goroutines, buffered channels, select multiplexing, and sync primitives.", "procedural", ["go concurrency goroutines", "golang channels select"], ["go", "goroutines", "channels", "sync"]),
        ("go-testing", "Go Testing, Table-Driven Tests & Benchmarks", "Write idiomatic Go table-driven tests, subtests, race detector checks, and memory allocation benchmarks.", "procedural", ["go table driven tests", "golang benchmark race detector"], ["go", "testing", "benchmarks", "race"]),
        ("c-fundamentals", "C System Programming & Memory Management", "Direct pointer arithmetic, dynamic memory allocation (malloc/free), struct alignment, and POSIX system APIs.", "procedural", ["c system programming pointers", "malloc free memory management"], ["c", "pointers", "memory", "posix"]),
        ("cpp-modern", "Modern C++ (C++20/23) Core Engineering", "Modern C++ features: RAII, move semantics, smart pointers, concepts, ranges, and std::format.", "procedural", ["modern c++ raii concepts", "c++ smart pointers ranges"], ["c++", "modern-cpp", "raii", "smart-pointers"]),
        ("csharp-fundamentals", "Modern C# & .NET 8+ Platform Engineering", "Modern C# language features: pattern matching, records, LINQ, async/await, and dependency injection.", "procedural", ["c# modern dotnet", "csharp pattern matching linq"], ["csharp", "dotnet", "linq", "async"]),
        ("java-modern", "Modern Java (Java 21+) & Virtual Threads", "Modern Java development: virtual threads (Project Loom), records, pattern matching, and streams.", "procedural", ["modern java virtual threads", "java 21 pattern matching"], ["java", "jvm", "loom", "threads"]),
        ("bash-scripting", "Robust Shell & Bash Automation", "Write defensive Bash scripts with strict error trapping (set -euo pipefail), argument parsing, and subshells.", "procedural", ["robust bash scripting", "defensive shell pipefail"], ["bash", "shell", "posix", "automation"]),
        ("powershell-automation", "PowerShell Advanced Scripting & Modules", "Develop reusable PowerShell cmdlets, pipeline processing, PSCustomObjects, and cross-platform PowerShell 7.", "procedural", ["powershell automation script", "powershell cmdlet module"], ["powershell", "windows", "pwsh", "automation"]),
        ("sql-advanced", "Advanced SQL & Window Functions", "Master complex SQL queries, recursive CTEs, analytic window functions, and execution plan optimization.", "procedural", ["advanced sql window functions", "recursive cte optimization"], ["sql", "cte", "window-functions", "queries"]),
        ("solidity-smart-contracts", "Solidity Smart Contract Security & Gas", "Write secure Ethereum smart contracts, reentrancy guards, ERC-20/721 standards, and EVM gas optimization.", "procedural", ["solidity smart contract security", "evm gas optimization reentrancy"], ["solidity", "ethereum", "smart-contracts", "evm"])
    ],
    "cloud": [
        ("aws-compute", "AWS Compute Architecture (EC2, ECS, EKS)", "Architect resilient compute clusters on AWS with auto-scaling groups, spot fleets, and containerized tasks.", "procedural", ["aws ec2 ecs compute", "aws auto scaling spot"], ["aws", "ec2", "ecs", "compute"]),
        ("aws-networking", "AWS VPC & Network Architecture", "Design secure VPC topologies, transit gateways, NAT gateways, VPC endpoints, and Route 53 routing.", "procedural", ["aws vpc network architecture", "transit gateway vpc endpoints"], ["aws", "vpc", "networking", "transit-gateway"]),
        ("aws-security", "AWS Identity & IAM Security Engineering", "Enforce least-privilege IAM policies, AWS Organizations SCPs, KMS encryption, and GuardDuty monitoring.", "procedural", ["aws iam security least privilege", "aws kms organizations scp"], ["aws", "iam", "security", "kms"]),
        ("azure-architecture", "Azure Cloud Infrastructure & Landing Zones", "Deploy enterprise Azure landing zones, virtual networks, Azure App Services, and subscription governance.", "procedural", ["azure landing zone architecture", "azure vnet governance"], ["azure", "cloud", "landing-zone", "vnet"]),
        ("gcp-architecture", "Google Cloud Platform Architecture", "Design GCP projects, VPC service controls, Compute Engine, Google Kubernetes Engine (GKE), and Cloud Run.", "procedural", ["gcp cloud architecture", "google cloud gke vpc"], ["gcp", "google-cloud", "gke", "cloud-run"]),
        ("cloudflare-edge", "Cloudflare Workers & Edge Infrastructure", "Build edge applications using Cloudflare Workers, KV, D1 SQL database, R2 object storage, and Zero Trust.", "procedural", ["cloudflare workers edge", "cloudflare d1 r2 storage"], ["cloudflare", "workers", "edge", "serverless"]),
        ("vercel-deployment", "Vercel Platform Engineering & Edge Functions", "Deploy full-stack web applications with Vercel edge middleware, preview environments, and analytics.", "procedural", ["vercel deployment configuration", "vercel edge middleware preview"], ["vercel", "deployment", "edge", "nextjs"])
    ],
    "finops": [
        ("cloud-cost-analysis", "Cloud Cost Analysis & Unit Economics", "Establish FinOps metrics, allocate tags, track unit costs per customer/transaction, and build cost models.", "procedural", ["cloud cost analysis finops", "cloud unit economics tags"], ["finops", "cost", "cloud", "unit-economics"]),
        ("aws-cost-optimization", "AWS Cost Optimization & Savings Plans", "Optimize AWS spend with Compute Savings Plans, Reserved Instances, EBS gp3 migrations, and S3 lifecycle rules.", "procedural", ["aws cost optimization savings plans", "reduce aws ec2 s3 spend"], ["aws", "finops", "cost", "savings-plans"]),
        ("gcp-cost-optimization", "GCP Cost Optimization & Committed Use", "Reduce GCP expenditures with Committed Use Discounts (CUDs), preemptible VMs, and BigQuery slot reservations.", "procedural", ["gcp cost optimization cud", "reduce gcp bigquery compute spend"], ["gcp", "finops", "cost", "cud"]),
        ("azure-cost-optimization", "Azure Cost Management & Reservations", "Optimize Azure spending via Azure Cost Management, hybrid benefits, reservations, and advisor recommendations.", "procedural", ["azure cost optimization reservations", "azure cost management advisor"], ["azure", "finops", "cost", "reservations"]),
        ("kubernetes-cost", "Kubernetes Cluster Cost Allocation & Kubecost", "Monitor and allocate pod, namespace, and workload costs in Kubernetes using Kubecost and OpenCost.", "procedural", ["kubernetes cost allocation kubecost", "opencost pod namespace spend"], ["kubernetes", "kubecost", "finops", "cost"]),
        ("idle-resource-detection", "Idle Cloud Resource Detection & Cleanup", "Automate discovery and termination of unattached EBS volumes, idle load balancers, and zombie instances.", "procedural", ["detect idle cloud resources", "cleanup unattached ebs volumes"], ["cleanup", "idle", "cost", "automation"]),
        ("rightsizing", "Cloud Compute & Database Rightsizing", "Analyze CPU, memory, and I/O utilization metrics to rightsize instances and database clusters without SLA risk.", "procedural", ["cloud rightsizing compute database", "instance rightsizing metrics"], ["rightsizing", "compute", "cost", "metrics"]),
        ("ai-inference-cost", "AI & LLM Inference Cost Optimization", "Reduce LLM API expenditures using prompt compression, semantic caching, token batching, and model routing.", "procedural", ["llm inference cost optimization", "reduce openai anthropic token spend"], ["llm", "tokens", "cost", "caching"])
    ],
    "ai": [
        ("model-selection", "LLM Model Selection & Cost-Performance Tradeoffs", "Evaluate LLM tradeoffs across latency, cost, reasoning capabilities, and context window requirements.", "knowledge", ["llm model selection tradeoff", "evaluate model latency cost"], ["ai", "llm", "models", "selection"]),
        ("model-evaluation", "Empirical LLM Benchmarking & Evaluation", "Build automated evaluation harnesses with golden datasets, LLM-as-judge scoring, and rubric grading.", "procedural", ["llm automated evaluation harness", "llm as a judge benchmark"], ["evaluation", "benchmark", "llm-judge", "rubrics"]),
        ("prompt-engineering", "Systematic Prompt Engineering & Chain-of-Thought", "Design effective system prompts, few-shot exemplars, structured instructions, and reasoning chains.", "procedural", ["prompt engineering system prompt", "few shot chain of thought"], ["prompt", "system-prompt", "few-shot", "reasoning"]),
        ("structured-output", "Structured Output Generation (JSON/Pydantic)", "Enforce deterministic schema extraction from LLMs using JSON Schema, Pydantic models, and constrained decoding.", "procedural", ["structured output json pydantic", "enforce llm schema extraction"], ["structured-output", "pydantic", "json", "schema"]),
        ("tool-calling", "LLM Tool Calling & Function Execution", "Design robust tool definitions, parameter schemas, error handling, and execution safety for tool-using LLMs.", "procedural", ["llm tool calling function execution", "tool definition schema llm"], ["tools", "function-calling", "mcp", "agents"]),
        ("rag", "Retrieval-Augmented Generation (RAG) Architecture", "Architect production RAG systems with document chunking, semantic retrieval, context stuffing, and citation attribution.", "procedural", ["retrieval augmented generation rag", "document chunking vector search"], ["rag", "retrieval", "embeddings", "vector"]),
        ("hybrid-search", "Hybrid Search (BM25 + Dense Vector)", "Combine sparse keyword search (BM25) with dense vector embeddings using Reciprocal Rank Fusion (RRF).", "procedural", ["hybrid search bm25 vector", "reciprocal rank fusion rrf"], ["hybrid-search", "bm25", "dense", "rrf"]),
        ("reranking", "Cross-Encoder & LLM Retrieval Reranking", "Boost retrieval precision by reranking candidate passages with Cohere, BGE-Reranker, or cross-encoders.", "procedural", ["retrieval reranking cross encoder", "cohere bge reranker pipeline"], ["reranking", "cross-encoder", "retrieval", "precision"]),
        ("embeddings", "Vector Embeddings Generation & Similarity Metrics", "Generate dense text embeddings, optimize chunk dimensions, and evaluate cosine, dot product, and Euclidean metrics.", "procedural", ["generate vector embeddings", "cosine similarity vector distance"], ["embeddings", "vector", "similarity", "cosine"]),
        ("fine-tuning", "LLM Parameter-Efficient Fine-Tuning (PEFT/LoRA)", "Fine-tune open-weight LLMs using LoRA, QLoRA, Hugging Face TRL, and custom instruction datasets.", "procedural", ["fine tune llm lora qlora", "peft instruction fine tuning"], ["fine-tuning", "lora", "qlora", "huggingface"]),
        ("quantization", "LLM Quantization & Hardware Inference", "Quantize model weights to GGUF, AWQ, and GPTQ formats for accelerated GPU/CPU inference without quality loss.", "procedural", ["llm quantization gguf awq", "quantize model weights gptq"], ["quantization", "gguf", "awq", "inference"]),
        ("vllm", "vLLM High-Throughput Inference Serving", "Deploy self-hosted LLMs with vLLM, PagedAttention, continuous batching, and tensor parallelism.", "procedural", ["vllm model serving deploy", "pagedattention continuous batching"], ["vllm", "serving", "gpu", "inference"]),
        ("multimodal", "Multimodal AI Vision & Audio Processing", "Process multimodal image, audio, and video inputs with vision-language models and transcription pipelines.", "procedural", ["multimodal vision language model", "process image audio inputs llm"], ["multimodal", "vision", "audio", "vlm"])
    ],
    "security": [
        ("threat-modeling", "Threat Modeling & STRIDE / PASTA Analysis", "Perform systematic application threat modeling using STRIDE, Attack Trees, and data flow diagrams (DFDs).", "knowledge", ["threat modeling stride pasta", "application threat model attack tree"], ["security", "stride", "threat-modeling", "risk"]),
        ("secure-architecture", "Secure Software Architecture & Zero Trust", "Design defensible architectures adhering to defense-in-depth, least privilege, and zero-trust principles.", "knowledge", ["secure software architecture design", "defense in depth zero trust"], ["security", "architecture", "zero-trust", "defense"]),
        ("secure-code-review", "Secure Code Review & Vulnerability Hunting", "Identify injection flaws, deserialization vulnerabilities, race conditions, and cryptographic weaknesses in code.", "procedural", ["secure code review audit", "vulnerability code inspection"], ["code-review", "vulnerabilities", "owasp", "security"]),
        ("sast", "Static Application Security Testing (SAST)", "Configure and interpret SAST scans using Semgrep, SonarQube, and CodeQL with custom security rulesets.", "procedural", ["sast scan semgrep codeql", "static application security testing"], ["sast", "semgrep", "codeql", "scanning"]),
        ("dast", "Dynamic Application Security Testing (DAST)", "Automate dynamic web vulnerability scanning using OWASP ZAP and Nuclei in CI/CD staging environments.", "procedural", ["dast web vulnerability scan", "owasp zap nuclei automation"], ["dast", "zap", "nuclei", "dynamic"]),
        ("container-security", "Container Security & Image Hardening", "Harden Dockerfiles, scan images with Trivy/Grype, enforce non-root execution, and minimize attack surfaces.", "procedural", ["container security image hardening", "trivy dockerfile vulnerability scan"], ["docker", "containers", "trivy", "hardening"]),
        ("kubernetes-security", "Kubernetes Security & Pod Security Standards", "Enforce Pod Security Standards (PSS), NetworkPolicies, RBAC least privilege, and Kyverno/OPA policies.", "procedural", ["kubernetes security rbac networkpolicy", "kyverno pod security standards"], ["kubernetes", "rbac", "network-policy", "k8s"]),
        ("iam", "Cloud Identity & Access Management (IAM)", "Design role-based and attribute-based access control (RBAC/ABAC), temporary credentials, and federation.", "procedural", ["cloud iam rbac abac design", "least privilege access credentials"], ["iam", "rbac", "abac", "identity"]),
        ("incident-response", "Security Incident Response & Forensics", "Execute security incident containment, eradication, log timeline reconstruction, and post-incident reviews.", "procedural", ["security incident response plan", "incident containment forensic timeline"], ["incident-response", "forensics", "containment", "breach"]),
        ("zero-trust", "Enterprise Zero-Trust Security Implementation", "Implement microsegmentation, explicit identity verification, device health validation, and least privilege.", "procedural", ["enterprise zero trust implementation", "microsegmentation identity validation"], ["zero-trust", "identity", "microsegmentation", "security"])
    ],
    "observability": [
        ("prometheus", "Prometheus Metrics & PromQL Monitoring", "Configure Prometheus metrics scrapers, custom application exporters, Alertmanager rules, and PromQL queries.", "procedural", ["prometheus metrics promql query", "alertmanager recording rules"], ["prometheus", "promql", "metrics", "monitoring"]),
        ("grafana", "Grafana Dashboard Engineering & Visualizations", "Design actionable operational dashboards, SLO tracking panels, dynamic variables, and alerting in Grafana.", "procedural", ["grafana dashboard design slo", "operational panels alerting grafana"], ["grafana", "dashboards", "visualization", "slo"]),
        ("opentelemetry", "OpenTelemetry Instrumentation & Collectors", "Instrument distributed services using OpenTelemetry SDKs, trace propagators, spans, and OpenTelemetry Collector.", "procedural", ["opentelemetry instrumentation tracing", "otel collector pipeline setup"], ["opentelemetry", "otel", "tracing", "telemetry"]),
        ("distributed-tracing", "Distributed Tracing & Request Context", "Track end-to-end request latency across microservices, identifying bottlenecks and trace sampling rates.", "procedural", ["distributed tracing request latency", "trace context propagation microservices"], ["tracing", "spans", "jaeger", "latency"]),
        ("logging", "Structured Logging & Centralized Log Aggregation", "Implement structured JSON logging, correlation IDs, log levels, and aggregation via Vector/FluentBit.", "procedural", ["structured json logging correlation id", "centralized log aggregation pipeline"], ["logging", "json", "correlation", "logs"]),
        ("metrics", "System & Application Metrics Architecture", "Define RED (Rate, Errors, Duration) and USE (Utilization, Saturation, Errors) metric strategies for services.", "procedural", ["metrics architecture red use method", "define application latency error metrics"], ["metrics", "red", "use", "sli"]),
        ("slo-sli", "Service Level Objectives (SLOs) & Error Budgets", "Define Service Level Indicators (SLIs), realistic Service Level Objectives (SLOs), and manage error budgets.", "procedural", ["define slo sli error budgets", "service level objective calculation"], ["slo", "sli", "error-budget", "reliability"]),
        ("postmortems", "Blameless Postmortems & Incident Reviews", "Facilitate blameless post-incident retrospectives, root-cause timelines, and preventative action items.", "knowledge", ["blameless postmortem incident review", "root cause retrospective action items"], ["postmortem", "incident", "retrospective", "sre"])
    ],
    "product": [
        ("requirements-engineering", "Software Requirements Engineering & Specs", "Elicit, structure, and formalize technical and functional requirements into unambiguous specifications.", "procedural", ["software requirements engineering", "technical functional specification"], ["requirements", "spec", "engineering", "prd"]),
        ("user-stories", "User Story Authoring & INVEST Criteria", "Author actionable, value-driven user stories adhering to INVEST criteria with clear business context.", "procedural", ["write user stories invest criteria", "agile user story backlog"], ["user-stories", "agile", "invest", "scrum"]),
        ("acceptance-criteria", "Acceptance Criteria & BDD Given-When-Then", "Formulate rigorous, testable acceptance criteria using Given-When-Then syntax and edge case definitions.", "procedural", ["acceptance criteria given when then", "bdd acceptance criteria drafting"], ["acceptance-criteria", "bdd", "gherkin", "qa"]),
        ("product-metrics", "Product Metrics & North Star Measurement", "Define North Star metrics, activation funnels, retention cohorts, and feature engagement indicators.", "procedural", ["product metrics north star", "retention cohort funnel metrics"], ["metrics", "north-star", "analytics", "funnels"]),
        ("experimentation", "A/B Testing & Product Experimentation", "Design statistically valid A/B experiments, determine sample sizes, and analyze conversion lift.", "procedural", ["a b testing product experimentation", "sample size statistical lift test"], ["ab-testing", "experimentation", "conversion", "stats"]),
        ("prioritization", "Feature Prioritization Frameworks (RICE/Kano)", "Evaluate roadmap features objectively using RICE scoring, Kano models, and MoSCoW prioritization.", "procedural", ["feature prioritization rice framework", "kano model product backlog"], ["prioritization", "rice", "kano", "roadmap"])
    ],
    "education": [
        ("tutoring", "Adaptive AI Tutoring & Socratic Guidance", "Deliver personalized, scaffolded educational instruction using the Socratic method and concept checking.", "knowledge", ["ai tutoring socratic method", "scaffolded educational guidance"], ["education", "tutoring", "socratic", "pedagogy"]),
        ("curriculum-design", "Curriculum Architecture & Learning Objectives", "Design comprehensive educational curricula with Bloom's Taxonomy, learning outcomes, and module sequences.", "procedural", ["curriculum design blooms taxonomy", "learning objective sequence"], ["curriculum", "blooms-taxonomy", "learning", "pedagogy"]),
        ("spaced-repetition", "Spaced Repetition & Cognitive Memory Systems", "Design spaced repetition review schedules, SuperMemo SM-2 algorithms, and active recall flashcards.", "procedural", ["spaced repetition sm2 algorithm", "active recall flashcard design"], ["spaced-repetition", "sm2", "flashcards", "memory"]),
        ("quiz-generation", "Educational Assessment & Quiz Generation", "Generate balanced multiple-choice, short-answer, and code challenge assessments with automated rubrics.", "procedural", ["generate educational quiz questions", "assessment multiple choice rubrics"], ["quiz", "assessment", "rubric", "testing"])
    ],
    "finance": [
        ("financial-analysis", "Corporate Financial Statement Analysis", "Analyze Balance Sheets, Income Statements, and Cash Flow Statements using key financial ratios.", "knowledge", ["financial statement ratio analysis", "balance sheet cash flow evaluation"], ["finance", "accounting", "ratios", "statements"]),
        ("financial-modeling", "Discounted Cash Flow (DCF) & Financial Modeling", "Build three-statement integrated financial models, forecast revenues, and compute DCF valuations.", "procedural", ["dcf financial valuation model", "three statement financial forecast"], ["modeling", "dcf", "valuation", "forecast"]),
        ("accounting", "GAAP / IFRS Accounting Principles & Ledger Entries", "Understand double-entry bookkeeping, accrual accounting principles, revenue recognition, and ledger audits.", "knowledge", ["gaap ifrs accounting principles", "double entry bookkeeping accruals"], ["accounting", "gaap", "ifrs", "ledger"])
    ],
    "creative": [
        ("graphic-design", "Digital Graphic Design & Visual Hierarchy", "Apply core graphic design principles: contrast, balance, alignment, color harmony, and typographic scale.", "procedural", ["graphic design visual hierarchy", "color harmony typographic scale"], ["design", "graphic-design", "typography", "color"]),
        ("ui-design", "UI Interface & Component Architecture", "Design accessible, scalable digital user interfaces, form systems, states, and responsive navigation.", "procedural", ["ui component interface design", "responsive form states design"], ["ui", "design", "components", "forms"]),
        ("figma", "Figma Design Systems & Auto Layout", "Master Figma design tokens, auto layout frames, component variants, interactive prototypes, and Dev Mode.", "procedural", ["figma auto layout design system", "figma component variants prototype"], ["figma", "tokens", "auto-layout", "components"]),
        ("creative-writing", "Creative Writing & Narrative Storytelling", "Develop compelling story arcs, character motivations, worldbuilding, and engaging dialogue across genres.", "knowledge", ["creative writing story arc", "narrative character dialogue development"], ["writing", "creative", "narrative", "storytelling"])
    ]
}


def main() -> None:
    created = 0
    updated = 0
    for domain, skills in CANONICAL_DOMAIN_SPECS_BATCH2.items():
        domain_dir = SKILLS_ROOT / domain
        domain_dir.mkdir(parents=True, exist_ok=True)
        for slug, title, desc, stype, triggers, keywords in skills:
            skill_dir = domain_dir / slug
            skill_dir.mkdir(parents=True, exist_ok=True)
            skill_file = skill_dir / "SKILL.md"

            content = create_skill_markdown(domain, slug, title, desc, stype, triggers, keywords)
            skill_file.write_text(content, encoding="utf-8")
            created += 1

    print(f"Batch 2 expansion complete. Created: {created}, Existing/Updated: {updated} skills across {len(CANONICAL_DOMAIN_SPECS_BATCH2)} domains.")


if __name__ == "__main__":
    main()
