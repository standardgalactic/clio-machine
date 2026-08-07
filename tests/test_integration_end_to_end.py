import json
import os
import subprocess
import tempfile
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
SPHEREPOP = REPO_ROOT / "bin" / "spherepop"
FORTH = REPO_ROOT / "bin" / "forth"


class IntegrationEndToEndTests(unittest.TestCase):
    def test_spherepop_cli_persistence_trace_and_jsonl(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            state_path = Path(tmpdir) / "spherepop_history.json"
            env = os.environ.copy()
            env["PYTHONPATH"] = str(REPO_ROOT)
            env["SPHEREPOP_STATE_PATH"] = str(state_path)

            for args in (
                ("pop", "5"),
                ("pop", "8"),
                ("bind", "0", "1"),
                ("refuse", "0", "--reason", "consumed"),
                ("collapse", "2", "1"),
            ):
                subprocess.run([str(SPHEREPOP), *args], check=True, env=env, cwd=REPO_ROOT)

            trace = subprocess.run(
                [str(SPHEREPOP), "trace"],
                check=True,
                env=env,
                cwd=REPO_ROOT,
                capture_output=True,
                text=True,
            ).stdout
            jsonl = subprocess.run(
                [str(SPHEREPOP), "jsonl"],
                check=True,
                env=env,
                cwd=REPO_ROOT,
                capture_output=True,
                text=True,
            ).stdout

            payload = json.loads(state_path.read_text(encoding="utf-8"))
            self.assertEqual(len(payload["events"]), 5)
            self.assertEqual(payload["events"][3]["op"], "REFUSE")
            self.assertEqual(payload["events"][3]["parents"], [0])
            self.assertEqual(payload["events"][4]["op"], "COLLAPSE")
            self.assertEqual(payload["events"][4]["parents"], [2, 1])
            self.assertEqual(payload["frontier"], [3, 4])
            self.assertIn("frontier=[3, 4]", trace)
            self.assertIn("0003 REFUSE", trace)
            self.assertIn("0004 COLLAPSE", trace)

            jsonl_rows = [json.loads(row) for row in jsonl.strip().splitlines()]
            self.assertEqual(len(jsonl_rows), 5)
            self.assertEqual(jsonl_rows[3]["op"], "REFUSE")
            self.assertEqual(jsonl_rows[4]["parents"], [2, 1])

    def test_forth_execution_emits_consistent_event_history(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            state_path = Path(tmpdir) / "forth_history.json"
            env = os.environ.copy()
            env["PYTHONPATH"] = str(REPO_ROOT)

            output = subprocess.run(
                [str(FORTH), "--state-path", str(state_path), "--show-trace", "2", "3", "+", "."],
                check=True,
                env=env,
                cwd=REPO_ROOT,
                capture_output=True,
                text=True,
            ).stdout

            payload = json.loads(state_path.read_text(encoding="utf-8"))
            ops = [event["op"] for event in payload["events"]]
            self.assertEqual(ops, ["POP", "POP", "BIND", "COLLAPSE", "REFUSE", "COLLAPSE"])
            self.assertEqual(payload["events"][2]["parents"], [0, 1])
            self.assertEqual(payload["events"][3]["parents"], [2, 0, 1])
            self.assertEqual(payload["events"][4]["parents"], [3])
            self.assertEqual(payload["events"][5]["parents"], [3])
            self.assertEqual(payload["frontier"], [4, 5])
            self.assertIn("5", output)
            self.assertIn("frontier=[4, 5]", output)


if __name__ == "__main__":
    unittest.main()
