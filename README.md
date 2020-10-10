# gen-lyrics

Some scripts for learn making datasets, training [aitextgen](https://docs.aitextgen.io/) and using a trained model.

*Aitextgen is a library for generating text using ia with [GPT-2](https://openai.com/blog/better-language-models/).*

## Requirements

- python3
- virtualenv(optional)

## Install

For install libraries run `pip install -r requirements.txt`

### Dataset

#### Songs

For use `songs2txt.py` run `python songs2txt.py artist`.

This script creates a `artist` folder with songs(using letras.com) in txt files.

#### Pdf files

For use `pdf2txt.py` run `python pdf2txt.py some-book.pdf some-book.txt`.

This script creates a `some-book.txt` file based on pdf text.

#### Merging text

For use `merge-texts.py` run `python merge-texts.py "./artist" artist.txt`

### Train

#### Using Colab

For use colab or jupyter, download `aitextgen-colab.ipynb` :)

#### Local environment

For `generator-training` run `python generator-training.py`

### Generating text

For generate text use `generator-with-trained-model` script. Run `python generator-with-trained-model.py 'some frase'`.

:sparkles: :sparkles: :sparkles: