'''
Test the grant resource type
'''
from contextlib import contextmanager
from unittest.mock import MagicMock, patch
import pytest

from auth0.v3.exceptions import Auth0Error

from src.validation.grant import auth0Validator
import src.grant as grant


@contextmanager
def does_not_raise():
    '''Helper for error raising'''
    yield


cases = [  # pylint: disable=invalid-name
    {
        'name': 'auth0_required_only',
        'provider': 'auth0',
        'parameters': {
            'Tenant': 'foo.com',
            'ApplicationId': '1234',
            'Audience': 'http://cr-unittest.com',
        },
        'expect': {
            'grant': {
                'application_id': '1234',
                'audience': 'http://cr-unittest.com',
            },
        }
    },
    {
        'name': 'auth0_all_config',
        'provider': 'auth0',
        'parameters': {
            'Tenant': 'foo.com',
            'ApplicationId': '1234',
            'Audience': 'http://cr-unittest.com',
            'Scope': ['scope1', 'scope2']
        },
        'expect': {
            'grant': {
                'application_id': '1234',
                'audience': 'http://cr-unittest.com',
                'scope': ['scope1', 'scope2']
            },
        }
    }
]
case_names = [case['name'] for case in cases]  # pylint: disable=invalid-name


@pytest.mark.parametrize('case', cases, ids=case_names)
def test_validate(case):
    '''test initializing the grant object'''
    excepted = False
    with case['expect'].get('error', does_not_raise()):
        doc = auth0Validator.validated(case['parameters'])
        if not doc:
            excepted = True
            raise Exception(auth0Validator.errors)

    # Do not test passed this point if an exception was raised
    if excepted:
        return

    assert doc == case['expect']['grant']


@pytest.mark.parametrize('case', cases, ids=case_names)
@patch('src.grant.config.get_provider')
def test_create(get_provider, case):
    '''test creating a grant'''
    provider = MagicMock()
    provider.create_grant.return_value = 'grantid'

    helper = MagicMock()
    helper.Data = {}

    get_provider.return_value = provider

    event = {
        'ResourceProperties': case['parameters'],
    }

    with case['expect'].get('error', does_not_raise()):
        grant.create(event, {}, helper)

    # Do not test passed this point if an exception was raised
    if 'error' in case['expect']:
        return

    provider.create_grant.assert_called_with(
        **case['expect']['grant']
    )

@patch('src.grant.config.get_provider')
def test_delete(get_provider):
    '''test deleting a grant'''
    provider = MagicMock()
    provider.delete_grant.return_value = 'grantid'
    helper = MagicMock()
    get_provider.return_value = provider
    event = {
        'PhysicalResourceId': 'foobar',
        'ResourceProperties': {
            'Tenant': 'mmm-id.auth0.com',
        },
    }
    grant.delete(event, {}, helper)
    provider.delete_grant.assert_called_with(
        'foobar'
    )

    provider.delete_grant.side_effect = Auth0Error(400, 'invalid_id', 'Path validation error: ')
    grant.delete(event, {}, helper)

    provider.delete_grant.side_effect = Auth0Error(403, 'invalid_token', 'Token is invalid')
    with pytest.raises(Auth0Error):
        grant.delete(event, {}, helper)
