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

def constituency_parse(sent):
  return sent._.parse_string.replace('(', '[').replace(')', ']')

# Import the data from the cc dataset
cc_data = "../Datasets/cc_en_head-0000_sample.txt"
sents = ""
number_of_lines_to_read = 1000  # number of lines we want to look at
with open(cc_data, 'r') as file:
    for i in range(number_of_lines_to_read):
        line = file.readline()
        if not line:
            break  # Exit the loop if there are no more lines.
        sents += line

doc = nlp(sents)

class ClauseParser():
  def __init__(self): 
      return
  def has_clause(self,sent)->bool:
      sent_cp = self.get_constituency_parse(sent)
      if 'SBAR' in sent_cp:
          return True
      else:
          return False
  def get_constituency_parse(self,sent:str)->str:
      return sent._.parse_string.replace('(', '[').replace(')', ']')

parser = ClauseParser()

all_data = pd.DataFrame()
all_data["sents"] = list(doc.sents)
all_data["has_clause"] = [parser.has_clause(sent) for sent in all_data.sents]

clause_data = all_data[all_data["has_clause"]]

print(clause_data["has_clause"].value_counts())
print(all_data["has_clause"].value_counts())

clause_data.sents.to_csv("sentences_filtered_1-1000.csv")




