import sys
sys.path.append('../ConstituencyParser/')

from ConstituencyParser import ConstituencyParser

parser = ConstituencyParser()

import benepar, spacy
nlp = spacy.load('en_core_web_md')
if spacy.__version__.startswith('2'):
    nlp.add_pipe(benepar.BeneparComponent("benepar_en3"))
else:
    nlp.add_pipe("benepar", config={"model": "benepar_en3"})

import pandas as pd

# Golden Data file paths
dec_path_golden = "../Datasets/Golden/declarative_golden_set_checked.csv"
pol_path_golden = "../Datasets/Golden/polar_golden_set_checked.csv"
alt_path_golden = "../Datasets/Golden/alternative_golden_set_checked.csv"
const_path_golden = "../Datasets/Golden/golden_set_constituents_checked.csv"
adv_path_golden = "../Datasets/Golden/adversarials_golden_set_checked.csv"

# Toy Dataset file paths
dec_path_toy = "../Datasets/ToyData/finite declarative clauses.txt"
pol_path_toy = "../Datasets/ToyData/finite polar interrogative clauses.txt"
alt_path_toy = "../Datasets/ToyData/finite alternative interrogative clauses.txt"
const_path_toy = "../Datasets/ToyData/finite constituent interrogative clauses.txt"
adv_path_toy = "../Datasets/ToyData/adversarial.txt"

# Use Constituency Parser to parse examples
def parse_golden(filename:str):
    golden_df = pd.read_csv(filename, usecols = [1,2,3,4], header=None, names = ['sent','has_clause','type','pred'])
    sents = golden_df.sent
    parses = [{}]*len(sents)
    for i,sent in enumerate(sents):
        sent_doc = nlp(sent)
        parsed_sent = list(sent_doc.sents)[0]
        parse = parser.get_embedded_clause(parsed_sent)
        type_parse =  parser.get_clause_type(parsed_sent)
        parses[i] = {'sentence': sent ,
                     'parsed_sentence' : str(parsed_sent),
                     'has_clause': parse[0], 
                     'predicate' : str(parse[1]),
                     'clause' : str(parse[2]),
                     'type' : type_parse,
                     'has_clause_real' : bool(golden_df.loc[i].has_clause),
                     'predicate_real': golden_df.loc[i].pred,
                     'type_real': golden_df.loc[i].type,
                     }
    return parses

# Get data frames for all types of sentences
dec_parsed = parse_golden(dec_path_golden)
dec_parsed_df = pd.DataFrame(dec_parsed)
pol_parsed = parse_golden(pol_path_golden)
pol_parsed_df = pd.DataFrame(pol_parsed)
alt_parsed = parse_golden(alt_path_golden)
alt_parsed_df = pd.DataFrame(alt_parsed)
const_parsed = parse_golden(const_path_golden)
const_parsed_df = pd.DataFrame(const_parsed)
adv_parsed = parse_golden(adv_path_golden)
adv_parsed_df = pd.DataFrame(adv_parsed)

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
