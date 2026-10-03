"""
Proterol Operators Family Omega (Livro V & Livro IX).
Operators are the transformational verbs of the ontology: A =[omega]=> B.
"""

from __future__ import annotations
from enum import Enum
from dataclasses import dataclass
from typing import Dict, List, Optional


class OperatorFamily(str, Enum):
    ONTOLOGICAL = "ontological"      # be, have, make
    RELATIONAL = "relational"        # map, link, split, join, change
    EPISTEMIC = "epistemic"          # measure, infer, test, learn, simulate, prove
    COMPUTATIONAL = "computational"  # compile, render, query, tokenize
    SEMIURGIC = "semiurgic"          # amplify, invert, dissolve, merge, transmute, resonate, anchor


@dataclass(frozen=True)
class Operator:
    name: str
    symbol: str
    family: OperatorFamily
    description: str
    signature: str

    def __str__(self) -> str:
        return self.name

    def __repr__(self) -> str:
        return f"Operator({self.name}, symbol='{self.symbol}', family={self.family.value})"


OPERATOR_DEFS: List[Operator] = [
    # Ontological
    Operator("be", "≡", OperatorFamily.ONTOLOGICAL, "Identity or ontological equivalence", "A -> A"),
    Operator("have", "∋", OperatorFamily.ONTOLOGICAL, "Attribute or possession relation", "A -> Property"),
    Operator("make", "⊳", OperatorFamily.ONTOLOGICAL, "Generative instantiation or production", "A -> Artifact"),

    # Relational
    Operator("map", "↦", OperatorFamily.RELATIONAL, "Homomorphic transformation or projection", "A -> B"),
    Operator("link", "⟷", OperatorFamily.RELATIONAL, "Bidirectional relational coupling", "A <-> B"),
    Operator("split", "⑂", OperatorFamily.RELATIONAL, "Decomposition into subcomponents", "A -> (A1, A2)"),
    Operator("join", "⨁", OperatorFamily.RELATIONAL, "Composition or union of structures", "(A, B) -> C"),
    Operator("change", "Δ", OperatorFamily.RELATIONAL, "State mutation across time or context", "S(t) -> S(t+1)"),

    # Epistemic
    Operator("measure", "μ", OperatorFamily.EPISTEMIC, "Quantification or metric extraction", "A -> Metric"),
    Operator("infer", "⊢", OperatorFamily.EPISTEMIC, "Logical or probabilistic inference", "Premises -> Conclusion"),
    Operator("test", "?", OperatorFamily.EPISTEMIC, "Falsification or verification check", "Hypothesis x Evidence -> Bool"),
    Operator("learn", "λ", OperatorFamily.EPISTEMIC, "Parameter updating from evidence", "Prior x Evidence -> Posterior"),
    Operator("simulate", "∿", OperatorFamily.EPISTEMIC, "Hypothetical execution over world model", "State x Policy -> Trajectory"),
    Operator("prove", "∎", OperatorFamily.EPISTEMIC, "Construction of a formal proof object", "Gamma |- Proposition -> Proof"),

    # Computational
    Operator("compile", "⚙", OperatorFamily.COMPUTATIONAL, "Lowering semantic AST to target runtime", "AST -> TargetIR"),
    Operator("render", "🖵", OperatorFamily.COMPUTATIONAL, "Synthesizing multimodal world representation", "Construct -> World"),
    Operator("query", "⌕", OperatorFamily.COMPUTATIONAL, "Semantic search across knowledge graph", "Graph x Query -> Matches"),
    Operator("tokenize", "🜏", OperatorFamily.COMPUTATIONAL, "Crystallizing semantic gene into verified token", "Gene -> Token"),

    # Semiurgic (Glyphtionary / Omni Laboratory)
    Operator("amplify", "▲", OperatorFamily.SEMIURGIC, "Scaling intensity or salience of a sign", "Sign -> Sign+"),
    Operator("invert", "▼", OperatorFamily.SEMIURGIC, "Reflecting sign to its dual or shadow", "Sign -> Sign*"),
    Operator("dissolve", "░", OperatorFamily.SEMIURGIC, "Decoupling rigid form into fluid potential", "Construct -> Atoms"),
    Operator("merge", "⋈", OperatorFamily.SEMIURGIC, "Synthesizing two signs into an emergent whole", "(S1, S2) -> S3"),
    Operator("transmute", "🜂", OperatorFamily.SEMIURGIC, "Cross-substrate ontological phase change", "Sign_A -> Sign_B"),
    Operator("resonate", "≋", OperatorFamily.SEMIURGIC, "Harmonic synchronization between disparate nodes", "Node1 ~ Node2"),
    Operator("anchor", "⚓", OperatorFamily.SEMIURGIC, "Grounding abstract meaning into persistent evidence", "Concept -> GroundedFact"),
]

OPERATORS: Dict[str, Operator] = {op.name: op for op in OPERATOR_DEFS}
OPERATORS_BY_SYMBOL: Dict[str, Operator] = {op.symbol: op for op in OPERATOR_DEFS}


def get_operator(key: str) -> Operator:
    norm = key.strip().lower()
    if norm in OPERATORS:
        return OPERATORS[norm]
    if key in OPERATORS_BY_SYMBOL:
        return OPERATORS_BY_SYMBOL[key]
    # Default to relational generic map if unknown
    return Operator(name=norm, symbol="->", family=OperatorFamily.RELATIONAL,
                    description=f"User-defined operator '{norm}'", signature="A -> B")
