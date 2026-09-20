---
name: records-management
description: "Organizational records lifecycle: classification, retention scheduling, disposition, compliance, and digital preservation"
category: archiving
version: 1.0.0
disable-model-invocation: false
risk: low
source: "https://github.com/Mr-Nobody-Anonymous/All-skills"
source_repository: "Mr-Nobody-Anonymous/All-skills"
source_path: "awesome_skills/archiving/records-management/SKILL.md"
license: "MIT"
imported_at: "2026-09-20"
---

# Records Management

## Scope
Records management is the systematic control of organizational records throughout their lifecycle — from creation through active use, retention, and final disposition. This skill covers classification, retention scheduling, disposition, compliance, and digital preservation.

## Records Lifecycle

### Phases
1. **Creation/Receipt**: Record is generated or received
2. **Classification**: Assigned to a records class with retention rules
3. **Active use**: Record is regularly accessed for business purposes
4. **Semi-active**: Infrequent access; may move to secondary storage
5. **Disposition**: Destruction, permanent retention, or transfer to archives

## Classification Systems

### Functional Classification
- Organize records by **business function**, not organizational structure
- Example hierarchy:
  - 100 — Governance & Corporate Management
  - 200 — Finance & Accounting
  - 300 — Human Resources
  - 400 — Legal & Compliance
  - 500 — Operations
  - 600 — Customer Relations
  - 700 — Information Technology

### Metadata Requirements
Every record should have:
- Title, description, creator
- Date created, date received
- Classification code
- Security classification (public, internal, confidential, restricted)
- Retention class and trigger event
- Format and location (physical/digital)

## Retention Scheduling

### Retention Schedule Structure
| Records Class | Description | Retention Period | Trigger | Disposition |
|--------------|-------------|-----------------|---------|-------------|
| Financial records | Invoices, receipts, ledgers | 7 years | End of fiscal year | Destroy |
| Employment records | Personnel files | 7 years | Termination date | Destroy |
| Contracts | Executed agreements | 10 years | Contract expiry | Review → destroy/archive |
| Board minutes | Corporate governance | Permanent | — | Transfer to archives |
| Correspondence | General business | 3 years | Date of record | Destroy |
| Tax records | Returns, supporting docs | 7 years (US IRS) | Filing date | Destroy |

### Legal Holds
- **Definition**: Suspension of normal disposition when litigation is reasonably anticipated
- **Scope**: All records potentially relevant to the legal matter
- **Process**: Legal issues hold notice → identify custodians → preserve records → release when resolved
- **Failure to comply**: Spoliation sanctions, adverse inference instructions

## Digital Records

### Email Management
- Classify by content, not by sender/recipient
- Auto-categorize with rules or ML
- Retention applied at classification level, not mailbox level

### Electronic Records Management Systems (ERMS)
- **Features**: Classification, retention automation, access control, audit trail, search, disposition workflow
- **Products**: OpenText, IBM FileNet, Hyland, Microsoft Purview, Alfresco
- **Integration**: SharePoint, email systems, ERP, CRM

### Digital Preservation
- **Format migration**: Convert obsolete formats to current standards (TIFF, PDF/A, XML)
- **Fixity checking**: Hash verification (SHA-256) to detect corruption
- **OAIS model**: Open Archival Information System — reference model for digital preservation
- **Trusted digital repositories**: ISO 16363 certification

## Compliance Requirements

### Key Regulations
| Regulation | Jurisdiction | Key Records Requirements |
|-----------|-------------|------------------------|
| SOX (Sarbanes-Oxley) | US | 7-year retention of financial audit records |
| GDPR | EU | Data minimization, right to erasure, DPIAs |
| HIPAA | US | 6-year retention of health records (from last effective date) |
| SEC Rule 17a-4 | US | 3-6 year retention of broker-dealer records (WORM storage) |
| Federal Records Act | US | Government records retention per NARA schedules |

### Defensible Disposition
- Follow approved retention schedule consistently
- Document disposition actions (what, when, who, authority)
- Never destroy records under legal hold
- Regular audits of retention compliance

## Standards
- **ISO 15489**: Information and documentation — Records management (Part 1: Concepts, Part 2: Guidelines)
- **ISO 16175**: Principles and functional requirements for records in electronic environments
- **ARMA International**: Generally Accepted Recordkeeping Principles (Information Governance Maturity Model)
- **DoD 5015.02**: Electronic Records Management standard (US Department of Defense)

## References
- Shepherd & Yeo — *Managing Records*
- ARMA International — *Records and Information Management*
- NARA — General Records Schedules (GRS)
