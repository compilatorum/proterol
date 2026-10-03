"""
Semantic Gene (Livro II — O átomo: Semantic Gene).
g = <id, tau, sigma, omega, pi, mu, rho, kappa, lambda>
"""

from __future__ import annotations
import json
import hashlib
from dataclasses import dataclass, field, asdict
from typing import List, Dict, Any, Optional

from proterol.core.types import ProterolType
from proterol.core.operators import Operator, get_operator


@dataclass
class GeneProvenance:
    """
    pi (provenance): origin source, author/agent, parent genes, timestamp, and verification hash.
    """
    source_uri: str = "compilatorum://corpus"
    author: str = "compilatorum"
    parent_gene_ids: List[str] = field(default_factory=list)
    timestamp: str = ""
    evidence_hash: str = ""

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class SemanticGene:
    """
    The fundamental semantic genome atom:
    g = <id, tau, sigma, omega, pi, mu, rho, kappa, lambda>
    """
    id: str                                  # id: identity
    tau: ProterolType                        # tau: type
    sigma: str                               # sigma: sign / glyph / symbol
    omega: List[str] = field(default_factory=list)   # omega: available operators
    pi: GeneProvenance = field(default_factory=GeneProvenance)  # pi: provenance
    mu: str = ""                             # mu: meaning / semantic sense definition
    rho: Dict[str, Any] = field(default_factory=dict)   # rho: rendering rules
    kappa: List[str] = field(default_factory=list)      # kappa: constraints / invariants
    lambda_: str = "CC-BY-SA-4.0"            # lambda: license / conditions of use

    def operators(self) -> List[Operator]:
        return [get_operator(op) for op in self.omega]

    def fingerprint(self) -> str:
        """
        Deterministic SHA-256 fingerprint of the semantic gene.
        Ensures content-addressable verifiable identity.
        """
        payload = {
            "id": self.id,
            "tau": self.tau.value,
            "sigma": self.sigma,
            "omega": sorted(self.omega),
            "mu": self.mu,
            "kappa": sorted(self.kappa),
            "lambda": self.lambda_,
            "parent_genes": sorted(self.pi.parent_gene_ids),
        }
        serialized = json.dumps(payload, sort_keys=True)
        return hashlib.sha256(serialized.encode("utf-8")).hexdigest()

    def compose(self, other: SemanticGene, new_id: Optional[str] = None) -> SemanticGene:
        """
        Algebraic gene composition: g1 (+) g2 -> g_composite.
        Produces an N1 (Motif) or composite gene.
        """
        composite_id = new_id or f"{self.id}+{other.id}"
        combined_type = ProterolType.CONSTRUCT if self.tau != other.tau else self.tau
        combined_sigma = f"{self.sigma}⊕{other.sigma}"
        combined_omega = sorted(list(set(self.omega + other.omega)))
        combined_mu = f"Composition({self.mu} ⊕ {other.mu})"
        combined_rho = {**self.rho, **other.rho}
        combined_kappa = sorted(list(set(self.kappa + other.kappa)))
        combined_license = self.lambda_ if self.lambda_ == other.lambda_ else f"{self.lambda_}; {other.lambda_}"

        prov = GeneProvenance(
            source_uri=f"{self.pi.source_uri}+{other.pi.source_uri}",
            author=self.pi.author,
            parent_gene_ids=[self.id, other.id],
            evidence_hash=hashlib.sha256(f"{self.fingerprint()}:{other.fingerprint()}".encode()).hexdigest(),
        )

        return SemanticGene(
            id=composite_id,
            tau=combined_type,
            sigma=combined_sigma,
            omega=combined_omega,
            pi=prov,
            mu=combined_mu,
            rho=combined_rho,
            kappa=combined_kappa,
            lambda_=combined_license,
        )

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "tau": self.tau.value,
            "sigma": self.sigma,
            "omega": self.omega,
            "pi": self.pi.to_dict(),
            "mu": self.mu,
            "rho": self.rho,
            "kappa": self.kappa,
            "lambda": self.lambda_,
            "fingerprint": self.fingerprint(),
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> SemanticGene:
        prov_data = data.get("pi", {})
        prov = GeneProvenance(
            source_uri=prov_data.get("source_uri", "compilatorum://corpus"),
            author=prov_data.get("author", "compilatorum"),
            parent_gene_ids=prov_data.get("parent_gene_ids", []),
            timestamp=prov_data.get("timestamp", ""),
            evidence_hash=prov_data.get("evidence_hash", ""),
        )
        return cls(
            id=data["id"],
            tau=ProterolType.from_str(data.get("tau", "Concept")),
            sigma=data.get("sigma", ""),
            omega=data.get("omega", []),
            pi=prov,
            mu=data.get("mu", ""),
            rho=data.get("rho", {}),
            kappa=data.get("kappa", []),
            lambda_=data.get("lambda", data.get("lambda_", "CC-BY-SA-4.0")),
        )
