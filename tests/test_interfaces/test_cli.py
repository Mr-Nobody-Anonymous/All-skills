import unittest
from interfaces.cli.terminal_interface import TerminalInterface

class TestCliInterface(unittest.TestCase):
    def test_cli_initialization(self):
        cli = TerminalInterface()
        self.assertIsNotNone(cli)

    def test_cli_process_input(self):
        cli = TerminalInterface()
        res = cli.process_command("hello world")
        self.assertIn("status", res)
        self.assertEqual(res["status"], "success")

if __name__ == "__main__":
    unittest.main()
