"""OpenChipEDA - Digital Circuit Simulation and EDA Platform.

This module provides the core classes for digital circuit modeling and simulation.
It includes Wire, Gate, and Chip classes for building and simulating digital circuits.
"""

from __future__ import annotations

import logging
from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional, Set, Union

# Configure logging
logger = logging.getLogger(__name__)


class Wire:
    """Represents a wire in a digital circuit.
    
    A wire can carry digital signals and connects gates together. It supports
    multiple bit widths and can be configured as input, output, or internal signals.
    
    Attributes:
        name: The name identifier of the wire.
        width: The bit width of the wire (default: 1).
        direction: The direction of the wire ('input', 'output', 'inout', or None).
        signal_type: The type of signal ('wire' or 'reg').
        value: The current value of the wire.
        next_value: The next value for two-phase simulation.
        drivers: List of gates that drive this wire.
        loads: List of gates that are driven by this wire.
        attributes: Additional attributes for the wire.
        delay: Propagation delay of the wire.
    """

    def __init__(
        self,
        name: str,
        width: int = 1,
        direction: Optional[str] = None,
        default_value: int = 0,
        signal_type: str = "wire",
        attributes: Optional[Dict[str, Any]] = None,
    ) -> None:
        """Initialize a Wire instance.
        
        Args:
            name: The name identifier of the wire.
            width: The bit width of the wire.
            direction: The direction of the wire ('input', 'output', 'inout', or None).
            default_value: The default value of the wire.
            signal_type: The type of signal ('wire' or 'reg').
            attributes: Additional attributes for the wire.
            
        Raises:
            ValueError: If width is less than 1 or direction is invalid.
        """
        if width < 1:
            raise ValueError("Wire width must be at least 1")
        
        valid_directions = {"input", "output", "inout", None}
        if direction not in valid_directions:
            raise ValueError(f"Invalid direction: {direction}. Must be one of {valid_directions}")
        
        self.name: str = name
        self.width: int = width
        self.direction: Optional[str] = direction
        self.signal_type: str = signal_type
        self.value: int = default_value
        self.next_value: int = default_value
        self.drivers: List[Any] = []
        self.loads: List[Any] = []
        self.attributes: Dict[str, Any] = attributes or {}
        self.delay: int = 0
        
        logger.debug(f"Created wire '{name}' with width {width}, direction {direction}")
        
    def connect_driver(self, driver: Any) -> None:
        """Record a driver for this wire.
        
        Args:
            driver: The gate or module that drives this wire.
        """
        self.drivers.append(driver)
        logger.debug(f"Connected driver {driver} to wire '{self.name}'")
        
    def connect_load(self, load: Any) -> None:
        """Record a load for this wire.
        
        Args:
            load: The gate or module that is driven by this wire.
        """
        self.loads.append(load)
        logger.debug(f"Connected load {load} to wire '{self.name}'")

    def __eq__(self, other: object) -> bool:
        """Check if this wire equals another wire.
        
        Args:
            other: The other object to compare with.
            
        Returns:
            True if the wires have the same name, False otherwise.
        """
        return isinstance(other, Wire) and self.name == other.name

    def __hash__(self) -> int:
        """Return hash of the wire based on its name.
        
        Returns:
            Hash value of the wire name.
        """
        return hash(self.name)
    
    def __str__(self) -> str:
        """Return string representation of the wire.
        
        Returns:
            String representation showing name, width, and direction.
        """
        return f"Wire('{self.name}', width={self.width}, direction={self.direction})"
    
    def __repr__(self) -> str:
        """Return detailed string representation of the wire.
        
        Returns:
            Detailed string representation of the wire.
        """
        return f"Wire(name='{self.name}', width={self.width}, direction={self.direction}, value={self.value})"


class Gate(ABC):
    """Abstract base class for all logic gates.
    
    A gate represents a basic logic operation in a digital circuit. It can have
    multiple inputs and outputs, and supports timing simulation.
    
    Attributes:
        name: The name identifier of the gate.
        inputs: List of input wires.
        outputs: List of output wires.
        delay: The propagation delay of the gate.
        attributes: Additional attributes for the gate.
    """

    def __init__(
        self,
        name: str,
        inputs: List[Wire],
        outputs: List[Wire],
        delay: int = 0,
        attributes: Optional[Dict[str, Any]] = None,
    ) -> None:
        """Initialize a Gate instance.
        
        Args:
            name: The name identifier of the gate.
            inputs: List of input wires.
            outputs: List of output wires.
            delay: The propagation delay of the gate.
            attributes: Additional attributes for the gate.
            
        Raises:
            ValueError: If inputs or outputs list is empty.
        """
        if not inputs:
            raise ValueError("Gate must have at least one input")
        if not outputs:
            raise ValueError("Gate must have at least one output")
            
        self.name: str = name
        self.inputs: List[Wire] = inputs
        self.outputs: List[Wire] = outputs
        self.delay: int = delay
        self.attributes: Dict[str, Any] = attributes or {}
        
        # Automatically connect signal driving relationships
        for wire in inputs:
            wire.connect_load(self)
        for wire in outputs:
            wire.connect_driver(self)
            
        logger.debug(f"Created gate '{name}' with {len(inputs)} inputs and {len(outputs)} outputs")
            
    def schedule_event(self, simulation_context: Any, time: int) -> None:
        """Schedule an event for event-driven simulation.
        
        Args:
            simulation_context: The simulation context to add events to.
            time: The time at which to schedule the event.
        """
        simulation_context.add_event(time + self.delay, self)

    @abstractmethod
    def simulate(self) -> None:
        """Simulate the gate's logic operation.
        
        This method should be implemented by subclasses to define the specific
        logic operation of the gate.
        """
        pass

    @abstractmethod
    def to_verilog(self) -> str:
        """Generate Verilog code for this gate.
        
        Returns:
            Verilog code string representing this gate.
        """
        pass
    
    def __str__(self) -> str:
        """Return string representation of the gate.
        
        Returns:
            String representation showing gate name and type.
        """
        return f"{self.__class__.__name__}('{self.name}')"


class AndGate(Gate):
    """Represents an AND logic gate.
    
    An AND gate outputs 1 only when all inputs are 1, otherwise outputs 0.
    Supports multiple inputs for multi-input AND operations.
    """

    def simulate(self) -> None:
        """Simulate the AND gate operation.
        
        Sets the output to 1 only if all inputs are 1, otherwise 0.
        """
        value = 1
        for wire in self.inputs:
            value &= wire.value
        self.outputs[0].value = value
        logger.debug(f"AND gate '{self.name}' simulation: inputs={[w.value for w in self.inputs]}, output={value}")

    def to_verilog(self) -> str:
        """Generate Verilog code for the AND gate.
        
        Returns:
            Verilog assign statement for the AND operation.
        """
        expr = " & ".join(wire.name for wire in self.inputs)
        return f"assign {self.outputs[0].name} = {expr};"


class OrGate(Gate):
    """Represents an OR logic gate.
    
    An OR gate outputs 1 when any input is 1, otherwise outputs 0.
    Supports multiple inputs for multi-input OR operations.
    """

    def simulate(self) -> None:
        """Simulate the OR gate operation.
        
        Sets the output to 1 if any input is 1, otherwise 0.
        """
        value = 0
        for wire in self.inputs:
            value |= wire.value
        self.outputs[0].value = value
        logger.debug(f"OR gate '{self.name}' simulation: inputs={[w.value for w in self.inputs]}, output={value}")

    def to_verilog(self) -> str:
        """Generate Verilog code for the OR gate.
        
        Returns:
            Verilog assign statement for the OR operation.
        """
        expr = " | ".join(wire.name for wire in self.inputs)
        return f"assign {self.outputs[0].name} = {expr};"


class NotGate(Gate):
    """Represents a NOT logic gate (inverter).
    
    A NOT gate inverts the input signal. Outputs 0 when input is 1, and 1 when input is 0.
    Supports multi-bit inputs with proper bit-width handling.
    """

    def simulate(self) -> None:
        """Simulate the NOT gate operation.
        
        Inverts the input value, handling multi-bit signals properly.
        """
        # Handle multi-bit signals with proper masking
        mask = (1 << self.outputs[0].width) - 1
        self.outputs[0].value = (~self.inputs[0].value) & mask
        logger.debug(f"NOT gate '{self.name}' simulation: input={self.inputs[0].value}, output={self.outputs[0].value}")

    def to_verilog(self) -> str:
        """Generate Verilog code for the NOT gate.
        
        Returns:
            Verilog assign statement for the NOT operation.
        """
        return f"assign {self.outputs[0].name} = ~{self.inputs[0].name};"


class XorGate(Gate):
    """Represents an XOR logic gate.
    
    An XOR gate outputs 1 when the number of 1s in the inputs is odd, otherwise outputs 0.
    Supports multiple inputs for multi-input XOR operations.
    """

    def simulate(self) -> None:
        """Simulate the XOR gate operation.
        
        Sets the output to 1 if the number of 1s in inputs is odd, otherwise 0.
        """
        value = 0
        for wire in self.inputs:
            value ^= wire.value
        self.outputs[0].value = value
        logger.debug(f"XOR gate '{self.name}' simulation: inputs={[w.value for w in self.inputs]}, output={value}")

    def to_verilog(self) -> str:
        """Generate Verilog code for the XOR gate.
        
        Returns:
            Verilog assign statement for the XOR operation.
        """
        expr = " ^ ".join(wire.name for wire in self.inputs)
        return f"assign {self.outputs[0].name} = {expr};"


class NandGate(Gate):
    """Represents a NAND logic gate.
    
    A NAND gate is the inverse of an AND gate. Outputs 0 only when all inputs are 1.
    """

    def simulate(self) -> None:
        """Simulate the NAND gate operation.
        
        Sets the output to 0 only if all inputs are 1, otherwise 1.
        """
        value = 1
        for wire in self.inputs:
            value &= wire.value
        self.outputs[0].value = 0 if value else 1
        logger.debug(f"NAND gate '{self.name}' simulation: inputs={[w.value for w in self.inputs]}, output={self.outputs[0].value}")

    def to_verilog(self) -> str:
        """Generate Verilog code for the NAND gate.
        
        Returns:
            Verilog assign statement for the NAND operation.
        """
        expr = " & ".join(wire.name for wire in self.inputs)
        return f"assign {self.outputs[0].name} = ~({expr});"


class NorGate(Gate):
    """Represents a NOR logic gate.
    
    A NOR gate is the inverse of an OR gate. Outputs 1 only when all inputs are 0.
    """

    def simulate(self) -> None:
        """Simulate the NOR gate operation.
        
        Sets the output to 1 only if all inputs are 0, otherwise 0.
        """
        value = 0
        for wire in self.inputs:
            value |= wire.value
        self.outputs[0].value = 0 if value else 1
        logger.debug(f"NOR gate '{self.name}' simulation: inputs={[w.value for w in self.inputs]}, output={self.outputs[0].value}")

    def to_verilog(self) -> str:
        """Generate Verilog code for the NOR gate.
        
        Returns:
            Verilog assign statement for the NOR operation.
        """
        expr = " | ".join(wire.name for wire in self.inputs)
        return f"assign {self.outputs[0].name} = ~({expr});"


class Chip:
    """Represents a digital circuit chip/module.
    
    A chip is a collection of gates and wires that form a complete digital circuit.
    It can have input/output ports and internal signals, and supports simulation
    and Verilog code generation.
    
    Attributes:
        name: The name identifier of the chip.
        ports: List of port wires (inputs/outputs).
        parameters: Dictionary of parameter values.
        internal_wires: List of internal signal wires.
        gates: List of logic gates in the chip.
        instances: List of sub-module instances.
        port_map: Mapping of port connections.
        attributes: Additional attributes for the chip.
        clock_domains: Dictionary of clock domain configurations.
    """

    def __init__(
        self,
        name: str,
        ports: Optional[List[Wire]] = None,
        parameters: Optional[Dict[str, Any]] = None,
        attributes: Optional[Dict[str, Any]] = None,
    ) -> None:
        """Initialize a Chip instance.
        
        Args:
            name: The name identifier of the chip.
            ports: List of port wires.
            parameters: Dictionary of parameter values.
            attributes: Additional attributes for the chip.
        """
        self.name: str = name
        self.ports: List[Wire] = ports or []
        self.parameters: Dict[str, Any] = parameters or {}
        self.internal_wires: List[Wire] = []
        self.gates: List[Gate] = []
        self.instances: List[Dict[str, Any]] = []
        self.port_map: Dict[str, Any] = {}
        self.attributes: Dict[str, Any] = attributes or {}
        self.clock_domains: Dict[str, Any] = {}
        
        logger.info(f"Created chip '{name}' with {len(self.ports)} ports")
        
    def add_port(self, wire: Wire) -> None:
        """Add a port to the chip.
        
        Args:
            wire: The wire to add as a port.
        """
        self.ports.append(wire)
        logger.debug(f"Added port '{wire.name}' to chip '{self.name}'")
        
    def add_internal_wire(self, wire: Wire) -> None:
        """Add an internal wire to the chip.
        
        Args:
            wire: The wire to add as an internal signal.
        """
        self.internal_wires.append(wire)
        logger.debug(f"Added internal wire '{wire.name}' to chip '{self.name}'")
        
    def instantiate(
        self,
        module: Any,
        instance_name: str,
        port_map: Dict[str, Any],
        parameter_map: Optional[Dict[str, Any]] = None,
    ) -> None:
        """Instantiate a sub-module within this chip.
        
        Args:
            module: The module to instantiate.
            instance_name: Name for this instance.
            port_map: Mapping of port connections.
            parameter_map: Mapping of parameter values.
        """
        self.instances.append({
            'module': module,
            'name': instance_name,
            'port_map': port_map,
            'parameter_map': parameter_map or {}
        })
        logger.debug(f"Instantiated module '{module}' as '{instance_name}' in chip '{self.name}'")

    def add_gate(self, gate: Gate) -> None:
        """Add a logic gate to the chip.
        
        Args:
            gate: The gate to add to the chip.
        """
        self.gates.append(gate)
        logger.debug(f"Added gate '{gate.name}' to chip '{self.name}'")
        
    def simulate(self, inputs: Dict[Wire, int]) -> Dict[str, int]:
        """Simulate the chip functionality.
        
        Args:
            inputs: Dictionary mapping input wires to their values.
            
        Returns:
            Dictionary containing all output port names and their values.
            
        Raises:
            ValueError: If an input wire is not found in the chip's ports.
        """
        # Validate inputs
        for wire in inputs:
            if wire not in self.ports or wire.direction != "input":
                raise ValueError(f"Wire '{wire.name}' is not an input port of chip '{self.name}'")
        
        # Reset all signals to 0
        for wire in self.ports + self.internal_wires:
            wire.value = 0
            
        # Set input values
        for wire, value in inputs.items():
            wire.value = value
            
        # Simulate all gates
        for gate in self.gates:
            gate.simulate()
            
        # Collect output results
        results: Dict[str, int] = {}
        for wire in self.ports:
            if wire.direction == "output":
                results[wire.name] = wire.value
                
        logger.info(f"Chip '{self.name}' simulation completed: {results}")
        return results
        
    def to_verilog(self) -> str:
        """Generate Verilog code for the chip.
        
        Returns:
            Complete Verilog module code for the chip.
        """
        verilog = f"module {self.name} (\n"
        
        # Port declarations
        ports = [wire.name for wire in self.ports]
        verilog += "  " + ",\n  ".join(ports) + "\n);\n\n"
        
        # Port definitions
        for wire in self.ports:
            if wire.direction == "input":
                verilog += f"  input [{wire.width-1}:0] {wire.name};\n"
            elif wire.direction == "output":
                verilog += f"  output [{wire.width-1}:0] {wire.name};\n"
            elif wire.direction == "inout":
                verilog += f"  inout [{wire.width-1}:0] {wire.name};\n"
                
        verilog += "\n"
        
        # Internal signal definitions
        for wire in self.internal_wires:
            verilog += f"  wire [{wire.width-1}:0] {wire.name};\n"
            
        verilog += "\n"
        
        # Gate connections
        for gate in self.gates:
            verilog += "  " + gate.to_verilog() + "\n"
            
        verilog += "endmodule\n"
        return verilog

    def generate_truth_table(self) -> str:
        """Generate a truth table for the circuit.
        
        Returns:
            String containing the formatted truth table.
        """
        # Get all input and output ports
        input_ports = [wire for wire in self.ports if wire.direction == "input"]
        output_ports = [wire for wire in self.ports if wire.direction == "output"]
        
        if not input_ports or not output_ports:
            return "没有足够的输入/输出端口来生成真值表"
        
        # Generate all possible input combinations
        input_combinations = []
        num_combinations = 2 ** len(input_ports)
        
        for i in range(num_combinations):
            combination = {}
            for j, port in enumerate(input_ports):
                # Extract bit value from binary representation
                bit_value = (i >> j) & 1
                combination[port] = bit_value
            input_combinations.append(combination)
        
        # Generate table header
        table = "真值表:\n"
        header = " | ".join([f"{port.name}" for port in input_ports]) + " | "
        header += " | ".join([f"{port.name}" for port in output_ports])
        table += header + "\n"
        table += "-" * len(header) + "\n"
        
        # Simulate each input combination and record results
        for inputs in input_combinations:
            # Reset all signals
            for wire in self.ports + self.internal_wires:
                wire.value = 0
                
            # Run simulation
            result = self.simulate(inputs)
            
            # Add row
            row = " | ".join([f"{inputs[port]}" for port in input_ports]) + " | "
            row += " | ".join([f"{result[port.name]}" for port in output_ports])
            table += row + "\n"
        
        return table
    
    def __str__(self) -> str:
        """Return string representation of the chip.
        
        Returns:
            String representation showing chip name and component counts.
        """
        return f"Chip('{self.name}', {len(self.ports)} ports, {len(self.gates)} gates, {len(self.internal_wires)} internal wires)"
