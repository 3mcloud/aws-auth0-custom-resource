"""Config util"""
import os

import boto3

from .constants import PROVIDER_STR, PROVIDER

cfn = boto3.client('cloudformation')
MANAGEMENT_PREFIX = 'arn:aws:secretsmanager:us-east-1:184518171237:secret:'

def get_provider(tenant):
    """Get the provider with authentication"""
    tenant_name = tenant.split('.')[0]
    environ = os.environ.get('ENVIRON')
    management_secret = f'{MANAGEMENT_PREFIX}{environ}/{PROVIDER_STR}/tenant/{tenant_name}'
    return PROVIDER(management_secret, tenant)


def set_tags(helper, event=None):
    """
    Get tags from the cloudformation stack and make them available for other operations
    :param helper: object used to get stack id
    """
    if not event:
        event = {}
    additional = event.get('ResourceProperties', {}).get('AllowAdGroups')
    additional = {'AllowAdGroups': additional} if additional else {}

    res = cfn.describe_stacks(StackName=helper.StackId)

    new_tags = {}
    raw_tags = res['Stacks'][0]['Tags']
    for tag in raw_tags:
        new_tags[tag['Key']] = tag['Value']
    new_tags.update(additional)
    helper.Data.update({'tags': new_tags})
    helper.Data.update({'stack_tags': raw_tags})
