import unittest

from forth.compiler import compile_source
from forth.vm import ForthVM


class ForthVmTests(unittest.TestCase):
    def test_forth_add_and_print(self) -> None:
        bytecode = compile_source("2 3 + .")
        vm = ForthVM()
        output = vm.execute(bytecode)

        self.assertEqual(output, [5])
        self.assertTrue(any(event.op == "BIND" for event in vm.history.events))
        self.assertTrue(any(event.op == "COLLAPSE" for event in vm.history.events))


if __name__ == "__main__":
    unittest.main()
