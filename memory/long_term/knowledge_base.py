"""
Knowledge Base for Structured Entity and Fact Storage.
Stores relational entities, triples (subject, predicate, object), and domain facts.
"""

from typing import List, Dict, Any, Optional

class KnowledgeBase:
    def __init__(self):
        self.triples: List[Dict[str, str]] = []
        self.entities: Dict[str, Dict[str, Any]] = {}

    def add_fact(self, subject: str, predicate: str, obj: str):
        self.triples.append({
            "subject": subject.lower().strip(),
            "predicate": predicate.lower().strip(),
            "object": obj.strip()
        })

    def query(self, subject: Optional[str] = None, predicate: Optional[str] = None) -> List[Dict[str, str]]:
        results = self.triples
        if subject:
            s_clean = subject.lower().strip()
            results = [r for r in results if r["subject"] == s_clean]
        if predicate:
            p_clean = predicate.lower().strip()
            results = [r for r in results if r["predicate"] == p_clean]
        return list(results)

    def set_entity_property(self, entity: str, key: str, value: Any):
        e_key = entity.lower().strip()
        if e_key not in self.entities:
            self.entities[e_key] = {}
        self.entities[e_key][key] = value

    def get_entity(self, entity: str) -> Optional[Dict[str, Any]]:
        return self.entities.get(entity.lower().strip())
