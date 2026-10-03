"""
Máquina Semiúrgica (M_sigma: G x Omega -> K).
Seção IV.3, Livro IX & Seção VIII/IX:
Transforma grafo de significado e operadores em constructos executáveis (K).
glyph -> meaning -> operation -> construct.
"""

from __future__ import annotations
from dataclasses import dataclass, field
from typing import Dict, List, Any, Optional

from proterol.core.types import ProterolType
from proterol.core.gene import SemanticGene
from proterol.core.operators import Operator, get_operator
from proterol.core.nexus import Nexus
from proterol.machines.semantic import SemanticGraph


@dataclass
class Capability:
    """
    Capability = Type + Precondition + Operation + Effect + Evidence (Seção VIII)
    """
    name: str
    tau: ProterolType
    preconditions: List[str]
    operation: str
    effects: List[str]
    evidence_spec: str

    def to_dict(self) -> Dict[str, Any]:
        return {
            "name": self.name,
            "type": self.tau.value,
            "preconditions": self.preconditions,
            "operation": self.operation,
            "effects": self.effects,
            "evidence_spec": self.evidence_spec,
        }


@dataclass
class Construct:
    """
    Construct K: An operational semiurgic entity synthesized from semantic genes and operators.
    """
    id: str
    name: str
    genes: List[SemanticGene] = field(default_factory=list)
    capabilities: List[Capability] = field(default_factory=list)
    transformations: List[Nexus] = field(default_factory=list)
    environment: Dict[str, Any] = field(default_factory=dict)
    state: Dict[str, Any] = field(default_factory=dict)
    metadata: Dict[str, Any] = field(default_factory=dict)

    def gene_ids(self) -> List[str]:
        return [g.id for g in self.genes]

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "name": self.name,
            "gene_ids": self.gene_ids(),
            "genes": [g.to_dict() for g in self.genes],
            "capabilities": [c.to_dict() for c in self.capabilities],
            "transformations": [t.to_dict() for t in self.transformations],
            "environment": self.environment,
            "state": self.state,
            "metadata": self.metadata,
        }


class SemiurgicMachine:
    """
    M_sigma: G x Omega -> K
    Semiurgy: Sign x Operator x Context -> Construct.
    Instantiates active constructs from meaning graphs and operators.
    """

    def synthesize(self, graph: SemanticGraph, construct_id: str,
                   target_genes: Optional[List[str]] = None,
                   active_operators: Optional[List[str]] = None) -> Construct:
        """
        Synthesize a Construct K from target genes and operations in G.
        """
        selected_genes: List[SemanticGene] = []
        if target_genes:
            for gid in target_genes:
                if gid in graph.genes:
                    selected_genes.append(graph.genes[gid])
        else:
            selected_genes = list(graph.genes.values())

        # Collect capabilities derived from genes and their available operators
        capabilities: List[Capability] = []
        for g in selected_genes:
            for op_name in g.omega:
                op = get_operator(op_name)
                cap = Capability(
                    name=f"{g.id}_{op.name}",
                    tau=g.tau,
                    preconditions=[f"valid_gene({g.id})"] + g.kappa,
                    operation=f"{op.name}({g.sigma})",
                    effects=[f"produce_{op.name}_result({g.id})"],
                    evidence_spec=f"hash({g.fingerprint()}:{op.name})",
                )
                capabilities.append(cap)

        # Collect relevant transformations (edges involving these genes)
        gene_id_set = {g.id for g in selected_genes}
        relevant_nexuses = [
            n for n in graph.nexuses
            if n.source in gene_id_set or n.target in gene_id_set
        ]

        construct = Construct(
            id=construct_id,
            name=f"Construct_{construct_id}",
            genes=selected_genes,
            capabilities=capabilities,
            transformations=relevant_nexuses,
            environment={"source": "compilatorum_runtime", "version": "0.1.0"},
            state={"status": "synthesized", "active": True},
            metadata={"gene_count": len(selected_genes), "capability_count": len(capabilities)},
        )

        return construct
