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
    '''
    The class assumes that the text span is already parsed with the SpaCy constituency parser.
    This defines a set of operations for extracting embedded clauses from the constituency tree structures of the
    SpaCy parser.
    '''

    def __init__(self):
        return
    def check_SBAR(self,span,has_SBAR = False)->bool:
        """Method for checking if the constituency representation contains a subordinate clause.
        :span: spacy.tokens.span.Span
            Parsed representation of of text string.
        :returns: bool
            Boolean indicating if the parser has a subordinate clause.
        """
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
        """Finds the nearest parent label as either VP NP or none.
        :span: spacy.tokens.span.span
            parsed representation of of text string.
        :returns: (bool, spacy.tokens.span.span)
            returns a tuple of indicating
                arg1: bool
                    if the parent label is a VP.
                arg2: spacy.tokens.span.span
                    The first (leftmost) child of the VP labeled span.
        """

        # Get the parent span
        parent = span._.parent

        # Check that it isn't empty
        if parent == None:
            return (False,None)

        # Check the part-of-speech label
        parent_label = parent._.labels
        if "VP" in parent_label:
            # Found VP parent
            return (True,list(parent._.children)[0])
        elif "NP" in parent_label:
            # Found NP parent
            return (False,None)
        else:
            # No NP or VP parent. Check next parent.
            return self.VP_parent(parent)

    def check_embedding_predicate(self,seg,has_predicate = (False,None)):
        """Checks if a subordinate cause (SBAR) is an embedding predicate.
        :seg: spacy.tokens.span.span
            parsed representation of of text string.
        :has_predicate: (bool,spacy.tokens.span.span)
            Carry the last finding in in case predicate has already been found.
        :returns: (bool, spacy.tokens.span.span)
            returns a tuple of indicating
                arg1: bool
                    if the parent label is a VP.
                arg2: spacy.tokens.span.span
                    The first (leftmost) child of the VP labeled span.
        """
        # Exit condition if the predicate has already been found
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
        """Returns an embedded clause and the embedding predicate if there is one in the given sentence.
        :seg: spacy.tokens.span.span
            Parsed representation of of text string.
        :has_predicate: (bool,spacy.tokens.span.span)
        :clause: str
            Embedding predicate if it has been previously found.
            Carry the last finding in in case predicate has already been found.
        :returns: [bool, spacy.tokens.span.span, str]
            returns a tuple of indicating
                arg1: bool
                    if the parent label is a VP.
                arg2: spacy.tokens.span.span
                    The first (leftmost) child of the VP labeled span.
        """
        # Return list if embedded clause has been found in a previous call
        if has_predicate[0]:
            return [has_predicate[0],has_predicate[1],clause]

        # Get children of segment and check if its not empty
        children = list(seg._.children)
        if len(children) == 0:
            return [False,None,None]

        # Recursively check all children for embedding predicate
        for child in children:
            # If embedding predicate is found in one of the children we can exit the loop.
            if has_predicate[0]:
                break
            c_label = child._.labels
            parent_head = self.VP_parent(child)     
            if parent_head[0]:
                if "SBAR" in c_label:
                    has_predicate = parent_head
                    clause = child
            has_predicate = self.get_embedded_clause(child,has_predicate,clause)
        return has_predicate
