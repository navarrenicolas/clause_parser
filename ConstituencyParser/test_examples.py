import benepar, spacy
nlp = spacy.load('en_core_web_md')
if spacy.__version__.startswith('2'):
    nlp.add_pipe(benepar.BeneparComponent("benepar_en3"))
else:
    nlp.add_pipe("benepar", config={"model": "benepar_en3"})

from ConstituencyParser import ConstituencyParser

decl_samples = open('../Datasets/ClauseEmbeddingExamples/finite-declarative-clauses.txt').read().replace('\n', ' ')
pol_samples = open('../Datasets/ClauseEmbeddingExamples/finite-polar-interrogative-clauses.txt').read().replace('\n', ' ')
const_samples = open('../Datasets/ClauseEmbeddingExamples/finite-consituent-interrogative-clauses.txt').read().replace('\n', ' ')
alt_samples = open('../Datasets/ClauseEmbeddingExamples/finite-alternative-interrogative-clauses.txt').read().replace('\n', ' ')
adv_samples = open('../Datasets/ClauseEmbeddingExamples/adversarial.txt').read().replace('\n', ' ')
all_examples = decl_samples + pol_samples + const_samples + alt_samples

all_doc = nlp(all_examples)
adv_doc = nlp(adv_samples)

parser = ConstituencyParser()

example_parse = [parser.get_embedded_clause(sent) for sent in all_doc.sents]
adv_parse = [parser.get_embedded_clause(sent) for sent in adv_doc.sents]

adv_parse

all_examples

example_parse

adv_samples
