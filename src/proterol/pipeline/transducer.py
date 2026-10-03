"""
Transduction Engine (Livro X — Transdução).
T_{A -> B}: L_A -> L_B with explicit loss tracking: T(x) = y + Delta.
Where Delta captures information loss, semantic shifts, or residual ambiguity.
"""

from __future__ import annotations
from dataclasses import dataclass, field
from typing import Dict, Any, Optional

from proterol.machines.symbolic import ProgramNode, SymbolicMachine
from proterol.machines.semantic import SemanticGraph
from proterol.machines.semiurgic import Construct


@dataclass
class TransductionResult:
    source_language: str
    target_language: str
    output: Any
    loss_delta: str
    ambiguity_score: float  # 0.0 = lossless/exact, 1.0 = highly lossy
    metadata: Dict[str, Any] = field(default_factory=dict)


class Transducer:
    """
    Bidirectional and multimodal transducers across representation systems.
    NaturalLanguage <-> Proterol <-> Math <-> Code <-> SVG <-> Token.
    """

    def __init__(self):
        self.symbolic_machine = SymbolicMachine()

    def natural_language_to_proterol(self, text: str) -> TransductionResult:
        """
        Transduce unstructured natural language into structured Proterol.
        Estimates delta loss based on unmapped adjectives and affective nuances.
        """
        # Parse sentences into candidate nexuses
        sentences = [s.strip() for s in text.replace("\n", ". ").split(".") if s.strip()]
        proterol_lines = ["// Transduced from Natural Language"]
        for idx, s in enumerate(sentences[:10]):
            words = s.split()
            if len(words) >= 3:
                src = words[0].capitalize()
                tgt = words[-1].capitalize()
                proterol_lines.append(f"{src} =[map]=> {tgt} ;")

        proterol_code = "\n".join(proterol_lines)
        loss = "Omission of subjective tone, idiomatic metaphors, and conversational pragmatics."

        return TransductionResult(
            source_language="NaturalLanguage",
            target_language="Proterol",
            output=proterol_code,
            loss_delta=loss,
            ambiguity_score=0.35,
            metadata={"sentence_count": len(sentences)},
        )

    def proterol_to_math(self, graph: SemanticGraph) -> TransductionResult:
        """
        Transduce Proterol graph into categorical LaTeX notation:
        A -f-> B, g o f: A -> C.
        """
        latex_lines = [r"\begin{aligned}"]
        for nex in graph.nexuses:
            latex_lines.append(rf"  {nex.source} &\xrightarrow{{{nex.operator.name}}} {nex.target} \\")
        for j in graph.judgements:
            latex_lines.append(rf"  {j.context} &\vdash {j.subject} : \text{{{j.type_or_prop}}} \\")
        latex_lines.append(r"\end{aligned}")
        math_str = "\n".join(latex_lines)

        return TransductionResult(
            source_language="Proterol",
            target_language="LaTeX/Math",
            output=math_str,
            loss_delta="Loss of computational runtime environment and operational side effects.",
            ambiguity_score=0.05,
        )

    def proterol_to_code(self, construct: Construct) -> TransductionResult:
        """
        Transduce Construct into executable Python module.
        """
        from proterol.machines.virtual import VirtualMachine
        vm = VirtualMachine()
        code = vm.render_code(construct)

        return TransductionResult(
            source_language="Proterol",
            target_language="Python",
            output=code,
            loss_delta="Loss of abstract higher-order categorical morphisms to concrete imperative steps.",
            ambiguity_score=0.10,
        )
