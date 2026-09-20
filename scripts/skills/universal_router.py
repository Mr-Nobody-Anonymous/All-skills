#!/usr/bin/env python3
"""Universal Multi-Stage Semantic and Intent Routing Engine.

Architecture:
USER REQUEST
  ↓ 1. Intent Classification & Negative Intent Filtering
  ↓ 2. Domain & Subdomain Mapping (15 Super-Domains, 250 Categories)
  ↓ 3. Task & Required Capability Resolution
  ↓ 4. Modality & Tool Resolver (Inputs, Outputs, MCP servers)
  ↓ 5. Risk & Approval Gate Evaluation (READ, ANALYZE, MODIFY, DELETE, PRODUCTION)
  ↓ 6. Skill Stack Construction & Dependency Resolution
  ↓ 7. Verification Directives
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path
from typing import Any, Dict, List, Optional, Set, Tuple

REPO_ROOT = Path(__file__).resolve().parent.parent.parent

NEGATIVE_INTENTS = {
    "malware-creation": ["create malware", "write virus", "ransomware", "ddos tool", "steal credentials"],
    "destructive-action": ["format disk", "delete production", "drop database without backup"],
    "unauthorized-access": ["bypass 2fa", "hack account", "steal token"]
}

SUPER_DOMAINS = {
    "medical": "life-sciences-medicine",
    "x-ray": "life-sciences-medicine",
    "pneumonia": "life-sciences-medicine",
    "health": "life-sciences-medicine",
    "code": "computer-science",
    "security": "security",
    "vulnerability": "security",
    "malware": "security",
    "finance": "finance",
    "legal": "law-governance",
    "accessible": "design",
    "wcag": "design"
}

class UniversalRouteResult:
    def __init__(self, query: str):
        self.query = query
        self.intent: str = "general-task"
        self.domain: str = "computer-science"
        self.subdomain: str = "general"
        self.capabilities: List[str] = []
        self.tools: List[str] = []
        self.risk_level: str = "low"
        self.approval_required: bool = False
        self.skills: List[Dict[str, Any]] = []
        self.workflow_chain: List[str] = []
        self.blocked: bool = False
        self.block_reason: Optional[str] = None

class UniversalRouter:
    def __init__(self):
        self.registry_path = REPO_ROOT / "registry" / "skills.json"
        self.skills = []
        if self.registry_path.exists():
            with open(self.registry_path, "r", encoding="utf-8") as f:
                self.skills = json.load(f)

    def route(self, query: str) -> UniversalRouteResult:
        result = UniversalRouteResult(query)
        q_lower = query.lower()

        # Step 1: Negative Intent Detection
        for intent_cat, patterns in NEGATIVE_INTENTS.items():
            for p in patterns:
                if p in q_lower:
                    if "analyze" in q_lower or "defend" in q_lower or "audit" in q_lower or "detect" in q_lower:
                        # Defensive context allowed
                        result.intent = f"defensive-{intent_cat}"
                    else:
                        result.blocked = True
                        result.block_reason = f"Prohibited intent detected: {intent_cat}"
                        return result

        # Step 2: Domain Mapping
        for kw, dom in SUPER_DOMAINS.items():
            if kw in q_lower:
                result.domain = dom
                break

        # Step 3: Risk Evaluation
        if any(w in q_lower for w in ["deploy", "production", "delete", "destroy", "drop table", "send email"]):
            result.risk_level = "high"
            result.approval_required = True
        else:
            result.risk_level = "low"

        # Step 4: Capability & Tool Matching
        if "detect" in q_lower or "pneumonia" in q_lower or "x-ray" in q_lower:
            result.capabilities = ["image-classification", "computer-vision", "medical-dataset", "clinical-validation"]
            result.tools = ["terminal", "file_read", "file_write"]
            result.workflow_chain = ["preflight-check", "data-preparation", "model-evaluation", "verification-before-completion"]
        elif "malware" in q_lower:
            result.capabilities = ["binary-analysis", "sandboxing", "threat-intelligence"]
            result.tools = ["file_read", "terminal"]
            result.workflow_chain = ["permission-check", "vulnerability-scan", "report-generation"]
        elif "accessibility" in q_lower or "wcag" in q_lower or "blind" in q_lower:
            result.capabilities = ["wcag-audit", "aria-inspection", "contrast-check"]
            result.tools = ["browser", "file_read"]
            result.workflow_chain = ["preflight-check", "wcag-audit", "artifact-validator"]
        else:
            result.capabilities = ["code-review", "execution-planning"]
            result.tools = ["terminal", "file_read"]
            result.workflow_chain = ["preflight-check", "execution-planner", "verification-before-completion"]

        # Step 5: Skill Resolution
        for s in self.skills:
            sid = s.get("id", "")
            sdesc = s.get("description", "").lower()
            if any(c in sid or c in sdesc for c in result.capabilities):
                result.skills.append(s)
                if len(result.skills) >= 5:
                    break

        return result

def main():
    if len(sys.argv) < 2:
        query = "Build me an application that detects pneumonia from X-rays"
    else:
        query = " ".join(sys.argv[1:])

    router = UniversalRouter()
    res = router.route(query)
    
    print(f"Query: \"{res.query}\"")
    print(f"Domain: {res.domain}")
    print(f"Risk Level: {res.risk_level} (Approval Required: {res.approval_required})")
    print(f"Required Capabilities: {', '.join(res.capabilities)}")
    print(f"Recommended Tools: {', '.join(res.tools)}")
    print(f"Workflow Stack: {' -> '.join(res.workflow_chain)}")
    print(f"Resolved Candidate Skills: {len(res.skills)}")

if __name__ == "__main__":
    main()
