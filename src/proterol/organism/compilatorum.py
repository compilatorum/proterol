"""
Compilatorum Formal Organism (Seção XI & XIV).
Maps the Compilatorum ecosystem repositories as typed semantic genes and constructs,
uniting them into a single living computational organism.
"""

from __future__ import annotations
from dataclasses import dataclass, field
from typing import Dict, List, Set, Optional

from proterol.core.types import ProterolType
from proterol.core.gene import SemanticGene, GeneProvenance
from proterol.core.nexus import Nexus
from proterol.core.operators import get_operator
from proterol.machines.semantic import SemanticGraph


@dataclass
class OrganismNode:
    name: str
    role_description: str
    glyph: str
    tau: ProterolType
    primary_operators: List[str]
    genes: List[str]
    dependencies: List[str] = field(default_factory=list)


COMPILATORUM_ECOSYSTEM: List[OrganismNode] = [
    OrganismNode("corpora", "Corpus multimodal e sedimentação cultural", "🧫", ProterolType.DATA,
                 ["query", "split", "anchor"], ["c_ling", "c_code", "c_math", "c_visual"]),
    OrganismNode("promptcraft", "Destilador e engenharia de intenções", "🧪", ProterolType.PROCESS,
                 ["infer", "measure", "amplify"], ["intent_refinement", "few_shot_distill"]),
    OrganismNode("glyphtionary", "Léxico, álgebra de signos e genoma semântico", "🔣", ProterolType.CONCEPT,
                 ["map", "transmute", "resonate"], ["semantic_atom", "glyph_algebra"]),
    OrganismNode("compilatum", "Monorepo-síntese e Meta-IR arqueológica", "🧠", ProterolType.CONSTRUCT,
                 ["compile", "join", "prove"], ["archeology_engine", "meta_ir"]),
    OrganismNode("cognitiv", "Metacognição e reflexão recursiva", "🪞", ProterolType.PROCESS,
                 ["reflect", "test", "change"], ["metacognition", "self_model"]),
    OrganismNode("SLM", "Modelo cognitivo leve e especializado", "🧬", ProterolType.AGENT,
                 ["infer", "learn", "simulate"], ["slm_inference", "compact_weights"]),
    OrganismNode("NaturalLanguageCognitiveArchitecture", "Arquitetura cognitiva em linguagem natural", "🧠", ProterolType.PROCESS,
                 ["map", "infer", "plan"], ["nl_reasoning", "executive_control"]),
    OrganismNode("emacs", "Ambiente de transcrição linguagem <-> código", "✍️", ProterolType.ARTIFACT,
                 ["compile", "link", "render"], ["editor_buffer", "lisp_bridge"]),
    OrganismNode("lakehouse", "Memória multimodal persistente e data lake", "💾", ProterolType.DATA,
                 ["anchor", "query", "have"], ["multimodal_storage", "delta_lake"]),
    OrganismNode("knowledge-weaver", "Tecer de grafos de conhecimento e hipervínculos", "🕸️", ProterolType.RELATION,
                 ["link", "join", "resonate"], ["graph_weave", "hyperedge_index"]),
    OrganismNode("oracle", "Agrofloresta computacional e curadoria hermenêutica", "🔮", ProterolType.PROCESS,
                 ["simulate", "measure", "transmute"], ["ecological_simulation", "curation_flow"]),
    OrganismNode("omni-laboratory", "Semiurgia, scene graph e renderização agêntica", "🎞️", ProterolType.CONSTRUCT,
                 ["render", "make", "amplify", "dissolve"], ["scene_graph", "manifold_render"]),
    OrganismNode("neurocoder", "Inteligência de código e autocompilação", "🤖", ProterolType.AGENT,
                 ["compile", "test", "infer"], ["code_synthesis", "ast_transform"]),
    OrganismNode("cadcad-explorer", "Simulação de dinâmicas de sistemas complexos", "🧮", ProterolType.PROCESS,
                 ["simulate", "measure", "test"], ["tokenomics_sim", "state_transition"]),
    OrganismNode("neurosimbolic-trader", "Decisão simbólico-quantitativa e mercado", "📈", ProterolType.AGENT,
                 ["infer", "measure", "change"], ["market_signals", "symbolic_policy"]),
    OrganismNode("DAO", "Governança descentralizada e tesouraria", "🏛️", ProterolType.ENTITY,
                 ["link", "join", "have"], ["voting_policy", "treasury_allocation"]),
    OrganismNode("value-curator", "Execução orientada por evidências e recibos criptográficos", "🛡️", ProterolType.PROOF,
                 ["prove", "test", "tokenize"], ["evidence_receipt", "deterministic_policy"]),
    OrganismNode("regenerativo", "Semântica ecológica e fluxos regenerativos", "🌱", ProterolType.CONCEPT,
                 ["resonate", "measure", "anchor"], ["bioregional_accounting", "carbon_cycles"]),
    OrganismNode("farcaster-nexus", "Comunicação e rede social descentralizada", "🌐", ProterolType.RELATION,
                 ["link", "map", "tokenize"], ["social_graph", "cast_provenance"]),
    OrganismNode("web3-launchpad", "Distribuição e mobilização de tokens", "🚀", ProterolType.PROCESS,
                 ["tokenize", "make", "link"], ["token_bonding_curve", "liquidity_nexus"]),
    OrganismNode("harness-engineering", "Ambiente de execução, harness e CI de agentes", "🧰", ProterolType.ARTIFACT,
                 ["test", "simulate", "compile"], ["agent_sandbox", "deterministic_eval"]),
    OrganismNode("molora", "Multiplicidade e adaptação de rank baixo", "🌀", ProterolType.CONCEPT,
                 ["split", "join", "learn"], ["adapter_routing", "manifold_lora"]),
    OrganismNode("kaelvive-reversa", "Espelhamento ontológico e engenharia reversa", "🪞", ProterolType.PROCESS,
                 ["invert", "dissolve", "infer"], ["reverse_ontology", "mirror_analysis"]),
    OrganismNode("InternalResources", "Recursos internos e assets de fundação", "⚡", ProterolType.DATA,
                 ["have", "anchor", "query"], ["foundational_specs", "private_assets"]),
    OrganismNode("planner", "Temporalização e agendamento de transformações", "⏳", ProterolType.PROCESS,
                 ["map", "change", "simulate"], ["temporal_dag", "schedule_engine"]),
]


class CompilatorumOrganism:
    """
    Formal coordinator modeling the Compilatorum repositories as a unified Proterol Semantic System.
    """

    def __init__(self):
        self.nodes = {n.name: n for n in COMPILATORUM_ECOSYSTEM}

    def to_semantic_graph(self) -> SemanticGraph:
        """
        Transform all nodes of the organism into a connected Proterol SemanticGraph.
        """
        graph = SemanticGraph()

        # Ingest nodes as semantic genes
        for node in self.nodes.values():
            gene = SemanticGene(
                id=node.name,
                tau=node.tau,
                sigma=node.glyph,
                omega=node.primary_operators,
                mu=node.role_description,
                pi=GeneProvenance(
                    source_uri=f"github.com/compilatorum/{node.name}",
                    author="compilatorum",
                ),
            )
            graph.add_gene(gene)

        # Build natural pipeline nexuses (Corpus -> Promptcraft -> Glyphtionary -> Compilatum -> ...)
        pipeline_sequence = [
            ("corpora", "promptcraft", "split", "Destilação de corpus"),
            ("promptcraft", "glyphtionary", "map", "Formalização léxica"),
            ("glyphtionary", "compilatum", "join", "Síntese no Meta-IR"),
            ("compilatum", "omni-laboratory", "make", "Renderização semiúrgica"),
            ("omni-laboratory", "oracle", "resonate", "Curadoria e agrofloresta"),
            ("oracle", "value-curator", "test", "Verificação por evidências"),
            ("value-curator", "DAO", "prove", "Validação de mandato"),
            ("DAO", "web3-launchpad", "tokenize", "Cristalização em tokens"),
            ("compilatum", "lakehouse", "anchor", "Persistência em lakehouse"),
            ("compilatum", "knowledge-weaver", "link", "Tecer do grafo de conhecimento"),
            ("knowledge-weaver", "oracle", "map", "Projeção ontológica no oráculo"),
            ("cadcad-explorer", "neurosimbolic-trader", "simulate", "Simulação de dinâmicas"),
            ("neurosimbolic-trader", "value-curator", "infer", "Decisão ancorada em prova"),
        ]

        for src, tgt, op_name, lbl in pipeline_sequence:
            if src in self.nodes and tgt in self.nodes:
                op = get_operator(op_name)
                graph.add_nexus(
                    Nexus(source=src, target=tgt, operator=op, label=lbl)
                )

        return graph

    def get_shared_genes(self, repo_a: str, repo_b: str) -> List[str]:
        """Check shared semantic genetic material between two repositories."""
        node_a = self.nodes.get(repo_a)
        node_b = self.nodes.get(repo_b)
        if not node_a or not node_b:
            return []
        return sorted(list(set(node_a.genes).intersection(set(node_b.genes))))

    def generate_organism_report(self) -> str:
        """Generate markdown summary of Compilatorum organism."""
        lines = [
            "# 🌳 Compilatorum — O Organismo Formal",
            "",
            "| Repositório | Glifo | Papel no Proterol | Tipo (τ) | Operadores Chave (Ω) |",
            "|:---|:---:|:---|:---|:---|",
        ]
        for n in self.nodes.values():
            ops = ", ".join(n.primary_operators)
            lines.append(f"| `{n.name}` | {n.glyph} | {n.role_description} | `{n.tau.value}` | `{ops}` |")
        lines.append("")
        return "\n".join(lines)
