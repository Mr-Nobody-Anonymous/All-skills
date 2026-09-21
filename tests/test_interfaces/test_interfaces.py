import unittest
from interfaces import TerminalInterface, VoiceInterface, WebInterface, RestApi, DesktopGui, ChatInterface
from core.pipeline import Pipeline

class TestInterfacesSubsystem(unittest.TestCase):
    def setUp(self):
        self.pipeline = Pipeline()

    def test_terminal_interface(self):
        term = TerminalInterface(self.pipeline)
        out = term.run_command("hello world")
        self.assertIsInstance(out, str)

    def test_voice_interface(self):
        voice = VoiceInterface(self.pipeline)
        wake = voice.on_wake_word_detected()
        self.assertIn("Awake", wake)
        res = voice.process_spoken_utterance("turn on lights")
        self.assertIn("spoken_text", res)

    def test_web_interface(self):
        web = WebInterface(self.pipeline)
        res = web.handle_http_request("GET", "/api/health")
        self.assertEqual(res["status"], "ok")

    def test_rest_api(self):
        api = RestApi(self.pipeline)
        res = api.route_request("/v1/skills/execute", {"prompt": "time query"})
        self.assertEqual(res.get("status"), "success")

    def test_desktop_gui(self):
        gui = DesktopGui(self.pipeline)
        self.assertIn("displayed", gui.show())

    def test_chat_interface(self):
        chat = ChatInterface(self.pipeline)
        res = chat.send_message("session_test", "hello")
        self.assertIn("reply", res)

if __name__ == "__main__":
    unittest.main()
