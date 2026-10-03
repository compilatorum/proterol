"""
Proterol Nexus (Livro IV — Sintaxe & Teoria das Categorias).
Fundamental transformational nexus: A =[omega]=> B.
Categorical composition: (A -f-> B) o (B -g-> C) = A -(g o f)-> C.
"""

from __future__ import annotations
from dataclasses import dataclass, field
from typing import Optional, Dict, Any, List

from proterol.core.operators import Operator, get_operator


@dataclass
class Nexus:
    """
    A transformational morphism between representations or nodes:
    source =[operator]=> target
    """
    source: str
    target: str
    operator: Operator
    label: Optional[str] = None
    attributes: Dict[str, Any] = field(default_factory=dict)
    provenance_hash: Optional[str] = None

    def compose(self, next_nexus: Nexus, composite_label: Optional[str] = None) -> Nexus:
        """
        Categorical composition: self (A -> B) composed with next_nexus (B -> C).
        Raises ValueError if targets do not match (morphism domain check).
        """
        if self.target != next_nexus.source:
            raise ValueError(
                f"Morphism composition error: cannot compose '{self.source} -> {self.target}' "
                f"with '{next_nexus.source} -> {next_nexus.target}'. Domain mismatch: {self.target} != {next_nexus.source}"
            )

        composite_op_name = f"{next_nexus.operator.name}∘{self.operator.name}"
        composite_op = Operator(
            name=composite_op_name,
            symbol=f"{next_nexus.operator.symbol}∘{self.operator.symbol}",
            family=next_nexus.operator.family,
            description=f"Composite morphism of {self.operator.name} followed by {next_nexus.operator.name}",
            signature=f"{self.source} -> {next_nexus.target}",
        )

        return Nexus(
            source=self.source,
            target=next_nexus.target,
            operator=composite_op,
            label=composite_label or f"({next_nexus.label or next_nexus.operator.name} ∘ {self.label or self.operator.name})",
            attributes={**self.attributes, **next_nexus.attributes, "composed_from": [str(self), str(next_nexus)]},
        )

    def __str__(self) -> str:
        lbl = f" '{self.label}'" if self.label else ""
        return f"{self.source} =[{self.operator.name}{lbl}]=> {self.target}"

    def to_dict(self) -> Dict[str, Any]:
        return {
            "source": self.source,
            "target": self.target,
            "operator": self.operator.name,
            "operator_symbol": self.operator.symbol,
            "label": self.label,
            "attributes": self.attributes,
        }
