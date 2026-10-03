"""
Proterol CLI (Command Line Interface).
Comprehensive tooling for parsing, compiling, verifying proofs, rendering, tokenizing,
inspecting the Compilatorum organism, and consulting the 12 Books of the Codex.
"""

from __future__ import annotations
import sys
import os
import argparse
import json
from pathlib import Path

from proterol import __version__
from proterol.machines.symbolic import SymbolicMachine
from proterol.machines.semantic import SemanticMachine
from proterol.pipeline.compiler import ProterolCompiler
from proterol.organism.compilatorum import CompilatorumOrganism
from proterol.token.crystallizer import TokenLevel


CODEX_DIR = Path(__file__).resolve().parent.parent.parent.parent / "codex"


def cmd_parse(args: argparse.Namespace) -> None:
    path = Path(args.file)
    if not path.exists():
        print(f"Error: file '{path}' not found.", file=sys.stderr)
        sys.exit(1)
    content = path.read_text(encoding="utf-8")
    sm = SymbolicMachine()
    ast = sm.parse(content)
    print(f"=== M_s Symbolic Machine AST ===")
    print(f"Source: {path}")
    print(f"Genes:       {len(ast.genes)}")
    for g in ast.genes:
        print(f"  • [{g.tau}] {g.id} (σ: {g.sigma}) -> mu: {g.mu[:40]}...")
    print(f"Nexuses:     {len(ast.nexuses)}")
    for n in ast.nexuses:
        print(f"  • {n.source} =[{n.operator}]=> {n.target}")
    print(f"Constructs:  {len(ast.constructs)}")
    for c in ast.constructs:
        print(f"  • {c.id} = {' ⊕ '.join(c.gene_components)}")
    print(f"Judgements:  {len(ast.judgements)}")
    for j in ast.judgements:
        print(f"  • {j.context} ⊢ {j.subject} : {j.type_or_prop}")
    print(f"Axioms:      {len(ast.axioms)}")
    for ax in ast.axioms:
        print(f"  • axiom {ax.name}: \"{ax.content}\"")


def cmd_compile(args: argparse.Namespace) -> None:
    path = Path(args.file)
    if not path.exists():
        print(f"Error: file '{path}' not found.", file=sys.stderr)
        sys.exit(1)
    content = path.read_text(encoding="utf-8")
    compiler = ProterolCompiler()
    cid = args.construct_id or path.stem.capitalize()
    res = compiler.compile(content, construct_id=cid)

    print(f"🔮 Proterol 10-Stage Pipeline Completed for '{cid}'\n")
    for step in res.feedback_notes:
        print(f"  ✓ {step}")
    print("\n=== Crystallized Token Metadata ===")
    print(f"Token ID:    #{res.token.token_id}")
    print(f"Level:       {res.token.level.value}")
    print(f"Fingerprint: {res.token.semantic_fingerprint}")
    print(f"Standard:    {res.token.erc_standard}")
    if res.token.token_bound_account:
        print(f"ERC-6551:    {res.token.token_bound_account.tba_address}")

    if args.output:
        out_path = Path(args.output)
        out_path.write_text(res.rendered_markdown, encoding="utf-8")
        print(f"\nWritten rendered Markdown documentation to '{out_path}'")


def cmd_render(args: argparse.Namespace) -> None:
    path = Path(args.file)
    if not path.exists():
        print(f"Error: file '{path}' not found.", file=sys.stderr)
        sys.exit(1)
    content = path.read_text(encoding="utf-8")
    compiler = ProterolCompiler()
    res = compiler.compile(content)

    fmt = args.format.lower()
    if fmt == "markdown" or fmt == "md":
        print(res.rendered_markdown)
    elif fmt == "mermaid":
        print(res.rendered_mermaid)
    elif fmt == "jsonld" or fmt == "json":
        print(res.rendered_jsonld)
    elif fmt == "code" or fmt == "python":
        print(res.rendered_code)
    else:
        print(f"Unknown format: {args.format}. Choose markdown, mermaid, jsonld, or code.", file=sys.stderr)


def cmd_prove(args: argparse.Namespace) -> None:
    path = Path(args.file)
    if not path.exists():
        print(f"Error: file '{path}' not found.", file=sys.stderr)
        sys.exit(1)
    content = path.read_text(encoding="utf-8")
    compiler = ProterolCompiler()
    res = compiler.compile(content)
    pcc = res.proof_carrying_construct

    print(f"=== Proof-Carrying Construct (K^π) ===")
    print(f"Construct:     {pcc.construct.id}")
    print(f"Proposition:   {pcc.proof.proposition}")
    print(f"Prover:        {pcc.proof.prover}")
    print(f"Digest:        {pcc.proof.evidence_digest}")
    print(f"Verified:      {'✅ VALID' if pcc.verify() else '❌ TAMPERED / INVALID'}")
    print("\n--- W3C Verifiable Credential ---")
    print(json.dumps(pcc.export_w3c_verifiable_credential(), indent=2))


def cmd_organism(args: argparse.Namespace) -> None:
    org = CompilatorumOrganism()
    print(org.generate_organism_report())


def cmd_codex(args: argparse.Namespace) -> None:
    if not CODEX_DIR.exists():
        print(f"Codex directory not found at: {CODEX_DIR}", file=sys.stderr)
        return

    book_num = args.book
    if book_num is None:
        print("=== PROTEROL CODEX — Índice dos 12 Livros ===")
        books = sorted(list(CODEX_DIR.glob("Book_*.md")))
        for b in books:
            first_line = b.read_text(encoding="utf-8").splitlines()[0]
            print(f"  • {b.name}: {first_line}")
        print("\nUse `proterol codex <1..12>` para visualizar um livro específico.")
        return

    pattern = f"Book_{int(book_num):02d}_*.md"
    matches = list(CODEX_DIR.glob(pattern))
    if not matches:
        print(f"Livro {book_num} não encontrado no Codex.", file=sys.stderr)
        return

    target_book = matches[0]
    print(f"=== {target_book.name} ===\n")
    print(target_book.read_text(encoding="utf-8"))


def main() -> None:
    parser = argparse.ArgumentParser(
        prog="proterol",
        description="PROTEROL — Language of Transformations, Executable Ontology & Semantic Genome",
    )
    parser.add_argument("--version", action="version", version=f"proterol {__version__}")
    subparsers = parser.add_subparsers(dest="command", help="Sub-commands")

    # parse
    p_parse = subparsers.add_parser("parse", help="Parse Proterol script into AST (M_s)")
    p_parse.add_argument("file", help="Path to .pro file")
    p_parse.set_defaults(func=cmd_parse)

    # compile
    p_comp = subparsers.add_parser("compile", help="Execute 10-stage compilation cycle")
    p_comp.add_argument("file", help="Path to .pro file")
    p_comp.add_argument("--construct-id", "-c", help="ID for synthesized construct")
    p_comp.add_argument("--output", "-o", help="Output path for rendered Markdown")
    p_comp.set_defaults(func=cmd_compile)

    # render
    p_rend = subparsers.add_parser("render", help="Render construct into multimodal world formats (M_v)")
    p_rend.add_argument("file", help="Path to .pro file")
    p_rend.add_argument("--format", "-f", default="markdown", choices=["markdown", "mermaid", "jsonld", "code"])
    p_rend.set_defaults(func=cmd_render)

    # prove
    p_prove = subparsers.add_parser("prove", help="Verify proof receipt of a Proof-Carrying Construct (K^pi)")
    p_prove.add_argument("file", help="Path to .pro file")
    p_prove.set_defaults(func=cmd_prove)

    # organism
    p_org = subparsers.add_parser("organism", help="Inspect Compilatorum 46-repository formal organism")
    p_org.set_defaults(func=cmd_organism)

    # codex
    p_codex = subparsers.add_parser("codex", help="Read from the 12 Books of the Proterol Codex")
    p_codex.add_argument("book", nargs="?", type=int, help="Book number (1 to 12)")
    p_codex.set_defaults(func=cmd_codex)

    args = parser.parse_args()
    if not args.command:
        parser.print_help()
        sys.exit(0)

    args.func(args)


if __name__ == "__main__":
    main()
