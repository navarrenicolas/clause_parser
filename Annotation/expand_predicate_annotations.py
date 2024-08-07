import spacy
import json
import os
import nested_lookup

nlp = spacy.load("en_core_web_sm")


#extract the string, lemma, and pos tags for the relevant tokens in the predicate
def get_pred_info(pred_str):
    final_pred = []
    doc = nlp(pred_str)

    #information for each token, from spacy
    token_annots = [{'str': token.text, 'lemma': token.lemma_, 'POS': token.pos_} for token in doc]
    pos_tags = [token.pos_ for token in doc]

    #we only want verbs, prepositions, adjectives, and (iff the predicate contains an adjective) auxiliaries
    for token in token_annots:
        pos = token['POS']
        if pos in ['VERB', 'ADP', 'ADJ'] or ("ADJ" in pos_tags and pos == "AUX"):
            final_pred.append(token)

    return final_pred


#apply get_pred_info function to an embedded clause dict
def fill_pred_info(embedded):
    new_emb = embedded
    full_pred = get_pred_info(embedded['predicate'][0]['str'])
    new_emb['predicate'] = full_pred
    return new_emb


#apply get_pred_info function to an embedded clause dict for nested clauses
def nested_fill(embedded):
    new_emb = []
    for n in embedded: 
        new_n = n
        full_pred = get_pred_info(n['predicate'][0]['str'])
        new_n['predicate'] = full_pred
        new_emb.append(new_n)
    return new_emb


#open and modify the annotated json file to include all relevant predicate info
def predicate_expander(filepath):
    with open(filepath, mode="r", encoding="utf-8") as f:
        data = json.load(f)

        #iterate through sentences
        for key in data.keys():
            embedded_clauses = data[key]['embedded clauses']

            #iterate recursively through all embedded clauses in the sentence
            for i, ec in enumerate(embedded_clauses):
                embedded_clauses[i] = fill_pred_info(ec)    

                if ec['embedded clauses'] != []: #nested
                    embedded_clauses[i]['embedded clauses'] = nested_lookup.nested_alter(embedded_clauses[i], 'embedded clauses', nested_fill)
    
    #replace original file
    os.remove(filepath)
    with open(filepath, 'w') as f:
        json.dump(data, f, indent=4)

predicate_expander("Annotation\\polar_golden_set.json")

