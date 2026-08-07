import unittest

from spherepop.history import History
from spherepop.primitives import Bind, Collapse, Pop, Refuse


class InvariantRegressionTests(unittest.TestCase):
    def test_event_indices_remain_immutable_across_mixed_operations(self) -> None:
        history = History()
        e0 = Pop(history, "alpha")
        e1 = Pop(history, "beta")
        e2 = Bind(history, e0, e1, value={"relation": "pair"})
        snapshot = list(history.events)

        e3 = Collapse(history, e2, e0, e1, value="merged")
        e4 = Refuse(history, e3, reason="consumed")
        e5 = Pop(history, "gamma")

        self.assertEqual([e0, e1, e2, e3, e4, e5], [0, 1, 2, 3, 4, 5])
        self.assertEqual(history.events[: len(snapshot)], snapshot)
        self.assertEqual(history.events[e2].parents, (e0, e1))
        self.assertEqual(history.events[e3].parents, (e2, e0, e1))
        self.assertEqual(history.events[e4].parents, (e3,))

    def test_frontier_behavior_is_stable_under_mixed_sequences(self) -> None:
        history = History()
        left = Pop(history, 2)
        right = Pop(history, 3)
        relation = Bind(history, left, right, value={"op": "*"})
        result = Collapse(history, relation, left, right, value=6)
        refusal = Refuse(history, result, reason="emitted")
        carry = Pop(history, "carry")
        reduced = Collapse(history, refusal, carry, value={"stage": 2})

        self.assertNotIn(left, history.frontier)
        self.assertNotIn(right, history.frontier)
        self.assertNotIn(relation, history.frontier)
        self.assertNotIn(result, history.frontier)
        self.assertNotIn(refusal, history.frontier)
        self.assertNotIn(carry, history.frontier)
        self.assertIn(reduced, history.frontier)
        self.assertEqual(history.events[refusal].value["target"], result)


if __name__ == "__main__":
    unittest.main()
