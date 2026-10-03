"""
PROTEROL — Language of Transformations, Executable Ontology & Semantic Genome
Root package for the Proterol implementation.
"""

__version__ = "0.1.0"
__author__ = "Compilatorum"
__license__ = "MIT"

from proterol.core.types import ProterolType, EpistemicStatus, Modality
from proterol.core.gene import SemanticGene, GeneProvenance
from proterol.core.nexus import Nexus
from proterol.core.operators import Operator, OPERATORS
from proterol.proof.checker import ProofCarryingConstruct, ProofReceipt
from proterol.token.crystallizer import Crystallizer, TokenLevel, CrystallizedToken
from proterol.pipeline.compiler import ProterolCompiler

__all__ = [
    "ProterolType",
    "EpistemicStatus",
    "Modality",
    "SemanticGene",
    "GeneProvenance",
    "Nexus",
    "Operator",
    "OPERATORS",
    "ProofCarryingConstruct",
    "ProofReceipt",
    "Crystallizer",
    "TokenLevel",
    "CrystallizedToken",
    "ProterolCompiler",
]
