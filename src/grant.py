'''
Grant CRUD handler
'''
import logging

import boto3
from crhelper import CfnResource
from auth0.v3.exceptions import Auth0Error

from .utils import config
from .lambdatype import LambdaDict, LambdaContext
from .validation.grant import auth0Validator

logger = logging.getLogger()  # pylint: disable=invalid-name
logger.setLevel(logging.INFO)

secrets_client = boto3.client('secretsmanager')  # pylint: disable=invalid-name


def create(event: LambdaDict, _: LambdaContext, helper: CfnResource) -> str:
    '''
    Create a client grant with the given name and audience
    '''
    props = event['ResourceProperties']
    validated = auth0Validator.validated(props)
    if not validated:
        raise Exception(auth0Validator.errors)
    provider = config.get_provider(props.get('Tenant'))
    grant_id = provider.create_grant(**validated)
    helper.Data['GrantId'] = grant_id
    return grant_id

def update(event, context, helper):  # pylint: disable=unused-argument
    '''
    update a client grant

    Updates don't really happen. The reason this might change is that the
    user might update a logical ID or reference for the grant. When this
    happens we really want to re-run create because we assume the original
    API or Application were removed.
    '''
    try:
        grant_id = create(event, context, helper)
    except Auth0Error as err:
        logger.error(err)
        if err.status_code != 409:
            raise err
        grant_id = event['PhysicalResourceId']

    helper.Data['GrantId'] = grant_id
    return grant_id

def delete(event, context, helper):  # pylint: disable=unused-argument
    '''delete a client grant'''
    logger.info(event)
    props = event['ResourceProperties']
    provider = config.get_provider(props.get('Tenant'))
    try:
        # deleting a grant id that doesn't exist does not raise exception
        # see e2e/test_errors.py
        provider.delete_grant(event['PhysicalResourceId'])
    except Auth0Error as err:
        logger.error(err)
        if 'Path validation error' in err.message:
            logger.error('physical resource id is not a \
            valid grant. Assuming this failed to create.')
            return
        raise
