import unittest

from spherepop.history import History
from spherepop.primitives import Bind, Collapse, Pop, Refuse


class SemanticInvariantTests(unittest.TestCase):
    def test_history_is_append_only(self) -> None:
        history = History()
        first = Pop(history, "alpha")
        baseline = list(history.events)

        second = Pop(history, "beta")
        Bind(history, first, second, value={"relation": "pair"})

        self.assertEqual(history.events[: len(baseline)], baseline)
        self.assertGreater(len(history.events), len(baseline))

    def test_bind_preserves_parent_links(self) -> None:
        history = History()
        left = Pop(history, 2)
        right = Pop(history, 3)

        relation = Bind(history, left, right, value={"op": "*"})

        self.assertEqual(history.events[relation].op, "BIND")
        self.assertEqual(history.events[relation].parents, (left, right))

    def test_refuse_does_not_delete_history(self) -> None:
        history = History()
        target = Pop(history, "token")
        size_before = len(history.events)

        refusal = Refuse(history, target, reason="not admissible")

        self.assertEqual(len(history.events), size_before + 1)
        self.assertEqual(history.events[target].value, "token")
        self.assertEqual(history.events[refusal].parents, (target,))

    def test_collapse_creates_new_representation(self) -> None:
        history = History()
        left = Pop(history, 5)
        right = Pop(history, 8)
        relation = Bind(history, left, right, value={"op": "+"})

        collapsed = Collapse(history, relation, left, right, value=13)

        self.assertEqual(history.events[collapsed].op, "COLLAPSE")
        self.assertEqual(history.events[collapsed].parents, (relation, left, right))
        self.assertEqual(history.events[collapsed].value, 13)
        self.assertIn(collapsed, history.frontier)

    def test_frontier_updates_are_monotonic(self) -> None:
        history = History()
        a = Pop(history, 1)
        b = Pop(history, 2)
        frontier_max_after_pop = max(history.frontier)

        relation = Bind(history, a, b)
        _ = Refuse(history, a, reason="consumed")
        collapsed = Collapse(history, relation, b, value=3)

        self.assertGreaterEqual(max(history.frontier), frontier_max_after_pop)
        self.assertIn(collapsed, history.frontier)
        self.assertNotIn(a, history.frontier)
        self.assertNotIn(b, history.frontier)


if __name__ == "__main__":
    unittest.main()
