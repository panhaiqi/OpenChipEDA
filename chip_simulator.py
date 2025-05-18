from src.eda_simulator_base import Wire, AndGate, NotGate, Chip

# 1. 定义信号线，支持多比特、方向和属性扩展
a = Wire("a", width=1, direction="input")
b = Wire("b", width=1, direction="input")
and_ab = Wire("and_ab", width=1)
out = Wire("out", width=1, direction="output")

# 2. 定义门
and1 = AndGate("and1", [a, b], [and_ab])
not1 = NotGate("not1", [and_ab], [out])

# 3. 组装芯片
chip = Chip("SimpleChip", attributes={"author": "OpenChipEDA"})
# 这些是端口，使用add_port
chip.add_port(a)  # 输入端口
chip.add_port(b)  # 输入端口
# 这是内部信号，使用add_internal_wire
chip.add_internal_wire(and_ab)
# 这是端口，使用add_port
chip.add_port(out)  # 输出端口
chip.add_gate(and1)
chip.add_gate(not1)

# 4. 仿真
inputs = {a: 1, b: 0}
result = chip.simulate(inputs)
print("仿真结果：", result)

# 5. （可选）导出Verilog
#print("Verilog代码：\n", chip.to_verilog())