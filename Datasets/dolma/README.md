# Downloading dolma

For this, you must edit the file `load_dolma.sh` and set the following parameters:

- `DATA_DIR`: directory to to load the dolma version of interest
- `DOLMA_ERSION`: version of dolma 
    - `v1.txt`
    - `v1.6`
    - `v1_5-sample.txt`
    - `v1_5.txt`
    - `v1_6-sample.txt`
    - `v1_6.txt`
    - `v1_7.txt`

If you would like to unzip the files upon loading the dataset you must pass `load_json` after calling the shell script.

Without loading JSON files

```
source scripts/load_dolma.sh
```

Loading JSON files

```
source scripts/load_dolma.sh load_json
```

# Extracting dataset text

## 1. Installing Rust

To extract all of the text entries you will need to run an executable function on each of the JSON files and dump the text data into a separate directory.

This module needs to be compiled in the rust programming language compatible with your computer architecture.

First load the rust programming language if you do not already have it

```
curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh
```

## 2. Compiling dolma json text extractor

Once you have the rust programming language loaded on your machine you can compile the script to extract text from all JSON files

```
$ cd rust/extract_json/
$ cagro build
$ cd ../../
```

The resulting executable should be compiled in `/target/debug/` as `extract_json`.
Then you may return to the previous directory and extract all json text with the

## 3. Extract all JSON text

Now that the extraction script is compiled you can run `extract_dataset.sh` to load all the text in the dataset.
Be sure to edit the appropriate `DATA_DIR` and `TEXT_DIR`

```
source scripts/extract_dataset.sh
```
