"""
Máquina Simbólica (M_s: Sigma* -> AST).
Seção IV.1 & Livro IV: Transforma sequências de signos/texto em Árvore Sintática Abstrata (AST).
"""

from __future__ import annotations
import re
from dataclasses import dataclass, field
from typing import List, Dict, Any, Optional

from proterol.core.types import ProterolType


@dataclass
class ASTNode:
    line_number: int = 1


@dataclass
class GeneNode(ASTNode):
    id: str = ""
    tau: str = "Concept"
    sigma: str = ""
    mu: str = ""
    omega: List[str] = field(default_factory=list)
    kappa: List[str] = field(default_factory=list)
    license: str = "CC-BY-SA-4.0"
    attributes: Dict[str, Any] = field(default_factory=dict)


@dataclass
class NexusNode(ASTNode):
    source: str = ""
    target: str = ""
    operator: str = "map"
    label: Optional[str] = None
    attributes: Dict[str, Any] = field(default_factory=dict)


@dataclass
class ConstructNode(ASTNode):
    id: str = ""
    gene_components: List[str] = field(default_factory=list)
    attributes: Dict[str, Any] = field(default_factory=dict)


@dataclass
class JudgementNode(ASTNode):
    context: str = "Gamma"
    subject: str = ""
    type_or_prop: str = ""
    proof: Optional[str] = None


@dataclass
class AxiomNode(ASTNode):
    name: str = ""
    content: str = ""


@dataclass
class ProgramNode(ASTNode):
    genes: List[GeneNode] = field(default_factory=list)
    nexuses: List[NexusNode] = field(default_factory=list)
    constructs: List[ConstructNode] = field(default_factory=list)
    judgements: List[JudgementNode] = field(default_factory=list)
    axioms: List[AxiomNode] = field(default_factory=list)


class SymbolicMachine:
    """
    M_s: Sigma* -> AST
    Parses textual Proterol notation into a structured AST.
    """

    # Nexus regex: A =[operator]=> B or A =[operator "label"]=> B or A -> B
    NEXUS_PATTERN = re.compile(
        r'^\s*([A-Za-z0-9_./-]+)\s*(?:=\[(\w+)(?:\s+"([^"]+)")?\]=>|-->|->)\s*([A-Za-z0-9_./-]+)(?:\s*;\s*)?$',
        re.MULTILINE
    )

    # Judgement regex: Context |- Subject : Type or Subject |- Subject : Type
    JUDGEMENT_PATTERN = re.compile(
        r'^\s*([A-Za-z0-9_]+)\s*(?:\|-|\u22a2)\s*([A-Za-z0-9_]+)\s*:\s*([A-Za-z0-9_]+)(?:\s*;\s*)?$',
        re.MULTILINE
    )

    # Construct regex: construct Id = g1 (+) g2 (+) g3
    CONSTRUCT_PATTERN = re.compile(
        r'^\s*construct\s+([A-Za-z0-9_-]+)\s*=\s*(.+?)(?:\s*;\s*)?$',
        re.MULTILINE
    )

    # Axiom regex: axiom Name = "Content"
    AXIOM_PATTERN = re.compile(
        r'^\s*axiom\s+([A-Za-z0-9_-]+)\s*=\s*"([^"]+)"(?:\s*;\s*)?$',
        re.MULTILINE
    )

    def parse(self, text: str) -> ProgramNode:
        program = ProgramNode()
        lines = text.splitlines()

        i = 0
        while i < len(lines):
            line = lines[i].strip()
            # Ignore comments and empty lines
            if not line or line.startswith("//") or line.startswith("#"):
                i += 1
                continue

            # 1. Judgement (e.g. Proterol |- Proterol : Language or Gamma |- e : tau)
            judg_match = self.JUDGEMENT_PATTERN.match(line)
            if judg_match:
                ctx, subj, typ = judg_match.groups()
                program.judgements.append(
                    JudgementNode(line_number=i + 1, context=ctx, subject=subj, type_or_prop=typ)
                )
                i += 1
                continue

            # 2. Axiom
            axiom_match = self.AXIOM_PATTERN.match(line)
            if axiom_match:
                name, content = axiom_match.groups()
                program.axioms.append(
                    AxiomNode(line_number=i + 1, name=name, content=content)
                )
                i += 1
                continue

            # 3. Construct definition
            const_match = self.CONSTRUCT_PATTERN.match(line)
            if const_match:
                cid, raw_expr = const_match.groups()
                # Split on (+) or + or \oplus
                genes = [g.strip() for g in re.split(r'\(\+\)|\+|\u2295', raw_expr) if g.strip()]
                program.constructs.append(
                    ConstructNode(line_number=i + 1, id=cid, gene_components=genes)
                )
                i += 1
                continue

            # 4. Nexus (A =[op]=> B)
            nexus_match = self.NEXUS_PATTERN.match(line)
            if nexus_match:
                src, op, lbl, tgt = nexus_match.groups()
                op_name = op if op else "map"
                program.nexuses.append(
                    NexusNode(
                        line_number=i + 1,
                        source=src,
                        target=tgt,
                        operator=op_name,
                        label=lbl,
                    )
                )
                i += 1
                continue

            # 5. Gene Block: gene <id> : <type> { ... }
            if line.startswith("gene "):
                gene_hdr_match = re.match(r'^gene\s+([A-Za-z0-9_-]+)\s*:\s*([A-Za-z0-9_]+)\s*\{?', line)
                if gene_hdr_match:
                    gid, gtype = gene_hdr_match.groups()
                    gene_node = GeneNode(line_number=i + 1, id=gid, tau=gtype)
                    # Accumulate block lines until '}'
                    block_content: List[str] = []
                    if "{" in line and "}" in line:
                        # Single-line gene block
                        inner = line[line.find("{") + 1 : line.rfind("}")]
                        block_content.append(inner)
                    else:
                        i += 1
                        while i < len(lines):
                            cur = lines[i].strip()
                            if "}" in cur:
                                break
                            block_content.append(cur)
                            i += 1
                    
                    self._populate_gene_fields(gene_node, "\n".join(block_content))
                    program.genes.append(gene_node)
                    i += 1
                    continue

            i += 1

        return program

    def _populate_gene_fields(self, gene: GeneNode, body: str) -> None:
        for raw_entry in re.split(r'[;\n]', body):
            entry = raw_entry.strip()
            if not entry or entry.startswith("//"):
                continue
            if ":" in entry:
                k, v = entry.split(":", 1)
                k = k.strip().lower()
                v = v.strip().strip('"\'')
                if k == "sign" or k == "sigma":
                    gene.sigma = v
                elif k == "meaning" or k == "mu" or k == "sense":
                    gene.mu = v
                elif k == "license" or k == "lambda":
                    gene.license = v
                elif k == "operators" or k == "omega":
                    ops = [op.strip().strip('"\'') for op in re.sub(r'[\[\]]', '', v).split(',') if op.strip()]
                    gene.omega = ops
                elif k == "constraints" or k == "kappa":
                    caps = [c.strip().strip('"\'') for c in re.sub(r'[\[\]]', '', v).split(',') if c.strip()]
                    gene.kappa = caps
                else:
                    gene.attributes[k] = v
