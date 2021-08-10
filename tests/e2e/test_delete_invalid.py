'''
Verify that deleting invalid resources does
not raise exceptions
'''
from unittest.mock import MagicMock
import src.utils.config
import src.grant
import src.application
import src.api

def test_delete_grant(monkeypatch):
    '''
    Test that deleting non-existent grants
    and invalid grant ids don't blow up
    '''
    monkeypatch.setenv('AUTH_PROVIDER', 'auth0')
    monkeypatch.setenv('ENVIRON', 'qa')
    event = {
        'PhysicalResourceId': 'cgr_foobarbazquxquux',
        'ResourceProperties': {
            'Tenant': 'mmm-id.auth0.com',

        }
    }
    context = MagicMock()
    helper = MagicMock()
    src.grant.delete(event, context, helper)

    event['PhysicalResourceId'] = 'invalid_id'
    src.grant.delete(event, context, helper)

def test_delete_api(monkeypatch):
    '''
    Test that deleting non-existent grants
    and invalid grant ids don't blow up
    '''
    monkeypatch.setenv('AUTH_PROVIDER', 'auth0')
    monkeypatch.setenv('ENVIRON', 'qa')
    event = {
        'PhysicalResourceId': 'foo-bar-baz',
        'ResourceProperties': {
            'Tenant': 'mmm-id.auth0.com',

        }
    }
    context = MagicMock()
    helper = MagicMock()
    src.api.delete(event, context, helper)

    event['PhysicalResourceId'] = 'invalid_id#id'
    src.api.delete(event, context, helper)

def test_delete_application(monkeypatch):
    '''
    Test that deleting non-existent applications
    and invalid application ids don't blow up
    '''
    monkeypatch.setenv('AUTH_PROVIDER', 'auth0')
    monkeypatch.setenv('ENVIRON', 'qa')
    # SEMS: 638590899720
    event = {
        # permission denied - SEMS account, unreal name
        # pylint: disable=line-too-long
        'PhysicalResourceId': 'arn:aws:secretsmanager:us-east-1:638590899720:secret:/auth0-cr-e2e-not-exists/foo',
        'ResourceProperties': {
            'Tenant': 'mmm-id.auth0.com',

        }
    }
    context = MagicMock()
    helper = MagicMock()
    src.application.delete(event, context, helper)

    event = {
        # resource not found
        # pylint: disable=line-too-long
        'PhysicalResourceId': 'arn:aws:secretsmanager:us-east-1:184518171237:secret:/auth0-cr-e2e-not-exists/foo',
        'ResourceProperties': {
            'Tenant': 'mmm-id.auth0.com',

        }
    }
    context = MagicMock()
    helper = MagicMock()
    src.application.delete(event, context, helper)

def test_delete_application_auth0(monkeypatch):
    '''
    Verify that deleting a non-existent application
    from Auth0 returns OK
    '''
    monkeypatch.setenv('AUTH_PROVIDER', 'auth0')
    monkeypatch.setenv('ENVIRON', 'qa')
    provider = src.utils.config.get_provider('mmm-id.auth0.com')
    provider.delete_application('cr-authn-test-fake-app-id')
