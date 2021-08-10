"""
Test the api resource type
"""
from contextlib import contextmanager
from unittest.mock import MagicMock, patch
import pytest

from auth0.v3.exceptions import Auth0Error

from src.validation.api import auth0Validator
import src.api as api


@contextmanager
def does_not_raise():
    """Helper for error raising"""
    yield


cases = [  # pylint: disable=invalid-name
    {
        'name': 'auth0_required_only',
        'provider': 'auth0',
        'parameters': {
            'Tenant': 'foo.com',
            'Audience': 'http://cr-unittest.com',
        },
        'expect': {
            'api': {
                'identifier': 'http://cr-unittest.com',
            },
        }
    },
    {
        'name': 'auth0_all_config',
        'provider': 'auth0',
        'parameters': {
            'Tenant': 'foo.com',
            'Audience': 'http://cr-unittest.com',
            'Name': 'unitteset-api',
            'Scopes': ['scope1', 'scope2'],
            'SigningAlg': 'HS256',
            'SigningSecret': 'secret',
            'AllowOfflineAccess': 'True',
            'TokenLifetime': '1234',
            'TokenDialect': 'access_token',
            'SkipConsentForVerifiableFirstPartyClients': 'True',
            'EnforcePolicies': True,
        },
        'expect': {
            'api': {
                'identifier': 'http://cr-unittest.com',
                'name': 'unitteset-api',
                'scopes': ['scope1', 'scope2'],
                'signing_alg': 'HS256',
                'signing_secret': 'secret',
                'allow_offline_access': True,
                'token_lifetime': 1234,
                'token_dialect': 'access_token',
                'skip_consent_for_verifiable_first_party_clients': True,
                'enforce_policies': True,
            },
        }
    }
]
case_names = [case['name'] for case in cases]  # pylint: disable=invalid-name


@pytest.mark.parametrize('case', cases, ids=case_names)
def test_validate(case):
    """test initializing the grant object"""
    excepted = False
    with case['expect'].get('error', does_not_raise()):
        doc = auth0Validator.validated(case['parameters'])
        if not doc:
            excepted = True
            raise Exception(auth0Validator.errors)

    # Do not test passed this point if an exception was raised
    if excepted:
        return

    assert doc == case['expect']['api']


@pytest.mark.parametrize('case', cases, ids=case_names)
@patch('src.grant.config.get_provider')
def test_create(get_provider, case):
    """test creating an api"""
    provider = MagicMock()
    provider.create_api.return_value = 'apiid'

    helper = MagicMock()
    helper.Data = {}

    get_provider.return_value = provider

    event = {
        'ResourceProperties': case['parameters'],
    }

    with case['expect'].get('error', does_not_raise()):
        api.create(event, {}, helper)

    # Do not test passed this point if an exception was raised
    if 'error' in case['expect']:
        return

    provider.create_api.assert_called_with(
        **case['expect']['api']
    )


@pytest.mark.parametrize('case', cases, ids=case_names)
@patch('src.grant.config.get_provider')
def test_update(get_provider, case):
    """test updating an api"""
    provider = MagicMock()
    provider.update_api.return_value = 'apiid'

    helper = MagicMock()
    helper.Data = {}

    get_provider.return_value = provider

    event = {
        'ResourceProperties': case['parameters'],
        'PhysicalResourceId': 'id',
        'OldResourceProperties': case['parameters'],
    }

    with case['expect'].get('error', does_not_raise()):
        api.update(event, {}, helper)

    # Do not test passed this point if an exception was raised
    if 'error' in case['expect']:
        return

    del case['expect']['api']['identifier']

    provider.update_api.assert_called_with(
        'id', **case['expect']['api']
    )


@patch('src.api.config.get_provider')
def test_delete(get_provider):
    """test deleting a grant"""
    provider = MagicMock()
    provider.delete_api.return_value = 'grantid'
    helper = MagicMock()
    get_provider.return_value = provider
    event = {
        'PhysicalResourceId': 'foobar',
        'ResourceProperties': {
            'Tenant': 'mmm-id.auth0.com',
        },
    }
    api.delete(event, {}, helper)
    provider.delete_api.assert_called_with('foobar')

    provider.delete_api.side_effect = Auth0Error(400, 'invalid_id', 'Path validation error: ')
    api.delete(event, {}, helper)

    provider.delete_api.side_effect = Auth0Error(403, 'invalid_token', 'Token is invalid')
    with pytest.raises(Auth0Error):
        api.delete(event, {}, helper)
