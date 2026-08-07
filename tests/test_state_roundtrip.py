import tempfile
import unittest
from pathlib import Path

from spherepop.primitives import Bind, Collapse, Pop, Refuse
from spherepop.state import load_history, save_history


class SpherepopStateRoundTripTests(unittest.TestCase):
    def test_round_trip_preserves_events_parents_and_frontier(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            path = Path(tmpdir) / "history.json"
            history = load_history(str(path))
            left = Pop(history, 5)
            right = Pop(history, 8)
            relation = Bind(history, left, right, value={"op": "+"})
            total = Collapse(history, relation, left, right, value=13)
            Refuse(history, total, reason="printed")

            save_history(history, str(path))
            reloaded = load_history(str(path))

            self.assertEqual(len(reloaded.events), len(history.events))
            self.assertEqual(reloaded.frontier, history.frontier)
            for index, original in enumerate(history.events):
                restored = reloaded.events[index]
                self.assertEqual(restored.op, original.op)
                self.assertEqual(restored.value, original.value)
                self.assertEqual(restored.parents, original.parents)

    def test_reloaded_history_remains_append_only(self) -> None:
        with tempfile.TemporaryDirectory() as tmpdir:
            path = Path(tmpdir) / "history.json"
            history = load_history(str(path))
            first = Pop(history, "seed")
            second = Collapse(history, first, value="stage-1")
            save_history(history, str(path))

            reloaded = load_history(str(path))
            baseline = list(reloaded.events)
            new_index = Pop(reloaded, "new")

            self.assertEqual(new_index, len(baseline))
            self.assertEqual(reloaded.events[: len(baseline)], baseline)
            self.assertEqual(reloaded.events[second].parents, (first,))


if __name__ == "__main__":
    unittest.main()
