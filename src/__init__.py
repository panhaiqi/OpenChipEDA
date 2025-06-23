"""OpenChipEDA - Digital Circuit Simulation and EDA Platform.

A Python-based platform for digital circuit modeling, simulation, and EDA.
"""

from .eda_simulator_base import (
    AndGate,
    Chip,
    Gate,
    NandGate,
    NorGate,
    NotGate,
    OrGate,
    Wire,
    XorGate,
)

__version__ = "0.1.0"
__author__ = "OpenChipEDA Contributors"
__license__ = "GPL-2.0"

__all__ = [
    "Wire",
    "Gate",
    "AndGate",
    "OrGate",
    "NotGate",
    "XorGate",
    "NandGate",
    "NorGate",
    "Chip",
] 