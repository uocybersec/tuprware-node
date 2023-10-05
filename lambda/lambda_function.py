import boto3
from urllib.parse import urljoin
from requests import get, post, put, delete

TEST_NODE_ADDRESS = "REDACTED" # for testing purposes

def get_proxy_secret() -> str: # fetch the proxy secret from DynamoDB
    db = boto3.resource('dynamodb') 
    table = db.Table('tuprware_internal_data')
    secret = table.get_item(
        Key={
            'data_name': 'tuprware_proxy_secret'
        }
    )['Item']['secret_value']
    return secret

def route_traffic(node_address: str, path: str, method: str, headers: dict, body: dict, proxy_secret: str) -> [str, int]:
    # node_address should contain the node's ipv4 AND port (which is always 5000)
    # supported HTTP methods: GET, POST, PUT, DELETE
    method = method.upper()
    headers['X-Tuprware-Proxy-Secret'] = proxy_secret
    endpoint = urljoin(node_address, path)
    res = None
    if method == "POST":
        res = post(endpoint, headers=headers, data=body)
    elif method == "GET":
        res = get(endpoint, headers=headers, data=body)
    elif method == "PUT":
        res = put(endpoint, headers=headers, data=body)
    elif method == "DELETE":
        res = delete(endpoint, headers=headers, data=body)
    else:
        return None, None

    return res.content.decode(), res.status_code

def lambda_handler(event: any, context: any) -> any:
    path = event['requestContext']['http']['path']
    headers = event['headers']
    method = event['requestContext']['http']['method']
    body = event.get('body') # will return None if there is no body

    proxy_secret = get_proxy_secret()

    nodeResponse, nodeStatusCode = route_traffic(
        node_address=TEST_NODE_ADDRESS,
        path=path, 
        method=method, 
        headers=headers, 
        body=body, 
        proxy_secret=proxy_secret
    ) # route the incoming HTTP request to one of the nodes (EC2) and get the response

    return {
        'lambdaStatusCode': 200,
        'nodeStatusCode': nodeStatusCode,
        'nodeResponse:': nodeResponse
    }
