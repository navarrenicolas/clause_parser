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

    def get_sentence(self,span):
        parent = span._.parent
        if parent == None :
            return span
        else:
            return self.get_sentence(parent)

    def get_predicate(self,span):
        """Returns the list of dictionaries of the embedding predicate token data of an SBAR span.
        The function assumes that the span is an embedded clause.
        :span: spacy.tokens.span.span
            parsed representation of of text string.
        :returns: [{'string': 'lemma': , 'POS': }]
            string: the original lexical token in the sentence
            lemma: represents the token lemma if the string is modulated by tense
            POS: the part-of-speech tag for the lexical token
        """
        final_pred = []
        token_annots = [{'str': token.text, 'lemma': token.lemma_, 'POS': token.pos_} for token in span]
        pos_tags = [token.pos_ for token in span]

        #we only want verbs, prepositions, adjectives, and (only if the predicate contains an adjective) auxiliaries
        for token in token_annots:
            pos = token['POS']
            if pos in ['VERB', 'ADP', 'ADJ'] or ("ADJ" in pos_tags and pos == "AUX"):
                final_pred.append(token)
        return final_pred
        
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
        sbar_idx = span[0].i
        # if 'CONJ' in self.get_sentence(span)[sbar_idx-1].pos_:
        #     return (False, None)
        # Get the parent span
        parent = span._.parent
        if parent == None:
            return (False,None)
        parent_label = parent._.labels
        if "VP" in parent_label:
            predicate = self.get_predicate(self.get_sentence(span)[parent[0].i:sbar_idx+1])
            if len(predicate) == 1:
                if predicate[0]['str']=='is':
                    return (False,None)
            return (True,predicate)        
        elif "NP" in parent_label:
            # Found NP parent
            return (False,None)
        else:
            # No NP or VP parent. Check next parent.
            return self.VP_parent(parent)


    def get_SBAR_spans(self,span):
        """Returns a list of SBAR spans given sentence.
        :span: spacy.tokens.span.span
            Parsed representation of of text string.
        :returns: [spacy.tokens.span.span]
        """    
        children = list(span._.children)
        spans = []
        if len(children)==0:
            return spans
        for child in children:
            if 'SBAR' in child._.labels:
                spans += [child]
            else:
                spans+= self.get_SBAR_spans(child)
        return spans

    def get_clause_type(self,span):
        """Returns the type of the embedded clause if there is one in the given sentence.
            Identifies clauses as one of 4 clause types
                - finite declarative
                - finite polar interrogative
                - finite constituent interrogative
                - finite alternative interrogative
            Otherwise the clause will be labeled with "other".

        :span: spacy.tokens.span.span
            Parsed representation of of text string.
        :has_predicate: (bool,spacy.tokens.span.span)
        :clause: str
            Embedding predicate if it has been previously found.
            Carry the last finding in in case predicate has already been found.
        :returns: str
            Embedded clause type label
        """
        # Convert to string to apply heuristic checks
        clause_str = str(span).lower()

        first_word = str(list(span._.children)[0]).lower()

        # Check for polar and alternative interrogatives
        if 'whether' in first_word: 
            if 'or not' in clause_str:
                return 'polar'
            if ' or ' in clause_str:
                return 'alternative'
            else:
                return 'polar'

        # Check for constituent
        if any([word in first_word for word in ['who', 'what', 'when', 'where', 'why', 'how','which']]):
            return 'constituent'

        return 'declarative'

    def parse_SBAR_clause(self,sentence,span):
        """ Returns a list of dictionaries with the embedded clause metadata.
            If none of the spans are detected as embedded clauses an empty list is returned

        :span: spacy.tokens.span.span
            Parsed representation of of text string. 
        :returns: [{'predicate': , 'type': , 'clause': , 'embedded clauses': }]
        """

        SBAR_spans = self.get_SBAR_spans(span)
        clauses = []
        
        for sbar in SBAR_spans:
            parent = self.VP_parent(sbar)
            # first_word = str(list(sbar._.children)[0]).lower()
            first_word = str(sbar[0])
            if len(self.get_SBAR_spans(sbar)) > 0:
                clauses += self.parse_SBAR_clause(sentence,sbar)
            if not parent[0] or first_word in ['because', 'since', 'while', 'as']:
                continue
            clauses += [{'sentence': str(sentence),
                        'predicate': parent[1],
                         'type': self.get_clause_type(sbar),
                         'clause' : str(sbar)
                         }]
        return clauses

    def parse_clauses(self,sentence):
        """ Returns a dictionary with all the embedded clause parse data

        :span: spacy.tokens.span.span
            Parsed representation of of text string. 
        :returns: {'sentence': , 'embedded clauses': }
        """
        return self.parse_SBAR_clause(sentence,sentence)
