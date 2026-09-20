#!/usr/bin/env python3
"""
Basic Usage Example: All-Skills Priority Import & Registry
"""

from scratch_priority_import import SkillLoader, SkillRegistry, SkillDomain


def main():
    print("=== All-Skills Priority System Demo ===\n")
    
    # 1. Initialize loader and populate default catalog
    loader = SkillLoader()
    loader.register_all_default_skills()
    registry = loader.registry
    
    print(f"Total Registered Skills: {registry.count}")
    print("Domain Distribution:")
    for domain, count in sorted(registry.domain_counts.items()):
        if count > 0:
            print(f"  - {domain:25}: {count}")
    
    # 2. Search skills
    print("\n--- Search Query: 'docker' ---")
    results = registry.search("docker")
    for r in results:
        print(f"Found: {r.name} [{r.domain.value}] (Level: {r.level.name}) - {r.description}")
        
    # 3. Resolve single skill dependencies
    target = "web.fullstack"
    print(f"\n--- Dependency Resolution for '{target}' ---")
    load_order = loader.resolver.resolve(target)
    for idx, dep in enumerate(load_order, 1):
        print(f"  {idx}. {dep}")


if __name__ == "__main__":
    main()
