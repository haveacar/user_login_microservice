import json
import os
import boto3
from botocore.exceptions import ClientError, NoCredentialsError


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


def send_email_smtp(recipient: str, subject: str, message: str, charset='UTF-8', sender: str = "web3m_test@coart.space",
                    region: str = 'us-east-1'):
    """
    Func send email by SMTP AWS
    Args:
        recipient: email recipient str
        subject: email subject str
        body_text: body str
        body_html: body str
        charset: UTF-8
        sender: email sender str
        region: str region

    """
    # Create a new SES client
    client = boto3.client('ses',
                          region_name=region,
                          aws_access_key_id=configuration.get('mail_access'),
                          aws_secret_access_key=configuration.get('mail_secret')
                          )

    try:
        # Provide the contents of the email.
        response = client.send_email(
            Destination={'ToAddresses': [recipient]},
            Message={
                'Body': {
                    'Html': {'Charset': charset, 'Data': message},
                    'Text': {'Charset': charset, 'Data': message},
                },
                'Subject': {'Charset': charset, 'Data': subject},
            },
            Source=sender,
        )
        print("Email sent! Message ID:"),
        print(response['MessageId'])

        return response.get('ResponseMetadata').get('HTTPStatusCode')

    except ClientError as e:
        print(e.response['Error']['Message'])
    except NoCredentialsError:
        print("Credentials not available")


# load configuration
configuration = upload_configuration()

# initialize secret manager
aws_secrets = SecretsManager(configuration.get('aws_access_key'), configuration.get('aws_secret_key'),
                             configuration.get('aws_region_name'))
secret_manager_keys = aws_secrets.get_secret('web3m-test-secrets')
