import json
from pathlib import Path
from encord import EncordUserClient, Project
from encord.project_ontology.classification_type import ClassificationType
import boto3
from botocore.exceptions import ClientError


def create_label():
    secret_name = "prasunSSHKey"
    region_name = "us-east-1"

    # Create a Secrets Manager client
    session = boto3.session.Session()
    client = session.client(
        service_name='secretsmanager',
        region_name=region_name
    )

    try:
        get_secret_value_response = client.get_secret_value(
            SecretId=secret_name
        )
    except ClientError as e:
        # For a list of exceptions thrown, see
        # https://docs.aws.amazon.com/secretsmanager/latest/apireference/API_GetSecretValue.html
        raise e

    # Decrypts secret using the associated KMS key.
    secret = get_secret_value_response['SecretString']
    
    user_client = EncordUserClient.create_with_ssh_private_key(secret)
    project: Project = user_client.get_project("65b8dd3a-cb7b-4cc2-a6b8-b9cdc31105f2")
    success: bool = project.add_classification(
        "Superhero",
        classification_type=ClassificationType.RADIO,
        required=True,
        options=["Batman", "Superman"],
    )
    print(success)
    return success
    
def lambda_handler(event, context):
    
    valid_token = create_label()
    print(valid_token)
    if valid_token:
        response = {
            'statusCode': 200,
            'body': json.dumps('Hello from Lambda!')
            }
    
        return response
    else:
        response = {
            'statusCode': 400,
            'body': json.dumps('Error from Lambda!')
            } 
        return response;
