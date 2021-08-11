"""
Verify that the update process works for connections in many cases
"""
from unittest.mock import MagicMock

import pytest
from auth0.v3.exceptions import Auth0Error

import src.utils.config
from src.auth0.index import Auth0Provider
import src.application


def check_app_enabled(app_id, conn_id, provider, enabled=True):
    """
    Check that the connection has the given app id enabled
    """
    conn = provider.auth0.connections.get(conn_id, ['enabled_clients'])
    assert enabled == (app_id in conn['enabled_clients'])


def test_application_connection(monkeypatch):
    """
    Test that the connections associated with an application work when created
    and updated.
    """
    provider = Auth0Provider(management_secret='qa/auth0/tenant/mmm-dev',
                             tenant='mmm-dev.auth0.com')
    monkeypatch.setenv('ENVIRON', 'qa')
    monkeypatch.setenv(
        'ROTATION', 'arn:aws:lambda:us-east-1:184518171237:function:qa-auth-rotation')
    # Use the aws/secretsmanager key for the test application
    monkeypatch.setenv('KMS_KEY_ID', '7c3f47f9-3bc8-41cd-8ccb-6ecfa1ab362a')
    ad_conn = 'con_WYljqEqcw2L8VU7c'
    social_conn = 'con_YfQqRmWmiRQ041D2'
    db_conn = 'con_xf0IqInFb8f6oApf'
    event = {
        'ResourceProperties': {
            'Tenant': 'mmm-dev.auth0.com',
            'Name': 'aws-cr-authn-e2e-app-connection',
            'Type': 'spa',
            'Description': 'End to end application',
            'Connections': [ad_conn, social_conn]
        }
    }
    context = MagicMock()
    helper = MagicMock()
    helper.Data = {'tags': {}, 'stack_tags': []}
    # Create the app with connections
    event['PhysicalResourceId'] = src.application.create(event, context, helper)
    for conn_id in [ad_conn, social_conn]:
        check_app_enabled(helper.Data['ClientId'], conn_id, provider)

    # Update the app with different connections
    event['OldResourceProperties'] = {'Connections': event['ResourceProperties']['Connections']}
    event['ResourceProperties']['Connections'] = [social_conn, db_conn]
    src.application.update(event, context, helper)
    for conn_id in [social_conn, db_conn]:
        check_app_enabled(helper.Data['ClientId'], conn_id, provider)
    # Make sure the first connection was disabled
    check_app_enabled(helper.Data['ClientId'], ad_conn, provider, enabled=False)

    # Clean up
    src.application.delete(event, context, helper)

    check_app_enabled(helper.Data['ClientId'], social_conn, provider, enabled=False)


def test_missing_connection_create(monkeypatch):
    """
    Test that a create and delete fail when a connection doesn't exist
    """
    provider = Auth0Provider(management_secret='qa/auth0/tenant/mmm-dev',
                             tenant='mmm-dev.auth0.com')
    monkeypatch.setenv('ENVIRON', 'qa')
    monkeypatch.setenv(
        'ROTATION', 'arn:aws:lambda:us-east-1:184518171237:function:qa-auth-rotation')
    # Use the aws/secretsmanager key for the test application
    monkeypatch.setenv('KMS_KEY_ID', '7c3f47f9-3bc8-41cd-8ccb-6ecfa1ab362a')
    bad_conn = 'con_AAaaaAaaa1A1AA1a'
    event = {
        'ResourceProperties': {
            'Tenant': 'mmm-dev.auth0.com',
            'Name': 'aws-cr-authn-e2e-app-connection-missing-create',
            'Type': 'spa',
            'Description': 'End to end application',
            'Connections': [bad_conn]
        }
    }
    context = MagicMock()
    helper = MagicMock()
    helper.Data = {'tags': {}, 'stack_tags': []}
    # Create the app with connections
    with pytest.raises(Auth0Error):
        src.application.create(event, context, helper)

    # Make sure the application was cleaned up in Auth0
    with pytest.raises(Auth0Error):
        provider.auth0.clients.get(helper.Data['ClientId'])
