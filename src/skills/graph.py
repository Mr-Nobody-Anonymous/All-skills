"""Machine-readable skill dependency and semantic conflict graph.

Provides tree navigation, dependency resolution, reverse-dependent discovery,
and conflict detection across the skill platform.
"""

from __future__ import annotations

import json
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, List, Optional, Set


@dataclass
class SkillNode:
    id: str
    name: str
    category: str
    description: str = ""
    dependencies: List[str] = field(default_factory=list)
    conflicts: List[str] = field(default_factory=list)
    tags: List[str] = field(default_factory=list)


@dataclass
class ConflictEdge:
    skill_a: str
    skill_b: str
    reason: str
    severity: str = "warn"  # info | warn | error


# Standard domain dependency relationships connecting core agent skills
CORE_SKILL_RELATIONSHIPS: Dict[str, Dict[str, Any]] = {
    "nextjs": {
        "name": "Next.js Fullstack Platform",
        "category": "web-development",
        "deps": ["react", "typescript", "seo", "authentication", "database", "deployment"],
        "conflicts": ["vue", "angular"]
    },
    "react": {
        "name": "React Framework",
        "category": "web-development",
        "deps": ["typescript", "accessibility", "testing", "state-management", "performance"],
        "conflicts": ["angular-state-management"]
    },
    "react-state-management": {
        "name": "React State Management (Zustand/Redux/Jotai)",
        "category": "web-development",
        "deps": ["react", "typescript"],
        "conflicts": ["angular-state-management"]
    },
    "angular-state-management": {
        "name": "Angular State Management (Signals/NgRx)",
        "category": "web-development",
        "deps": ["typescript"],
        "conflicts": ["react-state-management", "react"]
    },
    "saas-mvp-launcher": {
        "name": "SaaS MVP Launcher Playbook",
        "category": "fullstack",
        "deps": ["api-designer", "database-design", "react-state-management", "wcag-audit-patterns", "secrets-management", "ci-cd-and-automation"],
        "conflicts": []
    },
    "ai-engineer": {
        "name": "AI Systems & RAG Engineer",
        "category": "ai-ml",
        "deps": ["ai-engineering-toolkit", "agent-memory", "multi-agent-patterns", "evaluation"],
        "conflicts": []
    },
    "multi-agent-architect": {
        "name": "Multi-Agent Architect",
        "category": "ai-ml",
        "deps": ["multi-agent-patterns", "dispatching-parallel-agents", "agent-memory-systems", "verification-before-completion"],
        "conflicts": []
    },
    "database-design": {
        "name": "Database Architecture & Schema Design",
        "category": "database",
        "deps": ["database-migration", "performance-profiling"],
        "conflicts": []
    },
    "prisma-expert": {
        "name": "Prisma ORM Expert",
        "category": "database",
        "deps": ["database-design", "database-migration", "typescript"],
        "conflicts": ["drizzle-orm-expert"]
    },
    "drizzle-orm-expert": {
        "name": "Drizzle ORM Expert",
        "category": "database",
        "deps": ["database-design", "database-migration", "typescript"],
        "conflicts": ["prisma-expert"]
    },
    "kubernetes-architect": {
        "name": "Kubernetes & Cloud Native Architect",
        "category": "cloud-devops",
        "deps": ["kubernetes-deployment", "terraform-infrastructure", "cloud-devops", "secrets-management"],
        "conflicts": []
    },
    "code-reviewer": {
        "name": "Elite Code Reviewer",
        "category": "development",
        "deps": ["ast-code-transformation", "security-scanning-security-sast", "top-web-vulnerabilities"],
        "conflicts": []
    },
    "wcag-audit-patterns": {
        "name": "WCAG 2.2 Accessibility Auditing",
        "category": "web-development",
        "deps": ["accessibility-compliance-accessibility-audit", "playwright-skill"],
        "conflicts": []
    },
    "productivity.focus": {
        "name": "Deep Work Focus Session",
        "category": "productivity",
        "deps": ["productivity.unlazy"],
        "conflicts": ["productivity.brainstorming"]
    },
    "productivity.brainstorming": {
        "name": "Divergent Ideation & Brainstorming",
        "category": "productivity",
        "deps": [],
        "conflicts": ["productivity.focus", "productivity.unlazy"]
    },
    "productivity.unlazy": {
        "name": "Procrastination Breaker",
        "category": "productivity",
        "deps": [],
        "conflicts": ["productivity.brainstorming"]
    },
    "safe-production-mode": {
        "name": "Safe Read-Only Production Guardrails",
        "category": "security",
        "deps": ["security-sandboxing-guardrails"],
        "conflicts": ["direct-production-deployment"]
    },
    "direct-production-deployment": {
        "name": "Direct Unattended Production Deployer",
        "category": "cloud-devops",
        "deps": ["cloud-devops"],
        "conflicts": ["safe-production-mode"]
    }
}


class SkillGraph:
    """Directed graph representing dependencies, reverse-dependencies, and conflicts."""

    def __init__(self, workspace_root: Optional[Path] = None) -> None:
        self.workspace_root = workspace_root or Path.cwd()
        self.nodes: Dict[str, SkillNode] = {}
        self.conflicts: List[ConflictEdge] = []
        self._load_and_build()

    def _normalize_id(self, skill_id: str) -> str:
        s = skill_id.strip().lower()
        alias_map = {
            "reactjs": "react",
            "next": "nextjs",
            "next.js": "nextjs",
            "accessibility": "wcag-audit-patterns",
            "a11y": "wcag-audit-patterns",
            "testing": "tdd",
            "state-management": "react-state-management",
            "performance": "performance-profiling",
            "seo": "seo-geo",
            "authentication": "marketplace-rbac-audit",
            "database": "database-design",
            "deployment": "cloud-devops",
            "typescript": "development.typescript",
            "evaluation": "agent-evaluation",
            "brainstorming": "productivity.brainstorming",
            "focus": "productivity.focus",
            "unlazy": "productivity.unlazy",
            "prisma": "prisma-expert",
            "drizzle": "drizzle-orm-expert",
            "k8s": "kubernetes-architect",
            "kubernetes": "kubernetes-architect",
        }
        return alias_map.get(s, s)

    def _load_and_build(self) -> None:
        # 1. Seed with curated core relationships
        for node_id, data in CORE_SKILL_RELATIONSHIPS.items():
            node = SkillNode(
                id=node_id,
                name=data.get("name", node_id),
                category=data.get("category", "general"),
                dependencies=data.get("deps", []),
                conflicts=data.get("conflicts", []),
                tags=[node_id] + data.get("deps", [])
            )
            self.nodes[node_id] = node

        # 2. Add declared pairwise conflicts from skills/conflicts.json
        conflicts_file = self.workspace_root / "skills" / "conflicts.json"
        if conflicts_file.exists():
            try:
                cdata = json.loads(conflicts_file.read_text(encoding="utf-8"))
                for c in cdata.get("conflicts", []):
                    skills = c.get("skills", [])
                    if len(skills) >= 2:
                        edge = ConflictEdge(
                            skill_a=skills[0],
                            skill_b=skills[1],
                            reason=c.get("reason", "Incompatible operational requirements"),
                            severity=c.get("severity", "warn")
                        )
                        self.conflicts.append(edge)
                        # Ensure nodes record conflict
                        for i, s1 in enumerate(skills):
                            for j, s2 in enumerate(skills):
                                if i != j:
                                    if s1 in self.nodes and s2 not in self.nodes[s1].conflicts:
                                        self.nodes[s1].conflicts.append(s2)
            except Exception:
                pass

        # 3. Add canonical skills from skills/registry.json
        registry_file = self.workspace_root / "skills" / "registry.json"
        if registry_file.exists():
            try:
                rdata = json.loads(registry_file.read_text(encoding="utf-8"))
                for s in rdata.get("skills", []):
                    sid = s.get("id")
                    if sid and sid not in self.nodes:
                        self.nodes[sid] = SkillNode(
                            id=sid,
                            name=s.get("name", sid),
                            category=s.get("category", "canonical"),
                            description=s.get("description", ""),
                            dependencies=s.get("dependencies", []),
                            conflicts=[],
                            tags=s.get("tags", [])
                        )
            except Exception:
                pass

        # 4. Add active harness skills from manifest.json
        manifest_file = self.workspace_root / "manifest.json"
        if manifest_file.exists():
            try:
                mdata = json.loads(manifest_file.read_text(encoding="utf-8"))
                for sid, sinfo in mdata.get("skills", {}).items():
                    if sid not in self.nodes:
                        self.nodes[sid] = SkillNode(
                            id=sid,
                            name=sid.replace("-", " ").title(),
                            category=sinfo.get("category", "active-harness"),
                            description=sinfo.get("description", ""),
                            dependencies=sinfo.get("dependencies", []),
                            conflicts=[],
                            tags=[]
                        )
            except Exception:
                pass

        # 5. Add catalog library skills from awesome_skills/skills_index.json
        index_file = self.workspace_root / "awesome_skills" / "skills_index.json"
        if index_file.exists():
            try:
                with open(index_file, "r", encoding="utf-8") as f:
                    idata = json.load(f)
                for item in idata:
                    sid = item.get("id")
                    if sid and sid not in self.nodes:
                        self.nodes[sid] = SkillNode(
                            id=sid,
                            name=item.get("name", sid),
                            category=item.get("category", "awesome"),
                            description=item.get("description", ""),
                            dependencies=item.get("dependencies", []),
                            conflicts=[],
                            tags=item.get("tags", [])
                        )
            except Exception:
                pass

        # Record explicit conflict edges from CORE_SKILL_RELATIONSHIPS
        for node_id, data in CORE_SKILL_RELATIONSHIPS.items():
            for conflict_id in data.get("conflicts", []):
                norm_c = self._normalize_id(conflict_id)
                self.conflicts.append(
                    ConflictEdge(
                        skill_a=node_id,
                        skill_b=norm_c,
                        reason=f"Semantic architectural conflict between {node_id} and {norm_c}.",
                        severity="warn"
                    )
                )

    def resolve_skill(self, skill_query: str) -> Optional[SkillNode]:
        norm = self._normalize_id(skill_query)
        if norm in self.nodes:
            return self.nodes[norm]
        for sid, node in self.nodes.items():
            if norm == sid or norm in sid or norm in node.name.lower():
                return node
        return None

    def get_dependencies(self, skill_id: str, recursive: bool = False, visited: Optional[Set[str]] = None) -> List[str]:
        node = self.resolve_skill(skill_id)
        if not node:
            return []
        if not recursive:
            return list(node.dependencies)

        if visited is None:
            visited = set()
        visited.add(node.id)

        deps: List[str] = []
        for dep_id in node.dependencies:
            norm_dep = self._normalize_id(dep_id)
            if norm_dep not in deps and norm_dep != node.id:
                deps.append(norm_dep)
            child_node = self.resolve_skill(dep_id)
            if child_node and child_node.id not in visited:
                child_deps = self.get_dependencies(child_node.id, recursive=True, visited=visited)
                for cd in child_deps:
                    if cd not in deps and cd != node.id:
                        deps.append(cd)
        return deps

    def get_dependents(self, skill_id: str) -> List[str]:
        target = self.resolve_skill(skill_id)
        target_id = target.id if target else self._normalize_id(skill_id)
        dependents: List[str] = []
        for sid, node in self.nodes.items():
            norm_deps = [self._normalize_id(d) for d in node.dependencies]
            if target_id in norm_deps or skill_id in norm_deps:
                if sid not in dependents and sid != target_id:
                    dependents.append(sid)
        return sorted(dependents)

    def get_conflicts(self, skill_id: str) -> List[dict]:
        target = self.resolve_skill(skill_id)
        target_id = target.id if target else self._normalize_id(skill_id)
        conflicts: List[dict] = []
        for edge in self.conflicts:
            other = None
            if self._normalize_id(edge.skill_a) == target_id:
                other = self._normalize_id(edge.skill_b)
            elif self._normalize_id(edge.skill_b) == target_id:
                other = self._normalize_id(edge.skill_a)
            if other:
                conflicts.append({
                    "conflicts_with": other,
                    "reason": edge.reason,
                    "severity": edge.severity
                })
        return conflicts

    def render_ascii_tree(self, skill_id: str, max_depth: int = 2) -> str:
        node = self.resolve_skill(skill_id)
        if not node:
            return f"Skill '{skill_id}' not found in platform graph."

        lines: List[str] = [f"{node.name} ({node.id})"]

        def _render_children(parent_node: SkillNode, prefix: str, current_depth: int) -> None:
            if current_depth > max_depth or not parent_node.dependencies:
                return
            deps = parent_node.dependencies
            for i, dep_id in enumerate(deps):
                is_last = (i == len(deps) - 1)
                connector = "└── " if is_last else "├── "
                child_prefix = "    " if is_last else "│   "
                child_node = self.resolve_skill(dep_id)
                child_label = f"{child_node.name} ({child_node.id})" if child_node else dep_id
                lines.append(f"{prefix}{connector}{child_label}")
                if child_node and current_depth + 1 <= max_depth:
                    _render_children(child_node, prefix + child_prefix, current_depth + 1)

        _render_children(node, "", 1)
        return "\n".join(lines)

    def export_graph_json(self) -> dict:
        nodes_dict = {}
        for sid, node in self.nodes.items():
            nodes_dict[sid] = {
                "id": node.id,
                "name": node.name,
                "category": node.category,
                "dependencies": node.dependencies,
                "conflicts": node.conflicts,
            }
        edges_list = []
        for sid, node in self.nodes.items():
            for dep in node.dependencies:
                edges_list.append({
                    "source": sid,
                    "target": self._normalize_id(dep),
                    "type": "requires"
                })
        conflicts_list = [
            {
                "skill_a": c.skill_a,
                "skill_b": c.skill_b,
                "reason": c.reason,
                "severity": c.severity
            }
            for c in self.conflicts
        ]
        return {
            "version": 1,
            "nodes_count": len(nodes_dict),
            "nodes": nodes_dict,
            "edges": edges_list,
            "conflicts": conflicts_list
        }


def save_dependency_graph(repo_root: Path) -> Path:
    graph = SkillGraph(repo_root)
    out_file = repo_root / "dependency_graph.json"
    with open(out_file, "w", encoding="utf-8") as f:
        json.dump(graph.export_graph_json(), f, indent=2)
        f.write("\n")
    return out_file
