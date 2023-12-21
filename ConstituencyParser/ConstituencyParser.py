## Import libraries
# import benepar, spacy
# spacy.load('en_core_web_md')
# benepar.download('benepar_en3')

# #nlp.add_pipe('benepar', config={'model': 'benepar_en3'})
# self.nlp = spacy.load('en_core_web_md')
# if spacy.__version__.startswith('2'):
#     self.nlp.add_pipe(benepar.BeneparComponent("benepar_en3"))
# else:
#     self.nlp.add_pipe("benepar", config={"model": "benepar_en3"})

import re
from typing import List, Set, Dict, Tuple
from spacy import displacy

class ConstituencyParser():
    def __init__(self):
        return
    def check_SBAR(self,span,has_SBAR = False)->bool:
        if has_SBAR:
            return True
        children = list(span._.children)
        if len(children)==0:
            return  False    
        for child in children:
            if "SBAR" in child._.labels:
                has_SBAR = True
            else:
                has_SBAR = self.check_SBAR(child,has_SBAR)
        return has_SBAR
    def VP_parent(self,span):
        parent = span._.parent
        if parent == None:
            return (False,None)
        parent_label = parent._.labels
        if "VP" in parent_label:
            return (True,list(parent._.children)[0])
        elif "NP" in parent_label:
            return (False,None)
        else:
            return self.VP_parent(parent)
    def check_embedding_predicate(self,seg,has_predicate = (False,None)):
        if has_predicate[0]:
            return has_predicate
        children = list(seg._.children)
        if len(children) == 0:
            return (False,None)
        for child in children:
            c_label = child._.labels
            parent_head = self.VP_parent(child)     
            if parent_head[0]:
                if "SBAR" in c_label:
                    has_predicate = parent_head 
            has_predicate = self.check_embedding_predicate(child,has_predicate)
        return has_predicate    
    def get_embedded_clause(self,seg,has_predicate = (False,None),clause = None):
        if has_predicate[0]:
            return [has_predicate[0],has_predicate[1],clause]
        children = list(seg._.children)
        if len(children) == 0:
            return [False,None,None]
        for child in children:
            if has_predicate[0]:
                continue
            c_label = child._.labels
            parent_head = self.VP_parent(child)     
            if parent_head[0]:
                if "SBAR" in c_label:
                    has_predicate = parent_head
                    clause = child
            has_predicate = self.get_embedded_clause(child,has_predicate,clause)
        return has_predicate
