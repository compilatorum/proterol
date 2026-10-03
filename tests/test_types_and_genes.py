"""
Tests for Proterol Types, Epistemic Lattice, and Semantic Genes.
"""

import pytest
from proterol.core.types import ProterolType, EpistemicStatus, EpistemicValue
from proterol.core.gene import SemanticGene, GeneProvenance
from proterol.core.operators import get_operator, OPERATORS


def test_fundamental_types():
    assert ProterolType.ENTITY.value == "Entity"
    assert ProterolType.CONSTRUCT.value == "Construct"
    assert ProterolType.LANGUAGE.value == "Language"
    assert ProterolType.from_str("concept") == ProterolType.CONCEPT
    assert ProterolType.from_str("proof") == ProterolType.PROOF


def test_epistemic_metacritique():
    # Livro XIX: WellFormed != Valid != True != Useful != Valuable
    status = EpistemicStatus(
        is_well_formed=True,
        is_valid=True,
        truth=EpistemicValue.TRUE,
        is_useful=True,
        is_valuable=True,
    )
    assert status.validate_separation() is True

    # Ambiguous != Invalid
    ambig_status = EpistemicStatus(
        is_well_formed=True,
        is_valid=True,
        truth=EpistemicValue.AMBIGUOUS,
    )
    assert ambig_status.is_valid is True
    assert ambig_status.truth == EpistemicValue.AMBIGUOUS

    # Unknown != False
    unk_status = EpistemicStatus(
        is_well_formed=True,
        is_valid=True,
        truth=EpistemicValue.UNKNOWN,
    )
    assert unk_status.truth != EpistemicValue.FALSE


def test_semantic_gene_creation_and_fingerprint():
    gene = SemanticGene(
        id="CognitiveCore",
        tau=ProterolType.AGENT,
        sigma="🧠",
        omega=["infer", "test", "reflect"],
        mu="Capacidade de inferência dedutiva",
        kappa=["min_confidence > 0.8"],
        lambda_="MIT",
    )
    fp1 = gene.fingerprint()
    assert isinstance(fp1, str)
    assert len(fp1) == 64  # SHA-256

    # Determinism check
    fp2 = gene.fingerprint()
    assert fp1 == fp2


def test_gene_composition():
    # g1 (+) g2 -> g_composite
    g1 = SemanticGene(
        id="Perception",
        tau=ProterolType.PROCESS,
        sigma="👁️",
        omega=["measure"],
        mu="Sensor intake",
    )
    g2 = SemanticGene(
        id="Reasoning",
        tau=ProterolType.PROCESS,
        sigma="🧠",
        omega=["infer"],
        mu="Deductive inference",
    )
    composite = g1.compose(g2)
    assert composite.id == "Perception+Reasoning"
    assert "measure" in composite.omega
    assert "infer" in composite.omega
    assert composite.pi.parent_gene_ids == ["Perception", "Reasoning"]
