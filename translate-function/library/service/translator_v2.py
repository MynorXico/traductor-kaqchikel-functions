import zipfile
import sys
from subword_nmt.apply_bpe import BPE
import ctranslate2
import codecs
import pyonmttok

import os

sys.path.append('../')

from library.client.s3_client import download_file
from library.client.ssm_client import get_secret
from library.utils.preprocessing import clean
from library.utils.preprocessing import detokenize

local_file_dir = "/tmp"

bucket_name = get_secret('/traductor-kaqchikel-functions/BUCKET_NAME')

downloaded_models = []
print("Only first time:", os.listdir(local_file_dir))
def get_model_name(model):
    upper_model = model.upper()
    return get_secret(f"/traductor-kaqchikel-functions/{upper_model}_MODEL_NAME")


def download_model(model, model_name):
    print("Downloaded models:", downloaded_models)
    key = f"{model_name}.zip"
    local_file_path = f"{local_file_dir}/{key}"
    download_file(bucket_name, f"{model}/{key}", local_file_path)
    downloaded_models.append(model_name)
    return local_file_path


def download_vocabulary(model, model_name):
    vocab_file_s3_key = f"{model_name}_vocab.txt"
    vocab_file_local_path = f"{local_file_dir}/{vocab_file_s3_key}"
    download_file(bucket_name, f"{model}/{vocab_file_s3_key}", vocab_file_local_path)
    return vocab_file_local_path


def unzip_model(model_name):
    with zipfile.ZipFile(f"{local_file_dir}/{model_name}.zip", "r") as zip_ref:
        print(f"Unzipping model {model_name}")
        zip_ref.extractall(f"{local_file_dir}/{model_name}")
        print(f"Model unzipped successfully {model_name}")


def get_bpe_text(text, vocab_file_path):
    tokenizer = pyonmttok.Tokenizer(
        "aggressive",
        bpe_model_path=vocab_file_path,
        joiner_annotate=True,
        segment_numbers=True
    )

    tokenized_text, _ = tokenizer.tokenize(text)
    return ' '.join(tokenized_text)


def get_translation(text, model_name):
    print("Before loading translator")
    translator = ctranslate2.Translator(f"{local_file_dir}/{model_name}/{model_name}")
    print("Params: ", [text.split()])
    print("Result: ", translator.translate_batch([text.split()]))
    print("After loading translator:", translator.translate_batch([text.split()])[0][0]['tokens'])
    return " ".join(translator.translate_batch([text.split()])[0][0]['tokens'])


def translate_text(sentence, model):
    print("Original text:", sentence)
    preprocessed_sentence = clean(sentence)

    model_name = get_model_name(model)
    # Download vocab
    vocab_path = download_vocabulary(model, model_name)
    # Tokenize vocab
    tokenized_sentence = get_bpe_text(preprocessed_sentence, vocab_path)
    # Download model
    download_model(model, model_name)
    # Unzip model
    unzip_model(model_name)
    # Get translation
    print("Before tokenized translation")
    tokenized_translation = get_translation(tokenized_sentence, model_name)
    print("After tokenized translation")
    detokenized_translation = detokenize(tokenized_translation)
    print("Translated text: ", detokenized_translation)
    return detokenized_translation
