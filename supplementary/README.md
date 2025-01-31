# Automatic Extraction of Clausal Embedding Based on Large-Scale Text Data

`Annotation/`: GECS annotations for the structured and flattened representations of embedded clauses can be found in.

`src/`: The `ClauseParser` tool used to parse sentences in GECS 

`./sample_parses/`: The large scale dataset extracted from Dolma (omitted for submission size limitations)

`Statistics/`: The GECS evaluations and large scale analyses are in 



Assuming all python requirements the right model for parsing:

```
python -m spacy download en_core_web_sm
```

And in python for benepar:
```
>>>import benepar
>>> benepar.download('benepar_en3')
```
