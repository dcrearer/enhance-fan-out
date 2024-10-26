import json
import os
import base64
import boto3
import logging


logger = logging.getLogger()
logger.setLevel("INFO")

# Initialize the Kinesis client
kinesis_client = boto3.client('kinesis')

# Initialize the DynamoDB resource
dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table(os.environ['TABLE_NAME'])

def lambda_handler(event, context):    
    # Process each record in the batch
    for record in event['Records']:
        # Kinesis data is base64 encoded
        payload = base64.b64decode(record['kinesis']['data']).decode('utf-8')
        
        # Decode the payload (assuming it's JSON)
        try:
            data = json.loads(payload)
            # Process the data here
            process_data(data)
        except json.JSONDecodeError:
            logger.error(f"Failed to decode JSON: {payload}")
    
    return {
        'statusCode': 200,
        'body': json.dumps('Processing complete')
    }

def process_data(data):
    # Implement your data processing logic here
    table.put_item(Item=data)
    logger.info(f"Processing data: {data}")
    # Add your custom logic to handle the data