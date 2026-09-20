import unittest
from plugins.stt.plugin_stt_vosk import PluginVosk
from plugins.tts.plugin_tts_piper import PluginPiper

class TestPlugins(unittest.TestCase):
    def test_vosk_plugin(self):
        p = PluginVosk()
        res = p.execute()
        self.assertEqual(res["status"], "ok")

    def test_piper_plugin(self):
        p = PluginPiper()
        res = p.execute()
        self.assertEqual(res["status"], "ok")

if __name__ == "__main__":
    unittest.main()
