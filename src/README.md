# OpenChipEDA 核心代码结构

[English](#english-version) | [中文](#chinese-version)

---

## <span id="chinese-version">中文版</span>

本目录包含 OpenChipEDA 的核心数据结构与仿真引擎实现，为整个 EDA 平台提供基础。

### 核心文件

- `eda_simulator_base.py`: 提供基本的电路建模、仿真和代码生成功能

### 代码架构与工业级特性

OpenChipEDA 的核心架构设计已经接近工业级 EDA 工具的基础架构，特别是在网表表示和逻辑仿真部分：

#### 已实现的工业级特性
- ✅ **网表模型完备**：Wire、Gate、Chip 基本结构清晰
- ✅ **层次化设计**：支持模块实例化和端口映射
- ✅ **参数化支持**：Chip 支持参数传递
- ✅ **多位宽支持**：Wire 支持任意位宽
- ✅ **驱动-负载模型**：Wire 记录驱动源和负载
- ✅ **事件驱动框架**：具备事件调度基础设施
- ✅ **延迟建模**：支持门级延迟
- ✅ **时钟域概念**：为时序设计预留结构
- ✅ **Verilog 生成**：支持 RTL 代码生成

#### 与工业级 EDA 的差距
1. **时序分析**：缺少静态时序分析能力
2. **高级仿真**：缺少 delta 周期、竞态处理等
3. **综合优化**：无逻辑优化和技术映射
4. **验证能力**：无形式化验证、断言、覆盖率
5. **物理设计**：无布局布线、芯片规划能力
6. **可视化**：无波形显示和图形界面

### 可扩展性设计

核心代码采用高度模块化和面向对象设计，提供了多个关键的可扩展点：

1. **类继承机制**：易于扩展新的门类型和模块
2. **属性字典**：通用属性机制支持任意元数据扩展
3. **事件调度**：为完整事件驱动仿真提供基础
4. **连接关系模型**：驱动-负载关系支持复杂网表分析
5. **模块化设计**：关注点分离良好，便于扩展新功能

### 扩展示例

#### 添加时序元件

```python
class DFF(Gate):
    def __init__(self, name, d_input, clock, q_output, reset=None, delay=0):
        inputs = [d_input, clock]
        if reset: inputs.append(reset)
        super().__init__(name, inputs, [q_output], delay)
        self.prev_clk = 0  # 记录上一时钟状态
        
    def simulate(self):
        # 检测时钟上升沿
        if self.inputs[1].value == 1 and self.prev_clk == 0:
            self.outputs[0].value = self.inputs[0].value
        self.prev_clk = self.inputs[1].value
```

#### 构建事件驱动仿真引擎

```python
class EventDrivenSimulator:
    def __init__(self):
        self.time = 0
        self.event_queue = []  # (time, component)
        self.wave_data = {}  # 波形数据
        
    def add_event(self, time, component):
        # 使用优先队列添加事件
        import heapq
        heapq.heappush(self.event_queue, (time, component))
        
    def run_until(self, end_time):
        # 事件驱动执行
        import heapq
        while self.event_queue and self.time <= end_time:
            time, component = heapq.heappop(self.event_queue)
            self.time = time
            component.simulate()
```

### 扩展路线图

建议按以下顺序扩展功能，逐步向完整的工业级EDA工具靠拢：

1. 完善事件驱动仿真引擎
2. 添加时序元件和时序分析
3. 增加波形显示和调试功能
4. 扩展验证和测试功能
5. 添加优化和综合功能

### 使用方法

请参考根目录下的示例和测试文件，了解如何使用核心库构建和仿真电路，以及生成Verilog代码。

### 贡献指南

欢迎通过以下方式贡献：
- 添加新的门类型
- 扩展仿真引擎功能
- 增加新的HDL代码生成支持
- 改进文档和测试用例

贡献前请运行测试套件确保基本功能正常。

---

---

## <span id="english-version">English Version</span>

# OpenChipEDA Core Code Structure

This directory contains the core data structures and simulation engine implementation of OpenChipEDA, providing the foundation for the entire EDA platform.

### Core Files

- `eda_simulator_base.py`: Provides basic circuit modeling, simulation, and code generation functionality

### Code Architecture and Industry-grade Features

The core architecture design of OpenChipEDA is approaching industry-grade EDA tools' foundation, especially in netlist representation and logic simulation:

#### Implemented Industry-grade Features
- ✅ **Complete Netlist Model**: Clear Wire, Gate, and Chip basic structures
- ✅ **Hierarchical Design**: Supports module instantiation and port mapping
- ✅ **Parameterization Support**: Chip supports parameter passing
- ✅ **Multi-bit Width Support**: Wire supports arbitrary bit widths
- ✅ **Driver-Load Model**: Wire records drivers and loads
- ✅ **Event-driven Framework**: Provides event scheduling infrastructure
- ✅ **Delay Modeling**: Supports gate-level delays
- ✅ **Clock Domain Concept**: Reserves structures for timing design
- ✅ **Verilog Generation**: Supports RTL code generation

#### Gaps to Industry-grade EDA
1. **Timing Analysis**: Lacks static timing analysis capability
2. **Advanced Simulation**: Lacks delta cycles, race handling, etc.
3. **Synthesis Optimization**: No logic optimization and technology mapping
4. **Verification Capability**: No formal verification, assertions, coverage
5. **Physical Design**: No place and route, chip planning capabilities
6. **Visualization**: No waveform display and graphical interface

### Extensibility Design

The core code uses highly modularized and object-oriented design, providing several key extension points:

1. **Class Inheritance Mechanism**: Easy to extend new gate types and modules
2. **Attribute Dictionary**: Universal attribute mechanism supports arbitrary metadata extension
3. **Event Scheduling**: Provides foundation for complete event-driven simulation
4. **Connection Relationship Model**: Driver-load relationships support complex netlist analysis
5. **Modular Design**: Good separation of concerns, facilitating new function extensions

### Extension Examples

#### Adding Sequential Elements

```python
class DFF(Gate):
    def __init__(self, name, d_input, clock, q_output, reset=None, delay=0):
        inputs = [d_input, clock]
        if reset: inputs.append(reset)
        super().__init__(name, inputs, [q_output], delay)
        self.prev_clk = 0  # Record previous clock state
        
    def simulate(self):
        # Detect clock rising edge
        if self.inputs[1].value == 1 and self.prev_clk == 0:
            self.outputs[0].value = self.inputs[0].value
        self.prev_clk = self.inputs[1].value
```

#### Building Event-driven Simulation Engine

```python
class EventDrivenSimulator:
    def __init__(self):
        self.time = 0
        self.event_queue = []  # (time, component)
        self.wave_data = {}  # Waveform data
        
    def add_event(self, time, component):
        # Use priority queue to add events
        import heapq
        heapq.heappush(self.event_queue, (time, component))
        
    def run_until(self, end_time):
        # Event-driven execution
        import heapq
        while self.event_queue and self.time <= end_time:
            time, component = heapq.heappop(self.event_queue)
            self.time = time
            component.simulate()
```

### Extension Roadmap

It is recommended to extend functionality in the following order, gradually approaching a complete industry-grade EDA tool:

1. Improve the event-driven simulation engine
2. Add sequential elements and timing analysis
3. Add waveform display and debugging functionality
4. Extend verification and testing capabilities
5. Add optimization and synthesis functionality

### Usage

Please refer to the examples and test files in the root directory to understand how to use the core library to build and simulate circuits, as well as generate Verilog code.

### Contribution Guidelines

Contributions are welcome in the following ways:
- Adding new gate types
- Extending simulation engine functionality
- Adding support for new HDL code generation
- Improving documentation and test cases

Please run the test suite before contributing to ensure basic functionality works correctly.

---