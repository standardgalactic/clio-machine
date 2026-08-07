import os
import subprocess
import tempfile
import unittest
from pathlib import Path


REPO_ROOT = Path(__file__).resolve().parents[1]
SPHEREPOP = REPO_ROOT / "bin" / "spherepop"


class SpherepopCliTests(unittest.TestCase):
    def test_cli_sequence_and_trace(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            state_path = Path(tmpdir) / "history.json"
            env = os.environ.copy()
            env["PYTHONPATH"] = str(REPO_ROOT)
            env["SPHEREPOP_STATE_PATH"] = str(state_path)

            for args in (("pop", "5"), ("pop", "8"), ("bind", "0", "1"), ("collapse", "2")):
                subprocess.run([str(SPHEREPOP), *args], check=True, env=env, cwd=REPO_ROOT)

            trace = subprocess.run(
                [str(SPHEREPOP), "trace"],
                check=True,
                env=env,
                cwd=REPO_ROOT,
                capture_output=True,
                text=True,
            ).stdout

            self.assertIn("POP", trace)
            self.assertIn("BIND", trace)
            self.assertIn("COLLAPSE", trace)


if __name__ == "__main__":
    unittest.main()
