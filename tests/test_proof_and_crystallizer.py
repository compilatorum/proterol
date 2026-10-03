"""
Tests for Proof-Carrying Constructs and Crystallizer Genetic Tokens.
"""

import pytest
from proterol.core.types import ProterolType
from proterol.core.gene import SemanticGene
from proterol.machines.semiurgic import Construct, Capability
from proterol.proof.checker import ProofCarryingConstruct
from proterol.token.crystallizer import Crystallizer, TokenLevel


def test_proof_carrying_construct_verification():
    gene = SemanticGene(
        id="EvidenceGene",
        tau=ProterolType.PROOF,
        sigma="🛡️",
        omega=["prove"],
        mu="Verificação criptográfica determinística",
        kappa=["audit_passed == true"],
    )
    construct = Construct(
        id="AuditedSystem",
        name="AuditedSystem",
        genes=[gene],
        capabilities=[Capability(name="cap1", tau=ProterolType.PROOF, preconditions=[], operation="prove()", effects=[], evidence_spec="audit")],
    )

    pcc = ProofCarryingConstruct.create(construct, prover="compilatorum:test-prover")
    assert pcc.verify() is True

    # Tampering check: modifying construct should invalidate verification
    construct.state["tampered"] = True
    assert pcc.verify() is False

    # Export W3C Verifiable Credential
    construct.state.pop("tampered")
    assert pcc.verify() is True
    vc = pcc.export_w3c_verifiable_credential()
    assert "VerifiableCredential" in vc["type"]
    assert "evidenceDigest" in vc["proof"]


def test_crystallizer_n0_to_n5():
    cr = Crystallizer(start_id=100)
    gene = SemanticGene(
        id="Atom1",
        tau=ProterolType.CONCEPT,
        sigma="⚛",
        omega=["map"],
        mu="Atomo conceitual",
    )

    # N0 Atom
    t0 = cr.crystallize_gene(gene)
    assert t0.token_id == 100
    assert t0.level == TokenLevel.N0_ATOM
    assert t0.erc_standard == "ERC-1155"

    # Construct N4
    construct = Construct(id="Const1", name="Const1", genes=[gene])
    t4 = cr.crystallize_construct(construct, level=TokenLevel.N4_CONSTRUCT)
    assert t4.token_id == 101
    assert t4.level == TokenLevel.N4_CONSTRUCT
    assert t4.token_bound_account is not None
    assert t4.token_bound_account.tba_address.startswith("0x")

    # Recombination: NFT_A (+) NFT_B -> Construct_{AB}
    t_recombined = t0.recombine(t4, new_id=200)
    assert t_recombined.token_id == 200
    assert "Atom1" in t_recombined.genes


def test_metacritique_tokenization_eligibility():
    cr = Crystallizer()
    # Missing utility and provenance
    g_invalid = SemanticGene(id="Empty", tau=ProterolType.CONCEPT, sigma="∅", omega=[])
    g_invalid.pi.source_uri = ""

    with pytest.raises(ValueError, match="metacritical"):
        cr.crystallize_gene(g_invalid, force=False)
