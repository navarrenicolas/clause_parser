import benepar, spacy
spacy.load('en_core_web_md')
benepar.download('benepar_en3')

#nlp.add_pipe('benepar', config={'model': 'benepar_en3'})
nlp = spacy.load('en_core_web_md')
if spacy.__version__.startswith('2'):
    nlp.add_pipe(benepar.BeneparComponent("benepar_en3"))
else:
    nlp.add_pipe("benepar", config={"model": "benepar_en3"})

import re
from typing import List, Set, Dict, Tuple
from spacy import displacy

class ClauseParser():
  """
  Currently, the code takes in an individual string of all the sentences
  and then splits into the invidiual sentence. Returns a List of dictionaries
  with the following dictionary structure {sentence: sentence, predicate: predicate,
  clause_type: clause_type, clause: clause}. If the class does not find SBAR or a
  predicate, the example is completely ignored and not included in the final output
  result. If the code does not find a clause or clause type, None is return for
  those two variables, however they are still included in the final output results,
  just as clause_type: None or clause: None
  """

  def __init__(self):
    return

  def find_clause_type(self, mark_text: str, sent: str) -> str:
    if mark_text == "that":
      return "declarative"
    elif mark_text == "which":
      return "constituent"
    elif mark_text == "whether" or mark_text == "if":
      for token in sent:
        if str(token) == "or":
          if str(token.nbor()) == "not":
            return "polar"
          else:
            return "alternative"
      else:
        return "polar"
    return None

  def find_clause_with_mark(self, sent_dp: dict, sent: str) -> str:
    for arc in sent_dp['arcs']:
      if re.search(r"mark", arc["label"]):
        clause_type = self.find_clause_type(sent_dp["words"][arc["start"]]['text'], sent)
        clause_start = arc["start"]
        clause = ""
        for i in range(len(sent_dp["words"])):
          if i >= clause_start:
            clause += sent_dp["words"][i]["text"]
            clause += " "
        return clause.strip(), clause_type
    return None, None

  def find_clause_without_mark(self, sent_dp: dict) -> str:
    for arc in sent_dp['arcs']:
      if re.search(r"(c|p|x)comp", arc["label"]):
        clause_start = arc["start"] + 1
        clause = ""
        for i in range(len(sent_dp["words"])):
          if i >= clause_start:
            clause += sent_dp["words"][i]["text"]
            clause += " "
        return clause.strip()
    return None

  def confirm_mark(self, sent_dp: dict) -> bool:
    for arc in sent_dp['arcs']:
      if arc["label"] == "mark":
        return True
    return False

  def confirm_about(self, predicate: str) -> bool:
    if predicate == "about":
      return True
    else:
      return False

  def find_pos(self, predicate: str) -> str:
    predicate_nlp = nlp(predicate)
    for token in predicate_nlp:
      return token.pos_

  def find_predicate(self, sent_dp: dict) -> str:
    for arc in sent_dp['arcs']:
      if re.search(r"(c|p|x)comp", arc["label"]):
        predicate_index = arc["start"]
        if self.confirm_about(sent_dp["words"][predicate_index]['text']) == True:
          for inner_arc in sent_dp['arcs']:
            if inner_arc['end'] == predicate_index:
              return {"predicate": sent_dp["words"][inner_arc["start"]]['text'], "POS": self.find_pos(sent_dp["words"][inner_arc["start"]]['text']), "Preposition": sent_dp["words"][inner_arc["end"]]['text']}
        else:
          return {"Predicate": sent_dp["words"][predicate_index]['text'], "POS": self.find_pos(sent_dp["words"][predicate_index]['text']), "Preposition": None}
    return None

  def confirm_sbar(self, sent_cp: str) -> bool:
    if "SBAR" in sent_cp:
      return True
    else:
      return False

  def get_dependecy_parse(self, sent: str) -> str:
    return displacy.parse_deps(sent)

  def get_constitency_parse(self, sent: str) -> str:
    return sent._.

  def get_embedded_clauses(self, examples) -> List[dict]:
    all_clauses = []
    doc = nlp(examples)
    for sent in doc.sents:
      print(" ")
      print(sent)
      sent_cp = self.get_constitency_parse(sent)
      if self.confirm_sbar(sent_cp) is False:
        continue
      sent_dp = self.get_dependecy_parse(sent)
      predicate = self.find_predicate(sent_dp)
      if predicate == None:
        continue
      if self.confirm_mark(sent_dp) == True:
        clause, clause_type = self.find_clause_with_mark(sent_dp, sent)
      elif self.confirm_mark(sent_dp) == False:
        clause_type = "declarative"
        clause = self.find_clause_without_mark(sent_dp)
      all_clauses.append({"sentence": str(sent), "predicate": predicate, "clause type": clause_type, "clause": clause})
    return all_clauses

