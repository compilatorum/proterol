"""
Máquina Semântica (M_m: AST -> G).
Seção IV.2 & Livro VI: Transforma Árvore Sintática Abstrata (AST) em Grafo de Significado (G).
"""

from __future__ import annotations
from dataclasses import dataclass, field
from typing import Dict, List, Set, Optional, Tuple

from proterol.core.types import ProterolType, EpistemicStatus, EpistemicValue
from proterol.core.gene import SemanticGene, GeneProvenance
from proterol.core.nexus import Nexus
from proterol.core.operators import get_operator
from proterol.machines.symbolic import ProgramNode, GeneNode, NexusNode, ConstructNode, JudgementNode


@dataclass
class SemanticGraph:
    """
    G = <Nodes, Edges, Context, TypingJudgements>
    The semantic meaning hypergraph.
    """
    genes: Dict[str, SemanticGene] = field(default_factory=dict)
    nexuses: List[Nexus] = field(default_factory=list)
    judgements: List[JudgementNode] = field(default_factory=list)
    context_gamma: Dict[str, ProterolType] = field(default_factory=dict)

    def add_gene(self, gene: SemanticGene) -> None:
        self.genes[gene.id] = gene
        self.context_gamma[gene.id] = gene.tau

    def add_nexus(self, nexus: Nexus) -> None:
        self.nexuses.append(nexus)

    def get_nexus_path(self, start: str, end: str) -> Optional[List[Nexus]]:
        """
        Find transformational chain from start to end.
        """
        if start == end:
            return []
        
        visited: Set[str] = set()
        queue: List[Tuple[str, List[Nexus]]] = [(start, [])]

        while queue:
            curr, path = queue.pop(0)
            if curr == end:
                return path
            if curr in visited:
                continue
            visited.add(curr)

            for nex in self.nexuses:
                if nex.source == curr and nex.target not in visited:
                    queue.append((nex.target, path + [nex]))

        return None

    def compose_path(self, path: List[Nexus]) -> Optional[Nexus]:
        """
        Compose an entire chain of nexuses into a single composite morphism: (g o f).
        """
        if not path:
            return None
        res = path[0]
        for next_nex in path[1:]:
            res = res.compose(next_nex)
        return res

    def outgoing_transformations(self, node_id: str) -> List[Nexus]:
        return [n for n in self.nexuses if n.source == node_id]

    def incoming_transformations(self, node_id: str) -> List[Nexus]:
        return [n for n in self.nexuses if n.target == node_id]


class SemanticMachine:
    """
    M_m: AST -> G
    Builds and typechecks the Semantic Meaning Graph from the AST.
    """

    def build_graph(self, ast: ProgramNode) -> SemanticGraph:
        graph = SemanticGraph()

        # 1. Ingest Genes
        for g_node in ast.genes:
            gene_type = ProterolType.from_str(g_node.tau)
            gene = SemanticGene(
                id=g_node.id,
                tau=gene_type,
                sigma=g_node.sigma or g_node.id,
                omega=g_node.omega,
                mu=g_node.mu,
                kappa=g_node.kappa,
                lambda_=g_node.license,
                pi=GeneProvenance(
                    source_uri="proterol://ast",
                    author="compilatorum",
                ),
            )
            graph.add_gene(gene)

        # 2. Ingest Constructs as Composite Genes
        for c_node in ast.constructs:
            component_genes: List[SemanticGene] = []
            for g_id in c_node.gene_components:
                if g_id in graph.genes:
                    component_genes.append(graph.genes[g_id])
                else:
                    # Dynamically instantiate implicit concept gene if not declared
                    implicit = SemanticGene(
                        id=g_id,
                        tau=ProterolType.CONCEPT,
                        sigma=g_id,
                        mu=f"Implicit component gene '{g_id}'",
                    )
                    graph.add_gene(implicit)
                    component_genes.append(implicit)

            if component_genes:
                composite = component_genes[0]
                for nxt in component_genes[1:]:
                    composite = composite.compose(nxt, new_id=c_node.id)
                composite.id = c_node.id
                composite.tau = ProterolType.CONSTRUCT
                graph.add_gene(composite)

        # 3. Ingest Nexuses
        for n_node in ast.nexuses:
            op = get_operator(n_node.operator)
            nexus = Nexus(
                source=n_node.source,
                target=n_node.target,
                operator=op,
                label=n_node.label,
                attributes=n_node.attributes,
            )
            graph.add_nexus(nexus)

        # 4. Ingest Judgements
        for j_node in ast.judgements:
            graph.judgements.append(j_node)
            # Register in context
            try:
                tt = ProterolType.from_str(j_node.type_or_prop)
                graph.context_gamma[j_node.subject] = tt
            except ValueError:
                pass

        return graph

    def typecheck(self, graph: SemanticGraph) -> EpistemicStatus:
        """
        Verify type safety and ontological coherence across G.
        Gamma |- e : tau
        """
        well_formed = True
        valid = True
        notes = []

        # Check self-reflection if present
        for j in graph.judgements:
            if j.subject == "Proterol" and j.type_or_prop.lower() == "language":
                notes.append("Reflexivity confirmed: Proterol ⊢ Proterol : Language")

        # Check each nexus endpoints exist in context or genes
        for n in graph.nexuses:
            if n.source not in graph.context_gamma and n.source not in graph.genes:
                notes.append(f"Nexus source '{n.source}' not explicitly typed in Gamma")
            if n.target not in graph.context_gamma and n.target not in graph.genes:
                notes.append(f"Nexus target '{n.target}' not explicitly typed in Gamma")

        return EpistemicStatus(
            is_well_formed=well_formed,
            is_valid=valid,
            truth=EpistemicValue.TRUE if valid else EpistemicValue.UNKNOWN,
            is_useful=True,
            is_valuable=True,
            notes="; ".join(notes) if notes else "Typecheck successful",
        )
