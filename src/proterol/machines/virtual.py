"""
Máquina Virtual (M_v: K -> W).
Seção IV.4, Livro III & Livro X:
Transforma constructo K em mundos/manifestações renderizadas (W).
mu -> {text, math, code, glyph, graph, jsonld}.
"""

from __future__ import annotations
import json
from typing import Dict, Any, List

from proterol.machines.semiurgic import Construct


class VirtualMachine:
    """
    M_v: K -> W
    World Renderer: projects constructs into concrete multimodal artifacts.
    """

    def render_markdown(self, construct: Construct) -> str:
        """Render construct as rich Markdown documentation."""
        md = []
        md.append(f"# 🜂 Construct: {construct.name} (`{construct.id}`)\n")
        md.append(f"**State:** `{construct.state.get('status', 'unknown')}` | "
                  f"**Genes:** `{len(construct.genes)}` | "
                  f"**Capabilities:** `{len(construct.capabilities)}`\n")

        md.append("## 🧬 Semantic Genome (Genes)")
        md.append("| ID | Type (τ) | Sign (σ) | Meaning (μ) | Operators (Ω) | License (λ) |")
        md.append("|:---|:---|:---|:---|:---|:---|")
        for g in construct.genes:
            ops = ", ".join(g.omega) if g.omega else "—"
            md.append(f"| `{g.id}` | `{g.tau.value}` | `{g.sigma}` | {g.mu} | `{ops}` | `{g.lambda_}` |")
        md.append("")

        if construct.capabilities:
            md.append("## ⚙️ Operational Capabilities")
            md.append("| Capability | Type | Operation | Preconditions | Effects |")
            md.append("|:---|:---|:---|:---|:---|")
            for c in construct.capabilities:
                pre = ", ".join(c.preconditions) if c.preconditions else "—"
                eff = ", ".join(c.effects) if c.effects else "—"
                md.append(f"| `{c.name}` | `{c.tau.value}` | `{c.operation}` | `{pre}` | `{eff}` |")
            md.append("")

        if construct.transformations:
            md.append("## 🔀 Transformational Nexuses")
            md.append("```mermaid")
            md.append("flowchart LR")
            for t in construct.transformations:
                lbl = f"|{t.operator.symbol} {t.operator.name}|"
                md.append(f"    {t.source} -->{lbl} {t.target}")
            md.append("```\n")

        return "\n".join(md)

    def render_mermaid(self, construct: Construct) -> str:
        """Render Mermaid flowchart graph."""
        lines = ["flowchart TD"]
        for g in construct.genes:
            lines.append(f'    {g.id}["{g.sigma} ({g.id}): {g.tau.value}"]')
        for t in construct.transformations:
            lines.append(f'    {t.source} -->|"{t.operator.name}"| {t.target}')
        return "\n".join(lines)

    def render_jsonld(self, construct: Construct) -> str:
        """Render W3C JSON-LD graph."""
        graph_nodes = []
        for g in construct.genes:
            graph_nodes.append({
                "@id": f"proterol:gene:{g.id}",
                "@type": f"proterol:{g.tau.value}",
                "proterol:sign": g.sigma,
                "proterol:meaning": g.mu,
                "proterol:fingerprint": g.fingerprint(),
                "proterol:license": g.lambda_,
            })

        for t in construct.transformations:
            graph_nodes.append({
                "@type": "proterol:Nexus",
                "proterol:source": {"@id": f"proterol:gene:{t.source}"},
                "proterol:target": {"@id": f"proterol:gene:{t.target}"},
                "proterol:operator": t.operator.name,
            })

        doc = {
            "@context": {
                "proterol": "https://compilatorum.org/proterol/ontology#",
                "xsd": "http://www.w3.org/2001/XMLSchema#",
            },
            "@id": f"proterol:construct:{construct.id}",
            "@type": "proterol:Construct",
            "name": construct.name,
            "@graph": graph_nodes,
        }
        return json.dumps(doc, indent=2, ensure_ascii=False)

    def render_code(self, construct: Construct) -> str:
        """Render executable Python representation."""
        lines = [
            "# Auto-generated Proterol Executable Construct",
            f"# Construct ID: {construct.id}",
            "",
            "class ExecutableConstruct:",
            f"    id = '{construct.id}'",
            f"    name = '{construct.name}'",
            "",
            "    def __init__(self):",
            f"        self.genes = {json.dumps([g.id for g in construct.genes])}",
            f"        self.active = True",
            "",
            "    def execute(self, payload=None):",
            "        results = {}",
        ]
        for cap in construct.capabilities:
            lines.append(f"        # Capability: {cap.name}")
            lines.append(f"        results['{cap.name}'] = '{cap.operation}'")
        lines.append("        return results")
        lines.append("")
        lines.append("if __name__ == '__main__':")
        lines.append("    inst = ExecutableConstruct()")
        lines.append("    print('Running construct:', inst.name)")
        lines.append("    print(inst.execute())")
        return "\n".join(lines)
