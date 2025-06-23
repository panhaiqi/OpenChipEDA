"""Tests for basic chip functionality.

This module contains tests for the core chip simulation functionality,
including gate operations, chip simulation, and Verilog generation.
"""

from typing import TYPE_CHECKING, Dict

import pytest

from src.eda_simulator_base import AndGate, Chip, NotGate, Wire

class TestBasicChip:
    """Test class for basic chip functionality."""

    @pytest.fixture
    def simple_circuit(self) -> tuple[Wire, Wire, Wire, Wire, AndGate, NotGate, Chip]:
        """Create a simple circuit: out = NOT(AND(a, b)).
        
        Returns:
            Tuple containing all circuit components for testing.
        """
        # Build a simple circuit: out = NOT(AND(a, b))
        a = Wire("a", width=1, direction="input")
        b = Wire("b", width=1, direction="input")
        and_ab = Wire("and_ab", width=1)
        out = Wire("out", width=1, direction="output")
        and1 = AndGate("and1", [a, b], [and_ab])
        not1 = NotGate("not1", [and_ab], [out])

        chip = Chip("SimpleChip", ports=[a, b, out], attributes={"testcase": "basic"})
        # Add internal signal
        chip.add_internal_wire(and_ab)
        # Add gates
        chip.add_gate(and1)
        chip.add_gate(not1)
        
        return a, b, and_ab, out, and1, not1, chip

    def test_and_not_logic(self, simple_circuit: tuple[Wire, Wire, Wire, Wire, AndGate, NotGate, Chip]) -> None:
        """Test AND-NOT logic with all input combinations.
        
        Args:
            simple_circuit: Fixture providing circuit components.
        """
        a, b, and_ab, out, and1, not1, chip = simple_circuit
        
        # Test all input combinations
        test_vectors = [
            ({a: 0, b: 0}, 1),
            ({a: 0, b: 1}, 1),
            ({a: 1, b: 0}, 1),
            ({a: 1, b: 1}, 0),
        ]
        
        for inputs, expected_out in test_vectors:
            # Reset all signals before each test
            for wire in [a, b, and_ab, out]:
                wire.value = 0
                
            # Run simulation
            result = chip.simulate(inputs)
            assert result[out.name] == expected_out, (
                f"Input: {inputs}, Expected: {expected_out}, Got: {result[out.name]}"
            )

    def test_verilog_generation(self, simple_circuit: tuple[Wire, Wire, Wire, Wire, AndGate, NotGate, Chip]) -> None:
        """Test Verilog code generation.
        
        Args:
            simple_circuit: Fixture providing circuit components.
        """
        a, b, and_ab, out, and1, not1, chip = simple_circuit
        
        # Test Verilog code generation
        verilog = chip.to_verilog()
        
        # Verify module declaration exists
        assert f"module {chip.name}" in verilog
        
        # Verify port declarations exist
        for port in [a, b, out]:
            assert port.name in verilog
            
        # Verify internal signal declaration exists
        assert f"wire [{and_ab.width-1}:0] {and_ab.name}" in verilog
        
        # Verify gate connections exist
        assert f"assign {and_ab.name} =" in verilog
        assert f"assign {out.name} = ~{and_ab.name}" in verilog

    def test_truth_table_generation(self, simple_circuit: tuple[Wire, Wire, Wire, Wire, AndGate, NotGate, Chip]) -> None:
        """Test truth table generation.
        
        Args:
            simple_circuit: Fixture providing circuit components.
        """
        a, b, and_ab, out, and1, not1, chip = simple_circuit
        
        truth_table = chip.generate_truth_table()
        
        # Verify truth table contains expected content
        assert "真值表:" in truth_table
        assert a.name in truth_table
        assert b.name in truth_table
        assert out.name in truth_table
        
        # Verify all input combinations are present
        assert "0 | 0 | 1" in truth_table  # a=0, b=0, out=1
        assert "0 | 1 | 1" in truth_table  # a=0, b=1, out=1
        assert "1 | 0 | 1" in truth_table  # a=1, b=0, out=1
        assert "1 | 1 | 0" in truth_table  # a=1, b=1, out=0

    def test_invalid_input_wire(self, simple_circuit: tuple[Wire, Wire, Wire, Wire, AndGate, NotGate, Chip]) -> None:
        """Test that simulation raises error for invalid input wires.
        
        Args:
            simple_circuit: Fixture providing circuit components.
        """
        a, b, and_ab, out, and1, not1, chip = simple_circuit
        
        # Create an invalid wire that's not a port
        invalid_wire = Wire("invalid", width=1)
        
        with pytest.raises(ValueError, match="is not an input port"):
            chip.simulate({invalid_wire: 1})

    def test_wire_equality_and_hash(self) -> None:
        """Test wire equality and hash functionality."""
        wire1 = Wire("test", width=1)
        wire2 = Wire("test", width=2)  # Different width
        wire3 = Wire("other", width=1)  # Different name
        
        # Test equality
        assert wire1 == wire2  # Same name
        assert wire1 != wire3  # Different name
        
        # Test hash
        assert hash(wire1) == hash(wire2)  # Same name
        assert hash(wire1) != hash(wire3)  # Different name

    def test_gate_string_representation(self, simple_circuit: tuple[Wire, Wire, Wire, Wire, AndGate, NotGate, Chip]) -> None:
        """Test string representation of gates.
        
        Args:
            simple_circuit: Fixture providing circuit components.
        """
        a, b, and_ab, out, and1, not1, chip = simple_circuit
        
        assert str(and1) == "AndGate('and1')"
        assert str(not1) == "NotGate('not1')"

    def test_chip_string_representation(self, simple_circuit: tuple[Wire, Wire, Wire, Wire, AndGate, NotGate, Chip]) -> None:
        """Test string representation of chip.
        
        Args:
            simple_circuit: Fixture providing circuit components.
        """
        a, b, and_ab, out, and1, not1, chip = simple_circuit
        
        expected = "Chip('SimpleChip', 3 ports, 2 gates, 1 internal wires)"
        assert str(chip) == expected