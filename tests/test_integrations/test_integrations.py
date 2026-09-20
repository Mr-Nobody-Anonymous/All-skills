import unittest
from integrations.home_assistant.ha_client import HomeAssistantClient
from integrations.openai.chatgpt import ChatGPTClient

class TestIntegrations(unittest.TestCase):
    def test_ha_client(self):
        client = HomeAssistantClient()
        state = client.get_state("light.living_room")
        self.assertEqual(state["entity_id"], "light.living_room")

    def test_chatgpt_client(self):
        client = ChatGPTClient()
        res = client.complete("Hello")
        self.assertIn("Hello", res)

if __name__ == "__main__":
    unittest.main()
