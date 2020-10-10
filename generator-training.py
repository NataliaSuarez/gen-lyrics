from aitextgen.TokenDataset import TokenDataset
from aitextgen.tokenizers import train_tokenizer
from aitextgen.utils import GPT2ConfigCPU
from aitextgen import aitextgen

# Name of text for training
file_name = "spinetta.txt"

# Train a custom Tokenizer
# This will save two files: aitextgen-vocab.json and aitextgen-merges.txt,
# which are needed to rebuild the tokenizer
train_tokenizer(file_name)
vocab_file = "aitextgen-vocab.json"
merges_file = "aitextgen-merges.txt"

# GPT2ConfigCPU is a mini variant of GPT-2 optimized for CPU-training
# e.g. the # of input tokens here is 64 vs. 1024 for base GPT-2.
config = GPT2ConfigCPU()

# Instantiate aitextgen using the created tokenizer and config
ai = aitextgen(vocab_file=vocab_file, merges_file=merges_file, config=config)

# You can build datasets for training by creating TokenDatasets,
# which automatically processes the dataset with the appropriate size.
data = TokenDataset(file_name, vocab_file=vocab_file, merges_file=merges_file, block_size=64, save_cache=True)

# Train :muscle:
ai.train(data, batch_size=16, num_steps=5000)

# Generate text! :sparkles:
ai.generate_to_file(n=10, prompt="Río salvaje", max_length=100, temperature=1.2)
