"""
Terminal and Command-Line Interface.
Interactive prompt allowing users to query skills, route natural language commands,
and view structured execution results in terminal.
"""

from typing import Optional
from core.pipeline import Pipeline

class TerminalInterface:
    def __init__(self, pipeline: Optional[Pipeline] = None):
        self.pipeline = pipeline or Pipeline()

    def run_command(self, query: str) -> str:
        res = self.pipeline.process(query)
        if res.get("status") == "success":
            result = res.get("result", {})
            return str(result.get("text") or result)
        return f"Error: {res.get('error', 'Execution failed')}"

    def process_command(self, query: str) -> dict:
        return self.pipeline.process(query)

    def repl(self):
        print("All-Skills Interactive Terminal (Type 'exit' to quit)")
        while True:
            try:
                cmd = input("skill-os> ").strip()
                if cmd.lower() in ("exit", "quit"):
                    break
                if cmd:
                    out = self.run_command(cmd)
                    print(out)
            except (KeyboardInterrupt, EOFError):
                break


if __name__ == "__main__":
    # Run from the repository root:  python -m interfaces.cli.terminal_interface
    TerminalInterface().repl()
