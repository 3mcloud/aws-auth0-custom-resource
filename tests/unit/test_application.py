"""
Test the application resource type
"""
from contextlib import contextmanager
import json
from unittest.mock import MagicMock, patch, ANY
import pytest

import botocore
from auth0.v3.exceptions import Auth0Error

from src.validation.application import auth0Validator, tagsValidator
import src.application as app


@contextmanager
def does_not_raise():
    """patch non-raising calls"""
    yield


cases = [
    {
        'name': 'auth0_required_only',
        'parameters': {
            'Tenant': 'foo.com',
            'Type': 'spa',
            'Name': 'cr-unittest',
            'Description': 'test',
        },
        'expect': {
            'application': {
                'app_type': 'spa',
                'name': 'cr-unittest',
                'description': 'test',
                'client_metadata': {},
                'token_endpoint_auth_method': 'none',
                'grant_types': ['implicit', 'authorization_code', 'refresh_token'],
            },
        },
    },
    {
        'name': 'auth0_overwrite_default_spa_grants',
        'parameters': {
            'Tenant': 'foo.com',
            'Type': 'spa',
            'Name': 'cr-unittest',
            'Description': 'test',
            'GrantTypes': ['implicit', 'refresh_token'],
        },
        'expect': {
            'application': {
                'app_type': 'spa',
                'name': 'cr-unittest',
                'description': 'test',
                'client_metadata': {},
                'token_endpoint_auth_method': 'none',
                'grant_types': ['implicit', 'refresh_token'],
            },
        },
    },
    {
        'name': 'auth0_coerce_app_type',
        'parameters': {
            'Tenant': 'foo.com',
            'Type': 'm2m',
            'Name': 'cr-unittest',
            'Description': 'test',
        },
        'expect': {
            'application': {
                'app_type': 'non_interactive',
                'name': 'cr-unittest',
                'description': 'test',
                'client_metadata': {},
                'grant_types': ['client_credentials'],
                'token_endpoint_auth_method': 'client_secret_post',
            },
        },
    },
    {
        'name': 'auth0_m2m_grant_type_ok',
        'parameters': {
            'Tenant': 'foo.com',
            'Type': 'm2m',
            'Name': 'cr-unittest',
            'Description': 'test',
            'GrantTypes': ['client_credentials']
        },
        'expect': {
            'application': {
                'app_type': 'non_interactive',
                'name': 'cr-unittest',
                'description': 'test',
                'client_metadata': {},
                'grant_types': ['client_credentials'],
                'token_endpoint_auth_method': 'client_secret_post',
            },
        },
    },

    {
        'name': 'auth0_spa_grant_type_ok',
        'parameters': {
            'Tenant': 'foo.com',
            'Type': 'spa',
            'Name': 'cr-unittest',
            'Description': 'test',
            'GrantTypes': ['implicit']
        },
        'expect': {
            'application': {
                'app_type': 'spa',
                'name': 'cr-unittest',
                'description': 'test',
                'client_metadata': {},
                'grant_types': ['implicit'],
                'token_endpoint_auth_method': 'none',
            },
        },
    },
    {
        'name': 'auth0_refresh_token_ok',
        'parameters': {
            'Tenant': 'foo.com',
            'Type': 'spa',
            'Name': 'cr-unittest',
            'Description': 'test',
            'RefreshToken': {
                'RotationType': 'rotating'
            },
            'GrantTypes': [
                'refresh_token'
            ]
        },
        'expect': {
            'application': {
                'app_type': 'spa',
                'name': 'cr-unittest',
                'description': 'test',
                'grant_types': [
                    'refresh_token'
                ],
                'refresh_token': {
                    'rotation_type': 'rotating'
                },
                'client_metadata': {},
                'token_endpoint_auth_method': 'none',
            },
        },
    },
    {
        'name': 'auth0_m2m_grant_type_all',
        'parameters': {
            'Tenant': 'foo.com',
            'Type': 'm2m',
            'Name': 'cr-unittest',
            'Description': 'test',
            'GrantTypes': [
                'client_credentials',
                'implicit',
                'authorization_code',
                'refresh_token',
                'password',
                'mfa',
            ]
        },
        'expect': {
            'application': {
                'grant_types': [
                    'client_credentials',
                    'implicit',
                    'authorization_code',
                    'refresh_token',
                    'password',
                    'mfa'
                ],
                'token_endpoint_auth_method': 'client_secret_post',
                'name': 'cr-unittest',
                'description': 'test',
                'app_type': 'non_interactive',
                'client_metadata': {},
            },
        },
    },
    {
        'name': 'auth0_moar_config',
        'parameters': {
            'Tenant': 'foo.com',
            'Type': 'spa',
            'Name': 'cr-unittest',
            'Description': 'test',
            'LogoUri': '',
            'LoginURI': '',
            'CallbackUrls': [''],
            'LogoutUrls': [''],
            'WebOrigins': [''],
            'AllowedOrigins': [''],
            'JWTConfiguration': {
                'LifetimeInSeconds': '86400',
                'Scopes': {},
                'Alg': 'RS256',
            },
            'Connections': [
                'conn1',
                'conn2'
            ]
        },
        'expect': {
            'application': {
                'app_type': 'spa',
                'name': 'cr-unittest',
                'description': 'test',
                'logo_uri': '',
                'initiate_login_uri': '',
                'callbacks': [''],
                'allowed_logout_urls': [''],
                'web_origins': [''],
                'allowed_origins': [''],
                'jwt_configuration': {
                    'lifetime_in_seconds': 86400,
                    'scopes': {},
                    'alg': 'RS256',
                },
                'grant_types': ['implicit', 'authorization_code', 'refresh_token'],
                'client_metadata': {},
                'token_endpoint_auth_method': 'none',
            },
        }
    },
    {
        'name': 'auth0_invalid_type',
        'parameters': {
            'Tenant': 'foo.com',
            'Type': 'bar',
            'Name': 'cr-unittest',
            'Description': 'test',
        },
        'expect': {
            'error': pytest.raises(Exception, match='unallowed value bar'),
        }
    },
    {
        'name': 'auth0_tags',
        'parameters': {
            'Tenant': 'foo.com',
            'Type': 'spa',
            'Name': 'cr-unittest',
            'Description': 'test',
            'AllowAdGroups': [
                'foo',
                'bar'
            ],
            'ClientMetadata': {
                'baz': 'qux'
            }
        },
        'helper_data': {
            'tags': {
                'AllowAdGroups': [
                    'foo',
                    'bar',
                ]
            }
        },
        'expect': {
            'application': {
                'app_type': 'spa',
                'name': 'cr-unittest',
                'description': 'test',
                'client_metadata': {
                    'AllowAdGroups': '["foo","bar"]',
                    'baz': 'qux',
                },
                'grant_types': ['implicit', 'authorization_code', 'refresh_token'],
                'token_endpoint_auth_method': 'none',
            },
        },
    },
]
case_names = [case['name'] for case in cases]

# pylint: disable=line-too-long


@pytest.mark.skip('this test adds no value. Use it to debug the validator. case auth0_tags fails in this test')
@pytest.mark.parametrize('case', cases, ids=case_names)
def test_validate(case):
    """test initializing the application object"""
    excepted = False
    with case['expect'].get('error', does_not_raise()):
        doc = auth0Validator.validated(case['parameters'])
        if not doc:
            excepted = True
            raise Exception(auth0Validator.errors)

    # Do not test passed this point if an exception was raised
    if excepted:
        return

    assert doc == case['expect']['application']


@pytest.mark.parametrize('case', cases, ids=case_names)
@patch('src.application.config.get_provider')
@patch('src.application.secrets_client')
@patch('src.application.ssm')
def test_create(ssm, secrets_client, get_provider, case, monkeypatch):
    """test creating an application"""
    monkeypatch.setenv('KMS_KEY_ID', 'baz_key')
    monkeypatch.setenv('ENVIRON', 'qa')
    monkeypatch.setenv('ROTATION', 'arn:aws:qux')

    secrets_client.create_secret.return_value = {
        'ARN': 'arn:aws:secret',
        'Name': '/qa/auth0/crunittest',
    }
    provider = MagicMock()
    provider.create_application.return_value = ('foo', 'bar')  # client_id, client_secret

    helper = MagicMock()
    helper.Data = case.get('helper_data', {})

    get_provider.return_value = provider

    event = {
        'ResourceProperties': case['parameters'],
    }

    with case['expect'].get('error', does_not_raise()):
        app.create(event, {}, helper)

    # Do not test passed this point if an exception was raised
    if 'error' in case['expect']:
        return

    provider.create_application.assert_called_with(
        **case['expect']['application']
    )

    if 'Connections' in case['parameters']:
        provider.add_to_connection.assert_called_with(
            case['parameters']['Connections'][-1], helper.Data['ClientId']
        )

    if case['parameters']['Type'] == 'm2m':
        secrets_client.create_secret.assert_called_with(
            Name='/qa/auth0/crunittest',
            KmsKeyId='baz_key',
            SecretString=json.dumps({
                'client_id': 'foo',
                'client_secret': 'bar',
                'tenant': 'foo.com',
            }),
            Tags=None
        )
        secrets_client.rotate_secret.assert_called_with(
            SecretId='/qa/auth0/crunittest',
            RotationLambdaARN='arn:aws:qux',
            RotationRules={
                'AutomaticallyAfterDays': 30
            }
        )
        assert helper.Data['Arn'] == 'arn:aws:secret'
        assert helper.Data['Name'] == '/qa/auth0/crunittest'
    else:
        secret_name = '/qa/auth0/foo/client_secret'
        ssm.put_parameter.assert_called_with(Name=secret_name, Value='bar', Type='SecureString')
        assert helper.Data['ClientSecret'] == secret_name


@pytest.mark.parametrize('case', cases, ids=case_names)
@patch('src.application.config.get_provider')
@patch('src.application.secret.get_muxed_secret')
def test_update(get_muxed_secret, get_provider, case, monkeypatch):
    """test creating an application"""
    monkeypatch.setenv('KMS_KEY_ID', 'baz_key')
    monkeypatch.setenv('ENVIRON', 'qa')
    monkeypatch.setenv('ROTATION', 'arn:aws:qux')

    provider = MagicMock()
    provider.update_application.return_value = ('foo', 'bar')  # client_id, client_secret
    get_provider.return_value = provider

    get_muxed_secret.return_value = {
        'ARN': 'arn:aws:secret',
        'Name': '/qa/auth0/cr-unittest',
        'SecretValue': json.dumps({
            'client_id': 'foo-test'
        }),
    }

    helper = MagicMock()
    helper.Data = case.get('helper_data', {})
    physical_id = '/qa/auth0/crunittest' if case['parameters']['Type'] == 'm2m' else 'foo-test'
    event = {
        'ResourceProperties': case['parameters'],
        'OldResourceProperties': case['parameters'],
        'PhysicalResourceId': physical_id,
    }

    with case['expect'].get('error', does_not_raise()):
        app.update(event, {}, helper)

    # Do not test passed this point if an exception was raised
    if 'error' in case['expect']:
        return

    provider.update_application.assert_called_with(
        'foo-test',
        **case['expect']['application'],
    )

    if case['parameters']['Type'] == 'm2m':
        get_muxed_secret.assert_called_with(
            ANY,
            '/qa/auth0/crunittest',
            ANY
        )

        assert helper.Data['Arn'] == 'arn:aws:secret'
        assert helper.Data['Name'] == '/qa/auth0/crunittest'


def test_manage_connection():
    """Test managing a list of connections"""
    connections = ['conn1', 'conn2']
    app_id = '1234'
    method = MagicMock()
    assert [] == app.manage_connection(connections, app_id, method)
    assert method.call_count == len(connections)

    method.side_effect = Exception()
    assert connections == app.manage_connection(connections, app_id, method)


def test_update_connections():
    """test updating connections, one to add, one to remove, one to keep"""
    old = ['a', 'b']
    current = ['b', 'c']
    provider = MagicMock()
    app_id = '1234'

    app.update_connections(old, current, provider, app_id)
    provider.add_to_connection.assert_called_with('c', app_id)
    provider.remove_from_connection.assert_called_with('a', app_id)

    provider.add_to_connection.side_effect = Exception()

    with pytest.raises(Exception):
        app.update_connections(old, current, provider, app_id)


@patch('src.application.config.get_provider')
@patch('src.utils.secret.get_muxed_secret')
@patch('src.application.secrets_client', MagicMock())
@patch('src.application.ssm', MagicMock())
def test_delete(get_muxed_secret, get_provider):
    """test deleting an application"""
    get_muxed_secret.return_value = {
        'ARN': 'arn:aws:secret',
        'Name': '/qa/auth0/cr-unittest',
        'SecretValue': json.dumps({
            'client_id': 'foobar'
        }),
    }
    provider = MagicMock()
    provider.delete_app.return_value = 'appid'
    helper = MagicMock()
    get_provider.return_value = provider
    event = {
        'PhysicalResourceId': 'foobar',
        'ResourceProperties': {
            'Tenant': 'mmm-id.auth0.com',
        },
    }
    app.delete(event, {}, helper)
    provider.delete_application.assert_called_with('foobar')

    provider.delete_application.side_effect = Auth0Error(
        400, 'invalid_id', 'Path validation error: ')
    app.delete(event, {}, helper)

    provider.delete_application.side_effect = Auth0Error(403, 'invalid_token', 'Token is invalid')
    with pytest.raises(Auth0Error):
        app.delete(event, {}, helper)

    event['ResourceProperties']['Type'] = 'm2m'
    get_muxed_secret.side_effect = botocore.exceptions.ClientError({
        'Error': {
            'Message': 'not gonna do it. wouldn\'t be prudent',
            'Code': 'AccessDeniedException',
        }
    }, MagicMock())
    app.delete(event, {}, helper)


def test_default_tags():
    """
    Test the tags validation / stripping extra values
    """
    tags = {
        'AlternateContactEmail': 'ktruckenmiller@mmm.com',
        'ApplicationID': '227319dd-0762-4e59-8800-f18d30cce402',
        'ApplicationName': 'aws-cr-authn-regression',
        'CCOE_RechargeDepartment': '510520',
        'CustomerEnvironment': 'qa',
        'DataClassification': '3M General',
        'Environment': 'QA',
        'ITSMServiceName': 'CRSLBLK',
        'ProductOwnerEmail': 'ewalker3@mmm.com',
        'TeamName': 'sarahconnor',
        'Unit': 'crsl',
        'AllowAdGroups': ['foo', 'bar'],
    }
    validated = tagsValidator.validated(tags)
    assert validated == {
        'AllowAdGroups': '["foo","bar"]',
        'ApplicationID': '227319dd-0762-4e59-8800-f18d30cce402',
    }
