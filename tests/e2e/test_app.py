"""End to end test for auth0 spa app"""

from unittest.mock import MagicMock
import pytest

from src.application import create, delete


def test_app(monkeypatch):
    """Test the app methods"""
    monkeypatch.setenv('ENVIRON', 'qa')
    monkeypatch.setenv('AUTH_PROVIDER', 'auth0')

    event = {
        "ResourceProperties": {
            "ServiceToken": '1234',
            "Tenant": "mmm-dev.auth0.com",
            "Name": 'cr-authn-test-184518171237',
            "Type": "spa",
            "Description": "An e2e test to ensure the basics work always",
            "Connections": [
                "con_WYljqEqcw2L8VU7c"
            ],
            "OidcConformant": True,
            "CallbackUrls": [
                "http://localhost:3000"
            ],
            "LogoutUrls": [
                "http://localhost:3000"
            ],
            "WebOrigins": [
                "http://localhost:3000"
            ],
            "GrantTypes": [
                "refresh_token",
                # "authorization_code"
            ],
            "RefreshToken": {
                "RotationType": "rotating",
                "ExpirationType": "expiring",
                "TokenLifetime": 1800
            },
            "AllowedClients": [],
            'AuthMethod': 'None'
        }
    }
    mock_helper = MagicMock()
    mock_helper.Data = {}
    create(event, {}, mock_helper)
    client_id = mock_helper.Data['ClientId']
    delete_app(client_id)
    assert mock_helper.Data['ClientSecret'] == f'/qa/auth0/{client_id}/client_secret'



@pytest.mark.skip(reason="only use this to clean up the above when testing SPA apps")
def test_delete(monkeypatch):
    """Helper to delete an app."""
    app_id = 'UKvwmw3VLahKGflmV33UguRRcg0WRSQK'
    monkeypatch.setenv('ENVIRON', 'qa')
    monkeypatch.setenv('AUTH_PROVIDER', 'auth0')
    delete_app(app_id)


def delete_app(app_id):
    """Helper to delete an app that was created"""
    event = {
        "ResourceProperties": {
            "ServiceToken": '1234',
            "Tenant": "mmm-dev.auth0.com",
            "Name": 'cr-authn-test-184518171237',
            "Type": "spa",
            "Description": "An e2e test to ensure the basics work always",
            "Connections": [
                "con_WYljqEqcw2L8VU7c"
            ],
            "OidcConformant": True,
            "CallbackUrls": [
                "http://localhost:3000"
            ],
            "LogoutUrls": [
                "http://localhost:3000"
            ],
            "WebOrigins": [
                "http://localhost:3000"
            ],
            "GrantTypes": [
                "refresh_token",
                "authorization_code",
                "implicit"
            ],
            "RefreshToken": {
                "RotationType": "rotating",
                "ExpirationType": "expiring",
                "TokenLifetime": 1800
            },
            "AllowedClients": [],
        },
        'PhysicalResourceId': app_id
    }

    delete(event, {}, MagicMock())
