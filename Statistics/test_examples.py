import benepar, spacy
nlp = spacy.load('en_core_web_md')
if spacy.__version__.startswith('2'):
    nlp.add_pipe(benepar.BeneparComponent("benepar_en3"))
else:
    nlp.add_pipe("benepar", config={"model": "benepar_en3"})

import sys
sys.path.append('../ConstituencyParser/')
from ConstituencyParser import ConstituencyParser

import pandas as pd


# Toy Dataset file paths
dec_path_toy = "../Datasets/ToyData/finite declarative clauses.txt"
pol_path_toy = "../Datasets/ToyData/finite polar interrogative clauses.txt"
alt_path_toy = "../Datasets/ToyData/finite alternative interrogative clauses.txt"
const_path_toy = "../Datasets/ToyData/finite constituent interrogative clauses.txt"
adv_path_toy = "../Datasets/ToyData/adversarial.txt"

decl_samples = open(dec_path_toy).read()
pol_samples = open(pol_path_toy).read()
const_samples = open(const_path_toy).read()
alt_samples = open(alt_path_toy).read()
adv_samples = open(adv_path_toy).read()
all_examples = decl_samples + pol_samples + const_samples + alt_samples

dec_doc = nlp(decl_samples)
pol_doc = nlp(pol_samples)
const_doc = nlp(const_samples)
alt_doc = nlp(alt_samples)

all_doc = nlp(all_examples)
adv_doc = nlp(adv_samples)

def doc_sent_len(doc):
    return len(list(doc.sents))

parser = ConstituencyParser()

def get_example_sum(doc):
    return sum([parser.get_embedded_clause(sent)[0] for sent in doc.sents])

get_example_sum(adv_doc)

true_p = sum([get_example_sum(doc) for doc in [dec_doc,pol_doc,alt_doc,const_doc]])
false_p = get_example_sum(adv_doc)
false_n = 40 - true_p


all_precision = true_p/(true_p+false_p)
all_recall = true_p/(true_p+false_n)
all_f1 = 2*all_precision*all_recall/(all_precision+all_recall)

all_precision


[parser.get_clause_type(sent) for sent in alt_doc.sents]

example_parse = [parser.get_embedded_clause(sent) for sent in all_doc.sents]
adv_parse = [parser.get_embedded_clause(sent) for sent in adv_doc.sents]


type_parse = [parser.get_clause_type(sent) for sent in all_doc.sents]

adv_parse

all_examples

example_parse

adv_samples

pd.valu type_parse

# For getting some parsed strings

all_doc_sents = list(all_doc.sents)

import pyperclip

def replace_brackets(parsed_string):
    # Replace round brackets with square brackets
    replaced_string = parsed_string.replace('(', '[').replace(')', ']')
    # Wrap the string with \\begin{forest} and \\end{forest}\n",
    final_string = '\\begin{forest} ' + replaced_string + ' \\end{forest}'
    return final_string

test_doc = nlp("Mary loves a farmer")

pyperclip.copy(replace_brackets(list(test_doc.sents)[0]._.parse_string))

pyperclip.copy(replace_brackets(all_doc_sents[12]._.parse_string))

