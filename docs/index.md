# All-Skills Universal Documentation

Welcome to the **All-Skills Universal Voice Assistant & Multimodal Agent Operating System** documentation.

This platform bridges two powerful paradigms:
1. **Agent Skills Operating System**: A unified harness supporting 11 AI agent runtimes (Antigravity, Claude Code, Cursor, Codex, Windsurf, Roo Code, Cline, Goose, Kiro, OpenClaw, Gemini CLI) across 14,000+ domain skills.
2. **OpenVoiceOS (OVOS), Neon AI, and Mycroft Assistant Platform**: A voice and multimodal framework featuring 27 core categories, 714+ modeled skills, 405 built-in native skill implementations, and official OpenVoiceOS Skills Manager (OSM) synchronization.

---

## Quick Navigation

- [Installation Guide](file:///docs/installation.md): Set up the core framework, voice engines, and skill managers.
- [Configuration](file:///docs/configuration.md): Configure API keys, priority tiers, logging, and audio plugins.
- [Skill Catalog](file:///docs/skill_catalog.md): Comprehensive reference of all 27 categories, verified repos, and native packages.
- [Skill Development](file:///docs/skill_development.md): How to author, test, package, and publish new skills.
- [API Reference](file:///docs/api_reference.md): Core runtime engines, event bus, priority importer, and plugins.
- [Troubleshooting](file:///docs/troubleshooting.md): Diagnosing conflicts, audio issues, missing dependencies, and logs.
- [Contributing](file:///docs/contributing.md): Guidelines for upstream contributions, PRs, and quality gates.

---

## Architectural Principles

1. **Deterministic Execution**: Strict dependency management, zero circular imports, and verified AST syntax checking.
2. **Priority Tiers**: 7 latency-budgeted tiers from Tier 0 (Critical System) to Tier 6 (Lazy/On-Demand).
3. **Safety & Zero Deletions**: All repository operations preserve existing assets and enforce disk space quotas.
4. **Verified Upstreams**: Clear separation between verified active OpenVoiceOS/Neon repositories, archived Mycroft references, and built-in native implementations.
