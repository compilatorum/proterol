# 🜂 LIVRO IV — SINTAXE

> *"A sintaxe é o traçado dos caminhos possíveis pelo qual o significado pode viajar."*

---

## 1. A Unidade Sintática Fundamental: O Nexo

A unidade atômica da gramática Proterol é a declaração de transformação (o **nexo**):

$$A \xrightarrow{\omega} B$$

Na notação textual de máquina ($\Sigma^*$):

```proterol
Origem =[operador]=> Destino ;
```

onde:
- $A$ = Nó de origem (domínio);
- $B$ = Nó de destino (codomínio);
- $\omega$ = Operador de transformação em $\Omega$.

Podem ser anexados rótulos descritivos e atributos tipados:

```proterol
Corpus =[split "destilação léxica"]=> Atomos ;
```

---

## 2. Composição Categorial de Nexos

Os nexuses formam os morfismos de uma categoria. A composição é associativa e respeita o domínio/codomínio:

$$(A \xrightarrow{f} B) \circ (B \xrightarrow{g} C) \implies A \xrightarrow{g \circ f} C$$

```proterol
// Composição em cadeia
Corpus =[split]=> Atomos ;
Atomos =[map]=> Genes ;
Genes =[join]=> Constructo ;

// Morfismo composto inferido:
// Corpus =[ (join ∘ map ∘ split) ]=> Constructo ;
```

---

## 3. Declaração de Genes e Constructos

Um gene semântico é especificado como um bloco de atributos ontológicos:

```proterol
gene Reasoner : Agent {
    sign: "🧠" ;
    meaning: "Capacidade de inferência dedutiva e abdução causal" ;
    operators: [infer, test, reflect] ;
    constraints: ["min_confidence > 0.8"] ;
    license: "MIT" ;
}
```

E a composição de constructos por recombinação:

```proterol
construct SistemaOracular = Reasoner (+) Agrofloresta (+) Validador ;
```
