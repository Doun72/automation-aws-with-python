#!usr/bin/python
# -*- coding: utf-8 -*-

"""This script is."""

import boto3
import click

from bucket import BucketManager
from certificate import CertificateManager

session = None
bucket_manager = None
cert_manager = None

@click.group()
@click.option('--profile', help='Give the profile to use',default=None)
def cli(profile):
    """Webotron deploys web site to AWS."""
    global session, bucket_manager, cert_manager
    session_cfg = {}
    if profile:
        session_cfg['profile_name'] = profile
    session = boto3.Session(**session_cfg)
    bucket_manager = BucketManager(session)
    cert_manager = CertificateManager(session)

@cli.command('list_buckets')
def list_buckets ():
    """List the buckets."""
    for bucket in bucket_manager.all_buckets():
        print (bucket.name)

@cli.command('list_buckets_object')
@click.argument('bucket')
def list_buckets_object(bucket):
    """List objects in a S3 bucket."""
    for obj in bucket_manager.all_objects(bucket):
        print(obj)

@cli.command('create_and_configure_bucket')
@click.argument('bucket')
def create_and_configure_bucket(bucket):
    """Create and configure S3 bucket."""
    s3_bucket = bucket_manager.init_bucket(bucket)
    bucket_manager.set_bucket_policy(s3_bucket)
    bucket_manager.configure_Website(s3_bucket)
    return


@cli.command('sync')
@click.argument('pathname', type=click.Path(exists=True))
@click.argument('bucket')
def sync(pathname,bucket):
    """Sync content of a pathname to bucket."""
    bucket_manager.sync(pathname,bucket)

@cli.command('find_cert')
@click.argument('domain_name')
def find_cert(domain_name):
    """Find the certificate for the domain name."""
    print(cert_manager.find_matching_cert(domain_name))

if __name__ == '__main__':
    cli()
