import unittest
from core.pipeline import Pipeline
from core.intent_engine import IntentEngine
from core.priority_resolver import PriorityResolver

class TestEndToEndPipeline(unittest.TestCase):
    def setUp(self):
        self.pipeline = Pipeline()

    def test_pipeline_text_flow(self):
        result = self.pipeline.process("help me with my calendar")
        self.assertIsNotNone(result)
        self.assertIn("status", result)

    def test_pipeline_fallback_flow(self):
        result = self.pipeline.process("an unknown obscure query 12345")
        self.assertIsNotNone(result)

if __name__ == "__main__":
    unittest.main()
