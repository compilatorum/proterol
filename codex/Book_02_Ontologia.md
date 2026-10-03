# 🜂 LIVRO II — ONTOLOGIA

> *"No Proterol, existir é ser tipado dentro de um contexto de transformação."*

---

## 1. Julgamento de Tipo

Todo elemento manipulado pelo Proterol é um objeto tipado:

$$x : \tau$$

Um tipo $\tau$ estabelece não apenas os valores admissíveis, mas os morfismos nos quais o elemento pode legitimamente participar.

---

## 2. Tipos Fundamentais

O núcleo ontológico do Proterol fixa quatorze tipos fundamentais:

$$\tau \in \{ \text{Entity}, \text{Concept}, \text{Relation}, \text{Process}, \text{State}, \text{Property}, \text{Event}, \text{Agent}, \text{Data}, \text{Rule}, \text{Proof}, \text{Artifact}, \text{Context}, \text{Construct} \}$$

| Tipo | Descrição Ontológica | Exemplo no Ecossistema |
|:---|:---|:---|
| **Entity** | Nó identificável com persistência espaço-temporal ou lógica. | DAO, Ator, Smart Contract |
| **Concept** | Universal semântico, ideia ou abstração formal. | Regeneração, Liquidez, Prova |
| **Relation** | Conexão ou morfismo entre duas ou mais entidades. | Hiperaresta, Dependência, Paternidade |
| **Process** | Dinâmica contínua ou discreta de transformação de estados. | Pipeline, Destilação, Oráculo |
| **State** | Configuração instantânea de valores em um ponto do espaço-tempo. | Saldo, Checkpoint, Memória de Agente |
| **Property** | Atributo, métrica ou predicado atribuível a um nó. | Incerteza, Entropia, Licença |
| **Event** | Transição discreta demarcada por evidência ou timestamp. | Execução de Ordem, Votação, Commit |
| **Agent** | Entidade dotada de autonomia, política, sensores e atuadores. | Neurocoder, SLM, Trader Simbólico |
| **Data** | Sedimento informacional bruto ou estruturado. | Lakehouse, Embedding, Áudio |
| **Rule** | Restrição prescritiva, invariante ontológico ou transição lógica. | $\kappa$ (Constraint), Política Determinística |
| **Proof** | Testemunho formal de verdade, proveniência ou conformidade. | Recibo Criptográfico, Curry-Howard $\pi$ |
| **Artifact** | Produto concreto de uma semiurgia ou compilação. | Código Python, SVG, Relatório Markdown |
| **Context** | Ambiente cognitivo, parâmetros $\Gamma$ e horizonte de avaliação. | Escopo de Execução, Época, Comunidade |
| **Construct** | Composição semiúrgica agregada de genes e capacidades. | Omni-Laboratory Scene, Oracle Forest |

---

## 3. Subtipagem e Dependência

Os tipos do Proterol são extensíveis e dependentes:

$$\tau(x) \quad \text{onde o tipo depende do valor de } x$$

Um constructo $K$ possui tipo refinado por sua composição genética:

$$K : \text{Construct}(g_1 \oplus g_2 \oplus \dots \oplus g_n)$$
