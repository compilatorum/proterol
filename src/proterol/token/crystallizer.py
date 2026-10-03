"""
Crystallizer: Semantic Tokenization Engine (Seções III, X, XVIII, XIX & Livro XI).
NFT != JPEG -> NFT = Identity + Metadata + Semantics + Provenance + Interfaces.
Crystallizes Semantic Genes and Constructs into N0-N5 Genetic Tokens with ERC-721/1155/6551 compliance.
"""

from __future__ import annotations
import json
import hashlib
from enum import Enum
from dataclasses import dataclass, field, asdict
from typing import Dict, Any, List, Optional, Union

from proterol.core.gene import SemanticGene
from proterol.machines.semiurgic import Construct
from proterol.proof.checker import ProofCarryingConstruct


class TokenLevel(str, Enum):
    N0_ATOM = "N0_Atom"           # NFT_0 = g
    N1_MOTIF = "N1_Motif"         # NFT_1 = g1 (+) g2
    N2_SKILL = "N2_Skill"         # NFT_2 = {g1, ..., gn} + Omega
    N3_AGENT = "N3_Agent"         # NFT_3 = Genome + Runtime
    N4_CONSTRUCT = "N4_Construct" # NFT_4 = Agent + Data + Workflow + Interface
    N5_ECOSYSTEM = "N5_Ecosystem" # NFT_5 = Sum(Construct_i) + Relations + Treasury + Governance


@dataclass
class TokenBoundAccount:
    """ERC-6551 Token Bound Account representation."""
    implementation: str = "0x2D25602551487E34bcd6A126e854D202863B5418"
    chain_id: int = 1  # Ethereum mainnet or L2
    token_contract: str = "0xCompilatorumProterolRegistry"
    token_id: int = 1
    tba_address: str = ""

    def __post_init__(self):
        if not self.tba_address:
            # Deterministic simulation of ERC-6551 create2 address
            h = hashlib.sha256(f"{self.chain_id}:{self.token_contract}:{self.token_id}".encode()).hexdigest()
            self.tba_address = f"0x{h[:40]}"


@dataclass
class CrystallizedToken:
    """
    NFT as Crystallized Semantic Gene Carrier.
    """
    token_id: int
    level: TokenLevel
    name: str
    symbol: str
    description: str
    semantic_fingerprint: str
    genes: List[str]
    operators: List[str]
    provenance_uri: str
    license: str
    erc_standard: str = "ERC-1155"
    token_bound_account: Optional[TokenBoundAccount] = None
    properties: Dict[str, Any] = field(default_factory=dict)
    raw_metadata: Dict[str, Any] = field(default_factory=dict)

    def generate_svg_glyph(self) -> str:
        """
        Generate an algorithmic SVG glyph representing the crystallized semantic state.
        """
        color_map = {
            TokenLevel.N0_ATOM: "#3b82f6",       # Blue
            TokenLevel.N1_MOTIF: "#8b5cf6",      # Purple
            TokenLevel.N2_SKILL: "#ec4899",      # Pink
            TokenLevel.N3_AGENT: "#10b981",      # Emerald
            TokenLevel.N4_CONSTRUCT: "#f59e0b",  # Amber
            TokenLevel.N5_ECOSYSTEM: "#ef4444",  # Red
        }
        accent = color_map.get(self.level, "#6366f1")
        svg = f"""<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 400 400" width="100%" height="100%">
  <defs>
    <radialGradient id="bg" cx="50%" cy="50%" r="70%">
      <stop offset="0%" stop-color="#0f172a" />
      <stop offset="100%" stop-color="#020617" />
    </radialGradient>
    <filter id="glow" x="-20%" y="-20%" width="140%" height="140%">
      <feGaussianBlur stdDeviation="6" result="blur" />
      <feComposite in="SourceGraphic" in2="blur" operator="over" />
    </filter>
  </defs>
  <rect width="400" height="400" fill="url(#bg)" rx="24"/>
  <circle cx="200" cy="200" r="140" fill="none" stroke="{accent}" stroke-width="2" stroke-dasharray="6 4" opacity="0.4" />
  <circle cx="200" cy="200" r="100" fill="none" stroke="{accent}" stroke-width="3" filter="url(#glow)"/>
  <text x="200" y="215" font-family="monospace" font-size="54" fill="{accent}" font-weight="bold" text-anchor="middle" filter="url(#glow)">{self.symbol[:4]}</text>
  <text x="200" y="320" font-family="sans-serif" font-size="14" fill="#94a3b8" text-anchor="middle" letter-spacing="2">PROTEROL {self.level.value.upper()}</text>
  <text x="200" y="345" font-family="monospace" font-size="11" fill="#64748b" text-anchor="middle">#{self.token_id:04d} • {self.semantic_fingerprint[:12]}</text>
</svg>"""
        return svg

    def to_erc721_metadata(self) -> Dict[str, Any]:
        """Standard OpenSea / ERC-721 / ERC-1155 metadata schema."""
        attributes = [
            {"trait_type": "Token Level", "value": self.level.value},
            {"trait_type": "Gene Count", "value": len(self.genes)},
            {"trait_type": "License", "value": self.license},
            {"trait_type": "Semantic Fingerprint", "value": self.semantic_fingerprint},
        ]
        if self.token_bound_account:
            attributes.append({"trait_type": "ERC-6551 Account", "value": self.token_bound_account.tba_address})

        for op in self.operators:
            attributes.append({"trait_type": "Operator", "value": op})

        return {
            "name": f"{self.name} #{self.token_id}",
            "description": self.description,
            "image": f"data:image/svg+xml;utf8,{self.generate_svg_glyph()}",
            "external_url": f"https://compilatorum.org/proterol/tokens/{self.token_id}",
            "attributes": attributes,
            "proterol_semantics": {
                "genes": self.genes,
                "operators": self.operators,
                "provenance": self.provenance_uri,
            },
        }

    def recombine(self, other: CrystallizedToken, new_id: int) -> CrystallizedToken:
        """
        Recombination algebra: NFT_A (+) NFT_B -> Construct_{AB} (Seção XVIII).
        """
        combined_genes = sorted(list(set(self.genes + other.genes)))
        combined_ops = sorted(list(set(self.operators + other.operators)))
        fp = hashlib.sha256(f"{self.semantic_fingerprint}:{other.semantic_fingerprint}".encode()).hexdigest()

        return CrystallizedToken(
            token_id=new_id,
            level=TokenLevel.N4_CONSTRUCT if self.level != TokenLevel.N5_ECOSYSTEM else TokenLevel.N5_ECOSYSTEM,
            name=f"{self.name} ⊕ {other.name}",
            symbol="⊕",
            description=f"Recombined semantic token from #{self.token_id} and #{other.token_id}",
            semantic_fingerprint=fp,
            genes=combined_genes,
            operators=combined_ops,
            provenance_uri=f"{self.provenance_uri}+{other.provenance_uri}",
            license=self.license,
            erc_standard="ERC-6551",
            token_bound_account=TokenBoundAccount(token_id=new_id),
        )


class Crystallizer:
    """
    Engine for crystallizing genes, constructs, and agents into genetic tokens.
    Respects the Metacritique (Livro XIX): Tokenize(x) <=> Identity + Utility + Provenance + Circulation Rationale.
    """

    def __init__(self, start_id: int = 1):
        self.next_token_id = start_id

    def check_metacritical_eligibility(self, has_identity: bool, has_utility: bool,
                                        has_provenance: bool, has_circulation_rationale: bool) -> bool:
        """
        Livro XIX: Nem tudo é NFT.
        Tokenize(x) <==> Identity + Utility + Provenance + Circulation.
        """
        return has_identity and has_utility and has_provenance and has_circulation_rationale

    def crystallize_gene(self, gene: SemanticGene, force: bool = False) -> CrystallizedToken:
        """Crystallize N0 (Atom) token from a SemanticGene."""
        eligible = self.check_metacritical_eligibility(
            has_identity=bool(gene.id),
            has_utility=bool(gene.omega),
            has_provenance=bool(gene.pi.source_uri),
            has_circulation_rationale=True,
        )
        if not eligible and not force:
            raise ValueError(f"Gene '{gene.id}' fails metacritical tokenization criteria.")

        tid = self.next_token_id
        self.next_token_id += 1

        return CrystallizedToken(
            token_id=tid,
            level=TokenLevel.N0_ATOM,
            name=f"Gene: {gene.id}",
            symbol=gene.sigma or "GENE",
            description=f"Proterol Semantic Gene Atom: {gene.mu}",
            semantic_fingerprint=gene.fingerprint(),
            genes=[gene.id],
            operators=gene.omega,
            provenance_uri=gene.pi.source_uri,
            license=gene.lambda_,
            erc_standard="ERC-1155",
        )

    def crystallize_construct(self, construct_or_pcc: Union[Construct, ProofCarryingConstruct],
                              level: TokenLevel = TokenLevel.N4_CONSTRUCT) -> CrystallizedToken:
        """Crystallize construct or proof-carrying construct into N1..N5 token."""
        construct = construct_or_pcc.construct if isinstance(construct_or_pcc, ProofCarryingConstruct) else construct_or_pcc
        
        tid = self.next_token_id
        self.next_token_id += 1

        all_ops = []
        for g in construct.genes:
            all_ops.extend(g.omega)
        unique_ops = sorted(list(set(all_ops)))

        serialized = json.dumps(construct.to_dict(), sort_keys=True)
        fp = hashlib.sha256(serialized.encode()).hexdigest()

        return CrystallizedToken(
            token_id=tid,
            level=level,
            name=construct.name,
            symbol="🜏",
            description=f"Crystallized Proterol Construct with {len(construct.genes)} genes",
            semantic_fingerprint=fp,
            genes=[g.id for g in construct.genes],
            operators=unique_ops,
            provenance_uri=construct.environment.get("source", "compilatorum://proterol"),
            license="MIT",
            erc_standard="ERC-6551",
            token_bound_account=TokenBoundAccount(token_id=tid),
        )
