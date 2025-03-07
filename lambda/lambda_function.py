import boto3
import pandas as pd
import os
from datetime import datetime

s3 = boto3.client('s3', endpoint_url='http://localstack:4566')
dynamodb = boto3.resource('dynamodb', endpoint_url='http://localstack:4566')
table = dynamodb.Table('Metadata')

def lambda_handler(event, context):
    try:
        # Extract bucket and file name from S3 event
        bucket = event['Records'][0]['s3']['bucket']['name']
        key = event['Records'][0]['s3']['object']['key']
        
        # Download CSV from S3
        local_file = f'/tmp/{key}'
        s3.download_file(bucket, key, local_file)
        
        # Extract metadata using pandas
        df = pd.read_csv(local_file)
        metadata = {
            'filename': key,
            'upload_timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'file_size_bytes': os.path.getsize(local_file),
            'row_count': len(df),
            'column_count': len(df.columns),
            'column_names': list(df.columns)
        }
        
        # Store metadata in DynamoDB
        table.put_item(Item=metadata)
        print(f"Processed {key} successfully!")
        return {'statusCode': 200}
    
    except Exception as e:
        print(f"Error: {str(e)}")
        return {'statusCode': 500}