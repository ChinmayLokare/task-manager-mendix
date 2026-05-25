import json
import boto3
import pytest
from moto import mock_dynamodb
from lambda.handler import lambda_handler

@mock_dynamodb
def test_get_tasks_empty():
    # Set up mock DynamoDB
    dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
    dynamodb.create_table(
        TableName='tasks',
        KeySchema=[{'AttributeName': 'task_id', 'KeyType': 'HASH'}],
        AttributeDefinitions=[{'AttributeName': 'task_id', 'AttributeType': 'S'}],
        BillingMode='PAY_PER_REQUEST'
    )

    # Test GET with empty table
    event = {'httpMethod': 'GET', 'body': None}
    result = lambda_handler(event, None)

    assert result['statusCode'] == 200
    assert json.loads(result['body']) == []

@mock_dynamodb
def test_create_task():
    # Set up mock DynamoDB
    dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
    dynamodb.create_table(
        TableName='tasks',
        KeySchema=[{'AttributeName': 'task_id', 'KeyType': 'HASH'}],
        AttributeDefinitions=[{'AttributeName': 'task_id', 'AttributeType': 'S'}],
        BillingMode='PAY_PER_REQUEST'
    )

    # Test POST creating a task
    event = {
        'httpMethod': 'POST',
        'body': json.dumps({'title': 'Test task'})
    }
    result = lambda_handler(event, None)
    body = json.loads(result['body'])

    assert result['statusCode'] == 201
    assert body['title'] == 'Test task'
    assert body['status'] == 'pending'
    assert 'task_id' in body

@mock_dynamodb
def test_get_tasks_after_create():
    # Set up mock DynamoDB
    dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
    dynamodb.create_table(
        TableName='tasks',
        KeySchema=[{'AttributeName': 'task_id', 'KeyType': 'HASH'}],
        AttributeDefinitions=[{'AttributeName': 'task_id', 'AttributeType': 'S'}],
        BillingMode='PAY_PER_REQUEST'
    )

    # Create a task first
    post_event = {
        'httpMethod': 'POST',
        'body': json.dumps({'title': 'Test task'})
    }
    lambda_handler(post_event, None)

    # Now GET and verify it's there
    get_event = {'httpMethod': 'GET', 'body': None}
    result = lambda_handler(get_event, None)
    body = json.loads(result['body'])

    assert result['statusCode'] == 200
    assert len(body) == 1
    assert body[0]['title'] == 'Test task'