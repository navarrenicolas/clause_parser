# Automatic Extraction of Clausal Embedding Based on Large-Scale Text Data

**Iona Carslaw, Sivan Milton, Nicolas Navarre, Ciyang Qing, Wataru Ueagaki**

## Navigation

`Annotation/`: GECS annotations for the structured and flattened representations of embedded clauses can be found in.

`src/`: The `ClauseParser` tool used to parse sentences in GECS 

`Statistics/`: The GECS evaluations and large scale analyses

`Datasets/`: 
- Instructions on how to download and extract text data from dolma as 
- Toy (hand-crafted) examples of embedded clause sentences

## Parsing Details

Assuming all python requirements the right model for parsing:

```
python -m spacy download en_core_web_sm
```

And in python for benepar:
```
>>>import benepar
>>> benepar.download('benepar_en3')
```
