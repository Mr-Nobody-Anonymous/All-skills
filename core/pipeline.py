"""
Processing Pipeline for All-Skills Platform.
Orchestrates end-to-end flow: input -> intent classification -> priority resolution -> skill execution -> output formatting.
"""

from typing import Dict, Any, Optional
from .intent_engine import IntentEngine
from .priority_resolver import PriorityResolver
from .skill_manager import SkillManager
from .context_manager import ContextManager
from .event_bus import EventBus
from .error_handler import ErrorHandler

class Pipeline:
    def __init__(self,
                 skill_manager: Optional[SkillManager] = None,
                 intent_engine: Optional[IntentEngine] = None,
                 priority_resolver: Optional[PriorityResolver] = None,
                 context_manager: Optional[ContextManager] = None,
                 event_bus: Optional[EventBus] = None,
                 error_handler: Optional[ErrorHandler] = None):
        self.skill_manager = skill_manager or SkillManager()
        self.intent_engine = intent_engine or IntentEngine()
        self.priority_resolver = priority_resolver or PriorityResolver()
        self.context_manager = context_manager or ContextManager()
        self.event_bus = event_bus or EventBus()
        self.error_handler = error_handler or ErrorHandler()

    def process(self, user_input: str, session_id: str = "default") -> Dict[str, Any]:
        """Runs the complete cognitive pipeline."""
        context = self.context_manager.get_context(session_id) or {}
        self.event_bus.publish("pipeline:input_received", {"text": user_input, "session_id": session_id})

        try:
            # 1. Intent classification
            intent_result = self.intent_engine.classify(user_input)
            self.event_bus.publish("pipeline:intent_classified", intent_result)

            # 2. Priority resolution
            candidates = [intent_result]
            selected = self.priority_resolver.resolve(candidates, context)
            if not selected:
                return {"status": "error", "message": "No suitable skill found."}

            skill_id = selected.get("skill_id")
            skill = self.skill_manager.get_skill(skill_id)

            # 3. Execution
            if skill and hasattr(skill, "handle"):
                result = skill.handle(intent_result, context)
            else:
                result = {
                    "text": f"Simulated execution for {skill_id}",
                    "intent": intent_result.get("intent")
                }

            # 4. Context update
            self.context_manager.update_context(session_id, {
                "last_input": user_input,
                "last_intent": intent_result.get("intent"),
                "last_skill": skill_id
            })

            output = {
                "status": "success",
                "result": result,
                "intent": intent_result.get("intent"),
                "skill_id": skill_id
            }
            self.event_bus.publish("pipeline:output_ready", output)
            return output

        except Exception as e:
            handled = self.error_handler.handle(e, {"input": user_input, "session": session_id})
            return {"status": "error", "error": str(e), "handled": handled}
