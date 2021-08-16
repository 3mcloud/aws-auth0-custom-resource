"""Secret is a utility for getting a secrets manager secret value"""
import base64
import logging
from botocore.exceptions import ClientError

logger = logging.getLogger('aws-auth0-cr')

def get_muxed_secret(client, secret_id, stage='AWSCURRENT'):
    """
    Get a secret from secrets manager with the value
    decoded to SecretValue
    """
    try:
        get_secret_value_response = client.get_secret_value(
            SecretId=secret_id,
            VersionStage=stage
        )
        # Decrypts secret using the associated KMS CMK.
        # Depending on whether the secret is a string or binary,
        # one of these fields will be populated.
        if 'SecretString' in get_secret_value_response:
            secret = get_secret_value_response['SecretString']
        else:
            secret = base64.b64decode(
                get_secret_value_response['SecretBinary'])

        # normlized secret
        get_secret_value_response['SecretValue'] = secret
        return get_secret_value_response
    except ClientError as err:
        if err.response['Error']['Code'] == 'DecryptionFailureException':
            logger.error('Unable to decrypt secret: %s', err.response)
            raise err
        if err.response['Error']['Code'] == 'InternalServiceErrorException':
            logger.error(
                'Internal server error in secrets manager %s', err.response)
            raise err
        if err.response['Error']['Code'] == 'InvalidParameterException':
            logger.error('Invalid parameter error: %s', err.response)
            raise err
        if err.response['Error']['Code'] == 'InvalidRequestException':
            logger.error(
                'Invalid request for state of secret error: %s', err.response)
            raise err
        if err.response['Error']['Code'] == 'ResourceNotFoundException':
            logger.error('Resource not found error %s', err.response)
            raise err
        logger.error('Error with secretsmanager API call: %s', err.response)
        raise err

def get_secret(client, secret_id, stage='AWSCURRENT'):
    """Get a secret value from secrets manager"""
    resource = get_muxed_secret(client, secret_id, stage)
    return resource['SecretValue']
