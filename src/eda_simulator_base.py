class Wire:
    def __init__(self, name, width=1, direction=None, default_value=0, attributes=None):
        self.name = name
        self.width = width
        self.direction = direction  # 'input', 'output', 'inout', or None
        self.default_value = default_value
        self.value = default_value
        self.attributes = attributes or {}

    def __eq__(self, other):
        return isinstance(other, Wire) and self.name == other.name

    def __hash__(self):
        return hash(self.name)

class Gate:
    def __init__(self, name, inputs, output, attributes=None):
        self.name = name
        self.inputs = inputs  # List[Wire]
        self.output = output  # Wire
        self.attributes = attributes or {}

    def simulate(self):
        raise NotImplementedError

    def to_verilog(self):
        raise NotImplementedError

class AndGate(Gate):
    def simulate(self):
        # 支持任意输入数量（N输入与门）
        value = 1
        for wire in self.inputs:
            value &= wire.value
        self.output.value = value

    def to_verilog(self):
        input_expr = " & ".join(wire.name for wire in self.inputs)
        return f"assign {self.output.name} = {input_expr};"

class OrGate(Gate):
    def simulate(self):
        value = 0
        for wire in self.inputs:
            value |= wire.value
        self.output.value = value

    def to_verilog(self):
        input_expr = " | ".join(wire.name for wire in self.inputs)
        return f"assign {self.output.name} = {input_expr};"

class NotGate(Gate):
    def simulate(self):
        # 支持多比特，但这里只处理最低位
        self.output.value = ~self.inputs[0].value & ((1 << self.output.width) - 1)

    def to_verilog(self):
        return f"assign {self.output.name} = ~{self.inputs[0].name};"

class Chip:
    def __init__(self, name, attributes=None):
        self.name = name
        self.gates = []
        self.wires = []
        self.subchips = []  # 支持层次化
        self.attributes = attributes or {}

    def add_gate(self, gate):
        self.gates.append(gate)

    def add_wire(self, wire):
        self.wires.append(wire)

    def add_subchip(self, chip):
        self.subchips.append(chip)

    def simulate(self, input_values):
        # 赋值输入（支持Wire对象或name作为key）
        for wire_key, val in input_values.items():
            if isinstance(wire_key, Wire):
                wire_key.value = val
            elif isinstance(wire_key, str):
                for wire in self.wires:
                    if wire.name == wire_key:
                        wire.value = val
                        break
        # 仿真本层gates
        for gate in self.gates:
            gate.simulate()
        # 仿真子模块
        for chip in self.subchips:
            chip.simulate({})
        # 返回所有线的当前值
        result = {wire.name: wire.value for wire in self.wires}
        for chip in self.subchips:
            result.update({f"{chip.name}.{k}": v for k, v in chip.simulate({}).items()})
        return result

    def to_verilog(self):
        verilog = f"module {self.name}(...);\n"
        for wire in self.wires:
            wire_decl = f"  wire"
            if wire.width > 1:
                wire_decl += f" [{wire.width-1}:0]"
            wire_decl += f" {wire.name};\n"
            verilog += wire_decl
        for gate in self.gates:
            verilog += f"  {gate.to_verilog()}\n"
        for chip in self.subchips:
            verilog += f"  // Subchip: {chip.name}\n"
            verilog += chip.to_verilog()
        verilog += "endmodule\n"
        return verilog