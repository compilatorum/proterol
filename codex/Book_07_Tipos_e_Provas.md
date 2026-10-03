# 🜂 LIVRO VII — TIPOS E PROVAS

> *"Uma proposição é um tipo de problema; um programa é o método de sua resolução; uma prova é o testemunho indelével de que a solução existe."*

---

## 1. Julgamentos Formais

Um julgamento de tipagem no Proterol expressa a conformidade de um termo com seu tipo:

$$\Gamma \vdash e : \tau$$

Uma asserção proposicional tem a forma:

$$\Gamma \vdash P$$

---

## 2. O Isomorfismo de Curry–Howard no Proterol

O Proterol adota integralmente o princípio construtivo:

$$\boxed{\text{Proposition} \longleftrightarrow \text{Type}}$$

$$\boxed{\text{Proof} \longleftrightarrow \text{Program}}$$

Uma prova não é um mero selo burocrático externo. Uma prova é um **objeto de primeira classe** ($\pi$):

$$\pi : P$$

- Um **tipo** descreve a especificação de uma tarefa, requisito ou objetivo.
- Um **programa** (pipeline de nexos, script de agente) que atende a especificação é sua prova computacional.
- A execução bem-sucedida com verificação de invariantes produz o testemunho criptográfico $\pi$.

---

## 3. Semântica Baseada em Provas

Na semântica baseada em provas, o sentido de uma asserção não é seu "valor de verdade platônico em um mundo abstrato", mas a **coleção de suas provas possíveis**.

Assim, quando dizemos que um constructo Proterol é válido, portamos o objeto $\pi$ que reproduz ou certifica deterministicamente todas as transições de estado que o geraram.
