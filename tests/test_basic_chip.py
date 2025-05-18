import unittest
from src.eda_simulator_base import Wire, AndGate, NotGate, Chip

class TestBasicChip(unittest.TestCase):
    def setUp(self):
        # 构建一个简单的电路: out = NOT(AND(a, b))
        self.a = Wire("a", width=1, direction="input")
        self.b = Wire("b", width=1, direction="input")
        self.and_ab = Wire("and_ab", width=1)
        self.out = Wire("out", width=1, direction="output")
        self.and1 = AndGate("and1", [self.a, self.b], [self.and_ab])
        self.not1 = NotGate("not1", [self.and_ab], [self.out])

        self.chip = Chip("SimpleChip", ports=[self.a, self.b, self.out], attributes={"testcase": "basic"})
        # 添加内部信号
        self.chip.add_internal_wire(self.and_ab)
        # 添加门
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
            # 每次测试前重置所有信号
            for w in [self.a, self.b, self.and_ab, self.out]:
                w.value = 0
                
            # 运行仿真
            result = self.chip.simulate(inputs)
            self.assertEqual(result[self.out.name], expected_out, 
                             f"Input: {inputs}, Expected: {expected_out}, Got: {result[self.out.name]}")

    def test_verilog_generation(self):
        # 测试Verilog代码生成
        verilog = self.chip.to_verilog()
        # 验证模块声明存在
        self.assertIn(f"module {self.chip.name}", verilog)
        # 验证端口声明存在
        for port in [self.a, self.b, self.out]:
            self.assertIn(port.name, verilog)
        # 验证内部信号声明存在
        self.assertIn(f"wire [{self.and_ab.width-1}:0] {self.and_ab.name}", verilog)
        # 验证门连接存在
        self.assertIn(f"assign {self.and_ab.name} =", verilog)
        self.assertIn(f"assign {self.out.name} =", verilog)

if __name__ == "__main__":
    unittest.main()