#!/usr/bin/env python3
"""
Learning Path Generator: Generate progressive curriculum from fundamentals to specialized skills
"""

from scratch_priority_import import SkillLoader


def generate_curriculum(target_skills):
    loader = SkillLoader()
    loader.register_all_default_skills()
    
    # Resolve full dependency closure
    ordered_skills = loader.resolver.resolve_multiple(target_skills)
    
    print("=========================================================")
    print("       PROGRESSIVE AGENT / DEVELOPER CURRICULUM          ")
    print("=========================================================\n")
    
    for step, skill_name in enumerate(ordered_skills, 1):
        skill = loader.registry.get(skill_name)
        if skill:
            print(f"Step {step:02d}: [{skill.level.name:12}] {skill.name:25} ({skill.domain.value})")
            print(f"         Description: {skill.description}")
            if skill.repos:
                print(f"         Primary Ref: {skill.repos[0]}")
            print()


if __name__ == "__main__":
    # Example: Goal is to become an expert AI Agent Engineer
    goals = ["ai.agents", "ai.mlops", "devops.kubernetes"]
    generate_curriculum(goals)
