import json
import os
import boto3
from botocore.exceptions import ClientError

def upload_configuration(config_file: str = 'settings.json') -> dict:
    """
    Loads configuration settings from a specified JSON file.
    :param config_file: The name of the configuration file
    :return: A dictionary containing the configuration settings.
    """
    path = os.path.join(os.path.dirname(__file__), config_file)
    with open(path) as f:
        data = json.load(f)

    return data

class SecretsManager:
    """
    A class for interacting with AWS Secrets Manager.
    """

    def __init__(self, access_key, secret_key, region_name):
        """
        Initialize the SecretsManager with AWS credentials and region.
        """

        self.client = boto3.session.Session().client(
            service_name='secretsmanager',
            region_name=region_name,
            aws_access_key_id=access_key,
            aws_secret_access_key=secret_key
        )

    def get_secret(self, secret_name):
        """
        Retrieve a secret value from AWS Secrets Manager.
        """
        try:
            response = self.client.get_secret_value(SecretId=secret_name)
            return json.loads(response['SecretString'])
        except ClientError as e:
            print(f"An error occurred: {e}")
            raise e

# load configuration
configuration = upload_configuration()

# initialize secret manager
aws_secrets = SecretsManager(configuration.get('aws_access_key'), configuration.get('aws_secret_key'), configuration.get('aws_region_name'))
secret_manager_keys = aws_secrets.get_secret('web3m-test-secrets')