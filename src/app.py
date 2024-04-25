# Copyright Amazon.com, Inc. or its affiliates. All Rights Reserved.
# SPDX-License-Identifier: MIT-0

import boto3
import os
import json
import logging

logger = logging.getLogger()
logger.setLevel(logging.INFO)

dynamodb_resource = boto3.resource('dynamodb', 
                          region_name='us-east-1' # use your region_name
                          )

def lambda_handler(event, context):
  table = os.environ.get('DDB_TABLE')
  logging.info(f"## Loaded table name from environemt variable DDB_TABLE: {table}")
  dynamodbtable = dynamodb_resource.Table(table)
  item = dynamodbtable.get_item(TableName=table, Key={'id':1})
  currentnumber = item["Item"]["visitcount"]
  currentnumber += 1
  update_item_exiting_attribute(currentnumber)
  message = "Successfully inserted data!"
  return {
      "statusCode": 200,
      "headers": {
          'Access-Control-Allow-Origin': '*'
          
      },
      "body": json.dumps({"count": str(currentnumber)})
  }

      
def update_item_exiting_attribute(currentnumber):
    table = os.environ.get('DDB_TABLE')
    dynamodbtable = dynamodb_resource.Table(table)
    response = dynamodbtable.update_item(
        Key={"id": 1},
        UpdateExpression="set #visitcount = :n",
        ExpressionAttributeNames={
            "#visitcount": "visitcount",
        },
        ExpressionAttributeValues={
            ":n": str(currentnumber),
        },
        ReturnValues="UPDATED_NEW"
    )