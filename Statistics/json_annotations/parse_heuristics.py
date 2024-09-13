import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import sys
sys.path.append('../../')

from FullParser.ClauseParser import ClauseParser

parser = ClauseParser()

import benepar, spacy
nlp = spacy.load('en_core_web_trf')
if spacy.__version__.startswith('2'):
    nlp.add_pipe(benepar.BeneparComponent("benepar_en3"))
else:
    nlp.add_pipe("benepar", config={"model": "benepar_en3"})


# Golden Data file paths
dec_path_golden = "../../Annotation/declarative_golden_set.json"
pol_path_golden = "../../Annotation/polar_golden_set.json"
alt_path_golden = "../../Annotation/alternative_golden_set.json"
const_path_golden = "../../Annotation/constituent_golden_set.json"
adv_path_golden = "../../Annotation/adversarials_golden_set.json"
flat_path_golden = "../../Annotation/golden_sets_flattened.json"

def parse_flat_golden(filename:str):
    golden_df = pd.read_json(filename, orient = 'index')
    golden_parses = []
    parser_parses = []
    for sent in golden_df.sentence.value_counts().to_dict().keys() :
        parses = [dict(row) for i,row in (golden_df[golden_df.sentence == sent]).iterrows()]
        golden_parses.append(parses)
        sent_doc = nlp(sent)
        parsed_sent = list(sent_doc.sents)[0]
        parser_parses.append(parser.parse_clauses(parsed_sent))
    return (parser_parses, golden_parses)

flat_parsed, flat_golden = parse_flat_golden(flat_path_golden)
adv_parsed, adv_golden = parse_flat_golden(adv_path_golden)



def nlp_sents(string):
    return list(nlp(string).sents)

## Use Constituency Parser to parse examples
#def parse_golden(filename:str):
#    golden_df = pd.read_json(filename, orient = 'index')
#    sents = golden_df.sentence
#    parses = [{}]*len(sents)
#    for i,sent in enumerate(sents):
#        sent_doc = nlp(sent)
#        parsed_sent = list(sent_doc.sents)[0]
#        parses[i] = parser.parse_clauses(parsed_sent)
#    return (parses, golden_df)
#
## Get data frames for all types of sentences
#dec_parsed, dec_golden = parse_golden(dec_path_golden)
#dec_parsed_df = pd.DataFrame(dec_parsed)
#pol_parsed, pol_golden = parse_golden(pol_path_golden)
#pol_parsed_df = pd.DataFrame(pol_parsed)
#alt_parsed, alt_golden = parse_golden(alt_path_golden)
#alt_parsed_df = pd.DataFrame(alt_parsed)
#const_parsed, const_golden = parse_golden(const_path_golden)
#const_parsed_df = pd.DataFrame(const_parsed)
#adv_parsed, adv_golden = parse_golden(adv_path_golden)
#adv_parsed_df = pd.DataFrame(adv_parsed)
##Putting them all together
#golden_df = pd.concat([dec_golden,pol_golden,alt_golden,const_golden,adv_golden])
#parsed_df = pd.concat([dec_parsed_df,pol_parsed_df,alt_parsed_df,const_parsed_df,adv_parsed_df])


######### Sandbox ########


def get_predicate_string(predicate):
    if len(predicate) ==0:
        return ''
    pred_string = ''
    for item in predicate:
        pred_string += str(item['str']) + ' '
    return pred_string[:-1]


def filter_sentences(data,filt):
    return [data[idx] for idx in [i for i, e in enumerate(flat_golden) if filt(e)] ]

def filter_sentences_idx(filt):
    return [idx for idx in [i for i, e in enumerate(flat_golden) if filt(e)] ]


single_idx = filter_sentences_idx(lambda x: len(x) == 1)
multiple_idx = filter_sentences_idx(lambda x: len(x) > 1)


def compare_data(parsed,golden,feature):
    if feature== 'type':
        return [[any([(gp['clause'] == e['clause'] and  gp['type'] == e['type']) for e in parsed[i]]) for gp in gold]  for i,gold in enumerate(golden)]
    if feature=='predicate':
        return [[any([(get_predicate_string(gp['predicate']) == get_predicate_string(e['predicate'])) for e in parsed[i]]) for gp in gold]  for i,gold in enumerate(golden)]
    return [[any([gp[feature] == e[feature] for e in parsed[i]]) for gp in gold]  for i,gold in enumerate(golden)]


#########################
# Evaluate singles
#########################

parsed_single = [flat_parsed[i] for i in single_idx]
golden_single = [flat_golden[i] for i in single_idx]

# Clause detection

detected_clauses =  list(map(lambda x: len(x)>0,parsed_single))
np.mean(detected_clauses)

# clause and type

correct_clauses = compare_data(parsed_single,golden_single,'type')
np.mean(correct_clauses)

# Predicate detection

correct_predicates = compare_data(parsed_single,golden_single,'predicate')
np.mean(correct_predicates)

failed_single_predicates = [golden_single[i][0]['sentence'] for i,e in enumerate(correct_predicates) if (not e[0] and correct_clauses[i])]
#failed_single_predicates = [golden_single[i][0]['sentence'] for i,e in enumerate(correct_predicates) if (not e[0] and len(parsed_single[i])>0)]

len(failed_single_predicates) # 45


#########################
# Evaluate doubles
#########################

parsed_multiple = [flat_parsed[i] for i in single_idx]
golden_multiple = [flat_golden[i] for i in single_idx]

# Detection

detected_multiple = [len(gold) == len(parsed_multiple[i]) for i,gold in enumerate(golden_multiple)]
np.mean(detected_multiple)

failed_multiple_detect = [parsed_multiple[i] for i,detect in enumerate(detected_multiple) if not detect]

# clause and type

correct_clauses = compare_data(parsed_multiple,golden_multiple,'type')
np.mean(list(map(np.mean,correct_clauses)))

# Predicate detection

correct_predicates = compare_data(parsed_multiple,golden_multiple,'predicate')
np.mean(list(map(np.mean,correct_predicates)))


#########################
# Evaluate Overall
#########################

# Clause detection

detected_clauses = list(map(lambda x: len(x)>0,flat_parsed))
np.mean(detected_clauses)

failed_detects = [gp[0]['sentence'] for i,gp in enumerate(flat_golden) if not detected_clauses[i]]

len(failed_detects) # 20

# clause and type

correct_clauses = compare_data(flat_parsed,flat_golden,'type')
np.mean(list(map(all,correct_clauses)))

# Predicate detection

correct_predicates = compare_data(flat_parsed,flat_golden,'predicate')
np.mean(list(map(all,correct_predicates)))

failed_preds = [gp[0]['sentence'] for i,gp in enumerate(flat_golden) if (detected_clauses[i] and  not any(correct_predicates[i]))]

len(failed_preds) # 31



failed_clauses = [gp[0]['sentence'] for i,gp in enumerate(flat_golden) if (detected_clauses[i] and  not any(correct_clauses[i]) and all(correct_predicates[i]))] 


#########################
# Adversarial sentences
#########################

false_positives = [parse for parse in adv_parsed if len(parse)>0]

false_positive_sentences = [parse[0]['sentence'] for parse in false_positives]


#########################
# Failed sentences
#########################

def replace_brackets(parsed_string):
    # Replace round brackets with square brackets
    replaced_string = parsed_string.replace('(', '[').replace(')', ']')
    # Wrap the string with \begin{forest} and \end{forest}
    final_string = '\\begin{adjustbox}{width=0.8\\linewidth}' + '\\begin{forest} ' + replaced_string + ' \\end{forest}' + '\\end{adjustbox}\\\\'
    return final_string

def copy_latex_parse(sentence):
    ps = list(nlp(sentence).sents)[0]
    return replace_brackets(ps._.parse_string)

gold_clauses = []
for gold in flat_golden:
    for gp in gold:
        gold_clauses.append(gp['clause'])

# Quick reflection of the golden single predicates
gold_predicates = []
for gold in flat_golden:
    for gp in gold:
        gold_predicates.append(gp['predicate'])
gold_single_preds = pd.Series([pred[0]['lemma'] for pred in  filter(lambda x: len(x)==1,gold_predicates)])
gold_single_preds.value_counts()[0:10]


[pred for pred in gold_predicates if  len(pred)>2]

# Quick reflection of the parsed single predicates
parsed_predicates = []
for sent_parse in flat_parsed:
    for parse in sent_parse:
        parsed_predicates.append(parse['predicate'])
parsed_single_preds = pd.Series([pred[0]['lemma'] for pred in  filter(lambda x: len(x)==1,parsed_predicates)])
parsed_single_preds.value_counts()[0:10]

# Parsed predicates with more than 4 items (many more than the golden set)
list(pred for pred in parsed_predicates if len(pred)>4)

# Parsed predicates with more then one verb per embedding predicate (more than in the golden set)
list(pred for pred in parsed_predicates if (lambda x: len([pr for pr in pred if pr['POS'] == 'VERB'])>1)(pred))


# Find parse of sentences matching keywords
def find_parse(string):
    return [parse for parse in flat_parsed if (lambda x: (string in x[0]['sentence']) if len(x) > 0 else False)(parse)]
# Find golden parse of sentences matching keywords
def find_golden_parse(string):
    return [gp for gp in flat_golden if (string in gp[0]['sentence'])]

import nltk
def nlp_parse(sent):
    return nltk.Tree.fromstring(list(nlp(sent).sents)[0]._.parse_string).pretty_print()

# View the golden parses matching query
fail_idx = 12
print([(gp['predicate'], gp['clause']) for gp in find_golden_parse(failed_preds[fail_idx])[0]])
print([(p['predicate'],p['clause']) for p in find_parse(failed_preds[fail_idx])[0]])

nlp_parse(failed_preds[fail_idx])

nlp_parse("Whether Vengeance will include Sam Loeb's #26, and how DC will collect Mark Verheiden's issues after Jeph Loeb departs, remains to be seen.")



parser.parse_clauses(nlp_sents(failed_preds[fail_idx])[0])


find_parse(failed_preds[fail_idx])



###########################
## Predicate distribution stuff
########################


mega_acceptability = pd.read_csv('../../Datasets/mega-acceptability-v2/mega-acceptability-v2.tsv',sep='\t')
mega_verbs = (set(mega_acceptability.verb.values))

found_MA_preds = {pred for pred in set(gold_single_preds.values) if pred in mega_verbs}

extra_MA_preds = set(filter( lambda x: all(c.isalnum() for c in x), {pred for pred in set(gold_single_preds.values) if pred not in mega_verbs}))


len(found_MA_preds)

########################################
## Sentences with too many predicates 
########################################

# It's impossible to find out what that half-life is, which means that it is very hard to use it to estimate how much time it will stay in your system.

## This sentence has some tricky coordination
# It doesnt care and couldnt care whether you have to get up early to go to work and that waking up at 3:00 a.m. to answer its demand for food is not very considerate of it.

## More with coordination and false detection of a clause
# We're not sure whether pollsters were referring to Los Stop's version, Con su blanca palidez, though somehow we suspect not.



import pyperclip 

pyperclip.copy(failed_single_predicates[0])
pyperclip.copy(replace_brackets(nlp_sents(failed_single_predicates[2])[0]._.parse_string))


trees = ''
for sentence in failed_preds:
    trees += replace_brackets(list(nlp(sentence).sents)[0]._.parse_string) + '\n' 
pyperclip.copy(trees)


##########
# Old (unflattened data)
#########

#def get_all_embedded_clauses(entry):
#    if type(entry) == dict:
#        return get_all_embedded_clauses([entry])
#    clauses = []
#    for clause in entry:
#        if len(clause) == 0 :
#            'empty'
#            clauses += [[]]
#            continue
#        if type(clause) != dict:
#            print('Nesting!',type(clause))
#            clauses += get_all_embedded_clauses(clause['embedded clauses'])
#            continue
#        try: 
#            clauses += [{
#                'type': clause['type'],
#                'predicate': get_predicate_string(clause['predicate']),
#                'embedded_clause': clause['clause']
#                }]
#            clauses += get_all_embedded_clauses(clause['embedded clauses'])
#        except Exception as e:
#            print(f'Error:{e}',clause,type(clause))
#            clauses += [None]
#            pass
#    return clauses
#
#golden_ECs  = golden_df['embedded clauses'].apply(get_all_embedded_clauses)
#
#parsed_ECs = parsed_df['embedded clauses'].apply(get_all_embedded_clauses)
#
#matches = []
#non_matches = []
#singles = []
#multiples = []
#adversarials = []
#for idx,entry in enumerate(parsed_ECs):
#    golden_len =len( golden_ECs.iloc[idx])
#    if len(entry) == golden_len :
#        matches.append(idx) 
#    else:
#        non_matches.append(idx)
#    if golden_len > 1:
#        multiples.append(idx)
#    elif golden_len == 1:
#        singles.append(idx)
#    else:
#        adversarials.append(idx)
#
#
## Evaluating the singles
#
#
#singles_df = pd.DataFrame({'parsed' : list(parsed_ECs.iloc[singles]), 'golden': golden_ECs.iloc[singles]})
#singles_df = singles_df.assign(type=False, clause=False , predicate=False)
#for idx,golden_parse in enumerate(singles_df.golden):
#    try:
#        parse = singles_df.parsed.iloc[idx]
#        if len(parse)==0:
#            continue
#        parse_data = parse[0]
#        golden_data = golden_parse[0]
#        #Do the comparisons
#        type_correct = parse_data['type'] == golden_data['type']
#        clause_correct  = str(parse_data['embedded_clause']) == str(golden_data['embedded_clause'])
#        pred_correct = parse_data['predicate'] == golden_data['predicate']
#        #Save it in the results
#        singles_df['type'].iloc[idx] = type_correct
#        singles_df['clause'].iloc[idx] = clause_correct
#        singles_df['predicate'].iloc[idx] = pred_correct
#    except Exception as e:
#        print(f'Parser: {parse_data}')
#        print(f'Golden: {golden_data}')
#        pass
#
#
### Stats 
#
#singles_df.parsed.apply(lambda x: len(x)>0).mean()
#
#singles_df.type.mean()
#
#singles_df[singles_df['golden'].apply(lambda x: x[0]['type']) == 'declarative'].type.mean()
#
#singles_df.clause.mean()
#
#singles_df.predicate.mean()
#
#
### Get non detected sentences (false negatives)
#
#### Simple detection
#failed_singles = singles_df.parsed.apply(lambda x: len(x)==0)
#failed_singles_sents = golden_df.sentence.iloc[singles][failed_singles]
#
#
#### predicate detection
#failed_predicate_sents = golden_df.sentence.iloc[singles][(singles_df.predicate == False) &  (failed_singles.apply(lambda x: not x))]
#failed_predicate_golden = golden_df['embedded clauses'].iloc[singles][(singles_df.predicate == False) &  (failed_singles.apply(lambda x: not x))]
#failed_predicate_parses = parsed_df['embedded clauses'].iloc[singles][ list((singles_df.predicate == False) &  (failed_singles.apply(lambda x: not x)))]
#
#failed_predicate_golden.iloc[1]
#
#failed_predicate_parses.iloc[1]
#
#list(failed_predicate_golden.apply(lambda x: len(x[0]['predicate']) == 1))
#
#failed_predicate_sents[list(failed_predicate_golden.apply(lambda x: len(x[0]['predicate']) == 1))]
#
#
#
#### Golden predicates
#
#golden_predicates = []
#for entry in golden_ECs:
#    for ec in entry:
#        try: 
#            golden_predicates.append(ec['predicate'])
#        except Exception as e:
#            pass
#
#golden_predicates
#
#['is' == pred for pred in golden_predicates]
#
#is_preds = []
#for i,parse in enumerate(golden_ECs):
#    if not parse:
#        continue
#    for ec in parse:
#        if not ec:
#            print(i,parse)
#            continue
#        if ec['predicate']=='is':
#            is_preds.append(parse)
#            break
#
#len(failed_singles_sents) # 18
#
#len(failed_predicate_sents) # 74
#
## Evaluating the adversarials
#
#adversarials_df = parsed_ECs.iloc[adversarials]
#
#adversarials_df.apply(lambda x: len(x)==0).mean()
#
#
### Get false positives
#
#false_positives = adversarials_df.apply(lambda x: len(x)>0)
#false_positive_sents = golden_df.sentence.iloc[adversarials][list(false_positives)]
#
#len(false_positive_sents) #10
#
#
## Nested Embedded clauses
#
#
#multiples_nested = golden_ECs.iloc[multiples].apply(len) > golden_df['embedded clauses'].iloc[multiples].apply(len)
#
#nested_df = pd.DataFrame({'parsed' : list(parsed_ECs.iloc[multiples][list(multiples_nested)]), 
#                          'golden': list(golden_ECs.iloc[multiples][list(multiples_nested)])
#                          })
#
#
#nested_df.parsed.apply(len) == nested_df.golden.apply(len) 
#
#
#golden_df['embedded clauses'].iloc[multiples][list(multiples_nested)].apply(len)
#
#parsed_df['embedded clauses'].iloc[multiples][list(multiples_nested)].apply(len)
#
#golden_ECs.iloc[multiples][list(multiples_nested)].apply(len)
#
#parsed_ECs.iloc[multiples][list(multiples_nested)].apply(len)
#
#nested_sents = golden_df.sentence.iloc[np.array(multiples)[multiples_nested]]
#
#
## coordinated clauses
#
#multiples_coordinated = golden_ECs.iloc[multiples].apply(len) == golden_df['embedded clauses'].iloc[multiples].apply(len)
#
#coordinated_df = pd.DataFrame({
#    'parsed' : list(parsed_ECs.iloc[multiples][list(multiples_coordinated)]),
#    'golden': list(golden_ECs.iloc[multiples][list(multiples_coordinated)])
#    })
#
#golden_ECs.iloc[multiples][list(multiples_coordinated)]
#
#matched_coordinated = coordinated_df.parsed.apply(len) == coordinated_df.golden.apply(len) 
#
#coordinated_df[matched_coordinated].golden.apply(len)
#
#types_correct = []
#clauses_correct = []
#preds_correct = []
#for idx,golden_match in enumerate(coordinated_df[matched_coordinated].golden):
#    if None in golden_match:
#        print('none spotted')
#        continue
#    parsed_match = coordinated_df[matched_coordinated].parsed.iloc[idx]
#    for i in range(len(golden_match)):
#        types_correct.append(golden_match[i]['type']== parsed_match[i]['type'])
#        preds_correct.append(golden_match[i]['predicate']== parsed_match[i]['predicate'])
#        clauses_correct.append(str(golden_match[i]['embedded_clause']) == str(parsed_match[i]['embedded_clause']))
#
#np.mean(types_correct)
#
#np.mean(clauses_correct)
#
#np.mean(preds_correct)
#


##########################
