# -*- coding: utf-8 -*-

"""Class for S3 bucket."""
import mimetypes
from pathlib import Path
from botocore.exceptions import ClientError

class BucketManager():
    """docstring for BucketManager."""

    def __init__(self,session):
        """Init function."""
        self.session = session
        self.s3 = session.resource('s3')

    def all_buckets(self):
        """Get the bucket list."""
        return self.s3.buckets.all()

    def all_objects(self,bucket_name):
        """Get the list of object inside the bucket."""
        return self.s3.Bucket(bucket_name).objects.all()

    def init_bucket(self,bucket_name):
        """Initialize the S3 bucket."""
        s3_bucket = None
        try:
            s3_bucket = self.s3.create_bucket(Bucket=bucket_name,
                CreateBucketConfiguration={'LocationConstraint': self.session.region_name})
        except ClientError as e:
            if e.response['Error']['Code'] == 'BucketAlreadyOwnedByYou':
                s3_bucket = self.s3.Bucket(bucket_name)
            else:
                raise e
        return s3_bucket

    def set_bucket_policy(self,bucket):
        """Set the bucket policy."""
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
        pol = bucket.Policy()
        pol.put(Policy=policy)

    def configure_Website(self, bucket):
        """Configure the web site."""
        ws = bucket.Website()
        ws.put(WebSiteConfiguration={
            "ErrorDocument" : {'key','error.html'},
            "IndexDocument" : {'suffix','index.html'},
        })

    def upload_file(bucket,path,key):
        """Upload file into a S3 bucket."""
        content_type = mimetypes.guess_type(key)[0] or 'text/html'
        return bucket.upload_file(path,key,ExtraArgs={'Content',content_type})

    def sync(self,pathname,bucket_name):
        """Sync tree directory to S3 bucket."""
        s3_bucket = s3.Bucket(bucket_name)
        root = Path(pathname).expanduser().resolve()

        def handle_directory(target):
            for p in target.iterdir():
                if p.is_dir():handle_directory(p)
                if p.is_file():self.upload_file(s3_bucket, str(p), str(p.relative_to(root)))

        handle_directory(root)
