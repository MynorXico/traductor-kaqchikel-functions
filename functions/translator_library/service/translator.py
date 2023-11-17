import zipfile
import sys
from subword_nmt.apply_bpe import BPE
import ctranslate2
import codecs

sys.path.append('../')

from translator_library.client.s3_client import download_file
from translator_library.client.ssm_client import get_secret
from translator_library.utils.preprocessing import clean
from translator_library.utils.preprocessing import detokenize

local_file_dir = "/tmp"
bucket_name = get_secret('/traductor-kaqchikel-functions/BUCKET_NAME')
model_name = get_secret('/traductor-kaqchikel-functions/MODEL_NAME')

vocab_file = f"{model_name}_vocab.txt"
local_vocab_file = f"{local_file_dir}/{vocab_file}"


def init_translator():
    download_vocabulary()
    download_model()
    unzip_model()


def download_vocabulary():
    download_file(bucket_name, vocab_file, local_vocab_file)


def download_model():
    key = f"{model_name}.zip"
    local_file_path = f"{local_file_dir}/{key}"
    download_file(bucket_name, key, local_file_path)


def get_bpe_text(text):
    encoder = BPE(codecs.open(local_vocab_file, encoding='utf-8'))
    return encoder.process_line(text)


def get_translation(text):
    translator = ctranslate2.Translator(f"{local_file_dir}/{model_name}/{model_name}")
    return " ".join(translator.translate_batch([text.split()])[0][0]['tokens'])


def unzip_model():
    with zipfile.ZipFile(f"{local_file_dir}/{model_name}.zip", 'r') as zip_ref:
        print("Unzipping model")
        zip_ref.extractall(f"{local_file_dir}/{model_name}")
        print("Model unzipped successfully")


def translate_text(sentence):
    print("Original text: ", sentence)
    preprocessed_sentence = clean(sentence)
    tokenized_sentence = get_bpe_text(preprocessed_sentence)
    tokenized_translation = get_translation(tokenized_sentence)
    detokenized_translation = detokenize(tokenized_translation)
    print("Translated text: ", detokenized_translation)
    return detokenized_translation
