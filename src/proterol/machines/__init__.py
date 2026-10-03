"""
Proterol Overlapping Machines:
M_s (Symbolic): Sigma* -> AST
M_m (Semantic): AST -> G
M_sigma (Semiurgic): G x Omega -> K
M_v (Virtual): K -> W
"""

from proterol.machines.symbolic import SymbolicMachine, ProgramNode
from proterol.machines.semantic import SemanticMachine, SemanticGraph
from proterol.machines.semiurgic import SemiurgicMachine, Construct, Capability
from proterol.machines.virtual import VirtualMachine

__all__ = [
    "SymbolicMachine",
    "ProgramNode",
    "SemanticMachine",
    "SemanticGraph",
    "SemiurgicMachine",
    "Construct",
    "Capability",
    "VirtualMachine",
]
