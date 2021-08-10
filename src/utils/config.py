'''Config util'''
import logging
import os

import boto3

from src.auth_providers import PROVIDERS

cfn = boto3.client('cloudformation')  # pylint: disable=invalid-name
MANAGEMENT_PREFIX = 'arn:aws:secretsmanager:us-east-1:184518171237:secret:'


def set_logging_level(logger, level_str):
    '''Set up logging based on the LOGGING_LEVEL environment variable'''
    if level_str == 'CRITICAL':
        logger.setLevel(logging.CRITICAL)
    if level_str == 'ERROR':
        logger.setLevel(logging.ERROR)
    if level_str == 'WARNING':
        logger.setLevel(logging.WARNING)
    if level_str == 'INFO':
        logger.setLevel(logging.INFO)
    if level_str == 'DEBUG':
        logger.setLevel(logging.DEBUG)


def get_provider(tenant):
    '''Get the provider with authentication'''
    provider = os.environ.get('AUTH_PROVIDER')
    tenant_name = tenant.split('.')[0]
    environ = os.environ.get('ENVIRON')
    management_secret = f'{MANAGEMENT_PREFIX}{environ}/{provider}/tenant/{tenant_name}'
    return PROVIDERS[provider](management_secret, tenant)


def set_tags(helper, event=None):
    '''
    Get tags from the cloudformation stack and make them available for other operations
    :param helper: object used to get stack id
    '''
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
