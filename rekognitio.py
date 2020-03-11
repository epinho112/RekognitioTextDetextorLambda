import boto3
import json
import os
from botocore.vendored import requests

client=boto3.client('rekognition')
s3_client = boto3.client('s3')

def handler(event, context):
    record = event['Records']
    bucket = record[0]['s3']['bucket']['name']
    photo = record[0]['s3']['object']['key']
    text1 = "n"

    response=client.detect_text(Image={'S3Object':{'Bucket':bucket,'Name':photo}})
    textDetections=response['TextDetections']

    download_path = '/tmp/file01.txt'
    f = open(download_path, 'wt')
    
    for text in textDetections:
        text1 += text['DetectedText'] + " "
        
    f.write(text1)
    f.close()

    s3_client.upload_file(download_path, 'ep-rekognition-text', 'Upload.txt')