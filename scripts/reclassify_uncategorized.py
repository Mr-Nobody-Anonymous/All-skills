#!/usr/bin/env python3
"""Reclassify all 339 skills in awesome_skills/uncategorized into proper domain categories."""
from __future__ import annotations

import os
import re
import shutil
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
AWESOME_DIR = REPO_ROOT / "awesome_skills"
UNCAT_DIR = AWESOME_DIR / "uncategorized"


def classify_skill(skill_name: str, content: str) -> str:
    desc = ""
    m = re.search(r'description:\s*["\']?([^"\n\r]+)', content)
    if m:
        desc = m.group(1)

    s_lower = (skill_name + " " + desc).lower()

    if any(k in s_lower for k in ["finance", "accounting", "ledger", "tax", "money", "budget", "payment", "crypto", "defi", "stock", "invest", "revenue", "valuation"]):
        return "finance"
    if any(k in s_lower for k in ["legal", "law", "contract", "compliance", "patent", "regulatory", "gdpr", "hipaa", "terms"]):
        return "legal"
    if any(k in s_lower for k in ["health", "medical", "clinical", "patient", "doctor", "ehr", "hospital", "pharma", "wellness"]):
        return "health"
    if any(k in s_lower for k in ["hr", "recruiting", "employee", "onboarding", "payroll", "hiring", "people", "interview"]):
        return "hr-people"
    if any(k in s_lower for k in ["education", "learning", "curriculum", "teaching", "school", "student", "tutoring"]):
        return "education"
    if any(k in s_lower for k in ["security", "vulnerability", "attack", "cve", "exploit", "penetration", "reverse", "apk", "auth", "rbac", "sanitize"]):
        return "security"
    if any(k in s_lower for k in ["cloud", "aws", "azure", "gcp", "docker", "k8s", "kubernetes", "terraform", "infra", "deploy"]):
        return "cloud"
    if any(k in s_lower for k in ["test", "lint", "coverage", "qa", "audit", "benchmark", "accesslint"]):
        return "testing"
    if any(k in s_lower for k in ["market", "sales", "seo", "ad", "growth", "email", "copywriting", "crm"]):
        return "marketing"
    if any(k in s_lower for k in ["ai", "llm", "rag", "agent", "prompt", "model", "karpathy", "fine-tuning", "embedding"]):
        return "ai-ml"
    if any(k in s_lower for k in ["design", "ui", "ux", "css", "svg", "figma", "visual"]):
        return "design"
    if any(k in s_lower for k in ["mobile", "android", "ios", "react-native", "flutter"]):
        return "mobile"
    if any(k in s_lower for k in ["data", "sql", "database", "postgres", "analytics", "etl"]):
        return "data"
    return "development"


def main() -> None:
    if not UNCAT_DIR.exists():
        print("No uncategorized directory found.")
        return

    skills = [d for d in os.listdir(UNCAT_DIR) if (UNCAT_DIR / d).is_dir()]
    print(f"Reclassifying {len(skills)} skills from {UNCAT_DIR}...")

    counts: dict[str, int] = {}
    for skill_name in skills:
        src_path = UNCAT_DIR / skill_name
        md_file = src_path / "SKILL.md"
        content = ""
        if md_file.exists():
            content = md_file.read_text(encoding="utf-8", errors="ignore")

        target_cat = classify_skill(skill_name, content)
        dest_cat_dir = AWESOME_DIR / target_cat
        dest_cat_dir.mkdir(parents=True, exist_ok=True)
        dest_path = dest_cat_dir / skill_name

        if dest_path.exists():
            # If target already exists, merge/skip
            shutil.rmtree(src_path)
        else:
            shutil.move(str(src_path), str(dest_path))

        # Update category in SKILL.md if present
        dest_md = dest_path / "SKILL.md"
        if dest_md.exists():
            try:
                txt = dest_md.read_text(encoding="utf-8", errors="ignore")
                if "category:" in txt:
                    txt = re.sub(r'category:\s*[^\n\r]+', f'category: {target_cat}', txt)
                else:
                    # insert into frontmatter if frontmatter exists
                    if txt.startswith("---"):
                        txt = txt.replace("---", f"---\ncategory: {target_cat}", 1)
                dest_md.write_text(txt, encoding="utf-8")
            except Exception:
                pass

        counts[target_cat] = counts.get(target_cat, 0) + 1

    # Remove uncategorized folder if empty
    remaining = [d for d in os.listdir(UNCAT_DIR) if not d.startswith(".")]
    if not remaining:
        shutil.rmtree(UNCAT_DIR)
        print("Successfully removed empty uncategorized/ directory.")
    else:
        print(f"Warning: {len(remaining)} non-directory files remain in uncategorized/.")

    print("\nReclassification Summary:")
    for cat, cnt in sorted(counts.items(), key=lambda x: -x[1]):
        print(f"  {cat:<20}: {cnt} skills")


if __name__ == "__main__":
    main()
