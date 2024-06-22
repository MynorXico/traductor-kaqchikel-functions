import boto3

ssm = boto3.client('ssm')


def get_secret(secret_name):
    secret = ssm.get_parameter(Name=secret_name, WithDecryption=True)
    return secret.get('Parameter', {}).get('Value')
