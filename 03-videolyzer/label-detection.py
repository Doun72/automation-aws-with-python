# coding: utf-8
import boto3
session = boto3.Session(profile_name='nagradev-sts')
s3 = session.resource('s3')
bucket = s3.create_bucket(Bucket='rekognition-video-console-demo-iad-nagradev-hpog6p07mmj9k8n47t')
bucket = s3.create_bucket(Bucket='rekognition-video-console-demo-iad-nagradev-hpog6p07mmj9k8n47t',CrateBucketConfiguration={'LocationConstraint':session.region_name})
bucket = s3.create_bucket(Bucket='rekognition-video-console-demo-iad-nagradev-hpog6p07mmj9k8n47t',CreateBucketConfiguration={'LocationConstraint':session.region_name})
bucket = s3.create_bucket(Bucket='rekognition-video-console-demo-iad-nagradev-hpog6p07mmj9k8n47t',CreateBucketConfiguration={'LocationConstraint':session.region_name})
bucket = s3.create_bucket(Bucket='rekognition-video-console-demo-iad-nagradev',CreateBucketConfiguration={'LocationConstraint':session.region_name})
from pathlib import Path
pathname = '/Users/didierhunacek/Downloads/Man Texting On The Street.mp4'
path = Path(pathname).expanduser().resolve()
path
bucket.upload_file(str(path),str(path.name))
rekogniton_client = session.client('rekognition')
response = rekognition_client.start_lable_detection(Video={'S3Object':{'Bucket': bucket.name,'Name':path.name}}) 
response = rekogniton_client.start_lable_detection(Video={'S3Object':{'Bucket': bucket.name,'Name':path.name}}) 
response = rekogniton_client.start_label_detection(Video={'S3Object':{'Bucket': bucket.name,'Name':path.name}}) 
response
job_id= response['JobID']
job_id= response['JobId']
result = rekognition_client.get_label_detection(JobId=job_id)
result = rekogniton_client.get_label_detection(JobId=job_id)
result
