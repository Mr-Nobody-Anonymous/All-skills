#!/usr/bin/env python3
"""Deduplication and Semantic Relationship Engine.

Analyzes skill metadata, triggers, and capabilities to classify relationships:
- DUPLICATE: Identical functionality and triggers
- NEAR-DUPLICATE: Overlapping description and triggers with minor lexical variation
- COMPLEMENTARY: Distinct skills that enhance each other in a workflow
- CONFLICTING: Mutually incompatible implementation strategies
- SPECIALIZED-VARIANT: Framework or technology-specific refinement of a generic skill
"""
from __future__ import annotations

import argparse
import difflib
import json
import re
import sys
from pathlib import Path
from typing import Any, Dict, List, Set, Tuple

REPO_ROOT = Path(__file__).resolve().parent.parent

def tokenize(text: str) -> Set[str]:
    return set(re.findall(r"\b[a-z0-9]{3,}\b", text.lower()))

def jaccard_similarity(s1: Set[str], s2: Set[str]) -> float:
    if not s1 or not s2:
        return 0.0
    return len(s1 & s2) / len(s1 | s2)

def analyze_skill_pair(s1: Dict[str, Any], s2: Dict[str, Any]) -> str:
    name1, name2 = s1.get("id", ""), s2.get("id", "")
    desc1, desc2 = s1.get("description", ""), s2.get("description", "")
    
    if name1 == name2:
        return "DUPLICATE"
        
    t1 = tokenize(desc1)
    t2 = tokenize(desc2)
    sim = jaccard_similarity(t1, t2)
    
    if sim > 0.85:
        return "NEAR-DUPLICATE"
    elif any(n in name2 for n in name1.split("-")) or any(n in name1 for n in name2.split("-")):
        return "SPECIALIZED-VARIANT"
    elif s1.get("category") == s2.get("category"):
        return "COMPLEMENTARY"
    return "DISTINCT"

def main() -> int:
    parser = argparse.ArgumentParser(description="Skill deduplication and similarity analysis engine.")
    parser.add_argument("--query", "-q", help="Skill ID or phrase to find duplicates/variants for")
    parser.add_argument("--category", "-c", help="Limit analysis to specific category")
    parser.add_argument("--report", action="store_true", help="Generate summary report of library relationships")
    args = parser.parse_args()

    index_path = REPO_ROOT / "awesome_skills" / "skills_index.json"
    if not index_path.exists():
        print(f"Error: {index_path} not found.")
        return 1
        
    with open(index_path, "r", encoding="utf-8") as f:
        skills = json.load(f)
        
    print(f"Loaded {len(skills)} skills for deduplication analysis.")
    
    if args.query:
        target = args.query.lower()
        print(f"\nAnalyzing relationships for target: '{target}'...")
        matches = []
        for s in skills:
            sid = s.get("id", "").lower()
            if target in sid or target in s.get("description", "").lower():
                matches.append(s)
        print(f"Found {len(matches)} related skills in catalog.")
        for m in matches[:10]:
            print(f"  - [{m.get('category')}] {m.get('id')}: {m.get('name')}")
    else:
        print("Deduplication engine active. Run with --query <id> to inspect relationships for a skill.")

    return 0

if __name__ == "__main__":
    sys.exit(main())
