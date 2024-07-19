import json, time

def read_large_json(file_path):
    with open(file_path, 'r', encoding = 'utf-8') as f:
        for line in f:
            yield line

import benepar, spacy
nlp = spacy.load('en_core_web_md')
if spacy.__version__.startswith('2'):
    nlp.add_pipe(benepar.BeneparComponent("benepar_en3"))
else:
    nlp.add_pipe("benepar", config={"model": "benepar_en3"})



#########################
# DEBUGGING
#########################


# With preprocessed text
count = 0
t = time.time()
with open('cc_text/extracted_text.txt', 'r', encoding = 'utf-8') as f:
    for line in f:
        #if count < 40:
        #    count+=1
        #    continue
        try:
            text = line.strip(' \t\n\r')
            doc = nlp(text)
            print(f'count: {count}, sents: {len(list(doc.sents))}')
            count += 1
            if count > 100:
                print(f'Parse time: {time.time()-t}')
                break
        except Exception as e:
            print(f"Error encountered while processing line: {line.strip()}")
            pass  # Do nothing, continue to next line

# With JSON text
count = 0
with open('./loaded_samples/cc_en_head-0600.json', 'r') as f:
    for line in f:
        entry = json.loads(line)
        text = entry['text']#.strip('\t\n\r')
        print(f'count: {count}, text: {text}')
        count += 1
        t = time.time()
        doc = nlp(text)
        print(len(list(doc.sents)))
        print(f'Parse time: {time.time()-t}')
        count += 1
        if count >10:
            break

