"""OpenChipEDA Example - Digital Circuit Simulation.

This example demonstrates how to use OpenChipEDA to create and simulate
digital circuits, including various gate types and circuit configurations.
"""

import logging
from src.eda_simulator_base import (
    AndGate,
    Chip,
    NandGate,
    NorGate,
    NotGate,
    OrGate,
    Wire,
    XorGate,
)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def create_simple_circuit() -> Chip:
    """Create a simple AND-NOT circuit.
    
    Returns:
        A chip implementing the function: out = NOT(AND(a, b))
    """
    # Define signal wires with support for multi-bit, direction, and attributes
    a = Wire("a", width=1, direction="input")
    b = Wire("b", width=1, direction="input")
    and_ab = Wire("and_ab", width=1)
    out = Wire("out", width=1, direction="output")

    # Define gates
    and1 = AndGate("and1", [a, b], [and_ab])
    not1 = NotGate("not1", [and_ab], [out])

    # Assemble the chip
    chip = Chip("SimpleChip", attributes={"author": "OpenChipEDA"})
    chip.add_port(a)  # Input port
    chip.add_port(b)  # Input port
    chip.add_internal_wire(and_ab)  # Internal signal
    chip.add_port(out)  # Output port
    chip.add_gate(and1)
    chip.add_gate(not1)
    
    return chip


def create_xor_circuit() -> Chip:
    """Create an XOR circuit using basic gates.
    
    Returns:
        A chip implementing XOR using AND, OR, and NOT gates.
    """
    # Define wires
    a = Wire("a", width=1, direction="input")
    b = Wire("b", width=1, direction="input")
    not_a = Wire("not_a", width=1)
    not_b = Wire("not_b", width=1)
    and1_out = Wire("and1_out", width=1)
    and2_out = Wire("and2_out", width=1)
    out = Wire("out", width=1, direction="output")

    # Define gates: XOR = (NOT a AND b) OR (a AND NOT b)
    not1 = NotGate("not1", [a], [not_a])
    not2 = NotGate("not2", [b], [not_b])
    and1 = AndGate("and1", [not_a, b], [and1_out])
    and2 = AndGate("and2", [a, not_b], [and2_out])
    or1 = OrGate("or1", [and1_out, and2_out], [out])

    # Assemble the chip
    chip = Chip("XorChip", attributes={"description": "XOR using basic gates"})
    chip.add_port(a)
    chip.add_port(b)
    chip.add_internal_wire(not_a)
    chip.add_internal_wire(not_b)
    chip.add_internal_wire(and1_out)
    chip.add_internal_wire(and2_out)
    chip.add_port(out)
    chip.add_gate(not1)
    chip.add_gate(not2)
    chip.add_gate(and1)
    chip.add_gate(and2)
    chip.add_gate(or1)
    
    return chip


def create_parity_checker() -> Chip:
    """Create a 3-bit parity checker circuit.
    
    Returns:
        A chip that outputs 1 when the number of 1s in inputs is odd.
    """
    # Define wires
    a = Wire("a", width=1, direction="input")
    b = Wire("b", width=1, direction="input")
    c = Wire("c", width=1, direction="input")
    out = Wire("out", width=1, direction="output")

    # Use XOR for parity (XOR of all inputs)
    xor1 = XorGate("xor1", [a, b, c], [out])

    # Assemble the chip
    chip = Chip("ParityChecker", attributes={"description": "3-bit parity checker"})
    chip.add_port(a)
    chip.add_port(b)
    chip.add_port(c)
    chip.add_port(out)
    chip.add_gate(xor1)
    
    return chip


def main() -> None:
    """Main function demonstrating various circuit examples."""
    print("=== OpenChipEDA Circuit Simulation Examples ===\n")
    
    # Example 1: Simple AND-NOT circuit
    print("1. Simple AND-NOT Circuit (out = NOT(AND(a, b)))")
    print("=" * 50)
    chip1 = create_simple_circuit()
    
    # Simulate with different inputs
    inputs = {chip1.ports[0]: 1, chip1.ports[1]: 0}  # a=1, b=0
    result = chip1.simulate(inputs)
    print(f"Simulation result: {result}")
    
    # Generate truth table
    print("\nTruth table:")
    print(chip1.generate_truth_table())
    
    # Example 2: XOR circuit
    print("\n\n2. XOR Circuit using basic gates")
    print("=" * 50)
    chip2 = create_xor_circuit()
    
    # Test XOR functionality
    test_inputs = [
        ({chip2.ports[0]: 0, chip2.ports[1]: 0}, 0),
        ({chip2.ports[0]: 0, chip2.ports[1]: 1}, 1),
        ({chip2.ports[0]: 1, chip2.ports[1]: 0}, 1),
        ({chip2.ports[0]: 1, chip2.ports[1]: 1}, 0),
    ]
    
    for inputs, expected in test_inputs:
        result = chip2.simulate(inputs)
        actual = result[chip2.ports[2].name]
        print(f"XOR({list(inputs.values())[0]}, {list(inputs.values())[1]}) = {actual} (expected: {expected})")
    
    # Example 3: Parity checker
    print("\n\n3. 3-bit Parity Checker")
    print("=" * 50)
    chip3 = create_parity_checker()
    
    # Test parity functionality
    test_inputs = [
        ({chip3.ports[0]: 0, chip3.ports[1]: 0, chip3.ports[2]: 0}, 0),  # 0 ones
        ({chip3.ports[0]: 1, chip3.ports[1]: 0, chip3.ports[2]: 0}, 1),  # 1 one
        ({chip3.ports[0]: 1, chip3.ports[1]: 1, chip3.ports[2]: 0}, 0),  # 2 ones
        ({chip3.ports[0]: 1, chip3.ports[1]: 1, chip3.ports[2]: 1}, 1),  # 3 ones
    ]
    
    for inputs, expected in test_inputs:
        result = chip3.simulate(inputs)
        actual = result[chip3.ports[3].name]
        input_values = list(inputs.values())
        print(f"Parity({input_values[0]}, {input_values[1]}, {input_values[2]}) = {actual} (expected: {expected})")
    
    # Example 4: Verilog generation
    print("\n\n4. Verilog Code Generation")
    print("=" * 50)
    print("Generated Verilog for SimpleChip:")
    print(chip1.to_verilog())
    
    print("\nGenerated Verilog for XorChip:")
    print(chip2.to_verilog())
    
    print("\nGenerated Verilog for ParityChecker:")
    print(chip3.to_verilog())
    
    # Example 5: Demonstrate new gate types
    print("\n\n5. New Gate Types Demonstration")
    print("=" * 50)
    
    # Test NAND gate
    a = Wire("a", width=1)
    b = Wire("b", width=1)
    out = Wire("out", width=1)
    nand_gate = NandGate("nand1", [a, b], [out])
    
    a.value = 1
    b.value = 1
    nand_gate.simulate()
    print(f"NAND(1, 1) = {out.value} (expected: 0)")
    
    # Test NOR gate
    nor_gate = NorGate("nor1", [a, b], [out])
    a.value = 0
    b.value = 0
    nor_gate.simulate()
    print(f"NOR(0, 0) = {out.value} (expected: 1)")
    
    print("\n=== Examples completed successfully! ===")


if __name__ == "__main__":
    main()