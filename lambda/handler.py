import json
import boto3
import uuid 
from datetime import datetime

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table('tasks')

def lambda_handler(event, context):
    method = event['httpMethod']

    if method == 'GET':
        return get_tasks()
    elif method == 'POST':
        body = json.loads(event['body'])
        return create_task(body)
    else:
        return response(405,{'error':'Method not allowed'})
    
def get_tasks():
    result = table.scan()
    return response(200, result['Items'])

def create_task(body):
    task = {
        'task_id':str(uuid.uuid4()),
        'title':body['title'],
        'status':'pending',
        'created_at':datetime.utcnow().isoformat()
    }

    table.put_item(Item=task)
    return response(201, task)

def response(status_code, body):
    return {
        'statusCode': status_code,
        'headers': {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*'
        },
        'body': json.dumps(body)
    }