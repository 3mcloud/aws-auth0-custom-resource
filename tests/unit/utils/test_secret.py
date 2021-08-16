"""Tests for utils/secret"""

import base64
from unittest.mock import MagicMock as Mock
from botocore.exceptions import ClientError

from src.utils import secret


def test_get_secret():
    """Test for get_secret"""
    client = Mock()
    client.get_secret_value = Mock(
        return_value={'SecretString': '{"example":"value"}'})
    secret_id = 'arn:aws:secretsmanager:secret/id'
    secret.get_secret(client, secret_id)
    client.get_secret_value.assert_called_with(
        SecretId=secret_id, VersionStage='AWSCURRENT'
    )

    secret.get_secret(client, secret_id, stage='AWSPENDING')
    client.get_secret_value.assert_called_with(
        SecretId=secret_id, VersionStage='AWSPENDING'
    )

    expected = b'{"example":"value"}'
    client.get_secret_value = Mock(
        return_value={'SecretBinary': base64.b64encode(
            expected)}
    )
    res = secret.get_secret(client, secret_id)
    assert res == expected
    client.get_secret_value.assert_called_with(
        SecretId=secret_id, VersionStage='AWSCURRENT'
    )


def test_get_secret_error():
    """Test for get_secret with a variety of errors"""
    cases = [
        ClientError({'Error': {'Code': 'DecryptionFailureException'}}, 'get'),
        ClientError(
            {'Error': {'Code': 'InternalServiceErrorException'}}, 'get'),
        ClientError({'Error': {'Code': 'InvalidParameterException'}}, 'get'),
        ClientError({'Error': {'Code': 'InvalidRequestException'}}, 'get'),
        ClientError({'Error': {'Code': 'ResourceNotFoundException'}}, 'get'),
        ClientError({'Error': {'Code': 'UnknownException'}}, 'get'),
    ]
    client = Mock()
    logger = Mock()
    secret_id = 'arn:aws:secretsmanager:secret/id'

    for case in cases:
        thrown = False
        client.get_secret_value = Mock(side_effect=case)
        try:
            secret.get_secret(client, secret_id, logger)
        except ClientError as exc:
            thrown = True
            assert case == exc
        assert thrown
