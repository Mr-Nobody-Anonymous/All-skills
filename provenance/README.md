# 📜 Provenance & Software Bill of Materials (`provenance/`)

Tracks cryptographic digests, upstream Git commit hashes, license clearances, and
third-party attribution notices for the skills shipped in this repository.

## Where the records actually live

| Artifact | Location | Contents |
| :--- | :--- | :--- |
| Provenance records | [`registry/provenance.json`](../registry/provenance.json) | Per-skill source, upstream commit, digest, license and clearance status for all 398 canonical skills |
| CycloneDX SBOM | [`registry/sbom.json`](../registry/sbom.json) | CycloneDX 1.5 component inventory generated from the registry |
| Catalog source map | [`catalog/provenance/sources.json`](../catalog/provenance/sources.json) | Upstream repository map for catalog (`awesome_skills/`) entries |
| Attribution notices | [`THIRD_PARTY_NOTICES.md`](../THIRD_PARTY_NOTICES.md) | Upstream contributors, repositories and SPDX license identifiers |
| Schema | [`schemas/provenance.schema.json`](../schemas/provenance.schema.json) | JSON Schema every provenance record must satisfy |

## Regenerating

```bash
python scripts/generate_quality_and_sbom.py   # rewrite registry/sbom.json (+ quality map)
python scripts/allskills.py doctor --full     # verify provenance covers every canonical skill
python scripts/allskills.py provenance <skill-id>   # inspect one skill's provenance record
```

Every record carries an SPDX license identifier. Full license texts are **not**
vendored into this repository; they are published by the upstream projects linked
from each record and from [`THIRD_PARTY_NOTICES.md`](../THIRD_PARTY_NOTICES.md),
which keeps the tree free of duplicated, hard-to-audit copies.
