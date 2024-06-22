import json

from library.service.translator_v2 import translate_text

def lambda_handler(event, context):
    print("Lambda handler:")
    query = event.get('queryStringParameters', {}).get('query')
    model = event.get('queryStringParameters', {}).get('model')
    print("Query: ", query)
    print("Model:", model)
    return {
        "statusCode": 200,
        "headers": {
            "Access-Control-Allow-Origin": "*",  # Adjust this based on your requirements
            "Access-Control-Allow-Headers": "Content-Type,X-Amz-Date,Authorization,X-Api-Key,X-Amz-Security-Token",
            "Access-Control-Allow-Methods": "GET,OPTIONS",  # Adjust this based on your allowed methods
        },
        "body": json.dumps({
            "translation": translate_text(query, model),
            "source": query
        }),
    }
