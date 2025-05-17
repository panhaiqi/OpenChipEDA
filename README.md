# OpenChipEDA

[English](#english-version) | [中文](#chinese-version)

---

## <span id="chinese-version">中文版</span>

**OpenChipEDA** 是一个开源的、基于 Python 的芯片级数字电路仿真与EDA（电子设计自动化）统一平台。  
它致力于为数字电路的搭建、仿真与导出提供易用、可扩展、面向教学的环境，并规划支持更高级的EDA流程。

---

## ⭐️ 差异化优势

- **面向对象的电路建模**  
  用直观的 Python 类描述导线、门和芯片，无需 HDL 或 Verilog 基础即可上手。
- **原生 Python 仿真**  
  直接用 Python 搭建和仿真电路，适合原型设计、实验和教学。
- **无缝 Verilog 导出**  
  可一键将 Python 电路模型导出为 Verilog，便于后续专业 EDA 流程使用。
- **教学友好、低门槛**  
  专为学习者、教师和研究者设计，无需复杂工具链即可理解数字逻辑。
- **易于集成 Python 生态**  
  可与 Python 海量生态（AI、数据分析、可视化等）联动，拓展EDA探索与自动化。
- **快速原型与可扩展性**  
  方便扩展新门类型、电路模块，便于集成AI/EDA自动化项目。
- **补充HDL分析工具**  
  Pyverilog等工具聚焦于Verilog解析与分析，OpenChipEDA则强调Python代码级电路构建与仿真，二者互补。
- **开源与社区驱动**  
  免费开源，支持修改与扩展，适合科研、教学和开源硬件开发。

---

## 主要特性

- 模块化数字电路建模（线、门、芯片）
- 逻辑仿真（真值表、单步执行）
- Verilog 代码导出
- 易于 Python 脚本集成
- 新手与进阶用户皆宜
- 面向未来EDA/自动化扩展设计

---

## 目录结构

```
OpenChipEDA/
├── eda_simulator_base.py    # 核心建模与仿真模块
├── chip_simulator.py        # 示例与入口
├── tests/                   # 单元与集成测试
├── examples/                # 示例电路与脚本
├── docs/                    # 文档
├── LICENSE
└── README.md
```

---

## 快速开始

1. **克隆仓库:**
    ```bash
    git clone https://github.com/yourusername/OpenChipEDA.git
    cd OpenChipEDA
    ```

2. **运行示例:**
    ```bash
    python chip_simulator.py
    ```

3. **自定义你的电路:**
    - 编辑 `chip_simulator.py` 或新建脚本，导入 `eda_simulator_base.py`。

---

## 示例

```python
from eda_simulator_base import Wire, AndGate, NotGate, Chip

a, b, and_ab, out = Wire("a"), Wire("b"), Wire("and_ab"), Wire("out")
and1 = AndGate("and1", [a, b], and_ab)
not1 = NotGate("not1", [and_ab], out)

chip = Chip("SimpleChip")
chip.add_wire(a)
chip.add_wire(b)
chip.add_wire(and_ab)
chip.add_wire(out)
chip.add_gate(and1)
chip.add_gate(not1)

result = chip.simulate({a: 1, b: 0})
print("Simulation result:", result)
print("Generated Verilog:\n", chip.to_verilog())
```

---

## 许可证

详见 LICENSE 文件。

---

## 路线图

- [ ] **极致对象化与模块化电路建模**
    - 支持门级、组合逻辑、层次化/嵌套模块（便于教学与AI自动生成）
    - 参数化门/模块，增强灵活性和实验性

- [ ] **面向教学与交互友好体验**
    - 一键生成真值表和批量仿真结果
    - 交互式命令行与Jupyter支持，支持“所见即所得”电路编辑和仿真
    - 丰富的教学案例与实验模板

- [ ] **与Python生态融合的EDA自动化**
    - 与numpy/pandas/matplotlib无缝集成，实现波形可视化、数据分析与批量实验
    - 支持Python脚本一键导出Verilog，自动对接开源EDA工具链（如Yosys）

- [ ] **AI辅助与创新型EDA能力**
    - 集成AI/大模型自动设计、优化、验证电路
    - 支持电路等价性验证、自动化故障定位与诊断

- [ ] **可扩展可视化与Web/GUI前端**
    - Web/GUI交互界面，支持拖拽式电路搭建和实时仿真展示
    - 开放扩展接口，便于二次开发与社区创新

---

## 贡献

欢迎大家贡献代码、反馈问题、提出新需求！  
请直接提 issue 或 pull request。

---

## 鸣谢

- 灵感来源于PyRTL、Pyverilog、BinPy、DigSim 以及开源EDA/FPGA社区。

---

---

## <span id="english-version">English Version</span>

**OpenChipEDA** is an open-source, Python-based unified platform for chip-level digital circuit simulation and EDA (Electronic Design Automation).  
It aims to provide an easy-to-use, extensible, and educational environment for building, simulating, and exporting digital circuits, with future support for advanced EDA flows.

---

## ⭐️ Differentiators & Advantages

- **Object-Oriented Circuit Modeling**  
  Describe wires, gates, and entire chips using intuitive Python classes. No need for HDL or Verilog knowledge to get started.
- **Native Python Simulation**  
  Build and simulate circuits directly in Python—perfect for rapid prototyping, experimentation, and teaching.
- **Seamless Verilog Export**  
  Instantly export your Python-modeled circuits to Verilog for further use in professional EDA flows.
- **Educational Focus, Low Barrier to Entry**  
  Designed for learners, educators, and researchers—understand digital logic without steep learning curves or toolchain complexity.
- **Easy Integration with Python Ecosystem**  
  Leverage Python’s vast ecosystem (AI, data analysis, visualization) to enhance EDA exploration and automation.
- **Rapid Prototyping & Extensibility**  
  Easily extend with new gate types, circuit modules, or connect to AI/EDA automation projects.
- **Complementary to HDL Analysis Tools**  
  While tools like Pyverilog focus on parsing and analyzing Verilog, OpenChipEDA emphasizes hands-on, code-level circuit construction and simulation in Python.
- **Open Source & Community-Driven**  
  Freely available for modification and extension—ideal for research, teaching, and open hardware development.

---

## Features

- Modular digital circuit modeling (`Wire`, `Gate`, `Chip`)
- Logic simulation (truth table, single-step)
- Verilog code export
- Easy Python integration & scripting
- Friendly for both beginners and advanced users
- Designed for future EDA/automation extensions

---

## Directory Structure

```
OpenChipEDA/
├── eda_simulator_base.py    # Core circuit modeling and simulation classes
├── chip_simulator.py        # Example usage and entry point
├── tests/                   # Unit and integration tests (to be added)
├── examples/                # Example circuits and scripts (to be added)
├── docs/                    # Documentation (to be added)
├── LICENSE
└── README.md
```

---

## Quick Start

1. **Clone the repository:**
    ```bash
    git clone https://github.com/yourusername/OpenChipEDA.git
    cd OpenChipEDA
    ```

2. **Run the example:**
    ```bash
    python chip_simulator.py
    ```

3. **Define your own circuits:**
    - Edit `chip_simulator.py` or create a new Python script, importing from `eda_simulator_base.py`.

---

## Example

```python
from eda_simulator_base import Wire, AndGate, NotGate, Chip

a, b, and_ab, out = Wire("a"), Wire("b"), Wire("and_ab"), Wire("out")
and1 = AndGate("and1", [a, b], and_ab)
not1 = NotGate("not1", [and_ab], out)

chip = Chip("SimpleChip")
chip.add_wire(a)
chip.add_wire(b)
chip.add_wire(and_ab)
chip.add_wire(out)
chip.add_gate(and1)
chip.add_gate(not1)

result = chip.simulate({a: 1, b: 0})
print("Simulation result:", result)
print("Generated Verilog:\n", chip.to_verilog())
```

---

## License

See [LICENSE](LICENSE) for details.

---

## Roadmap

- [ ] **Extreme object-oriented and modular circuit modeling**
    - Support for gate-level, combinational logic, hierarchical/nested modules (ideal for teaching and AI-generated designs)
    - Parameterized gates/modules for greater flexibility and experimentation

- [ ] **Teaching-oriented and interactive user experience**
    - One-click truth table generation and batch simulation results
    - Interactive command-line and Jupyter support for WYSIWYG circuit editing and simulation
    - Rich teaching cases and experiment templates

- [ ] **EDA automation integrated with the Python ecosystem**
    - Seamless integration with numpy/pandas/matplotlib for waveform visualization, data analysis, and batch experiments
    - One-click Verilog export from Python scripts, with automatic connection to open-source EDA toolchains (e.g., Yosys)

- [ ] **AI-assisted and innovative EDA capabilities**
    - Integration of AI/large models for automatic design, optimization, and verification of circuits
    - Support for circuit equivalence checking, automated fault localization and diagnosis

- [ ] **Extensible visualization and Web/GUI frontend**
    - Web/GUI interactive interface for drag-and-drop circuit building and real-time simulation display
    - Open extension interfaces to facilitate secondary development and community innovation

---

## Contributing

Contributions, bug reports, and feature requests are welcome!  
Please open an issue or submit a pull request.

---

## Acknowledgements

- Inspired by PyRTL, Pyverilog, BinPy, DigSim, and the open-source EDA/FPGA communities.

---