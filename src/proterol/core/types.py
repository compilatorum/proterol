"""
Proterol Types & Epistemic Lattice.
Livro II (Ontologia) & Livro XIX (Metacrítica).
"""

from __future__ import annotations
from enum import Enum
from dataclasses import dataclass
from typing import Optional, Set


class ProterolType(str, Enum):
    """
    Fundamental Proterol types (Livro II — Ontologia).
    Every element in Proterol is a typed object: x : tau.
    """
    ENTITY = "Entity"
    CONCEPT = "Concept"
    RELATION = "Relation"
    PROCESS = "Process"
    STATE = "State"
    PROPERTY = "Property"
    EVENT = "Event"
    AGENT = "Agent"
    DATA = "Data"
    RULE = "Rule"
    PROOF = "Proof"
    ARTIFACT = "Artifact"
    CONTEXT = "Context"
    CONSTRUCT = "Construct"
    # Meta-type for self-reflection (Livro XII: Proterol |- Proterol : Language)
    LANGUAGE = "Language"

    @classmethod
    def from_str(cls, val: str) -> ProterolType:
        norm = val.strip().capitalize()
        for member in cls:
            if member.value.lower() == norm.lower():
                return member
        raise ValueError(f"Unknown ProterolType: '{val}'. Expected one of {[m.value for m in cls]}")


class Modality(str, Enum):
    """
    Semantic manifest modalities (Livro III — Semiótica).
    mu -> {text, math, code, glyph, image, audio, graph}
    """
    TEXT = "text"
    MATH = "math"
    CODE = "code"
    GLYPH = "glyph"
    IMAGE = "image"
    AUDIO = "audio"
    GRAPH = "graph"


class EpistemicValue(str, Enum):
    """
    Epistemic truth-values respecting the three metacritiques:
    - Unknown != False
    - Ambiguous != Invalid
    """
    TRUE = "true"
    FALSE = "false"
    UNKNOWN = "unknown"
    AMBIGUOUS = "ambiguous"


@dataclass(frozen=True)
class EpistemicStatus:
    """
    The 5 distinct dimensions of evaluation (Livro XIX):
    WellFormed != Valid != True != Useful != Valuable
    """
    is_well_formed: bool
    is_valid: bool
    truth: EpistemicValue = EpistemicValue.UNKNOWN
    is_useful: Optional[bool] = None
    is_valuable: Optional[bool] = None
    notes: str = ""

    def validate_separation(self) -> bool:
        """
        Enforce the metacritical invariant:
        Formalizable(P) does not imply True(P).
        WellFormed does not automatically imply Valid, True, or Valuable.
        """
        # If not well formed, it cannot be formally valid
        if not self.is_well_formed and self.is_valid:
            return False
        return True

    def __repr__(self) -> str:
        return (
            f"EpistemicStatus(well_formed={self.is_well_formed}, "
            f"valid={self.is_valid}, truth={self.truth.value}, "
            f"useful={self.is_useful}, valuable={self.is_valuable})"
        )
