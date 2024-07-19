import json, time

def read_large_json(file_path):
    with open(file_path, 'r', encoding = 'utf-8') as f:
        for line in f:
            yield line

def extract_json_text(input_dir,output_dir,filename,chunk_size = 100):
    texts = []
    entry_count = 0

    for line in read_large_json(input_dir+filename+'.json'):
        entry = json.loads(line)
        texts.append(entry['text'])
        entry_count += 1
        if entry_count > chunk_size:
            with open(output_dir+filename+'.txt', 'a') as out_f:
                out_f.write('\n'.join(texts))
        if texts:
            with open(output_dir+filename+'.txt', 'a') as out_f:
                out_f.write('\n'.join(texts))
# Usage
file = 'v1_5r2_sample-0000'
input_dir = './loaded_samples/'
output_dir = './sample_text/'

extract_json_text(input_dir,output_dir,file)
