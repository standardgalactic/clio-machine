import unittest

from spherepop.history import History
from spherepop.primitives import Bind, Collapse, Pop, Refuse


class SpherepopHistoryTests(unittest.TestCase):
    def test_append_only_history_with_frontier_updates(self) -> None:
        history = History()
        e0 = Pop(history, 5)
        e1 = Pop(history, 8)
        e2 = Bind(history, e0, e1)
        e3 = Collapse(history, e2)
        Refuse(history, e3, reason="test")

        self.assertEqual(len(history.events), 5)
        self.assertEqual(history.events[2].op, "BIND")
        self.assertEqual(history.events[3].op, "COLLAPSE")
        self.assertEqual(history.events[4].op, "REFUSE")
        self.assertNotIn(e3, history.frontier)


if __name__ == "__main__":
    unittest.main()
