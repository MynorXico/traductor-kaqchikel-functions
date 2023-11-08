import json
import sys


from subword_nmt.apply_bpe import BPE
import ctranslate2
import codecs

import boto3
import zipfile

import os

sys.path.append('../')
def download_file_from_s3(bucket_name, key, local_file_path):
    # Create an S3 client
    s3 = boto3.client('s3')

    # Download the file
    try:
        s3.download_file(bucket_name, key, local_file_path)
        print(f"File downloaded successfully to {local_file_path}")
    except Exception as e:
        print(f"Error downloading file: {e}")

# Example usage
bucket_name = 'mx-models'
key = 'bpe-vocab-es-merged-before.txt'  # Specify the key or path of the file in the bucket
local_file_path = '/tmp/bpe-vocab-es-merged-before.txt'  # Specify the local path where you want to save the file

download_file_from_s3(bucket_name, key, local_file_path)


bucket_name = 'mx-models'
key = '90018.zip'  # Specify the key or path of the file in the bucket
local_file_path = '/tmp/90018.zip'  # Specify the local path where you want to save the file

download_file_from_s3(bucket_name, key, local_file_path)


with zipfile.ZipFile('/tmp/90018.zip', 'r') as zip_ref:
    zip_ref.extractall('/tmp/90018')


# import requests


def clean(sentence):
    sentence = sentence.lower()
    sentence = sentence.strip()
    sentence = sentence.replace("’", "'")
    sentence = sentence.replace('"', "")
    sentence = sentence.replace("’", "'")  # r"[\s]+[\n]+")
    sentence = sentence.replace(r"\t", " ")
    sentence = sentence.replace(r"[\s]+[\n]+", " ")
    sentence = sentence.replace(r"\s", " ")
    return sentence

def detokenize(sentence):
    return sentence.replace("@@ ", "")

def lambda_handler(event):
    """Sample pure Lambda function

    Parameters
    ----------
    event: dict, required
        API Gateway Lambda Proxy Input Format

        Event doc: https://docs.aws.amazon.com/apigateway/latest/developerguide/set-up-lambda-proxy-integrations.html#api-gateway-simple-proxy-for-lambda-input-format

    context: object, required
        Lambda Context runtime methods and attributes

        Context doc: https://docs.aws.amazon.com/lambda/latest/dg/python-context-object.html

    Returns
    ------
    API Gateway Lambda Proxy Output Format: dict

        Return doc: https://docs.aws.amazon.com/apigateway/latest/developerguide/set-up-lambda-proxy-integrations.html
    """

    # try:
    #     ip = requests.get("http://checkip.amazonaws.com/")
    # except requests.RequestException as e:
    #     # Send some context about this error to Lambda Logs
    #     print(e)

    #     raise e

    es_bpe = BPE(codecs.open("/tmp/bpe-vocab-es-merged-before.txt", encoding='utf-8'))
    translator = ctranslate2.Translator("/tmp/90018/90018")
    query = event.get('queryStringParameters', {}).get('query')
    print("Original text: ", query)
    query = clean(query)
    bpe_tokenized = es_bpe.process_line(query)
    res = " ".join(translator.translate_batch([bpe_tokenized.split()])[0][0]['tokens'])
    print("Translated text: ", res)

    return {
        "statusCode": 200,
        "headers": {
            "Access-Control-Allow-Origin": "*",  # Adjust this based on your requirements
            "Access-Control-Allow-Headers": "Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token",
            "Access-Control-Allow-Methods": "GET,OPTIONS",  # Adjust this based on your allowed methods
        },
        "body": json.dumps({
            "translation": detokenize(res).replace("@@", ""), #"hello world",
            # "location": ip.text.replace("\n", "")
            "source": query
        }),
    }
