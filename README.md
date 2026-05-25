
# Task Manager — Serverless AWS Application

## Overview
A serverless task management application built with AWS Lambda, API Gateway, and DynamoDB. The project demonstrates cloud-native backend development, automated testing with pytest and moto, and a fully automated CI/CD pipeline using GitHub Actions.

## Architecture

Client (HTTP Request)
        ↓
   API Gateway (REST)
        ↓
  Lambda Function (Python)
        ↓
   DynamoDB (Storage)

## Tech Stack
- Backend: Python, AWS Lambda
- Database: AWS DynamoDB
- API: AWS API Gateway
- Infrastructure: AWS IAM
- Testing: pytest, moto (AWS mocking)
- CI/CD: GitHub Actions

## Project Structure
task-manager-mendix/
├── app/
│   └── handler.py
├── tests/
│   ├── conftest.py
│   └── test_handler.py
├── .github/
│   └── workflows/
│       └── deploy.yml
└── README.md

## API Endpoints
GET /tasks - Retrieve all tasks
POST /tasks - Create a new task

## Request and Response Examples

GET /tasks Response:
[
  {
    "task_id": "7b7e9941-e7ce-4841-8f38-90f7a3389102",
    "title": "My first task",
    "status": "pending",
    "created_at": "2026-05-25T15:40:17.478067"
  }
]

POST /tasks Request:
{
  "title": "My first task"
}

POST /tasks Response:
{
  "task_id": "7b7e9941-e7ce-4841-8f38-90f7a3389102",
  "title": "My first task",
  "status": "pending",
  "created_at": "2026-05-25T15:40:17.478067"
}

## CI/CD Pipeline
The GitHub Actions pipeline runs on every push to main:
1. Sets up Python 3.11
2. Installs dependencies including pytest and moto
3. Runs all unit tests
4. If tests pass, packages and deploys the Lambda function to AWS
5. If tests fail, deployment is blocked

## Automated Testing
Tests use moto to mock AWS services locally without requiring real AWS credentials.

Three test cases are covered:
- GET returns 200 and empty list when no tasks exist
- POST creates a task and returns 201 with correct fields
- GET returns the created task after it has been added

## Running Tests Locally
pip install pytest moto boto3
pytest tests/ -v

## Live API
Base URL: https://8vtysbua06.execute-api.us-east-1.amazonaws.com/prod

## Low-Code Platform Note
This project was planned to include a Mendix frontend to demonstrate low-code platform integration with the REST API backend. Due to account verification issues during setup, the frontend layer was not completed. I am currently pursuing the Mendix Rapid Developer certification to build hands-on experience with the platform.

## Key Engineering Decisions
- SQS not used here: for a simple task manager direct Lambda invocation via API Gateway is sufficient. SQS would be added for async processing at scale.
- DynamoDB over PostgreSQL: access patterns are simple key-value lookups by task ID with no complex joins needed.
- moto for testing: mocking AWS services locally makes tests fast, free, and independent of real AWS infrastructure.
