# Stanford Neural Parser

import stanza

nlp = stanza.Pipeline(lang='en', processors='tokenize,pos,constituency')

doc = nlp('Jim know this sentence has an embedded clause')
for sentence in doc.sentences:
        print(sentence.constituency)

# Parse the example sentences


