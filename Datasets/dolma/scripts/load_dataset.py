import os
from datasets import load_dataset

os.environ["DATA_DIR"] = "./dolma_sample_example/"
dataset = load_dataset("allenai/dolma", split="train")

