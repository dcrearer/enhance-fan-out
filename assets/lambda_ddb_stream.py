import json
import os
import base64
import boto3
import logging


logger = logging.getLogger()
logger.setLevel("INFO")

def lambda_handler(event, context):
    for record in event["Records"]:
        event_name = record["eventName"]
        if event_name == "INSERT":
            new_image = record["dynamodb"]["NewImage"]
            logger.info(f"Processing data: {new_image}")
    
    return {
        'statusCode': 200,
        'body': json.dumps('New Item Added')
    }