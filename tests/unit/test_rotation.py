""" Tests for the rotation lambda. """

import json
from unittest.mock import patch, MagicMock as Mock, ANY
import pytest
import botocore
from src import rotation

ARN = 'arn:aws:secretsmanager:::secrets/fakesecret'
URL = 'unit-test.url.com'


@patch('src.rotation.client')
@patch('src.rotation.config')
def test_handler_no_rotation(mock_config, mock_secrets):
    """Test the handler when no rotation needs to occur"""
    mock_secrets.describe_secret.return_value = {'RotationEnabled': False}
    mock_secrets.get_secret_value.return_value = {'SecretString': json.dumps(
        {'tenant': 'mmm-dev'}
    )}
    token = 'token'
    provider = 'auth0'
    mock_config.get_provider.return_value = provider
    with pytest.raises(ValueError):
        rotation.lambda_handler(
            {
                'SecretId': ARN,
                'ClientRequestToken': token,
                'Step': 'createSecret'
            },
            {}
        )

@patch('src.rotation.rollback_secret')
@patch('src.rotation.client')
@patch('src.rotation.config')
def test_handler_rollback(mock_config, mock_secrets, rollback_secret):
    """Test the handler when secret is rotated but secrets manager can't update"""
    mock_secrets.describe_secret.return_value = {
        'RotationEnabled': True,
        'VersionIdsToStages': {
            'token': ['AWSPENDING']
        }
    }
    mock_secrets.get_secret_value.return_value = {'SecretString': json.dumps(
        {'tenant': 'mmm-dev', 'client_secret': 'foo', 'client_id': 'bar'}
    )}
    token = 'token'
    mock_config.get_provider.return_value.rotate_client_secret.return_value = 'baz'
    mock_secrets.put_secret_value.side_effect = botocore.exceptions.ClientError(
        {'Error': {'Code':'ResourceExistsException'},},
        'ResourceExistsException'
    )
    rotation.lambda_handler(
        {
            'SecretId': ARN,
            'ClientRequestToken': token,
            'Step': 'createSecret'
        },
        {}
    )
    mock_secrets.put_secret_value.assert_called_with(
        SecretId='arn:aws:secretsmanager:::secrets/fakesecret',
        ClientRequestToken='token',
        SecretString=json.dumps({'tenant': 'mmm-dev', 'client_secret': 'baz', 'client_id': 'bar'}),
        VersionStages=['AWSPENDING'],
    )
    rollback_secret.assert_called_with(
        ANY,
        {'tenant': 'mmm-dev', 'client_secret': 'foo', 'client_id': 'bar'},
    )

@patch('src.rotation.client')
@patch('src.rotation.config')
def test_handler_no_token(mock_config, mock_secrets):
    """Test the handler when there is no token"""
    mock_secrets.describe_secret.return_value = {
        'RotationEnabled': True,
        'VersionIdsToStages': {}
    }
    mock_secrets.get_secret_value.return_value = {'SecretString': json.dumps(
        {'tenant': 'mmm-dev'}
    )}
    token = 'token'
    provider = 'auth0'
    mock_config.get_provider.return_value = provider
    with pytest.raises(ValueError):
        rotation.lambda_handler(
            {
                'SecretId': ARN,
                'ClientRequestToken': token,
                'Step': 'createSecret'
            },
            {}
        )


@patch('src.rotation.client')
@patch('src.rotation.config')
def test_handler_is_current(mock_config, mock_secrets):
    """When the token passed is already the current"""
    mock_secrets.describe_secret.return_value = {
        'RotationEnabled': True,
        'VersionIdsToStages': {
            'token': ['AWSCURRENT']
        }
    }
    mock_secrets.get_secret_value.return_value = {'SecretString': json.dumps(
        {'tenant': 'mmm-dev'}
    )}
    token = 'token'
    provider = 'auth0'
    mock_config.get_provider.return_value = provider
    rotation.lambda_handler(
        {
            'SecretId': ARN,
            'ClientRequestToken': token,
            'Step': 'createSecret'
        },
        {}
    )


@patch('src.rotation.client')
@patch('src.rotation.config')
def test_handler_no_pending(mock_config, mock_secrets):
    """When there is no pending version to change"""
    mock_secrets.describe_secret.return_value = {
        'RotationEnabled': True,
        'VersionIdsToStages': {
            'token': []
        }
    }
    mock_secrets.get_secret_value.return_value = {'SecretString': json.dumps(
        {'tenant': 'mmm-dev'}
    )}
    token = 'token'
    provider = 'auth0'
    mock_config.get_provider.return_value = provider
    with pytest.raises(ValueError):
        rotation.lambda_handler(
            {
                'SecretId': ARN,
                'ClientRequestToken': token,
                'Step': 'createSecret'
            },
            {}
        )


@patch('src.rotation.client')
@patch('src.rotation.create_secret')
@patch('src.rotation.config')
def test_handler_create(mock_config, mock_create, mock_secrets):
    """Test the handler with a create event"""
    mock_secrets.describe_secret.return_value = {
        'RotationEnabled': True,
        'VersionIdsToStages': {
            'token': ['AWSPENDING']
        }
    }
    mock_secrets.get_secret_value.return_value = {'SecretString': json.dumps(
        {'tenant': 'mmm-dev'}
    )}
    token = 'token'
    provider = 'auth0'
    mock_config.get_provider.return_value = provider
    rotation.lambda_handler(
        {
            'SecretId': ARN,
            'ClientRequestToken': token,
            'Step': 'createSecret'
        },
        {}
    )
    mock_create.assert_called_with(mock_secrets, provider, ARN, token)


@patch('src.rotation.client')
@patch('src.rotation.set_secret')
@patch('src.rotation.config')
def test_handler_set(mock_config, mock_set, mock_secrets):
    """Test the handler for setting a secret"""
    mock_secrets.describe_secret.return_value = {
        'RotationEnabled': True,
        'VersionIdsToStages': {
            'token': ['AWSPENDING']
        }
    }
    mock_secrets.get_secret_value.return_value = {'SecretString': json.dumps(
        {'tenant': 'mmm-dev'}
    )}
    token = 'token'
    provider = 'auth0'
    mock_config.get_provider.return_value = provider
    rotation.lambda_handler(
        {
            'SecretId': ARN,
            'ClientRequestToken': token,
            'Step': 'setSecret'
        },
        {}
    )
    mock_set.assert_called_with()


@patch('src.rotation.client')
@patch('src.rotation.test_secret')
@patch('src.rotation.config')
def test_handler_test(mock_config, mock_test, mock_secrets):
    """Test the handler with a test event"""
    mock_secrets.describe_secret.return_value = {
        'RotationEnabled': True,
        'VersionIdsToStages': {
            'token': ['AWSPENDING']
        }
    }
    mock_secrets.get_secret_value.return_value = {'SecretString': json.dumps(
        {'tenant': 'mmm-dev'}
    )}
    token = 'token'
    provider = 'auth0'
    mock_config.get_provider.return_value = provider
    rotation.lambda_handler(
        {
            'SecretId': ARN,
            'ClientRequestToken': token,
            'Step': 'testSecret'
        },
        {}
    )
    mock_test.assert_called_with(mock_secrets, provider, ARN)


@patch('src.rotation.client')
@patch('src.rotation.finish_secret')
@patch('src.rotation.config')
def test_handler_finish(mock_config, mock_finish, mock_secrets):
    """Test the handler with a finish event"""
    mock_secrets.describe_secret.return_value = {
        'RotationEnabled': True,
        'VersionIdsToStages': {
            'token': ['AWSPENDING']
        }
    }
    mock_secrets.get_secret_value.return_value = {'SecretString': json.dumps(
        {'tenant': 'mmm-dev'}
    )}
    token = 'token'
    provider = 'auth0'
    mock_config.get_provider.return_value = provider
    rotation.lambda_handler(
        {
            'SecretId': ARN,
            'ClientRequestToken': token,
            'Step': 'finishSecret'
        },
        {}
    )
    mock_finish.assert_called_with(mock_secrets, ARN, token)


@patch('src.rotation.client')
@patch('src.rotation.config')
def test_handler_invalid_step(mock_config, mock_secrets):
    """Test the handler with an invalid step"""
    mock_secrets.describe_secret.return_value = {
        'RotationEnabled': True,
        'VersionIdsToStages': {
            'token': ['AWSPENDING']
        }
    }
    mock_secrets.get_secret_value.return_value = {'SecretString': json.dumps(
        {'tenant': 'mmm-dev'}
    )}
    token = 'token'
    provider = 'auth0'
    mock_config.get_provider.return_value = provider
    with pytest.raises(ValueError):
        rotation.lambda_handler(
            {
                'SecretId': ARN,
                'ClientRequestToken': token,
                'Step': 'invalidStep'
            },
            {}
        )


@patch('src.rotation.secret.get_secret')
def test_create_secret_exists(mock_get_secret):
    """Test the create method"""
    client_id = 'client_id'
    new_secret = 'new_secret'
    mock_get_secret.return_value = json.dumps({
        'client_id': client_id,
        'client_secret': 'old_secret'
    })
    provider = Mock()
    provider.rotate_client_secret.return_value = new_secret
    client = Mock()
    token = 'token'
    rotation.create_secret(client, provider, ARN, token)
    mock_get_secret.assert_called_with(
        client, ARN, rotation.logger)
    provider.rotate_client_secret.assert_called_with(client_id=client_id)
    client.put_secret_value.assert_called_with(
        SecretId=ARN,
        ClientRequestToken=token,
        SecretString=json.dumps(
            {'client_id': client_id, 'client_secret': new_secret}),
        VersionStages=['AWSPENDING']
    )


def test_set_secret():
    """Test the set secret method"""
    # The method does nothing at the moment
    rotation.set_secret()


@patch('src.rotation.secret.get_secret')
def test_test_secret(mock_get_secret):
    """Test the test_secret method"""
    tenant = 'mmm-id.auth0.com'
    client_id = 'client_id'
    client_secret = 'client_secret'
    mock_get_secret.return_value = json.dumps({
        'tenant': tenant,
        'client_id': client_id,
        'client_secret': client_secret
    })
    provider = Mock()
    provider.get_application.return_value={'client_secret':client_secret}
    client = Mock()
    assert rotation.test_secret(client, provider, ARN)
    mock_get_secret.assert_called_with(
        client=client, secret_id=ARN, logger=rotation.logger, stage='AWSPENDING')


@patch('src.rotation.secret.get_secret')
def test_test_secret_fail(mock_get_secret):
    """Test the test_secret method when the test fails"""
    tenant = 'mmm-id.auth0.com'
    client_id = 'client_id'
    client_secret = 'client_secret'
    mock_get_secret.return_value = json.dumps({
        'tenant': tenant,
        'client_id': client_id,
        'client_secret': client_secret
    })
    provider = Mock()
    client = Mock()
    provider.get_application.return_value={'client_secret':'foobarbazquxquux'}
    with pytest.raises(ValueError):
        rotation.test_secret(client, provider, ARN)
    mock_get_secret.assert_called_with(
        client=client, secret_id=ARN, logger=rotation.logger, stage='AWSPENDING')


def test_finish_secret():
    """Test the finish_secret method"""
    mock_secrets = Mock()
    token = 'ver2'
    mock_secrets.describe_secret.return_value = {
        'VersionIdsToStages': {
            'ver1': ['AWSCURRENT'],
            'ver2': ['AWSPENDING']
        }
    }
    rotation.finish_secret(mock_secrets, ARN, token)
    mock_secrets.describe_secret.assert_called_with(SecretId=ARN)
    mock_secrets.update_secret_version_stage.assert_called_with(
        SecretId=ARN,
        VersionStage='AWSCURRENT',
        MoveToVersionId=token,
        RemoveFromVersionId='ver1'
    )


def test_finish_secret_finished():
    """ Test that it doesn't update the secret if it's already AWSCURRENT"""
    mock_secrets = Mock()
    token = 'ver1'
    mock_secrets.describe_secret.return_value = {
        'VersionIdsToStages': {
            'ver1': ['AWSCURRENT'],
            'ver2': ['AWSPENDING']
        }
    }
    rotation.finish_secret(mock_secrets, ARN, token)
    mock_secrets.describe_secret.assert_called_with(SecretId=ARN)
    mock_secrets.update_secret_version_stage.assert_not_called()
