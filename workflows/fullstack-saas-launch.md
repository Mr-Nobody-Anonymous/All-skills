# Full-Stack SaaS Launch Workflow Playbook

> **Target Objective**: Build and ship a production-grade, profitable SaaS MVP rapidly with solid design tokens, type-safe database schemas, robust authentication, and accessible UI.

---

## Workflow Sequence

```
┌────────────────────────────────────────────────────────────────────────────────────────┐
│                              FULL-STACK SAAS LAUNCH FLOW                               │
├─────────────────┬──────────────────┬─────────────────┬────────────────┬────────────────┤
│ 1. MVP STRATEGY │ 2. DESIGN SYSTEM │ 3. DATABASE/ORM │ 4. AUTH & RBAC │ 5. ACCESSIBLE  │
│    & SCOPING    │    & TOKENS      │    SCHEMAS      │    PERMISSIONS │    UI & QA     │
├─────────────────┼──────────────────┼─────────────────┼────────────────┼────────────────┤
│ saas-mvp-       │ design-system &  │ database-design │ marketplace-   │ wcag-audit &   │
│ launcher        │ tailwind-system  │ & prisma-expert │ rbac-audit     │ playwright     │
└─────────────────┴──────────────────┴─────────────────┴────────────────┴────────────────┘
```

---

## Phase 1: MVP Scoping & Core Value Loop
- **Primary Skills**: [`.agents/skills/saas-mvp-launcher/SKILL.md`](../.agents/skills/saas-mvp-launcher/SKILL.md) & [`.agents/skills/micro-saas-launcher/SKILL.md`](../.agents/skills/micro-saas-launcher/SKILL.md)
- **Actions**:
  1. Initialize state: `python scripts/manage_state.py init fullstack-saas-launch`.
  2. Define the core loop: Problem ➔ Solution ➔ Monetization trigger.
  3. Strip away non-essential features (cut back to the single highest-value workflow).
- **Exit Gate**: 1-page PRD defining the core user journey.

---

## Phase 2: Design System & Visual Foundation
- **Primary Skills**: [`.agents/skills/design-system/SKILL.md`](../.agents/skills/design-system/SKILL.md) & [`.agents/skills/tailwind-design-system/SKILL.md`](../.agents/skills/tailwind-design-system/SKILL.md)
- **Actions**:
  1. Establish color tokens (avoid browser defaults; use curated HSL palettes).
  2. Configure typography scales, button states, and layout grids.
  3. Implement responsive navigation and mobile breakpoints.
- **Exit Gate**: Reusable component tokens and responsive app shell.

---

## Phase 3: Database Modeling & Type-Safe ORM
- **Primary Skills**: [`.agents/skills/database-design/SKILL.md`](../.agents/skills/database-design/SKILL.md), [`.agents/skills/prisma-expert/SKILL.md`](../.agents/skills/prisma-expert/SKILL.md), [`.agents/skills/drizzle-orm-expert/SKILL.md`](../.agents/skills/drizzle-orm-expert/SKILL.md)
- **Actions**:
  1. Design normalized relational schema (Users, Teams, Subscriptions, Resources).
  2. Implement foreign keys, indexes on high-frequency query columns, and timestamps.
  3. Generate and verify database migrations with rollback safety:
     ```bash
     python scripts/run_hook.py pre active.database-migration
     ```
- **Exit Gate**: Clean migrations executed and type-safe client generated.

---

## Phase 4: Authentication, Stripe Billing & RBAC
- **Primary Skill**: [`.agents/skills/marketplace-rbac-audit/SKILL.md`](../.agents/skills/marketplace-rbac-audit/SKILL.md)
- **Actions**:
  1. Implement session authentication and protected API middleware.
  2. Configure tenant boundary checks (ensure Tenant A cannot access Tenant B data).
  3. Integrate Stripe checkout session and webhook listeners.
- **Exit Gate**: Authorization audit passes; webhook signatures verified.

---

## Phase 5: Accessibility, Browser QA & Deployment
- **Primary Skills**: [`.agents/skills/wcag-audit-patterns/SKILL.md`](../.agents/skills/wcag-audit-patterns/SKILL.md), [`.agents/skills/browser-automation/SKILL.md`](../.agents/skills/browser-automation/SKILL.md), [`.agents/skills/cloud-devops/SKILL.md`](../.agents/skills/cloud-devops/SKILL.md)
- **Actions**:
  1. Run WCAG 2.2 accessibility audit (contrast, keyboard navigation, aria-labels).
  2. Run Playwright end-to-end user smoke tests.
  3. Configure Docker container and CI/CD deployment pipeline.
- **Exit Gate**: All automated browser tests pass, zero accessibility blockers, ready for traffic.
