"""Tests for all gate types.

This module contains tests for all logic gate types including AND, OR, NOT,
XOR, NAND, and NOR gates.
"""

from typing import TYPE_CHECKING

import pytest

from src.eda_simulator_base import (
    AndGate,
    NandGate,
    NorGate,
    NotGate,
    OrGate,
    Wire,
    XorGate,
)

# Remove unnecessary pytest type imports since they're not used in this file

class TestLogicGates:
    """Test class for all logic gate types."""

    @pytest.fixture
    def basic_wires(self) -> tuple[Wire, Wire, Wire]:
        """Create basic wires for testing.
        
        Returns:
            Tuple containing input wires and output wire.
        """
        a = Wire("a", width=1)
        b = Wire("b", width=1)
        out = Wire("out", width=1)
        return a, b, out

    def test_and_gate(self, basic_wires: tuple[Wire, Wire, Wire]) -> None:
        """Test AND gate logic.
        
        Args:
            basic_wires: Fixture providing test wires.
        """
        a, b, out = basic_wires
        and_gate = AndGate("and1", [a, b], [out])
        
        # Test all input combinations
        test_cases = [
            (0, 0, 0),  # a=0, b=0, out=0
            (0, 1, 0),  # a=0, b=1, out=0
            (1, 0, 0),  # a=1, b=0, out=0
            (1, 1, 1),  # a=1, b=1, out=1
        ]
        
        for a_val, b_val, expected in test_cases:
            a.value = a_val
            b.value = b_val
            and_gate.simulate()
            assert out.value == expected, f"AND({a_val}, {b_val}) = {out.value}, expected {expected}"

    def test_or_gate(self, basic_wires: tuple[Wire, Wire, Wire]) -> None:
        """Test OR gate logic.
        
        Args:
            basic_wires: Fixture providing test wires.
        """
        a, b, out = basic_wires
        or_gate = OrGate("or1", [a, b], [out])
        
        # Test all input combinations
        test_cases = [
            (0, 0, 0),  # a=0, b=0, out=0
            (0, 1, 1),  # a=0, b=1, out=1
            (1, 0, 1),  # a=1, b=0, out=1
            (1, 1, 1),  # a=1, b=1, out=1
        ]
        
        for a_val, b_val, expected in test_cases:
            a.value = a_val
            b.value = b_val
            or_gate.simulate()
            assert out.value == expected, f"OR({a_val}, {b_val}) = {out.value}, expected {expected}"

    def test_not_gate(self, basic_wires: tuple[Wire, Wire, Wire]) -> None:
        """Test NOT gate logic.
        
        Args:
            basic_wires: Fixture providing test wires.
        """
        a, b, out = basic_wires
        not_gate = NotGate("not1", [a], [out])
        
        # Test both input values
        test_cases = [
            (0, 1),  # a=0, out=1
            (1, 0),  # a=1, out=0
        ]
        
        for a_val, expected in test_cases:
            a.value = a_val
            not_gate.simulate()
            assert out.value == expected, f"NOT({a_val}) = {out.value}, expected {expected}"

    def test_xor_gate(self, basic_wires: tuple[Wire, Wire, Wire]) -> None:
        """Test XOR gate logic.
        
        Args:
            basic_wires: Fixture providing test wires.
        """
        a, b, out = basic_wires
        xor_gate = XorGate("xor1", [a, b], [out])
        
        # Test all input combinations
        test_cases = [
            (0, 0, 0),  # a=0, b=0, out=0
            (0, 1, 1),  # a=0, b=1, out=1
            (1, 0, 1),  # a=1, b=0, out=1
            (1, 1, 0),  # a=1, b=1, out=0
        ]
        
        for a_val, b_val, expected in test_cases:
            a.value = a_val
            b.value = b_val
            xor_gate.simulate()
            assert out.value == expected, f"XOR({a_val}, {b_val}) = {out.value}, expected {expected}"

    def test_nand_gate(self, basic_wires: tuple[Wire, Wire, Wire]) -> None:
        """Test NAND gate logic.
        
        Args:
            basic_wires: Fixture providing test wires.
        """
        a, b, out = basic_wires
        nand_gate = NandGate("nand1", [a, b], [out])
        
        # Test all input combinations
        test_cases = [
            (0, 0, 1),  # a=0, b=0, out=1
            (0, 1, 1),  # a=0, b=1, out=1
            (1, 0, 1),  # a=1, b=0, out=1
            (1, 1, 0),  # a=1, b=1, out=0
        ]
        
        for a_val, b_val, expected in test_cases:
            a.value = a_val
            b.value = b_val
            nand_gate.simulate()
            assert out.value == expected, f"NAND({a_val}, {b_val}) = {out.value}, expected {expected}"

    def test_nor_gate(self, basic_wires: tuple[Wire, Wire, Wire]) -> None:
        """Test NOR gate logic.
        
        Args:
            basic_wires: Fixture providing test wires.
        """
        a, b, out = basic_wires
        nor_gate = NorGate("nor1", [a, b], [out])
        
        # Test all input combinations
        test_cases = [
            (0, 0, 1),  # a=0, b=0, out=1
            (0, 1, 0),  # a=0, b=1, out=0
            (1, 0, 0),  # a=1, b=0, out=0
            (1, 1, 0),  # a=1, b=1, out=0
        ]
        
        for a_val, b_val, expected in test_cases:
            a.value = a_val
            b.value = b_val
            nor_gate.simulate()
            assert out.value == expected, f"NOR({a_val}, {b_val}) = {out.value}, expected {expected}"

    def test_multi_input_and_gate(self) -> None:
        """Test AND gate with multiple inputs."""
        a = Wire("a", width=1)
        b = Wire("b", width=1)
        c = Wire("c", width=1)
        out = Wire("out", width=1)
        
        and_gate = AndGate("and3", [a, b, c], [out])
        
        # Test various combinations
        test_cases = [
            (0, 0, 0, 0),  # All 0s
            (1, 1, 1, 1),  # All 1s
            (1, 0, 1, 0),  # Mixed
            (0, 1, 0, 0),  # Mixed
        ]
        
        for a_val, b_val, c_val, expected in test_cases:
            a.value = a_val
            b.value = b_val
            c.value = c_val
            and_gate.simulate()
            assert out.value == expected, f"AND({a_val}, {b_val}, {c_val}) = {out.value}, expected {expected}"

    def test_multi_input_xor_gate(self) -> None:
        """Test XOR gate with multiple inputs (parity function)."""
        a = Wire("a", width=1)
        b = Wire("b", width=1)
        c = Wire("c", width=1)
        out = Wire("out", width=1)
        
        xor_gate = XorGate("xor3", [a, b, c], [out])
        
        # Test parity function (odd number of 1s = 1, even = 0)
        test_cases = [
            (0, 0, 0, 0),  # 0 ones
            (1, 0, 0, 1),  # 1 one
            (1, 1, 0, 0),  # 2 ones
            (1, 1, 1, 1),  # 3 ones
        ]
        
        for a_val, b_val, c_val, expected in test_cases:
            a.value = a_val
            b.value = b_val
            c.value = c_val
            xor_gate.simulate()
            assert out.value == expected, f"XOR({a_val}, {b_val}, {c_val}) = {out.value}, expected {expected}"

    def test_verilog_generation(self, basic_wires: tuple[Wire, Wire, Wire]) -> None:
        """Test Verilog code generation for all gate types.
        
        Args:
            basic_wires: Fixture providing test wires.
        """
        a, b, out = basic_wires
        
        # Test each gate type
        gates = [
            AndGate("and1", [a, b], [out]),
            OrGate("or1", [a, b], [out]),
            NotGate("not1", [a], [out]),
            XorGate("xor1", [a, b], [out]),
            NandGate("nand1", [a, b], [out]),
            NorGate("nor1", [a, b], [out]),
        ]
        
        for gate in gates:
            verilog = gate.to_verilog()
            assert "assign" in verilog
            assert out.name in verilog
            assert gate.name not in verilog  # Gate name shouldn't be in Verilog

    def test_gate_validation(self) -> None:
        """Test gate validation (empty inputs/outputs)."""
        wire = Wire("test", width=1)
        
        # Test empty inputs
        with pytest.raises(ValueError, match="at least one input"):
            AndGate("invalid", [], [wire])
        
        # Test empty outputs
        with pytest.raises(ValueError, match="at least one output"):
            AndGate("invalid", [wire], []) 