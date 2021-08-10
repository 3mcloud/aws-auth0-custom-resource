'''Rotation is used to rotate auth resource secrets'''

import logging
import json
import os
import boto3
import botocore
from auth0.v3.exceptions import Auth0Error
from .utils import config, secret

logger = logging.getLogger()  # pylint: disable=invalid-name
logger.setLevel(logging.INFO)  # set INFO level by default

# Setup the client
client = boto3.client('secretsmanager')  # pylint: disable=invalid-name


def lambda_handler(event, context):
    '''Secrets Manager Rotation Handler

    Args:
      event (dict): Lambda dictionary of event parameters. These keys must include the following:
        - SecretId: The secret ARN or identifier
        - ClientRequestToken: The ClientRequestToken of the secret version
        - Step: The rotation step (one of createSecret, setSecret, testSecret, or finishSecret)
      context (LambdaContext): The Lambda runtime information
    Raises:
      ResourceNotFoundException: If the secret with the specified arn and stage does not exist
      ValueError: If the secret is not properly configured for rotation
      KeyError: If the event parameters do not contain the expected keys
    '''
    # Set up logging based on the LOGGING_LEVEL environment variable
    level_str = os.getenv('LOGGING_LEVEL', 'INFO')
    config.set_logging_level(logger, level_str)
    logger.debug(event)
    logger.debug(context)

    arn = event['SecretId']
    token = event['ClientRequestToken']
    step = event['Step']
    metadata = client.describe_secret(SecretId=arn)

    logger.info('rotating %s at step %s', arn, step)

    # Make sure the version is staged correctly
    if not metadata['RotationEnabled']:
        logger.error("Secret %s is not enabled for rotation", arn)
        raise ValueError("Secret %s is not enabled for rotation" % arn)
    versions = metadata['VersionIdsToStages']
    if token not in versions:
        logger.error(
            "Secret version %s has no stage for rotation of secret %s.", token, arn)
        raise ValueError(
            "Secret version %s has no stage for rotation of secret %s." % (token, arn))
    if "AWSCURRENT" in versions[token]:
        logger.info(
            "Secret version %s already set as AWSCURRENT for secret %s.", token, arn)
        return
    if "AWSPENDING" not in versions[token]:
        logger.error(
            "Secret version %s not set as AWSPENDING for rotation of secret %s.", token, arn)
        raise ValueError(
            "Secret version %s not set as AWSPENDING for rotation of secret %s." % (token, arn))

    # Get the tenant from the secret string
    secret_contents = json.loads(secret.get_secret(client, arn, logger))
    tenant = secret_contents['tenant']

    logger.info('tenant %s', tenant)

    provider = config.get_provider(tenant)

    if step == "createSecret":
        create_secret(client, provider, arn, token)

    elif step == "setSecret":
        set_secret()

    elif step == "testSecret":
        test_secret(client, provider, arn)

    elif step == "finishSecret":
        finish_secret(client, arn, token)

    else:
        raise ValueError("Invalid step parameter")


def create_secret(secrets_client, provider, secret_id, token):
    '''Default secret method

    If the secret does not yet exist, it throws an error. Since creating auth secrets
    and rotating them is atomic, this also sets the secret.
    '''
    logger.info('create secret %s', secret_id)
    # Get the secret contents
    secret_val = json.loads(secret.get_secret(
        secrets_client, secret_id, logger))
    # Rotate the secret
    new_client_secret = provider.rotate_client_secret(
        client_id=secret_val['client_id'])
    new_secret_val = {**secret_val, 'client_secret': new_client_secret}
    try:
        secrets_client.put_secret_value(
            SecretId=secret_id,
            ClientRequestToken=token,
            SecretString=json.dumps(new_secret_val),
            VersionStages=['AWSPENDING']
        )
    except botocore.exceptions.ClientError as error:
        if error.response['Error']['Code'] != 'ResourceExistsException':
            raise error
        rollback_secret(provider, secret_val)
    logger.info('create secret finished')

def rollback_secret(provider, secret_val):
    '''rollback a secret in auth0 that failed to update in secrets manager'''
    logger.info('secret failed to update in secrets manager. rolling back')
    provider.update_application(
        client_id=secret_val['client_id'],
        client_secret=secret_val['client_secret'],
    )

def set_secret():
    '''Default set method, does nothing.

    Since creating auth secret and rotating them is atomic, this method does nothing.
    '''


def test_secret(secrets_client, provider, arn):
    '''Test the client id/client secret pair are the same
    in secrets manager as they are in the provider

    Args:
      client (client): The secrets manager service client
      arn (string): The arn of the secrets manager secret
    '''
    logger.info('test secret %s', arn)
    new_secret = json.loads(secret.get_secret(
        client=secrets_client, secret_id=arn, logger=logger, stage="AWSPENDING"))

    application = provider.get_application(
        client_id=new_secret['client_id'],
        fields=['client_secret']
    )
    if application['client_secret'] != new_secret['client_secret']:
        logger.error('test_secret: secrets to not match')
        raise ValueError('test_secret: secrets to not match')

    return True


def finish_secret(secrets_client, arn, token):
    '''Finish the secret by marking it as AWSCURRENT

    This method finalizes the rotation process by marking the secret version passed
    in as the AWSCURRENT secret.
    Args:
      client (client): The secrets manager service client
      arn (string): The secret ARN or other identifier
      token (string): The ClientRequestToken associated with the secret version
    Raises:
      ResourceNotFoundException: If the secret with the specified arn does not exist
    '''
    logger.info('finish secret')
    # First describe the secret to get the current version
    metadata = secrets_client.describe_secret(SecretId=arn)
    current_version = None
    for version in metadata["VersionIdsToStages"]:
        if "AWSCURRENT" in metadata["VersionIdsToStages"][version]:
            if version == token:
                # The correct version is already marked as current, return
                logger.info(
                    "finishSecret: Version %s already marked as AWSCURRENT for %s", version, arn)
                return
            current_version = version
            break

    # Finalize by staging the secret version current
    secrets_client.update_secret_version_stage(
        SecretId=arn,
        VersionStage="AWSCURRENT",
        MoveToVersionId=token,
        RemoveFromVersionId=current_version)
    logger.info(
        "finishSecret: Successfully set AWSCURRENT stage to version %s for secret %s.", token, arn)
