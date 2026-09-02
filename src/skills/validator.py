"""Skill validation â€” checks SKILL.md, paths, conflicts, and basic safety."""
from __future__ import annotations

import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict, List, Set

from .lifecycle import is_valid as lifecycle_valid
from .registry import Registry, SkillEntry
from .security import scan_skill


@dataclass
class ValidationResult:
    ok: bool
    errors: List[str] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)
    info: List[str] = field(default_factory=list)

    def add_error(self, msg: str) -> None:
        self.errors.append(msg)
        self.ok = False

    def add_warning(self, msg: str) -> None:
        self.warnings.append(msg)

    def add_info(self, msg: str) -> None:
        self.info.append(msg)


REQUIRED_FRONTMATTER = {"name", "description", "category", "version"}
REQUIRED_SECTIONS = {
    "Purpose", "When to Use", "When NOT to Use", "Capabilities", "Inputs",
    "Workflow", "Tools", "Examples", "Safety", "Source", "Notes",
}


class Validator:
    def __init__(self, registry: Registry, skills_root: Path) -> None:
        self.registry = registry
        self.skills_root = skills_root

    def validate_all(self) -> ValidationResult:
        result = ValidationResult(ok=True)
        ids_seen: Set[str] = set()
        alias_map: Dict[str, List[str]] = {}
        for entry in self.registry.entries:
            self._validate_entry(entry, result)
            if entry.id in ids_seen:
                result.add_error(f"duplicate skill id: {entry.id}")
            ids_seen.add(entry.id)
            for alias in entry.aliases or []:
                alias_key = str(alias).strip().lower()
                if alias_key:
                    alias_map.setdefault(alias_key, []).append(entry.id)
        # Duplicate aliases across different skills confuse the router.
        for alias, ids in sorted(alias_map.items()):
            if len(set(ids)) > 1:
                result.add_warning(f"duplicate alias {alias!r} shared by: {', '.join(sorted(set(ids)))}")
        # Orphaned on-disk skills that are not registered.
        registered_paths = {entry.path.replace("/", "/") for entry in self.registry.entries}
        for skill_md in self.skills_root.rglob("SKILL.md"):
            if "_quarantine" in skill_md.parts:
                continue
            rel_dir = skill_md.relative_to(self.skills_root).parent.as_posix()
            if rel_dir not in registered_paths:
                result.add_warning(f"orphaned skill dir not in registry: {rel_dir}")
        # Circular composition chains (e.g. A -> B -> A).
        for cycle in self.detect_circular_chains():
            result.add_error(f"circular skill chain: {cycle}")
        # Declared conflicts (skills/conflicts.json).
        self._check_conflicts(result)
        return result

    def detect_circular_chains(self) -> List[str]:
        """Detect cycles formed by composes_with / suggests_after edges."""
        graph: Dict[str, List[str]] = {}
        for entry in self.registry.entries:
            targets = [
                t for t in entry.composes_with + entry.suggests_after
                if self.registry.get(t) is not None
            ]
            graph[entry.id] = targets
        cycles: List[str] = []
        visited: Set[str] = set()
        stack: List[str] = []

        def dfs(node: str) -> None:
            if node in stack:
                start = stack.index(node)
                cycles.append(" -> ".join(stack[start:] + [node]))
                return
            if node in visited:
                return
            stack.append(node)
            visited.add(node)
            for child in graph.get(node, []):
                dfs(child)
            stack.pop()

        for node in list(graph.keys()):
            dfs(node)
        return cycles

    def _check_conflicts(self, result: ValidationResult) -> None:
        from .conflicts import load_conflicts

        conflicts = load_conflicts(self.skills_root.parent)
        for conflict in conflicts.all():
            missing = [s for s in conflict.skills if self.registry.get(s) is None]
            if missing:
                result.add_error(
                    f"conflict references unknown skill(s): {', '.join(missing)}"
                )
                continue
            entries = [self.registry.get(s) for s in conflict.skills]
            if entries and all(e is not None and e.enabled for e in entries):
                msg = f"active conflict: {' + '.join(conflict.skills)} â€” {conflict.reason}"
                if conflict.severity == "error":
                    result.add_error(msg)
                elif conflict.severity == "warn":
                    result.add_warning(msg)
                else:
                    result.add_info(msg)

    def validate_one(self, skill_id: str) -> ValidationResult:
        result = ValidationResult(ok=True)
        entry = self.registry.get(skill_id)
        if not entry:
            result.add_error(f"skill not found: {skill_id}")
            return result
        self._validate_entry(entry, result)
        return result

    # ---- internals -------------------------------------------------------

    def _validate_entry(self, entry: SkillEntry, result: ValidationResult) -> None:
        # Path exists
        skill_dir = self.skills_root / Path(*entry.path.split("/"))
        if not skill_dir.exists():
            result.add_error(f"[{entry.id}] skill path does not exist: {skill_dir}")
            return
        skill_md = skill_dir / "SKILL.md"
        if not skill_md.exists():
            result.add_error(f"[{entry.id}] SKILL.md missing at {skill_md}")
            return
        try:
            text = skill_md.read_text(encoding="utf-8")
        except Exception as e:
            result.add_error(f"[{entry.id}] cannot read SKILL.md: {e}")
            return
        # Frontmatter sanity
        if not text.startswith("---"):
            result.add_error(f"[{entry.id}] SKILL.md is missing YAML frontmatter")
        else:
            from .frontmatter import parse_frontmatter
            meta, _ = parse_frontmatter(text)
            for k in REQUIRED_FRONTMATTER:
                if k not in meta or not meta[k]:
                    result.add_error(f"[{entry.id}] required frontmatter key missing or empty: {k}")
            if meta.get("name") != entry.name:
                result.add_error(f"[{entry.id}] frontmatter name does not match registry")
            if meta.get("category") != entry.category:
                result.add_error(f"[{entry.id}] frontmatter category does not match registry")
        headings = {m.group(1).strip().lower() for m in re.finditer(r"^##\s+(.+?)\s*$", text, re.MULTILINE)}
        for section in sorted(REQUIRED_SECTIONS):
            if section.lower() not in headings:
                result.add_error(f"[{entry.id}] required section missing: {section}")
        expected_path = f"{entry.category}/{entry.name}"
        if entry.path != expected_path:
            result.add_error(f"[{entry.id}] path must be {expected_path}, got {entry.path}")
        for target in entry.composes_with + entry.suggests_after:
            if not self.registry.get(target):
                result.add_error(f"[{entry.id}] composition target not found: {target}")
        # Lifecycle sanity.
        lifecycle = (entry.lifecycle or "enabled").strip().lower()
        if not lifecycle_valid(lifecycle):
            result.add_error(f"[{entry.id}] invalid lifecycle state: {lifecycle!r}")
        elif lifecycle in {"disabled", "quarantined", "deprecated"} and entry.enabled:
            result.add_warning(f"[{entry.id}] lifecycle is {lifecycle!r} but registry enabled=true")
        elif lifecycle == "enabled" and not entry.enabled:
            result.add_warning(f"[{entry.id}] lifecycle is 'enabled' but registry enabled=false")
        # Oversized SKILL.md hurts context loading.
        try:
            size = skill_md.stat().st_size
        except OSError:
            size = 0
        if size >= 200_000:
            result.add_error(f"[{entry.id}] SKILL.md too large: {size} bytes")
        elif size >= 100_000:
            result.add_warning(f"[{entry.id}] SKILL.md is large: {size} bytes")
        # Invalid routing rules (blank aliases/triggers/keywords).
        for field_name in ("aliases", "triggers", "keywords"):
            for value in getattr(entry, field_name, []) or []:
                if not str(value).strip():
                    result.add_error(f"[{entry.id}] empty {field_name} entry")
        # Duplicate alias within a single skill.
        seen_aliases: Set[str] = set()
        for alias in entry.aliases or []:
            a = str(alias).strip().lower()
            if a and a in seen_aliases:
                result.add_warning(f"[{entry.id}] duplicate alias within skill: {alias!r}")
            seen_aliases.add(a)
        # Static inspection only â€” third-party scripts are never executed.
        for finding in scan_skill(entry, skill_dir):
            message = f"[{entry.id}] {finding.path} contains suspicious pattern: {finding.label}"
            if finding.severity == "high":
                result.add_error(message)
            else:
                result.add_warning(message)
        if not (skill_dir / "README.md").exists():
            result.add_error(f"[{entry.id}] README.md missing")
        source_repository = meta.get("source_repository") if text.startswith("---") else None
        if source_repository:
            for key in ("source_path", "source_commit", "license", "original_author"):
                if not meta.get(key):
                    result.add_error(f"[{entry.id}] imported skill metadata missing: {key}")
            if not (skill_dir / "LICENSE").exists():
                result.add_error(f"[{entry.id}] imported skill LICENSE missing")
            if not (skill_dir / "references" / "upstream-SKILL.md").exists():
                result.add_error(f"[{entry.id}] upstream SKILL reference missing")
