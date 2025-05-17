import unittest
from src.eda_simulator_base import Wire, AndGate, NotGate, Chip

class TestBasicChip(unittest.TestCase):
    def setUp(self):
        # 构建一个简单的电路: out = NOT(AND(a, b))
        self.a = Wire("a", width=1, direction="input")
        self.b = Wire("b", width=1, direction="input")
        self.and_ab = Wire("and_ab", width=1)
        self.out = Wire("out", width=1, direction="output")
        self.and1 = AndGate("and1", [self.a, self.b], self.and_ab)
        self.not1 = NotGate("not1", [self.and_ab], self.out)

        self.chip = Chip("SimpleChip", attributes={"testcase": "basic"})
        self.chip.add_wire(self.a)
        self.chip.add_wire(self.b)
        self.chip.add_wire(self.and_ab)
        self.chip.add_wire(self.out)
        self.chip.add_gate(self.and1)
        self.chip.add_gate(self.not1)

    def test_and_not(self):
        # 测试所有输入组合
        test_vectors = [
            ({self.a: 0, self.b: 0}, 1),
            ({self.a: 0, self.b: 1}, 1),
            ({self.a: 1, self.b: 0}, 1),
            ({self.a: 1, self.b: 1}, 0),
        ]
        for inputs, expected_out in test_vectors:
            result = self.chip.simulate(inputs)
            self.assertEqual(result[self.out.name], expected_out, f"Input: {inputs}, Expected: {expected_out}, Got: {result[self.out.name]}")

if __name__ == "__main__":
    unittest.main()