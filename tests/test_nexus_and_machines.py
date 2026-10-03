"""
Tests for Proterol Nexus Categorical Composition and the 4 Machines.
"""

import pytest
from proterol.core.nexus import Nexus
from proterol.core.operators import get_operator
from proterol.machines.symbolic import SymbolicMachine
from proterol.machines.semantic import SemanticMachine
from proterol.machines.semiurgic import SemiurgicMachine
from proterol.machines.virtual import VirtualMachine


def test_nexus_categorical_composition():
    # (A -f-> B) o (B -g-> C) = A -(g o f)-> C
    op_split = get_operator("split")
    op_map = get_operator("map")

    n1 = Nexus(source="Corpus", target="Atoms", operator=op_split, label="destilar")
    n2 = Nexus(source="Atoms", target="Genes", operator=op_map, label="mapear")

    composed = n1.compose(n2)
    assert composed.source == "Corpus"
    assert composed.target == "Genes"
    assert "map∘split" in composed.operator.name

    # Domain mismatch should raise ValueError
    n3 = Nexus(source="Different", target="World", operator=op_map)
    with pytest.raises(ValueError):
        n1.compose(n3)


def test_symbolic_machine_parser():
    code = """
    // Sample script
    Proterol |- Proterol : Language ;
    axiom Founder = "Não traduza apenas palavras." ;

    gene Alpha : Concept {
        sign: "α" ;
        meaning: "Início" ;
        operators: [make, map] ;
        license: "MIT" ;
    }

    Alpha =[make]=> Omega ;
    construct TestConstruct = Alpha ;
    """
    sm = SymbolicMachine()
    ast = sm.parse(code)

    assert len(ast.judgements) == 1
    assert ast.judgements[0].subject == "Proterol"
    assert len(ast.axioms) == 1
    assert len(ast.genes) == 1
    assert ast.genes[0].id == "Alpha"
    assert len(ast.nexuses) == 1
    assert ast.nexuses[0].source == "Alpha"
    assert ast.nexuses[0].target == "Omega"
    assert len(ast.constructs) == 1


def test_semantic_semiurgic_virtual_pipeline():
    code = """
    gene Sensor : Agent {
        sign: "📡" ;
        meaning: "Entrada sensorial" ;
        operators: [measure] ;
    }

    gene Actuator : Agent {
        sign: "🦾" ;
        meaning: "Atuador físico" ;
        operators: [change] ;
    }

    Sensor =[link]=> Actuator ;
    """
    sm = SymbolicMachine()
    ast = sm.parse(code)

    # M_m: AST -> G
    sem = SemanticMachine()
    graph = sem.build_graph(ast)
    assert len(graph.genes) == 2
    assert len(graph.nexuses) == 1

    status = sem.typecheck(graph)
    assert status.is_well_formed is True

    # M_sigma: G x Omega -> K
    semiurgic = SemiurgicMachine()
    construct = semiurgic.synthesize(graph, construct_id="RoboticFeedback")
    assert construct.id == "RoboticFeedback"
    assert len(construct.capabilities) >= 2

    # M_v: K -> W
    vm = VirtualMachine()
    md = vm.render_markdown(construct)
    mermaid = vm.render_mermaid(construct)
    jsonld = vm.render_jsonld(construct)
    code_out = vm.render_code(construct)

    assert "RoboticFeedback" in md
    assert "flowchart TD" in mermaid
    assert "@context" in jsonld
    assert "class ExecutableConstruct" in code_out
