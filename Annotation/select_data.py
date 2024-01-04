# For parser
import benepar, spacy
spacy.load('en_core_web_md')
benepar.download('benepar_en3')
from spacy import displacy

# For annotation data
import pandas as pd

nlp = spacy.load('en_core_web_md')
if spacy.__version__.startswith('2'):
    nlp.add_pipe(benepar.BeneparComponent("benepar_en3"))
else:
    nlp.add_pipe("benepar", config={"model": "benepar_en3"})

import sys
sys.path.append('../ConstituencyParser/')
from ConstituencyParser import ConstituencyParser
parser = ConstituencyParser()

# Import the data from the cc dataset sample
cc_data = "../Datasets/cc_en_head-0000_sample.txt"

def get_polar_alternative_sentences(number_of_lines_to_read = 500, batch = 0):
    with open(cc_data, 'r') as file, open('../Datasets/cc_en_head_polar_alternative_filter.txt', 'w') as outfile:
        sents_str  = ''
        for i in range(number_of_lines_to_read*batch):
            file.readline()
        for i in range(number_of_lines_to_read):
            line = file.readline()
            if not line:
                break  # Exit the loop if there are no more lines.
            if len(line) < 5:
                continue
            line_lower = line.lower()
            if 'whether' in line_lower or 'or' in line_lower:
                sents_str += line 
        outfile.write(sents_str)

def get_constituent_sentences(number_of_lines_to_read = 500, batch = 0):
    with open(cc_data, 'r') as file, open('../Datasets/cc_en_head_constituent_filter.txt', 'w') as outfile:
        sents_str  = ''
        for i in range(number_of_lines_to_read*batch):
            file.readline()
        for i in range(number_of_lines_to_read):
            line = file.readline()
            if not line:
                break  # Exit the loop if there are no more lines.
            if len(line) < 5:
                continue
            line_lower = line.lower()
            if 'what' in line_lower or 'which' in line_lower:
                sents_str += line 
        outfile.write(sents_str)

def get_sentences(number_of_lines_to_read = 500, batch = 0):
    with open(cc_data, 'r') as file:
        sents_str  = ''
        for i in range(number_of_lines_to_read*batch):
            file.readline()
        for i in range(number_of_lines_to_read):
            line = file.readline()
            if not line:
                break  # Exit the loop if there are no more lines.
            if len(line) < 5:
                continue
            sents_str += line
        doc = nlp(sents_str)
        sents = [{}]*len(list(doc.sents))
        for i,sent in enumerate(doc.sents):
            embedding  = parser.get_embedded_clause(sent)
            if not embedding[0]:
                continue
            clause = embedding[2]
            child = list(clause._.children)[0]
            child_label = child._.labels
            if 'which' in str(child):
                clause_type = 'constituent'
            elif 'if' in str(child) or 'whether' in str(child):
                clause_type = 'polar-alternative'
            else:
                clause_type = 'declarative'
            sents[i] = {'sentence' : str(sent),
                        'predicted_type': clause_type,
                        'embedding_predicate': str(embedding[1])
                        }
    return sents

# Uncomment to get filtered data

#n_batches = 3
#batch_sents = [[]]*n_batches
#for batch in range(n_batches):
#    batch_sents[batch] = get_sentences(batch=batch,number_of_lines_to_read=5000)
#
#get_constituent_sentences(number_of_lines_to_read=100000)
#get_polar_alternative_sentences(number_of_lines_to_read=100000)

