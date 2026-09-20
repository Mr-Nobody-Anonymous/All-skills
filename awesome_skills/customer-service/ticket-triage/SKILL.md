---
name: ticket-triage
description: "Support ticket classification, priority assignment, routing, SLA management, and escalation workflows"
category: customer-service
version: 1.0.0
disable-model-invocation: false
risk: low
source: "https://github.com/Mr-Nobody-Anonymous/All-skills"
source_repository: "Mr-Nobody-Anonymous/All-skills"
source_path: "awesome_skills/customer-service/ticket-triage/SKILL.md"
license: "MIT"
imported_at: "2026-09-20"
---

# Ticket Triage

## Scope
Ticket triage is the process of classifying, prioritizing, and routing incoming customer support requests to ensure timely resolution within SLA targets. This skill covers triage frameworks, automation strategies, and escalation workflows.

## Triage Framework

### Priority Classification
| Priority | Definition | Response SLA | Resolution SLA | Examples |
|----------|-----------|-------------|----------------|---------|
| P1 (Critical) | Service down, no workaround, business impact | 15 min | 4 hours | Complete outage, data loss, security breach |
| P2 (High) | Major functionality impaired, workaround exists | 1 hour | 8 hours | Feature broken for many users, degraded performance |
| P3 (Medium) | Minor functionality affected, workaround available | 4 hours | 24 hours | Non-critical bug, cosmetic issue, single user |
| P4 (Low) | Enhancement request, question, documentation | 24 hours | 5 business days | Feature request, how-to question |

### Classification Dimensions
1. **Impact**: How many users/revenue affected?
   - Enterprise-wide > Team > Individual
2. **Urgency**: How time-sensitive is the resolution?
   - Blocking work > Degraded > Inconvenient > Nice-to-have
3. **Complexity**: How much expertise is needed?
   - Known fix > Investigation needed > Engineering escalation > Product change

### Routing Matrix
| Category | Route To | Criteria |
|----------|----------|---------|
| Billing/Account | Billing team | Payment, invoicing, subscription, refund |
| Technical - Tier 1 | Frontline support | Known issues, password resets, basic config |
| Technical - Tier 2 | Senior support | Complex debugging, integration issues |
| Technical - Tier 3 | Engineering | Bug confirmation, code-level investigation |
| Security | Security team | Vulnerability report, data breach, unauthorized access |
| Feature request | Product team | Enhancement, new capability, UX feedback |

## Triage Decision Tree
```
1. Is this a security incident?
   → YES: Route to Security (P1 immediately)
   → NO: Continue

2. Is the service completely unavailable?
   → YES: P1, route to on-call engineering
   → NO: Continue

3. How many users are affected?
   → Many (>10): P2, route to Tier 2
   → Few (2-10): P3, route to Tier 1/2
   → One: P3/P4, route to Tier 1

4. Is there a workaround?
   → YES: Lower priority by one level
   → NO: Maintain priority

5. Is this a known issue?
   → YES: Link to existing ticket, apply known fix
   → NO: Create new investigation ticket
```

## Automation Strategies
- **Auto-classification**: ML model trained on historical tickets (category, priority, routing)
- **Keyword matching**: Rules engine for common patterns ("can't log in" → Auth team)
- **Sentiment analysis**: Detect frustrated/angry customers → flag for priority handling
- **Auto-response**: Acknowledge receipt, provide self-service links, set expectations
- **SLA clock**: Automatically start and track response/resolution timers

## Escalation Workflow
1. **Functional escalation**: Tier 1 → Tier 2 → Tier 3 → Engineering
2. **Hierarchical escalation**: After SLA breach → Manager → Director → VP
3. **Escalation triggers**:
   - SLA approaching (75% of time elapsed)
   - Customer explicitly requests escalation
   - Multiple contacts for same issue
   - VIP/enterprise customer

## Metrics
- **First Response Time (FRT)**: Time from ticket creation to first human response
- **Average Resolution Time (ART)**: Total time to close ticket
- **First Contact Resolution (FCR)**: % resolved in single interaction
- **Ticket backlog**: Open tickets by priority and age
- **SLA compliance rate**: % of tickets resolved within SLA
- **CSAT**: Customer satisfaction score per ticket

## Tools
- **Zendesk**: Ticketing, automation, reporting
- **Freshdesk**: Multi-channel support platform
- **Jira Service Management**: ITSM-oriented
- **Intercom**: Conversational support with bot triage
- **PagerDuty**: On-call management and incident escalation

## References
- ITIL 4 — Incident Management practice
- HDI — Support Center Certification standards
