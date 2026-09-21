import unittest
from memory import (
    ConversationBuffer,
    WorkingMemory,
    VectorStore,
    KnowledgeBase,
    UserProfiles,
    EventMemory
)

class TestMemorySubsystem(unittest.TestCase):
    def test_conversation_buffer(self):
        buf = ConversationBuffer(max_turns=3)
        buf.add_turn("user", "turn 1")
        buf.add_turn("bot", "turn 2")
        buf.add_turn("user", "turn 3")
        buf.add_turn("bot", "turn 4")
        self.assertEqual(len(buf.get_recent_history()), 3)
        self.assertEqual(buf.get_recent_history()[-1]["message"], "turn 4")

    def test_working_memory(self):
        wm = WorkingMemory()
        wm.set("active_task", "review_code")
        self.assertEqual(wm.get("active_task"), "review_code")
        self.assertIn("active_task", wm.snapshot())

    def test_vector_store(self):
        vs = VectorStore("test_collection")
        vs.add("play jazz music", {"domain": "music"})
        vs.add("turn off living room lights", {"domain": "home"})
        results = vs.search("jazz songs", top_k=1)
        self.assertEqual(len(results), 1)
        self.assertIn("jazz", results[0]["text"])

    def test_knowledge_base(self):
        kb = KnowledgeBase()
        kb.add_fact("Paris", "is_capital_of", "France")
        facts = kb.query(subject="Paris")
        self.assertEqual(len(facts), 1)
        self.assertEqual(facts[0]["object"], "France")

    def test_user_profiles(self):
        up = UserProfiles()
        up.set_preference("user_1", "theme", "dark")
        self.assertEqual(up.get_preference("user_1", "theme"), "dark")

    def test_event_memory(self):
        em = EventMemory()
        entry = em.record_event("alarm_triggered", "Morning alarm fired")
        self.assertIsNotNone(entry["id"])
        events = em.query_events("alarm_triggered")
        self.assertEqual(len(events), 1)

if __name__ == "__main__":
    unittest.main()
