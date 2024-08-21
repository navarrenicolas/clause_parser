import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import sys
sys.path.append('../../')

from FullParser.ClauseParser import ClauseParser

parser = ClauseParser()

import benepar, spacy
nlp = spacy.load('en_core_web_md')
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


# Toy Dataset file paths
dec_path_toy = "../Datasets/ToyData/finite declarative clauses.txt"
pol_path_toy = "../Datasets/ToyData/finite polar interrogative clauses.txt"
alt_path_toy = "../Datasets/ToyData/finite alternative interrogative clauses.txt"
const_path_toy = "../Datasets/ToyData/finite constituent interrogative clauses.txt"
adv_path_toy = "../Datasets/ToyData/adversarial.txt"


def get_clause_structure(clauses):
    if len (clauses)==0:
        return []
    structure= []
    for entry in clauses:
        sub_clauses = entry['embedded clauses']
        if(len(sub_clauses)) > 0:
            structure += get_clause_structure(entry)
            continue
        structure += []
    return structure

def count_complex_sentences(filename:str):
    golden_df = pd.read_json(filename, orient = 'index')
    print(f'Total: {golden_df.shape[0]} complex: {golden_df.shape[0] - list(golden_df['embedded clauses'].apply(len)).count(1)}')

    
# Use Constituency Parser to parse examples
def parse_golden(filename:str):
    golden_df = pd.read_json(filename, orient = 'index')
    sents = golden_df.sentence
    parses = [{}]*len(sents)
    for i,sent in enumerate(sents):
        sent_doc = nlp(sent)
        parsed_sent = list(sent_doc.sents)[0]
        parses[i] = parser.parse_clauses(parsed_sent)
        
    return (parses, golden_df)


# Get data frames for all types of sentences
dec_parsed, dec_golden = parse_golden(dec_path_golden)
dec_parsed_df = pd.DataFrame(dec_parsed)
pol_parsed, pol_golden = parse_golden(pol_path_golden)
pol_parsed_df = pd.DataFrame(pol_parsed)
alt_parsed, alt_golden = parse_golden(alt_path_golden)
alt_parsed_df = pd.DataFrame(alt_parsed)
const_parsed, const_golden = parse_golden(const_path_golden)
const_parsed_df = pd.DataFrame(const_parsed)
adv_parsed, adv_golden = parse_golden(adv_path_golden)
adv_parsed_df = pd.DataFrame(adv_parsed)
#Putting them all together
golden_df = pd.concat([dec_golden,pol_golden,alt_golden,const_golden,adv_golden])
parsed_df = pd.concat([dec_parsed_df,pol_parsed_df,alt_parsed_df,const_parsed_df,adv_parsed_df])

######### Sandbox ########

def get_predicate_string(clause):
    pred_string = ''
    predicate = clause['predicate']
    for item in predicate:
        pred_string += str(item['str']) + ' '
    return pred_string[:-1]


[get_predicate_string(pol_golden.iloc[i]['embedded clauses'][0]) for i in range(10,90)]

[get_predicate_string(pol_parsed[i]['embedded clauses'][]['predicate']) for i in range(10,90)]

dec_golden.iloc[3]['embedded clauses'][0]['predicate']


def compare_clauses(parsed,golden):
    if len(golden) !=  len(parsed):
        return 'failed'
    comparisons = []
    if len(golden) == 0:
        return 'adversarial'
    for j, golden_data in enumerate(golden):
        comparisons.append({
                'golden_type': golden_data['type'],
                'golden_predicate': get_predicate_string(golden_data),
                'golden_clause': golden_data['clause'],
                'parsed_type': parsed[j]['type'],
                'parsed_predicate': get_predicate_string(parsed[j]),
                'parsed_clause': str(parsed[j]['clause']),
                'embedding': compare_clauses( parsed[j]['embedded clauses'],golden[j]['embedded clauses'])
                })
    return comparisons

def check_stats(parsed,golden):
    evals = []
    for i, parse_embed in enumerate(parsed['embedded clauses']):
        golden_embed = golden.iloc[i]['embedded clauses'] 
        sent = golden.iloc[i]['sentence']
        evals.append({
            'sentence': sent ,
            'comparison': compare_clauses(parse_embed,golden_embed)
            })
    return evals

(parsed_df['embedded clauses'].iloc[0], golden_df['embedded clauses'].iloc[0])
golden_df['embedded clauses'].iloc[0][0]['clause'][0]
str(parsed_df['embedded clauses'].iloc[0][0]['clause'])

x = check_stats(parsed_df,golden_df)
y = pd.DataFrame(x)

y.type.fillna(False).mean()
y.clause.fillna(False).mean()
y.predicate.fillna(False).mean()


failed_sentences = y[y['comparison'] == 'failed']

adverserial_sentences = y[ (y['comparison'] == 'adversarial') ]

coordinated_sentences = y[(y['comparison'].apply(len)>1) & (y['comparison'] != 'adversarial') & (y['comparison'] != 'failed')]

single_sentences = y[(y['comparison'].apply(len)==1) & (y['comparison'] != 'failed') & (y['comparison'] != 'adversarial')]

positive_sentences = y[ (y['comparison'] != 'adversarial') ]



# Quick Averages

def check_comparison(comp,feature:str):
    if comp == 'adversarial':
        return [True]
    if comp == 'failed':
        return [False]
    else:
        return list(map(lambda c: c['golden_'+feature] == c['parsed_'+feature], comp)) 

def evaluate_feature(df,feature: str):
    return df.comparison.apply(lambda x: check_comparison(x,feature))
    #.apply(lambda x: sum(x)/len(x))

np.mean(list(map(sum , evaluate_feature(positive_sentences,'type'))))

np.mean(list(map(sum , evaluate_feature(positive_sentences,'clause'))))

np.mean(list(map(sum , evaluate_feature(positive_sentences,'predicate'))))

np.mean(list(map(sum , evaluate_feature(y,'type'))))

np.mean(list(map(sum , evaluate_feature(y,'clause'))))

np.mean(list(map(sum , evaluate_feature(y,'predicate'))))

# Failed sentences


def replace_brackets(parsed_string):
    # Replace round brackets with square brackets
    replaced_string = parsed_string.replace('(', '[').replace(')', ']')
    # Wrap the string with \begin{forest} and \end{forest}
    final_string = '\\begin{forest} ' + replaced_string + ' \\end{forest}'
    return final_string


trees = ''
for sentence in failed_sentences.sentence:
    trees += replace_brackets(list(nlp(sentence).sents)[0]._.parse_string) + '\n'



##########################


# Get toy data
decl_samples = open(dec_path_toy).read().replace('\n', ' ')
pol_samples = open(pol_path_toy).read().replace('\n', ' ')
const_samples = open(const_path_toy).read().replace('\n', ' ')
alt_samples = open(alt_path_toy).read().replace('\n', ' ')
adv_samples = open(adv_path_toy).read().replace('\n', ' ')
all_examples = decl_samples + pol_samples + const_samples + alt_samples

decl_doc = nlp(decl_samples)
pol_doc = nlp(pol_samples)
alt_doc = nlp(alt_samples)
const_doc = nlp(const_samples)
adv_doc = nlp(adv_samples)

pol_examples_parsed = [parser.get_clause_type(sent) for sent in pol_doc.sents]

adv_examples_parsed = [parser.get_embedded_clause(sent)[0] for sent in adv_doc.sents]

adv_examples_parsed

adv_example_list = list(adv_doc.sents)

adv_examples_failed = []
for i,p in enumerate(adv_examples_parsed):
    if p:
        str(adv_example_.append(adv_example_list[i]))

adv_examples_failed

pd.DataFrame(adv_examples_failed)


hard_adv.to_csv(r'natural_failed_adv.txt', header=None, index=None, sep=' ', mode='a')

# Define the set of trouble makers
def trouble_makers(df):
    return df[df.sentence != df.parsed_sentence]

dec_trouble = trouble_makers(dec_parsed_df)
pol_trouble = trouble_makers(pol_parsed_df)
alt_trouble = trouble_makers(alt_parsed_df)
const_trouble = trouble_makers(const_parsed_df)
adv_trouble = trouble_makers(adv_parsed_df)

# Filter based on the parsing accuracy
all_parsed = pd.concat([dec_parsed_df.drop(dec_trouble.index),
                        pol_parsed_df.drop(pol_trouble.index),
                        alt_parsed_df.drop(alt_trouble.index),
                        const_parsed_df.drop(const_trouble.index),
                        adv_parsed_df.drop(adv_trouble.index)])


# Save Adverserial Fails

adv_parsed = all_parsed[pd.isna(all_parsed['type_real'])]


hard_adv = adv_parsed[adv_parsed['has_clause']]['sentence']

hard_adv.to_csv(r'natural_failed_adv.txt', header=None, index=None, sep=' ', mode='a')


# Clause Accuracy 


no_adv = all_parsed[pd.notna(all_parsed['type_real'])]

no_adv.groupby('type_real')['has_clause'].mean()

## Precision and Recall
true_p = all_parsed[all_parsed.has_clause & all_parsed.has_clause_real]
false_p = all_parsed[all_parsed.has_clause & ~all_parsed.has_clause_real]
false_n = all_parsed[~all_parsed.has_clause & all_parsed.has_clause_real]

all_precision = true_p.shape[0]/(true_p.shape[0]+false_p.shape[0])
all_recall = true_p.shape[0]/(true_p.shape[0]+false_n.shape[0])
all_f1 = 2*all_precision*all_recall/(all_precision+all_recall)

all_accuracy = all_parsed.has_clause==all_parsed.has_clause_real

# Filter based on only detected items and non-adversarial examples
all_predicates = all_parsed[all_accuracy & ~all_parsed.predicate_real.isnull()]

# Predicate Accuracy
all_predicates.loc[:,'predicate_accuracy'] = all_predicates.predicate==all_predicates.predicate_real

all_predicates.predicate_accuracy.mean()

## Predicate accuracy per condition

### Declarative
predicate_accuracy_dec = all_predicates['predicate_accuracy'] [all_predicates['type_real']=='declarative'].mean()
### Alternative
predicate_accuracy_alt = all_predicates['predicate_accuracy'] [all_predicates['type_real']=='alternative'].mean()
### Polar
predicate_accuracy_pol = all_predicates['predicate_accuracy'] [all_predicates['type_real']=='polar'].mean()
### Constituent
predicate_accuracy_const = all_predicates['predicate_accuracy'] [all_predicates['type_real']=='constituent'].mean()


# Type accuracy
all_predicates.loc[:,'type_accuracy'] = all_predicates.type==all_predicates.type_real

all_predicates.type_accuracy.mean()

# Type accuracy per condition

### Declarative
type_accuracy_dec = all_predicates['type_accuracy'] [all_predicates['type_real']=='declarative'].mean()
### Alternative
type_accuracy_alt = all_predicates['type_accuracy'] [all_predicates['type_real']=='alternative'].mean()
### Polar
type_accuracy_pol = all_predicates['type_accuracy'] [all_predicates['type_real']=='polar'].mean()
### Constituent
type_accuracy_const = all_predicates['type_accuracy'] [all_predicates['type_real']=='constituent'].mean()


print('Clause Prediction Precision',all_precision)
print('Clause Prediction Recall',all_recall)
print('Clause Prediction F1',all_f1)
print('Clause Prediction accuracy',all_accuracy.mean())
print('Predicate detection accuracy (Declarative): ',predicate_accuracy_dec )
print('Predicate detection accuracy (Alternative): ',predicate_accuracy_alt )
print('Predicate detection accuracy (Polar): ',predicate_accuracy_pol )
print('Predicate detection accuracy (Constituent): ',predicate_accuracy_const )
print('Type detection accuracy (Declarative): ',type_accuracy_dec )
print('Type detection accuracy (Alternative): ',type_accuracy_alt )
print('Type detection accuracy (Polar): ',type_accuracy_pol )
print('Type detection accuracy (Constituent): ',type_accuracy_const )
