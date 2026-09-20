"""
CLI interface for the skill system
"""

import argparse
import json
import logging
import sys
from .registry import SkillRegistry, SkillDomain
from .loader import SkillLoader
from .priority import PriorityManager
from .resolver import DependencyResolver


def main():
    parser = argparse.ArgumentParser(description="All Skills Management CLI")
    subparsers = parser.add_subparsers(dest='command', help='Commands')
    
    # List command
    list_parser = subparsers.add_parser('list', help='List skills')
    list_parser.add_argument('--domain', '-d', help='Filter by domain')
    list_parser.add_argument('--level', '-l', help='Filter by level')
    list_parser.add_argument('--tag', '-t', help='Filter by tag')
    list_parser.add_argument('--format', choices=['text', 'json'], default='text')
    
    # Search command
    search_parser = subparsers.add_parser('search', help='Search skills')
    search_parser.add_argument('query', help='Search query')
    
    # Info command
    info_parser = subparsers.add_parser('info', help='Skill details')
    info_parser.add_argument('skill', help='Skill name')
    
    # Load command
    load_parser = subparsers.add_parser('load', help='Load skills')
    load_parser.add_argument('--all', action='store_true', help='Load all')
    load_parser.add_argument('--domain', '-d', help='Load by domain')
    load_parser.add_argument('--skill', '-s', help='Load specific skill')
    
    # Stats command
    subparsers.add_parser('stats', help='Show statistics')
    
    # Deps command
    deps_parser = subparsers.add_parser('deps', help='Show dependencies')
    deps_parser.add_argument('skill', help='Skill name')
    deps_parser.add_argument('--tree', action='store_true', help='Show tree')
    deps_parser.add_argument('--reverse', action='store_true', help='Reverse deps')
    
    # Validate command
    subparsers.add_parser('validate', help='Validate all dependencies')
    
    # Export command
    export_parser = subparsers.add_parser('export', help='Export catalog')
    export_parser.add_argument('--output', '-o', default='catalog.json')
    
    args = parser.parse_args()
    
    logging.basicConfig(level=logging.INFO)
    loader = SkillLoader()
    loader.register_all_default_skills()
    registry = loader.registry
    resolver = DependencyResolver(registry)
    
    if args.command == 'list':
        skills = registry.get_all()
        if args.domain:
            try:
                domain = SkillDomain(args.domain)
                skills = registry.get_by_domain(domain)
            except ValueError:
                print(f"Unknown domain: {args.domain}")
                return
        if args.tag:
            skills = [s for s in skills if args.tag in s.tags]
        
        if args.format == 'json':
            print(json.dumps([{
                'name': s.name,
                'domain': s.domain.value,
                'level': s.level.name,
                'priority': s.priority,
            } for s in skills], indent=2))
        else:
            for s in sorted(skills, key=lambda x: (x.domain.value, x.priority)):
                print(f"  [{s.level.name:15}] {s.name:40} ({s.domain.value})")
    
    elif args.command == 'search':
        results = registry.search(args.query)
        for s in results:
            print(f"  {s.name:40} - {s.description[:60]}...")
    
    elif args.command == 'info':
        skill = registry.get(args.skill)
        if skill:
            print(f"Name:         {skill.name}")
            print(f"Domain:       {skill.domain.value}")
            print(f"Level:        {skill.level.name}")
            print(f"Priority:     {skill.priority}")
            print(f"Description:  {skill.description}")
            print(f"Dependencies: {', '.join(skill.dependencies) or 'None'}")
            print(f"Tags:         {', '.join(skill.tags)}")
            print(f"Repos:        {', '.join(skill.repos) or 'None'}")
            print(f"Loaded:       {skill.loaded}")
        else:
            print(f"Skill '{args.skill}' not found")
    
    elif args.command == 'load':
        if args.all:
            results = loader.load_all()
            print(f"Loaded {sum(1 for v in results.values() if v)} / {len(results)} skills.")
        elif args.domain:
            try:
                domain = SkillDomain(args.domain)
                results = loader.load_domain(domain)
                print(f"Loaded domain {domain.value}: {sum(1 for v in results.values() if v)} skills.")
            except ValueError:
                print(f"Unknown domain: {args.domain}")
        elif args.skill:
            success = loader.load_skill(args.skill)
            print(f"Load '{args.skill}': {'SUCCESS' if success else 'FAILED'}")
        else:
            print("Specify --all, --domain <domain>, or --skill <name>")
    
    elif args.command == 'stats':
        stats = registry.stats()
        print(f"\nTotal Skills: {stats['total_skills']}")
        print(f"\nBy Domain:")
        for domain, count in sorted(stats['domains'].items()):
            if count > 0:
                print(f"  {domain:30} {count}")
        print(f"\nBy Level:")
        for level, count in stats['levels'].items():
            if count > 0:
                print(f"  {level:20} {count}")
    
    elif args.command == 'deps':
        if args.tree:
            tree = resolver.get_dependency_tree(args.skill)
            print(json.dumps(tree, indent=2))
        elif args.reverse:
            deps = resolver.get_reverse_dependencies(args.skill)
            print(f"Skills that depend on '{args.skill}':")
            for d in deps:
                print(f"  - {d}")
        else:
            deps = resolver.resolve(args.skill)
            print(f"Load order for '{args.skill}':")
            for i, d in enumerate(deps, 1):
                print(f"  {i}. {d}")
    
    elif args.command == 'validate':
        pm = PriorityManager(registry)
        missing = pm.validate_dependencies()
        cycles = resolver.find_cycles()
        
        if missing:
            print("Missing dependencies:")
            for skill, dep in missing:
                print(f"  {skill} -> {dep} (MISSING)")
        else:
            print("✓ All dependencies satisfied")
        
        if cycles:
            print("\nCircular dependencies:")
            for cycle in cycles:
                print(f"  {' -> '.join(cycle)}")
        else:
            print("✓ No circular dependencies")
    
    elif args.command == 'export':
        catalog = registry.export_catalog()
        with open(args.output, 'w', encoding="utf-8") as f:
            json.dump(catalog, f, indent=2)
        print(f"Catalog exported to {args.output}")
    
    else:
        parser.print_help()


if __name__ == '__main__':
    main()
