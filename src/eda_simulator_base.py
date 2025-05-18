class Wire:
    def __init__(self, name, width=1, direction=None, default_value=0, signal_type="wire", attributes=None):
        self.name = name
        self.width = width
        self.direction = direction  # 'input', 'output', 'inout', or None
        self.signal_type = signal_type  # 'wire' or 'reg'
        self.value = default_value
        self.next_value = default_value  # 用于两阶段仿真
        self.drivers = []  # 驱动该信号的门/模块
        self.loads = []    # 被该信号驱动的门/模块
        self.attributes = attributes or {}
        self.delay = 0     # 传播延迟
        
    def connect_driver(self, driver):
        """记录驱动源，支持多驱动检测"""
        self.drivers.append(driver)
        
    def connect_load(self, load):
        """记录负载，支持扇出分析"""
        self.loads.append(load)

    def __eq__(self, other):
        return isinstance(other, Wire) and self.name == other.name

    def __hash__(self):
        return hash(self.name)

class Gate:
    def __init__(self, name, inputs, outputs, delay=0, attributes=None):
        self.name = name
        self.inputs = inputs      # List[Wire]
        self.outputs = outputs    # List[Wire] - 支持多输出
        self.delay = delay        # 门延迟
        self.attributes = attributes or {}
        # 自动连接信号驱动关系
        for wire in inputs:
            wire.connect_load(self)
        for wire in outputs:
            wire.connect_driver(self)
            
    def schedule_event(self, simulation_context, time):
        """支持事件驱动仿真"""
        simulation_context.add_event(time + self.delay, self)

    def simulate(self):
        raise NotImplementedError

    def to_verilog(self):
        raise NotImplementedError

class AndGate(Gate):
    def simulate(self):
        # 支持多输入与门
        value = 1
        for wire in self.inputs:
            value &= wire.value
        self.outputs[0].value = value

    def to_verilog(self):
        expr = " & ".join(wire.name for wire in self.inputs)
        return f"assign {self.outputs[0].name} = {expr};"

class OrGate(Gate):
    def simulate(self):
        value = 0
        for wire in self.inputs:
            value |= wire.value
        self.outputs[0].value = value

    def to_verilog(self):
        expr = " | ".join(wire.name for wire in self.inputs)
        return f"assign {self.outputs[0].name} = {expr};"

class NotGate(Gate):
    def simulate(self):
        # 按位宽处理
        mask = (1 << self.outputs[0].width) - 1
        self.outputs[0].value = (~self.inputs[0].value) & mask

    def to_verilog(self):
        return f"assign {self.outputs[0].name} = ~{self.inputs[0].name};"

class Chip:
    def __init__(self, name, ports=None, parameters=None, attributes=None):
        self.name = name
        self.ports = ports or []      # 明确定义接口端口
        self.parameters = parameters or {}  # 支持参数化
        self.internal_wires = []      # 内部信号
        self.gates = []
        self.instances = []           # 子模块实例
        self.port_map = {}            # 端口映射
        self.attributes = attributes or {}
        self.clock_domains = {}       # 时钟域管理
        
    def add_port(self, wire):
        """添加端口"""
        self.ports.append(wire)
        
    def add_internal_wire(self, wire):
        """添加内部信号"""
        self.internal_wires.append(wire)
        
    def instantiate(self, module, instance_name, port_map, parameter_map=None):
        """实例化子模块，支持端口映射和参数传递"""
        self.instances.append({
            'module': module,
            'name': instance_name,
            'port_map': port_map,
            'parameter_map': parameter_map or {}
        })

    def add_gate(self, gate):
        """添加逻辑门"""
        self.gates.append(gate)
    def simulate(self, inputs):
        """仿真芯片功能
        
        Args:
            inputs: 输入值字典 {Wire: value}
            
        Returns:
            字典，包含所有输出端口的名称和值
        """
        # 首先设置输入值
        for wire, value in inputs.items():
            wire.value = value
            
        # 对所有门进行仿真
        for gate in self.gates:
            gate.simulate()
            
        # 收集输出结果
        results = {}
        for wire in self.ports:
            if wire.direction == "output":
                results[wire.name] = wire.value
                
        return results
        
    def to_verilog(self):
        """生成Verilog代码"""
        verilog = f"module {self.name} (\n"
        
        # 端口声明
        ports = [wire.name for wire in self.ports]
        verilog += "  " + ",\n  ".join(ports) + "\n);\n\n"
        
        # 端口定义
        for wire in self.ports:
            if wire.direction == "input":
                verilog += f"  input [{wire.width-1}:0] {wire.name};\n"
            elif wire.direction == "output":
                verilog += f"  output [{wire.width-1}:0] {wire.name};\n"
            elif wire.direction == "inout":
                verilog += f"  inout [{wire.width-1}:0] {wire.name};\n"
                
        verilog += "\n"
        
        # 内部信号定义
        for wire in self.internal_wires:
            verilog += f"  wire [{wire.width-1}:0] {wire.name};\n"
            
        verilog += "\n"
        
        # 门级连接
        for gate in self.gates:
            verilog += "  " + gate.to_verilog() + "\n"
            
        verilog += "endmodule\n"
        return verilog
