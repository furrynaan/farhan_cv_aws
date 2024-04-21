# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: MIT-0

import boto3
import os
import json
import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)

dynamodb_client = boto3.client('dynamodb')

def lambda_handler(event, context):
  table = os.environ.get('DDB_TABLE')
  logging.info(f"## Loaded table name from environemt variable DDB_TABLE: {table}")
  if event["body"]:
      item = json.loads(event["body"])
      logging.info(f"## Received payload: {item}")
      currentnumber = item["currentnumber"]
      currentnumber += currentnumber
      update_item_exiting_attribute(currentnumber)
      message = "Successfully inserted data!"
      return {
          "statusCode": 200,
          "headers": {
              "Content-Type": "application/json"
          },
          "body": json.dumps({"message": message})
      }
  else:
      logging.info("## Received request without a payload")
      dynamodb_client.put_item(TableName=table,Item={"year": {'N':'2012'}, "title": {'S':'The Amazing Spider-Man 2'}})
      message = "Successfully inserted data!"
      return {
          "statusCode": 200,
          "headers": {
              "Content-Type": "application/json"
          },
          "body": json.dumps({"message": message})
      }
      
def update_item_exiting_attribute(currentnumber):
    table = os.environ.get('DDB_TABLE')
    response = dynamodb_client.update_item(
        Key={"id": {"N" : "1"}},
        UpdateExpression="set #visitcount = :n",
        ExpressionAttributeNames={
            "#visitcount": "visitcount",
        },
        ExpressionAttributeValues={
            ":n": {"N" : currentnumber,
        }},
        ReturnValues="UPDATED_NEW",
        TableName=table
    )