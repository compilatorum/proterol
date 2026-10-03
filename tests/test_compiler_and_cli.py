"""
Tests for Proterol Compiler, Organism, Transducer, and Hermeneutics.
"""

from proterol.pipeline.compiler import ProterolCompiler
from proterol.pipeline.transducer import Transducer
from proterol.hermeneutics.functor import HermeneuticFunctor, HumanIntent, MachineState
from proterol.organism.compilatorum import CompilatorumOrganism


def test_compiler_10_stages():
    source = """
    gene DataLake : Data {
        sign: "💾" ;
        meaning: "Lakehouse storage" ;
        operators: [query, anchor] ;
    }

    gene Oracle : Process {
        sign: "🔮" ;
        meaning: "Ecological reasoning" ;
        operators: [simulate, test] ;
    }

    DataLake =[query]=> Oracle ;
    """
    compiler = ProterolCompiler()
    res = compiler.compile(source, construct_id="TestPipeline")

    assert len(res.feedback_notes) == 10
    assert res.construct.id == "TestPipeline"
    assert res.proof_carrying_construct.verify() is True
    assert res.token.level.value == "N4_Construct"
    assert "💾" in res.rendered_markdown
    assert "@context" in res.verifiable_credential


def test_transducer_loss_tracking():
    td = Transducer()
    res = td.natural_language_to_proterol("The agent perceives signals from the environment. Then it acts.")
    assert res.target_language == "Proterol"
    assert res.loss_delta != ""
    assert res.ambiguity_score > 0.0


def test_hermeneutic_functor_spiral():
    hf = HermeneuticFunctor()
    intent = HumanIntent(
        purpose="Criar agrofloresta sintrópica em código",
        metaphor="Floresta como máquina estocástica regenerativa",
    )
    rep = hf.h2a(intent)
    assert len(rep.hypotheses) >= 1

    state = MachineState(graph_size=12, active_constructs=["OracleForest"], evidence_collected=["hash123"])
    synth = hf.a2h(state)
    assert "coherent across 12 nodes" in synth.synthesis


def test_compilatorum_organism():
    org = CompilatorumOrganism()
    assert "compilatum" in org.nodes
    assert "oracle" in org.nodes
    assert "value-curator" in org.nodes

    graph = org.to_semantic_graph()
    assert len(graph.genes) >= 20
    assert len(graph.nexuses) >= 10

    # Path from corpora to value-curator
    path = graph.get_nexus_path("corpora", "value-curator")
    assert path is not None
    assert len(path) >= 3
