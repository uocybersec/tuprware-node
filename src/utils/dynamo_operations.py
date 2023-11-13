import boto3
import docker
import json
import os
from dotenv import load_dotenv

load_dotenv()

# THERE NEEDS TO BE A THREAD RUNNING SOMETHING THAT CONSTANTLY KEEPS DYNAMODB AND THE NODE IN SYNC

dynamoDB_worker = boto3.client(
    'lambda',
    aws_access_key_id=os.getenv('AWS_ACCESS_KEY'),
    aws_secret_access_key=os.getenv('AWS_SECRET_KEY'),
    region_name='us-east-1'
)

docker_client = docker.from_env()

def invoke_lambda(payload: object) -> object:
    response = dynamoDB_worker.invoke(
        FunctionName='dynamoDBWorker',
        Payload=json.dumps(payload).encode()
    )
    return json.loads(response['Payload'].read())

def get_running_instance_id(user_id: str) -> str:
    payload = {
        'action': 'read',
        'user_id': user_id
    }
    response = invoke_lambda(payload)
    body = response['body']
    if body.get('Item'):
        return body['Item']['instance_id'] # get the instance id in dynamoDB

    return None

def set_running_instance_id(user_id: str, instance_id: str) -> int:
    payload = {
        'action': 'write',
        'data': {
            'user_id': user_id,
            'instance_id': instance_id
        }
    }
    response = invoke_lambda(payload)
    return response['statusCode']

def delete_running_instance_id(user_id: str) -> int:
    payload = {
        'action': 'delete',
        'user_id': user_id
    }
    response = invoke_lambda(payload)
    return response['statusCode']

