import json
import sys

sys.path.append('../')
from translator_library.service.translator import translate_text
from translator_library.service.translator import init_translator

init_translator()


def lambda_handler(event, context):
    query = event.get('queryStringParameters', {}).get('query')
    return {
        "statusCode": 200,
        "headers": {
            "Access-Control-Allow-Origin": "*",  # Adjust this based on your requirements
            "Access-Control-Allow-Headers": "Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token",
            "Access-Control-Allow-Methods": "GET,OPTIONS",  # Adjust this based on your allowed methods
        },
        "body": json.dumps({
            "translation": translate_text(query),
            "source": query
        }),
    }
