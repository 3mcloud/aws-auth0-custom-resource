'''
API CRUD handler
'''
import logging

from auth0.v3.exceptions import Auth0Error
import boto3
from crhelper import CfnResource

from .utils import config
from .lambdatype import LambdaDict, LambdaContext
from .validation.api import auth0Validator

logger = logging.getLogger()  # pylint: disable=invalid-name
logger.setLevel(logging.INFO)

secrets_client = boto3.client('secretsmanager')  # pylint: disable=invalid-name


def create(event: LambdaDict, _: LambdaContext, helper: CfnResource) -> str:
    '''
    Create an api with the given identifier
    '''
    props = event['ResourceProperties']
    validated = auth0Validator.validated(props)
    if not validated:
        raise Exception(auth0Validator.errors)
    provider = config.get_provider(props.get('Tenant'))
    api_id = provider.create_api(**validated)
    helper.Data['ApiId'] = api_id
    helper.Data['Audience'] = props.get('Audience')
    return api_id


def update(event: LambdaDict, _: LambdaContext, helper: CfnResource) -> str:
    '''
    Update an API
    '''
    props = event['ResourceProperties']
    validated = auth0Validator.validated(props)
    if not validated:
        raise Exception(auth0Validator.errors)
    provider = config.get_provider(props.get('Tenant'))

    api_id = event['PhysicalResourceId']
    # Handle audience change with creating a new resource
    if props['Audience'] != event['OldResourceProperties']['Audience']:
        logger.info('New audience, deleting old resource and creating a new one.')
        api_id = provider.create_api(**validated)
        delete_handle_err(provider, event['PhysicalResourceId'])
    else:
        del validated['identifier']
        provider.update_api(event['PhysicalResourceId'], **validated)
    helper.Data['ApiId'] = api_id
    helper.Data['Audience'] = props.get('Audience')
    return event['PhysicalResourceId']


def delete(event: LambdaDict, context: LambdaContext, helper: CfnResource):  # pylint: disable=unused-argument
    '''Delete an api'''
    props = event['ResourceProperties']
    provider = config.get_provider(props['Tenant'])
    delete_handle_err(provider, event['PhysicalResourceId'])


def delete_handle_err(provider, api_id):
    '''Delete an API and handle the errors'''
    try:
        # deleting an api id that doesn't exist does not raise exception
        # see e2e/test_errors.py
        provider.delete_api(api_id)
    except Auth0Error as err:
        logger.error(err)
        if 'Path validation error' in err.message:
            logger.error('physical resource id is not a \
            valid id. Assuming this failed to create.')
            return
        raise
