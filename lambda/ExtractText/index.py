import json
import urllib.parse
import boto3
import os

print('Loading function')

def lambda_handler(event, context):
    
    file_obj = event['Records'][0]
    key = urllib.parse.unquote_plus(event['Records'][0]['s3']['object']['key'])
    filename = key.split('/')[-1]
    print(key, 'key')
    print(filename, 'filename')
    bucket = event['Records'][0]['s3']['bucket']['name']
    print(bucket)
    
    try:
        textract = boto3.client('textract')
        response = textract.start_document_text_detection(
        DocumentLocation={
            'S3Object': {
                'Bucket': bucket,
                'Name': key,
            }
        },
        JobTag=filename + '_Job',
        NotificationChannel={
            'RoleArn': 'arn:aws:iam::295572101288:role/SNSFullAccess',
            'SNSTopicArn': 'arn:aws:sns:us-east-1:295572101288:AWSTextract'
        })
        job_id = response['JobId']
        print(job_id)
        print("triggered")
        return 'Triggered PDF Processing for ' + filename
    except Exception as e:
        print(e)
        print('Error getting object {} from bucket {}. Make sure they exist and your bucket is in the same region as this function.'.format(key, bucket))
        raise e