# -*- coding: utf-8 -*-

"""Class for certificate."""
from pprint import pprint

class CertificateManager():
    """docstring for BucketManager."""

    def __init__(self,session):
        """Init function."""
        self.session = session
        self.client = session.client('acm', region_name='us-east-1')

    def certmatches(self,cert_arn,domain_name):
        """Certificate matches with the domain_name."""
        cert_details = self.client.describe_certificate(CertificateArn=cert_arn)
        alt_names = cert_details['Certificate']['SubjectAlternativeNames']
        for name in alt_names:
            if name == domain_name:
                return True
            if name[0] == '*' and domain_name.endswith(name[1:]):
                return True
        return False

    def find_matching_cert(self, domain_name):
        """Find certificate equals to the domain name."""
        paginator = self.client.get_paginator('list_certificates')
        for page in paginator.paginate(CertificateStatuses=['ISSUED']):
            for cert in page['CertificateSummaryList']:
                if self.certmatches(cert['CertificateArn'],domain_name):
                    return cert
        return None
