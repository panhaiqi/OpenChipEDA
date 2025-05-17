from eda_simulator_base import Wire, AndGate, NotGate, Chip

# 1. 定义信号线
a = Wire("a")
b = Wire("b")
and_ab = Wire("and_ab")
out = Wire("out")

# 2. 定义门
and1 = AndGate("and1", [a, b], and_ab)
not1 = NotGate("not1", [and_ab], out)

# 3. 组装芯片
chip = Chip("SimpleChip")
chip.add_wire(a)
chip.add_wire(b)
chip.add_wire(and_ab)
chip.add_wire(out)
chip.add_gate(and1)
chip.add_gate(not1)

# 4. 仿真
inputs = {a: 1, b: 0}
result = chip.simulate(inputs)
print("仿真结果：", result)

# 5. （可选）导出Verilog
#print("Verilog代码：\n", chip.to_verilog())