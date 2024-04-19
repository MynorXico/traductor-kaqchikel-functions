import zipfile
import sys
from subword_nmt.apply_bpe import BPE
import ctranslate2
import codecs
import pyonmttok

sys.path.append('../')

from translator_library.client.s3_client import download_file
from translator_library.client.ssm_client import get_secret
from translator_library.utils.preprocessing import clean
from translator_library.utils.preprocessing import detokenize

local_file_dir = "/tmp"
bucket_name = get_secret('/traductor-kaqchikel-functions/BUCKET_NAME')

eskaq_model_name = get_secret('/traductor-kaqchikel-functions/ESKAQ_MODEL_NAME')
kaqes_model_name = get_secret('/traductor-kaqchikel-functions/KAQES_MODEL_NAME')

eskaq_vocab_file = f"{eskaq_model_name}_vocab.txt"
kaqes_vocab_file = f"{kaqes_model_name}_vocab.txt"

local_eskaq_vocab_file = f"{local_file_dir}/{eskaq_vocab_file}"
local_kaqes_vocab_file = f"{local_file_dir}/{kaqes_vocab_file}"


def init_translator():
    download_vocabularies()
    download_models()
    unzip_models()


def download_vocabularies():
    download_file(bucket_name, f"eskaq/{eskaq_vocab_file}", local_eskaq_vocab_file)
    download_file(bucket_name, f"kaqes/{kaqes_vocab_file}", local_kaqes_vocab_file)

def download_models():
    # eskaq
    eskaq_key = f"{eskaq_model_name}.zip"
    eskaq_local_file_path = f"{local_file_dir}/{eskaq_key}"
    download_file(bucket_name, f"eskaq/{eskaq_key}", eskaq_local_file_path)
    # kaqes
    kaqes_key = f"{kaqes_model_name}.zip"
    kaqes_local_file_path = f"{local_file_dir}/{kaqes_key}"
    download_file(bucket_name, f"kaqes/{kaqes_key}", kaqes_local_file_path)

def unzip_models():
    with zipfile.ZipFile(f"{local_file_dir}/{eskaq_model_name}.zip", 'r') as zip_ref:
        print("Unzipping model")
        zip_ref.extractall(f"{local_file_dir}/{eskaq_model_name}")
        print("Model unzipped successfully")
    with zipfile.ZipFile(f"{local_file_dir}/{kaqes_model_name}.zip", 'r') as zip_ref:
        print("Unzipping model")
        zip_ref.extractall(f"{local_file_dir}/{kaqes_model_name}")
        print("Model unzipped successfully")





def get_bpe_text(text, model):
    vocab_file = local_kaqes_vocab_file if model == 'kaqes' else local_eskaq_vocab_file

    tokenizer = pyonmttok.Tokenizer(
        "aggressive",
        bpe_model_path=vocab_file,
        joiner_annotate=True,
        segment_numbers=True
    )

    tokenized_text, _ = tokenizer.tokenize(text)
    return ' '.join(tokenized_text)

def get_translation(text, model):
    model_name = kaqes_model_name if model == 'kaqes' else eskaq_model_name
    translator = ctranslate2.Translator(f"{local_file_dir}/{model_name}/{model_name}")
    return " ".join(translator.translate_batch([text.split()])[0][0]['tokens'])





def translate_text(sentence, model):
    print("Original text: ", sentence)
    preprocessed_sentence = clean(sentence)
    tokenized_sentence = get_bpe_text(preprocessed_sentence, model)
    tokenized_translation = get_translation(tokenized_sentence, model)
    detokenized_translation = detokenize(tokenized_translation)
    print("Translated text: ", detokenized_translation)
    return detokenized_translation
