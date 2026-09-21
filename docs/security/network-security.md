# Network Security & Interface Hardening Policy

**Document Version:** 1.0.0  
**Effective Date:** 2026-09-21  
**Scope:** HTTP/REST APIs, WebSockets, Voice Streaming, MCP Connectors, and Skill Egress  

---

## 1. Network Boundary Architecture

The All-Skills platform provides Web, API, and Voice endpoints for multi-agent interactions. The network architecture strictly separates local development from production deployments:

```
[Client / Agent Request]
         │
         ▼
[Reverse Proxy / TLS 1.3 Termination] (NGINX / Cloudflare / Envoy)
         │  - Rate Limiting (100 req/min/IP)
         │  - Request Size Limit (10MB max)
         │  - WAF & Sanitization
         ▼
[Authentication Gate]
         │  - Bearer Token / API Key / OAuth2
         │  - Tenant & Workspace Context Extraction
         ▼
[All-Skills Core API / Interface] (127.0.0.1:8000)
         │
         ▼
[Outbound Skill Egress Filter]
         ├── Allowed: Declared in SKILL.md (e.g., api.github.com)
         └── Denied: Undeclared domains, internal RFC1918 IPs, cloud metadata (169.254.169.254)
```

---

## 2. Environment Binding Requirements

| Environment | Allowed Host Bindings | TLS Requirement | Authentication | Default Port |
| :--- | :--- | :--- | :--- | :--- |
| **Development** | `127.0.0.1` (Localhost ONLY) | Optional (HTTP/WS) | Disabled or Local Token | `8000` |
| **Testing / CI** | `127.0.0.1` | Disabled | Test Mock Tokens | Ephemeral |
| **Production** | Reverse Proxy (`127.0.0.1` internal, TLS public) | **Mandatory TLS 1.3** | **Mandatory** (Bearer / API Key) | `443` public, `8000` internal |

> [!WARNING]
> Binding to `0.0.0.0` without an upstream TLS reverse proxy and authentication gateway is **strictly prohibited in production**. The default `config.yaml` is set to `127.0.0.1` to prevent accidental public exposure.

---

## 3. Production Ingress Controls

1. **Transport Layer Security (TLS)**:
   - Minimum TLS version: **TLS 1.3** (TLS 1.2 permitted only for legacy agent clients).
   - Perfect Forward Secrecy (PFS) ciphers required (`TLS_AES_128_GCM_SHA256`, `TLS_AES_256_GCM_SHA384`).
2. **Authentication & Access Tokens**:
   - Every API request must supply `Authorization: Bearer <token>` or `X-AllSkills-API-Key: <key>`.
   - API keys are cryptographically hashed (SHA-256) before comparison; raw keys are never logged.
3. **Rate Limiting & Abuse Prevention**:
   - Default tier: 100 requests / minute per client IP / API key.
   - Burst limit: 150 requests / minute.
   - Exceeded limits return HTTP `429 Too Many Requests` with `Retry-After` header.
4. **Payload Restrictions**:
   - Maximum HTTP body size: **10 MB**.
   - Chunked transfer encoding validated to prevent HTTP request smuggling.

---

## 4. Outbound Egress & Domain Whitelisting

Skills requiring network access must explicitly declare targeted domains in their `SKILL.md` frontmatter:

```yaml
network_access:
  enabled: true
  allowed_domains:
    - "api.github.com"
    - "raw.githubusercontent.com"
```

### Prohibited Outbound Targets
The platform egress filter unconditionally drops outbound traffic directed to:
- **Cloud Metadata Endpoints**: `http://169.254.169.254/` (AWS/GCP/Azure instance credentials).
- **Private RFC1918 Ranges**: `10.0.0.0/8`, `172.16.0.0/12`, `192.168.0.0/16` (internal host scanning).
- **Localhost Loopback**: `127.0.0.1`, `::1` (preventing SSRF to local administrative ports).
- **Dynamic DNS / Raw IP Webhooks**: Disallowed unless explicitly whitelisted in security policy.

---

## 5. Network Audit & Incident Logging

All network ingress and egress events generate structured audit records:
```json
{
  "timestamp": "2026-09-21T12:00:00Z",
  "event": "egress_request",
  "skill_id": "development.git-sync",
  "target_host": "api.github.com",
  "decision": "ALLOW",
  "policy_version": "1.0.0"
}
```
Credentials, authorization headers, and request payloads are automatically redacted (`********`) prior to log ingestion.
