class Wire:
    def __init__(self, name):
        self.name = name
        self.value = 0  # 仿真用，可扩展为多位

class Gate:
    def __init__(self, name, inputs, output):
        self.name = name
        self.inputs = inputs  # List[Wire]
        self.output = output  # Wire

    def simulate(self):
        raise NotImplementedError

    def to_verilog(self):
        raise NotImplementedError

class AndGate(Gate):
    def simulate(self):
        self.output.value = self.inputs[0].value & self.inputs[1].value

    def to_verilog(self):
        return f"assign {self.output.name} = {self.inputs[0].name} & {self.inputs[1].name};"

class OrGate(Gate):
    def simulate(self):
        self.output.value = self.inputs[0].value | self.inputs[1].value

    def to_verilog(self):
        return f"assign {self.output.name} = {self.inputs[0].name} | {self.inputs[1].name};"

class NotGate(Gate):
    def simulate(self):
        self.output.value = ~self.inputs[0].value & 1  # 只适合单比特

    def to_verilog(self):
        return f"assign {self.output.name} = ~{self.inputs[0].name};"

class Chip:
    def __init__(self, name):
        self.name = name
        self.gates = []
        self.wires = []

    def add_gate(self, gate):
        self.gates.append(gate)

    def add_wire(self, wire):
        self.wires.append(wire)

    def simulate(self, input_values):
        for wire, val in input_values.items():
            wire.value = val
        for gate in self.gates:
            gate.simulate()
        return {wire.name: wire.value for wire in self.wires}

    def to_verilog(self):
        verilog = f"module {self.name}(...);\n"
        for wire in self.wires:
            verilog += f"  wire {wire.name};\n"
        for gate in self.gates:
            verilog += f"  {gate.to_verilog()}\n"
        verilog += "endmodule\n"
        return verilog