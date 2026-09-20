#!/usr/bin/env python3
"""
Domain Loading Example: Isolate and load skills for a specific engineering domain
"""

from scratch_priority_import import SkillLoader, SkillDomain


def main():
    loader = SkillLoader()
    loader.register_all_default_skills()
    
    domain = SkillDomain.CYBERSECURITY
    print(f"Loading skills for domain: {domain.value}\n")
    
    results = loader.load_domain(domain)
    for skill_name, loaded in results.items():
        status = "SUCCESS" if loaded else "FAILED"
        print(f"  [{status}] {skill_name}")
        
    report = loader.get_load_report()
    print(f"\nTotal loading time: {report['total_load_time']:.4f}s")


if __name__ == "__main__":
    main()
