---
name: computational-linguistics
description: "Natural language processing foundations: tokenization, parsing, semantics, machine translation, and language models"
category: linguistics
version: 1.0.0
disable-model-invocation: false
risk: low
source: "https://github.com/Mr-Nobody-Anonymous/All-skills"
source_repository: "Mr-Nobody-Anonymous/All-skills"
source_path: "awesome_skills/linguistics/computational-linguistics/SKILL.md"
license: "MIT"
imported_at: "2026-09-20"
---

# Computational Linguistics

## Scope
Computational linguistics combines linguistics and computer science to model, analyze, and generate human language. This skill covers NLP foundations, formal grammars, statistical methods, and modern neural approaches.

## Formal Language Theory

### Chomsky Hierarchy
| Type | Grammar | Recognizer | Example |
|------|---------|-----------|---------|
| 3 (Regular) | A → aB, A → a | Finite automaton | Morphological patterns |
| 2 (Context-free) | A → α | Pushdown automaton | Phrase structure syntax |
| 1 (Context-sensitive) | αAβ → αγβ | Linear bounded | Some natural language phenomena |
| 0 (Unrestricted) | α → β | Turing machine | General computation |

### Parsing
- **Constituency parsing**: Tree structure (S → NP VP, VP → V NP)
- **Dependency parsing**: Head-dependent relations (nsubj, dobj, amod)
- **Algorithms**: CYK (CFG, O(n³)), Earley (general CFG), shift-reduce, transition-based, graph-based
- **Treebanks**: Penn Treebank, Universal Dependencies (UD)

## Core NLP Pipeline

### Text Processing
1. **Tokenization**: Split text into tokens (word, subword: BPE/WordPiece/SentencePiece)
2. **Sentence segmentation**: Identify sentence boundaries
3. **Morphological analysis**: Lemmatization, stemming, POS tagging
4. **Named entity recognition (NER)**: Person, organization, location, date, etc.
5. **Syntactic parsing**: Constituency or dependency parse
6. **Semantic analysis**: Word sense disambiguation, semantic role labeling

### Part-of-Speech Tagging
- **Tag sets**: Universal POS tags (17), Penn Treebank (45)
- **Methods**: HMM (generative), CRF (discriminative), BiLSTM-CRF, Transformer-based
- **Accuracy**: State-of-the-art > 97% on English

### Statistical Methods
- **n-gram language models**: P(w₁...wₙ) = Π P(wᵢ|wᵢ₋₁...wᵢ₋ₖ)
  - Smoothing: Add-k, Kneser-Ney, modified Kneser-Ney
  - Perplexity: PP = exp(-1/N Σ log P(wᵢ|context))
- **TF-IDF**: tf(t,d) × log(N/df(t)) for document representation
- **Topic models**: LDA (Latent Dirichlet Allocation)

### Neural Approaches
- **Word embeddings**: Word2Vec (CBOW, Skip-gram), GloVe, FastText
- **Sequence models**: RNN, LSTM, GRU → bidirectional variants
- **Attention mechanism**: Scaled dot-product attention: Attention(Q,K,V) = softmax(QKᵀ/√d)V
- **Transformers**: Self-attention, multi-head attention, positional encoding
- **Pre-trained LMs**: BERT, GPT, T5, LLaMA — fine-tune or prompt for downstream tasks

## Key Tasks & Evaluation

| Task | Metrics | Benchmarks |
|------|---------|-----------|
| Machine translation | BLEU, METEOR, COMET | WMT, FLORES |
| Sentiment analysis | Accuracy, F1 | SST, IMDb |
| Question answering | EM, F1 | SQuAD, Natural Questions |
| Summarization | ROUGE, BERTScore | CNN/DailyMail, XSum |
| NER | Entity-level F1 | CoNLL-2003 |

## Computational Tools
- **spaCy**: Industrial-strength NLP in Python
- **NLTK**: Educational NLP toolkit
- **Hugging Face Transformers**: Pre-trained models
- **Stanza (Stanford)**: Multi-language NLP pipeline
- **CoreNLP**: Java-based, linguistic annotation

## Standards & References
- Jurafsky & Martin — *Speech and Language Processing* (3rd ed., online)
- Manning & Schütze — *Foundations of Statistical NLP*
- Universal Dependencies (universaldependencies.org)
