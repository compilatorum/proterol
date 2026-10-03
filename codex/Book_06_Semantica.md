# 🜂 LIVRO VI — SEMÂNTICA

> *"O significado de uma expressão nunca é intrínseco aos seus caracteres; é a função que ela desempenha em um contexto de interpretação."*

---

## 1. Semântica Contextualizada $\llbracket e \rrbracket_\Gamma$

A denotação de qualquer expressão $e$ no Proterol é sempre indexada pelo contexto $\Gamma$:

$$\llbracket e \rrbracket_\Gamma$$

Para um nexo transformacional $A \xrightarrow{f} B$:

$$\llbracket A \xrightarrow{f} B \rrbracket_\Gamma = f\left(\llbracket A \rrbracket_\Gamma, \llbracket B \rrbracket_\Gamma\right)$$

Se o contexto $\Gamma$ for alterado (por exemplo, transição de um ambiente puramente matemático para um ambiente de contrato econômico descentralizado), o nexo adquire novas valências e consequências práticas.

---

## 2. A Separação dos Quatro Níveis Semiótico-Operacionais

O Proterol impõe rigorosamente a distinção:

$$\boxed{\text{syntax} \neq \text{semantics} \neq \text{pragmatics} \neq \text{execution}}$$

1. **Sintaxe:** A boa formação das cadeias de signos segundo as regras da gramática formal.
2. **Semântica:** O mapeamento dos signos em nós conceituais e relações em $\mathcal{G}$.
3. **Pragmática:** O impacto do signo sobre o agente receptor e seu contexto no mundo.
4. **Execução:** A mutação de estado computacional em memória física ou na cadeia de blocos.

Uma expressão pode ser sintaticamente perfeita e ainda carecer de aplicabilidade pragmática; inversamente, uma heurística pragmática pode necessitar de formalização sintática para ser compilada em código verificável.
