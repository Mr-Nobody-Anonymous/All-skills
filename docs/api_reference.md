# API Reference Manual

The platform's runtime subsystem is modularized across [`core/`](file:///core/), [`scratch_priority_import/`](file:///scratch_priority_import/), [`plugins/`](file:///plugins/), [`integrations/`](file:///integrations/), and [`shared/`](file:///shared/).

---

## 1. Core Modules (`core/`)

- [`core/skill_manager.py`](file:///core/skill_manager.py): High-level orchestrator managing skill lifecycle, discovery, registration, and shutdown.
- [`core/skill_loader.py`](file:///core/skill_loader.py): Dynamic loader instantiating skill classes and injecting message buses. Defines `BaseVoiceSkill`.
- [`core/priority_engine.py`](file:///core/priority_engine.py): Executes tasks within prioritized tiers (Tier 0 to Tier 6) with latency enforcement.
- [`core/conflict_resolver.py`](file:///core/conflict_resolver.py): Resolves multi-skill intent overlaps using confidence scoring, context matching, and user pinning.
- [`core/intent_router.py`](file:///core/intent_router.py): Multi-stage intent parsing utilizing exact vocab match, regex rules, and semantic embeddings.
- [`core/event_bus.py`](file:///core/event_bus.py): Real-time pub/sub message bus connecting speech engines, skills, and hardware abstraction layers.
- [`core/plugin_system.py`](file:///core/plugin_system.py): Plugin loader for STT, TTS, Wake Word, Audio, Intent, and PHAL providers.
- [`core/health_checker.py`](file:///core/health_checker.py): Real-time telemetry monitoring memory RSS, CPU percentage, latency, and error rates.

---

## 2. Priority Importer (`scratch_priority_import/`)

- [`scratch_priority_import/priority_levels.py`](file:///scratch_priority_import/priority_levels.py): Defines `PriorityTier` enums and millisecond latency budgets.
- [`scratch_priority_import/skill_registry.py`](file:///scratch_priority_import/skill_registry.py): Metadata store registering version, dependencies, conflicts, and tiers.
- [`scratch_priority_import/dependency_graph.py`](file:///scratch_priority_import/dependency_graph.py): Directed acyclic graph calculating in-degree, out-degree, and transitive dependencies.
- [`scratch_priority_import/circular_dependency_detector.py`](file:///scratch_priority_import/circular_dependency_detector.py): Depth-first cycle detector preventing circular import locks.
- [`scratch_priority_import/lazy_loader.py`](file:///scratch_priority_import/lazy_loader.py): Deferred proxy loader instantiating heavyweight packages on first invocation.
- [`scratch_priority_import/resource_monitor.py`](file:///scratch_priority_import/resource_monitor.py): System resource tracker ensuring memory footprint does not exceed threshold.

---

## 3. Integrations (`integrations/`)

- `home_assistant`: Direct REST/WebSocket client for entity querying and state toggle.
- `google`: OAuth2 integration for Google Calendar, Maps, and Drive.
- `microsoft`: Microsoft Graph API integration for Outlook and Teams.
- `aws`: S3, IoT Core, and Alexa bridge.
- `openai`: ChatGPT fallback, Whisper STT, and DALL-E image generation.
- `anthropic`: Claude reasoning and complex task synthesis.
- `spotify`: Spotify Web API playback and playlist controller.
- `databases`: Connectors for SQLite, PostgreSQL, Redis, and MongoDB.

---

## 4. Shared Libraries (`shared/`)

- `api_clients`: Reusable REST, GraphQL, WebSocket, gRPC, and MQTT clients.
- `auth`: OAuth2 token store, API key manager, and JWT verification.
- `cache`: In-memory LRU, disk-backed, and Redis TTL caches.
- `localization`: 12 language packs (`en-us`, `es-es`, `fr-fr`, `de-de`, `pt-br`, `it-it`, `zh-cn`, `ja-jp`, `ko-kr`, `ar-sa`, `hi-in`, `ru-ru`).
- `security`: AES encryption, SHA hashing, input sanitization, and token rate limiting.
