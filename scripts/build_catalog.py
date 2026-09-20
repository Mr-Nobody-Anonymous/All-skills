#!/usr/bin/env python3
"""Build and synchronize awesome_skills/skills_index.json and awesome_skills/CATALOG.md."""
from __future__ import annotations

import json
import os
import re
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
AWESOME_DIR = REPO_ROOT / "awesome_skills"


def extract_skill_metadata(skill_dir: Path, cat_name: str) -> dict:
    skill_id = skill_dir.name
    md_file = skill_dir / "SKILL.md"
    name = skill_id
    desc = f"Specialized instructions for {skill_id.replace('-', ' ')}."
    risk = "low"
    version = "1.0.0"
    source = "community"
    license_type = "MIT"

    if md_file.exists():
        try:
            with open(md_file, "r", encoding="utf-8", errors="ignore") as f:
                content = f.read(1500)
            if content.startswith("---"):
                parts = content.split("---", 2)
                if len(parts) >= 3:
                    for line in parts[1].splitlines():
                        l = line.strip()
                        if l.startswith("name:") and name == skill_id:
                            name = l.split(":", 1)[1].strip().strip('"\'')
                        elif l.startswith("description:") and desc.startswith("Specialized instructions"):
                            raw_d = l.split(":", 1)[1].strip().strip('"\'')
                            if len(raw_d) >= 5:
                                desc = raw_d
                        elif l.startswith("risk:"):
                            risk = l.split(":", 1)[1].strip().strip('"\'')
                        elif l.startswith("version:"):
                            version = l.split(":", 1)[1].strip().strip('"\'')
                        elif l.startswith("source:"):
                            source = l.split(":", 1)[1].strip().strip('"\'')
                        elif l.startswith("license:"):
                            license_type = l.split(":", 1)[1].strip().strip('"\'')
        except Exception:
            pass

    return {
        "id": skill_id,
        "name": name,
        "category": cat_name,
        "description": desc,
        "risk": risk,
        "version": version,
        "source": source,
        "license": license_type,
        "path": f"awesome_skills/{cat_name}/{skill_id}/SKILL.md"
    }


def build_catalog() -> tuple[Path, Path, int]:
    cats = sorted([
        d for d in os.listdir(AWESOME_DIR)
        if (AWESOME_DIR / d).is_dir() and not d.startswith(".") and d not in ("node_modules", ".git")
    ])

    from concurrent.futures import ThreadPoolExecutor

    def process_category(cat: str) -> tuple[str, list[dict]]:
        cat_path = AWESOME_DIR / cat
        cat_skills = []
        try:
            for s in sorted(os.listdir(cat_path)):
                sdir = cat_path / s
                if sdir.is_dir() and not s.startswith("."):
                    meta = extract_skill_metadata(sdir, cat)
                    cat_skills.append(meta)
        except Exception:
            pass
        return cat, cat_skills

    with ThreadPoolExecutor(max_workers=16) as executor:
        results = list(executor.map(process_category, cats))

    skills_index: list[dict] = []
    category_map: dict[str, list[dict]] = {}

    for cat, cat_skills in results:
        category_map[cat] = cat_skills
        skills_index.extend(cat_skills)

    # 1. Save skills_index.json
    index_path = AWESOME_DIR / "skills_index.json"
    with open(index_path, "w", encoding="utf-8") as f:
        json.dump(skills_index, f, indent=2, ensure_ascii=False)
        f.write("\n")

    # 2. Build CATALOG.md
    total_skills = len(skills_index)
    lines = [
        "# 📚 Awesome Skills Catalog\n",
        f"Complete categorized index of **{total_skills:,} Agent Skills** across **{len(cats)} domain categories**.\n",
        "Every skill contains a standardized, load-on-demand `SKILL.md` instruction playbook with YAML frontmatter, compatible across Claude Code, Cursor, Codex CLI, Antigravity, and Gemini CLI.\n",
        "## 🧭 Categories Index\n"
    ]

    for cat in cats:
        count = len(category_map[cat])
        display_name = cat.replace("-", " ").title()
        lines.append(f"- [{display_name}](#{cat}) ({count} skills)")

    lines.append(f"\n*Total skills indexed: {total_skills:,} across {len(cats)} categories*\n")
    lines.append("---\n")

    for cat in cats:
        skills = category_map[cat]
        display_name = cat.replace("-", " ").title()
        lines.append(f"## <a id=\"{cat}\"></a>📁 {display_name} ({len(skills)} skills)\n")
        lines.append("| Skill ID | Name | Risk | Description |")
        lines.append("| :--- | :--- | :---: | :--- |")
        for s in skills:
            sid = s["id"]
            name = s["name"]
            risk = s["risk"]
            desc = s["description"].replace("\n", " ").strip()
            if len(desc) > 130:
                desc = desc[:127] + "..."
            desc = desc.replace("|", "\\|")
            rel_link = f"[{sid}]({cat}/{sid}/SKILL.md)"
            lines.append(f"| {rel_link} | `{name}` | `{risk}` | {desc} |")
        lines.append("\n---\n")

    catalog_path = AWESOME_DIR / "CATALOG.md"
    catalog_path.write_text("\n".join(lines), encoding="utf-8")

    return index_path, catalog_path, total_skills


def main() -> None:
    print("Building awesome_skills/skills_index.json and CATALOG.md...")
    index_path, catalog_path, total = build_catalog()
    print(f"Successfully generated {index_path} ({total:,} items)")
    print(f"Successfully generated {catalog_path} ({total:,} skills cataloged)")


if __name__ == "__main__":
    main()
