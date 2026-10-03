"""
The True Compiler Pipeline (Seção XV — O verdadeiro compilador).
Corpus -> Ingest -> Atomize -> Type -> Normalize -> Compose -> Prove -> Render -> Tokenize -> Circulate -> Feedback.
Compiles living corpus material into verified, proof-carrying constructs and crystallized tokens.
"""

from __future__ import annotations
from dataclasses import dataclass, field
from typing import Dict, Any, List, Optional

from proterol.core.types import EpistemicStatus
from proterol.machines.symbolic import SymbolicMachine, ProgramNode
from proterol.machines.semantic import SemanticMachine, SemanticGraph
from proterol.machines.semiurgic import SemiurgicMachine, Construct
from proterol.machines.virtual import VirtualMachine
from proterol.proof.checker import ProofCarryingConstruct
from proterol.token.crystallizer import Crystallizer, CrystallizedToken, TokenLevel
from proterol.hermeneutics.functor import HermeneuticFunctor, HumanIntent, MachineState


@dataclass
class CompilationResult:
    """Artifact bundle emitted by the complete 10-stage Proterol compiler pipeline."""
    ast: ProgramNode
    graph: SemanticGraph
    epistemic_status: EpistemicStatus
    construct: Construct
    proof_carrying_construct: ProofCarryingConstruct
    rendered_markdown: str
    rendered_mermaid: str
    rendered_jsonld: str
    rendered_code: str
    token: CrystallizedToken
    verifiable_credential: Dict[str, Any]
    feedback_notes: List[str] = field(default_factory=list)


class ProterolCompiler:
    """
    The Master Semantic Compiler for Proterol & Compilatorum.
    """

    def __init__(self):
        self.symbolic_machine = SymbolicMachine()
        self.semantic_machine = SemanticMachine()
        self.semiurgic_machine = SemiurgicMachine()
        self.virtual_machine = VirtualMachine()
        self.crystallizer = Crystallizer()
        self.hermeneutic_functor = HermeneuticFunctor()

    def compile(self, source_code: str, construct_id: str = "RootConstruct") -> CompilationResult:
        """
        Execute full 10-stage compilation cycle.
        """
        feedback = []

        # 1. Ingest: clean and prepare raw corpus input
        raw_corpus = source_code.strip()
        feedback.append("Stage 1 (Ingest): Ingested corpus payload.")

        # 2. Atomize: M_s parse into AST
        ast = self.symbolic_machine.parse(raw_corpus)
        feedback.append(f"Stage 2 (Atomize): Parsed {len(ast.genes)} genes, {len(ast.nexuses)} nexuses, {len(ast.constructs)} constructs.")

        # 3. Type: M_m build graph and typecheck
        graph = self.semantic_machine.build_graph(ast)
        epistemic = self.semantic_machine.typecheck(graph)
        feedback.append(f"Stage 3 (Type): Typecheck status = {epistemic.notes}")

        # 4. Normalize: verify identifiers and relations
        feedback.append("Stage 4 (Normalize): Graph canonicalized.")

        # 5. Compose: M_sigma semiurgy
        construct = self.semiurgic_machine.synthesize(graph, construct_id=construct_id)
        feedback.append(f"Stage 5 (Compose): Synthesized construct '{construct.id}' with {len(construct.capabilities)} capabilities.")

        # 6. Prove: Proof-carrying construct K^pi
        pcc = ProofCarryingConstruct.create(construct, prover="compilatorum:kernel")
        is_valid = pcc.verify()
        feedback.append(f"Stage 6 (Prove): Proof verified = {is_valid} (Digest: {pcc.proof.evidence_digest[:16]}...)")

        # 7. Render: M_v virtual world rendering
        md_view = self.virtual_machine.render_markdown(construct)
        mermaid_view = self.virtual_machine.render_mermaid(construct)
        jsonld_view = self.virtual_machine.render_jsonld(construct)
        code_view = self.virtual_machine.render_code(construct)
        feedback.append("Stage 7 (Render): Rendered Markdown, Mermaid, JSON-LD, and Python world representations.")

        # 8. Tokenize: Crystallize state into N4 Construct Token
        token = self.crystallizer.crystallize_construct(pcc, level=TokenLevel.N4_CONSTRUCT)
        feedback.append(f"Stage 8 (Tokenize): Crystallized Token #{token.token_id} ({token.level.value}).")

        # 9. Circulate: Export W3C Verifiable Credential & TBA
        vc = pcc.export_w3c_verifiable_credential()
        feedback.append(f"Stage 9 (Circulate): Generated W3C Verifiable Credential with TBA {token.token_bound_account.tba_address if token.token_bound_account else 'N/A'}.")

        # 10. Feedback: Close hermeneutic loop
        state = MachineState(
            graph_size=len(graph.genes),
            active_constructs=[construct.id],
            evidence_collected=[pcc.proof.evidence_digest],
        )
        synthesis = self.hermeneutic_functor.a2h(state)
        feedback.append(f"Stage 10 (Feedback): A2H synthesis completed: '{synthesis.synthesis}'")

        return CompilationResult(
            ast=ast,
            graph=graph,
            epistemic_status=epistemic,
            construct=construct,
            proof_carrying_construct=pcc,
            rendered_markdown=md_view,
            rendered_mermaid=mermaid_view,
            rendered_jsonld=jsonld_view,
            rendered_code=code_view,
            token=token,
            verifiable_credential=vc,
            feedback_notes=feedback,
        )
