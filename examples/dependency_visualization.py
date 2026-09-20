#!/usr/bin/env python3
"""
Dependency Visualization Example: Render nested ASCII trees for complex capabilities
"""

import json
from scratch_priority_import import SkillLoader
from scratch_priority_import.utils import render_ascii_tree


def main():
    loader = SkillLoader()
    loader.register_all_default_skills()
    
    target = "blockchain.defi"
    print(f"=== Dependency Tree for '{target}' ===\n")
    
    tree = loader.resolver.get_dependency_tree(target)
    print(render_ascii_tree(tree))
    
    print("\nJSON Tree Representation:")
    print(json.dumps(tree, indent=2))


if __name__ == "__main__":
    main()
