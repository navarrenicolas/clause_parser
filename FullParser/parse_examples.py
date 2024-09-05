import spacy, benepar

import numpy as np
import matplotlib.pyplot as plt
import time

nlp = spacy.load('en_core_web_md')

if spacy.__version__.startswith('2'):
    nlp.add_pipe(benepar.BeneparComponent("benepar_en3"))
else:
    nlp.add_pipe("benepar", config={"model": "benepar_en3"})

import sys
sys.path.append('../')
from FullParser.ClauseParser import ClauseParser
import pandas as pd

parser = ClauseParser()


def read_file(file_path):
    with open(file_path, 'r', encoding = 'utf-8') as f:
        for line in f:
            yield line

dolma_path = "../Datasets/dolma/dolma/dolma_text/"
current_file = "v1_5r2_sample-0005.txt"

t = time.time()
times = []
line_count = 1
ECs = []
for line in read_file(dolma_path+current_file):
    sline = line.strip('\n')
    if len(line) <100 :
        try:
            doc = nlp(sline)
            for sent in doc.sents:
                parse = parser.parse_clauses(sent)
                if parse != []:
                    # print(f'Line {line_count} has an embedded clause!')
                    ECs.append(parse)
        except Exception as e:
            #print(f"Error encountered while processing line {line_count}: {sline}")
            print(e)
            pass  # Do nothing, continue to next line
    line_count+=1
    if line_count % 1000 == 0:
        print(f'Time to parse 1000 entries: {time.time()-t}')
        times.append(time.time()-t)
        t = time.time()
    if line_count > 1000 :
        break

flat_ECs = []
for parse in ECs:
    flat_ECs += parse

pd.DataFrame(flat_ECs).to_json(current_file+'.json')
