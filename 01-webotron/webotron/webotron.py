import boto3
import click
import botocore.exceptions from ClientError

session = boto3.Session(profile_name='nagradev-sts')
s3 = session.resource('s3')

@click.group()
def cli():
    "Webotron deploys web site to AWS"
    pass

@cli.command('list_buckets')
def list_buckets ():
    "List the buckets"
    for bucket in s3.buckets.all():
        print (bucket.name)

@cli.command('list_buckets_object')
@click.argument('bucket')
def list_buckets_object(bucket):
    "List objects in a S3 bucket"
    for obj in s3.Bucket(bucket).objects.all():
        print(obj)

@cli.command('create_and_configure_bucket')
@click.argument('bucket')
def create_and_configure_bucket(bucket):
    "Create and configure S3 bucket"
    s3_bucket = None
    try:
        s3_bucket = s3.create_bucket(Bucket=bucket,
            CreateBucketConfiguration={'LocationConstraint': session.region_name})
    except ClientError as e:
        if e.response['Error']['Code'] == 'BucketAlreadyOwnedByYou':
            s3_bucket = s3.Bucket(bucket)
        else:
            raise e

    policy = """
    {
    "Version":"2012-10-17",
    "Statement":[
        {
            "Sid":"PublicRead",
            "Effect":"Allow",
            "Principal": "*",
            "Action":["s3:GetObject"],
            "Resource":["arn:aws:s3:::%s/*"]
        }
    ]
    }
    """ % bucket.name
    #remove any space
    policy = policy.strip()
    pol = s3_bucket.Policy()
    pol.put(Policy=policy)
    ws = s3_bucket.Website()
    ws.put(WebSiteConfiguration={
        "ErrorDocument" : {'key','error.html'},
        "IndexDocument" : {'suffix','index.html'},

    })
    return


if __name__ == '__main__':
    cli()
