from aitextgen.TokenDataset import TokenDataset
from aitextgen.tokenizers import train_tokenizer
from aitextgen.utils import GPT2ConfigCPU
from aitextgen import aitextgen
import os, sys

text = sys.argv[1]
vocab_file = "aitextgen-vocab.json"
merges_file = "aitextgen-merges.txt"

config = GPT2ConfigCPU()

ai = aitextgen(model="trained_model/pytorch_model.bin", vocab_file=vocab_file, merges_file=merges_file, config=config)

ai.generate_to_file(n=10, prompt=text, max_length=140, temperature=0.6)
