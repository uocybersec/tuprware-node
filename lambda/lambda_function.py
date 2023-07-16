# Example of events:
# 
# Writing a key-value pair
# {
#     "action": "write",
#     "data": {
#         "user_id": "<USER ID>",
#         "instance_id": "<INSTANCE ID>"
#     }
# }
# 
# Reading a key-value pair
# {
#     "action": "read",
#     "user_id": "<USER ID>"
# }
#
# Deleting a key-value pair
# {
#     "action": "delete",
#     "user_id": "<USER ID>"
# }

import boto3

def lambda_handler(event, context):
    db = boto3.resource('dynamodb')
    table = db.Table('containers_spawned')
    action = event['action']
    if action == 'write':
        data = event['data']
        response = table.put_item(Item=data)
    elif action == 'read':
        user_id = event['user_id']
        response = table.get_item(
            Key={
                'user_id': user_id
            }
        )
    elif action == 'delete':
        user_id = event['user_id']
        response = table.delete_item(
            Key={
                'user_id': user_id
            }
        )
    else:
        return {
            'statusCode': 400,
            'body': "Unknown selected action. The action must either be 'read', 'write', or 'delete'."
        }
    
    return {
        'statusCode': 200,
        'body': response
    }

