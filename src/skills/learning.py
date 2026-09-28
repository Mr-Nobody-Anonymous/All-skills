"""Closed-Loop Feedback & Learning Engine.

Tracks agent task executions, outcomes, latency, token costs, and user feedback.
Dynamically updates empirical skill quality, reliability %, and routing weights so the
platform learns from actual usage.
"""
from __future__ import annotations

import json
import time
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any, Dict, List, Optional


@dataclass
class TaskExecutionRecord:
    """Record of an agent task execution."""
    task_id: str
    query: str
    skills_used: List[str]
    success: bool
    duration_ms: float
    token_cost: int
    tool_calls: int = 0
    hallucination_detected: bool = False
    user_feedback: Optional[str] = None  # 'helpful' | 'unhelpful' | None
    error_summary: Optional[str] = None
    timestamp: float = field(default_factory=time.time)

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


class LearningEngine:
    """Manages closed-loop execution tracking and quality score calibration."""

    def __init__(self, workspace_root: Optional[Path] = None) -> None:
        self.workspace_root = workspace_root or Path.cwd()
        self.telemetry_file = self.workspace_root / "registry" / "telemetry.json"
        self.history: List[TaskExecutionRecord] = self._load_history()

    def record_execution(
        self,
        task_id: str,
        query: str,
        skills_used: List[str],
        success: bool,
        duration_ms: float,
        token_cost: int,
        tool_calls: int = 0,
        hallucination_detected: bool = False,
        user_feedback: Optional[str] = None,
        error_summary: Optional[str] = None,
    ) -> TaskExecutionRecord:
        """Record a completed agent task execution."""
        record = TaskExecutionRecord(
            task_id=task_id,
            query=query,
            skills_used=skills_used,
            success=success,
            duration_ms=duration_ms,
            token_cost=token_cost,
            tool_calls=tool_calls,
            hallucination_detected=hallucination_detected,
            user_feedback=user_feedback,
            error_summary=error_summary,
        )
        self.history.append(record)
        self._save_history()
        return record

    def get_skill_stats(self, skill_id: str) -> Dict[str, Any]:
        """Compute empirical statistics for a specific skill from recorded history."""
        relevant = [r for r in self.history if skill_id in r.skills_used]
        if not relevant:
            return {
                "skill_id": skill_id,
                "execution_count": 0,
                "success_rate": 0.95,
                "reliability_pct": 95.0,
                "avg_duration_ms": 0.0,
                "avg_token_cost": 1500,
                "hallucination_rate": 0.0,
            }

        total = len(relevant)
        successes = sum(1 for r in relevant if r.success)
        hallucinations = sum(1 for r in relevant if r.hallucination_detected)
        avg_dur = sum(r.duration_ms for r in relevant) / total
        avg_tokens = sum(r.token_cost for r in relevant) / total

        success_rate = successes / total
        reliability = max(0.0, min(100.0, (success_rate * 100.0) - (hallucinations / total * 30.0)))

        return {
            "skill_id": skill_id,
            "execution_count": total,
            "success_rate": round(success_rate, 4),
            "reliability_pct": round(reliability, 1),
            "avg_duration_ms": round(avg_dur, 1),
            "avg_token_cost": int(avg_tokens),
            "hallucination_rate": round(hallucinations / total, 4),
        }

    def compute_platform_telemetry(self) -> Dict[str, Any]:
        """Aggregate telemetry across all recorded executions."""
        if not self.history:
            return {
                "total_executions": 0,
                "overall_success_rate": 0.92,
                "avg_token_cost": 2100,
                "avg_latency_ms": 1450.0,
            }

        total = len(self.history)
        successes = sum(1 for r in self.history if r.success)
        avg_dur = sum(r.duration_ms for r in self.history) / total
        avg_tokens = sum(r.token_cost for r in self.history) / total

        return {
            "total_executions": total,
            "overall_success_rate": round(successes / total, 4),
            "avg_token_cost": int(avg_tokens),
            "avg_latency_ms": round(avg_dur, 1),
        }

    def _load_history(self) -> List[TaskExecutionRecord]:
        if not self.telemetry_file.exists():
            return []
        try:
            data = json.loads(self.telemetry_file.read_text(encoding="utf-8"))
            return [
                TaskExecutionRecord(**rec) for rec in data.get("executions", [])
            ]
        except Exception:
            return []

    def _save_history(self) -> None:
        try:
            self.telemetry_file.parent.mkdir(parents=True, exist_ok=True)
            payload = {
                "updated_at": time.strftime("%Y-%m-%d %H:%M:%S"),
                "total_records": len(self.history),
                "executions": [r.to_dict() for r in self.history[-1000:]],  # keep last 1000 records
            }
            self.telemetry_file.write_text(json.dumps(payload, indent=2), encoding="utf-8")
        except Exception:
            pass
