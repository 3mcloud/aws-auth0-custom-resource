"""
Application CRUD handler
"""
import json
import logging
import os

import boto3
import botocore
from botocore.exceptions import ClientError
from crhelper import CfnResource
import stringcase
from auth0.v3.exceptions import Auth0Error

from .lambdatype import LambdaContext, LambdaDict
from .utils import config, secret
from .validation.application import (
    auth0Validator,
    tagsValidator,
)

logger = logging.getLogger('aws-auth0-cr')

secrets_client = boto3.client('secretsmanager')
ssm = boto3.client('ssm')


def create(event: LambdaDict, _: LambdaContext, helper: CfnResource) -> str:  # pylint: disable=too-many-locals
    """
    Create an application with the given name and kind
    """
    props = event['ResourceProperties']
    validated = auth0Validator.validated(event['ResourceProperties'])
    if not validated:
        raise Exception(auth0Validator.errors)

    tags = tagsValidator.validated(helper.Data.get('tags', {}))
    validated['client_metadata'].update(tags)

    provider = config.get_provider(props['Tenant'])
    client_id, client_secret = provider.create_application(
        **validated,
    )
    helper.Data['ClientId'] = client_id

    try:
        env = os.getenv('ENVIRON')
        # Enable the application for all the connections
        for conn_id in props.get('Connections', []):
            provider.add_to_connection(conn_id, client_id)

        # Only do secretsmanager resource for m2m apps, use ssm for the rest
        if props.get('Type') != 'm2m':
            helper.Data['ClientId'] = client_id
            param_name = f'/{env}/auth0/{client_id}/client_secret'
            ssm.put_parameter(
                Name=param_name,
                Value=client_secret,
                Type='SecureString'
            )
            helper.Data['ClientSecret'] = param_name
            return client_id

        # Add secrets manager secret for m2m apps
        kms_key = os.environ.get('KMS_KEY_ID')
        rotation = os.getenv('ROTATION')

        # Create the secrets manager secret with the provider information
        prop_name = stringcase.lowercase(stringcase.alphanumcase(props['Name']))
        name = f"/{env}/auth0/{prop_name}"
        app_secret = secrets_client.create_secret(
            Name=name,
            KmsKeyId=kms_key,
            SecretString=json.dumps({
                'client_id': client_id,
                'client_secret': client_secret,
                'tenant': props['Tenant'],
            }),
            Tags=helper.Data.get('stack_tags'),
        )
        secrets_client.rotate_secret(
            SecretId=name,
            RotationLambdaARN=rotation,
            RotationRules={
                'AutomaticallyAfterDays': 30
            }
        )
        helper.Data['Arn'] = app_secret['ARN']
        helper.Data['Name'] = name
        helper.Data['ClientId'] = client_id
        return name
    except Exception as err:  # pylint: disable=broad-except
        # delete client_id from auth0 since this failed
        provider.delete_application(client_id)
        raise err


def manage_connection(connections, app_id, method):
    """Manage adding or removing an application from a connection"""
    failed = []
    for conn_id in connections:
        try:
            method(conn_id, app_id)
        except Exception as err:  # pylint: disable=broad-except
            print(err)
            failed.append(conn_id)
    return failed


def update_connections(old, current, provider, app_id):
    """
    Update the connections for the application

    Add any new connections and remove any connections that are no longer specified
    """

    add_connections = list(set(current) - set(old))
    remove_connections = list(set(old) - set(current))

    failed_add = []
    failed_delete = []

    failed_add = manage_connection(add_connections, app_id, provider.add_to_connection)
    failed_delete = manage_connection(remove_connections, app_id, provider.remove_from_connection)

    if failed_add or failed_delete:
        raise Exception(
            'failed to add: %s, failed to delete: %s' % (failed_add, failed_delete))


def update(event: LambdaDict, context: LambdaContext, helper: CfnResource):  # pylint: disable=unused-argument
    """Update an application"""
    props = event['ResourceProperties']
    validated = auth0Validator.validated(props)
    if not validated:
        raise Exception(auth0Validator.errors)
    tags = tagsValidator.validated(helper.Data.get('tags', {}))
    if 'AllowAdGroups' in event['OldResourceProperties'] and 'AllowAdGroups' not in props:
        validated['client_metadata'].update({'AllowAdGroups': None})
    validated['client_metadata'].update(tags)
    provider = config.get_provider(props['Tenant'])

    if props.get('Type') != event['OldResourceProperties'].get('Type', None):
        raise Exception(
            'Changing Type is not supported. Create a new resource and remove the old one instead')
    if props.get('Type') != 'm2m':
        app_id = event['PhysicalResourceId']
    else:
        # Get the secret for the client_id
        resource = secret.get_muxed_secret(
            secrets_client,
            event['PhysicalResourceId'],
            logger)
        app_secret = json.loads(resource['SecretValue'])
        app_id = app_secret['client_id']

    # Update the connections
    current = props.get('Connections', [])
    old = event['OldResourceProperties'].get('Connections', [])

    update_connections(old, current, provider, app_id)

    # Update the app in Auth0
    client_id = provider.update_application(app_id, **validated)
    helper.Data['ClientId'] = client_id
    if props.get('Type') == 'm2m':
        helper.Data['Arn'] = resource['ARN']
        helper.Data['Name'] = event['PhysicalResourceId']

    return event['PhysicalResourceId']


def delete(event: LambdaDict, context: LambdaContext, helper: CfnResource):  # pylint: disable=unused-argument
    """Delete an application"""
    props = event['ResourceProperties']
    provider = config.get_provider(props['Tenant'])
    ok_exceptions = (
        'AccessDeniedException',
        'ResourceNotFoundException'
    )

    if props.get('Type') == 'm2m' or event['PhysicalResourceId'].startswith('/'):
        try:
            # Get the secret for the client_id
            app_secret = json.loads(secret.get_secret(
                secrets_client,
                event['PhysicalResourceId'],
            ))
            app_id = app_secret['client_id']
        except botocore.exceptions.ClientError as err:
            # Client errors related to the secret not existing.
            # Assume the secret is gone and call this a success
            logger.error(err, exc_info=True)
            if err.response['Error']['Code'] in ok_exceptions:
                logger.error('Unable to load secret for delete. Assuming it is gone')
                return
            raise
    else:
        app_id = event['PhysicalResourceId']

    # Delete the app in Auth0
    try:
        # deleting an application id that doesn't exist does not raise exception
        # see e2e/test_errors.py
        provider.delete_application(app_id)
    except Auth0Error as err:
        logger.error(err)
        if 'Path validation error' in err.message:
            logger.error('physical resource id is not a \
            valid id. Assuming this failed to create.')
            return
        raise

    # Delete the secret in secretsmanager
    # Don't catch exceptions. This secret must exist since we
    # got it from secrets manager in order to make it here
    if props.get('Type') == 'm2m':
        secrets_client.delete_secret(
            SecretId=event['PhysicalResourceId'],
            ForceDeleteWithoutRecovery=True
        )
    # Try deleting the client secret
    try:
        env = os.getenv('ENVIRON')
        ssm.delete_parameter(
            Name=f'/{env}/auth0/{app_id}/client_secret'
        )
    except ClientError:
        logger.info("Old version, client secret ssm param not found")
