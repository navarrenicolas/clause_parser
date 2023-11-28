import json
from ClauseParser import ClauseParser

##
# Import the examples
## 

decl_samples = open('../Datasets/ClauseEmbeddingExamples/finite-declarative-clauses.txt').read().replace('\n', ' ')
pol_samples = open('../Datasets/ClauseEmbeddingExamples/finite-polar-interrogative-clauses.txt').read().replace('\n', ' ')
const_samples = open('../Datasets/ClauseEmbeddingExamples/finite-consituent-interrogative-clauses.txt').read().replace('\n', ' ')
alt_samples = open('../Datasets/ClauseEmbeddingExamples/finite-alternative-interrogative-clauses.txt').read().replace('\n', ' ')
adv_samples = open('../Datasets/ClauseEmbeddingExamples/adversarial.txt').read().replace('\n', ' ')
all_examples = decl_samples + pol_samples + const_samples + alt_samples

## Parser
parser = ClauseParser()

parsed_examples = parser.get_embedded_clauses(all_examples)

filename = "../Parsed_Data/parsed_examples.json"
# Open the file in write mode
with open(filename, "w") as file:
    # Pass the file object to json.dump()
    json.dump(parsed_examples, file)

##
# Import dataset
##
#common_crawl_sample = open('../Datasets/cc_en_head-0000_sample.txt').read().replace('\n', ' ')


