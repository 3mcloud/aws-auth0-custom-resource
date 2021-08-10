# pylint: disable=redefined-outer-name
"""Tests for auth0/index.py"""
from unittest.mock import patch, MagicMock as Mock
import pytest
from src.auth0.index import Auth0Provider
import src.auth0.index as index


@pytest.fixture(name='fake_auth0')
@patch('src.auth0.index.boto3')
@patch('src.auth0.index.secret')
@patch('src.auth0.index.Auth0Provider.authenticate')
def fixture_fake_auth0(_, secret, boto):
    """Test for auth0provider object creation and fixture

    Fixture is used to call object methods in below tests
    """
    secrets = Mock()
    boto.client.return_value = secrets
    secret.get_secret.return_value = (
        '{"tenant": "mmm-id.auth0.com", "AUTH0_CLIENT_ID": "asdlfwo30a", '
        '"AUTH0_CLIENT_SECRET": "2029nvlda0:#--9D(1nvl1"}'
    )
    provider = Auth0Provider('secret', 'mmm-id')
    provider.auth0 = Mock()
    return provider


@patch('src.auth0.index.GetToken')
@patch('src.auth0.index.Auth0')
def test_authenticate(auth0_obj, get_token, fake_auth0):
    """Test for authenticate method"""
    fake_token = Mock()
    get_token.return_value = fake_token
    access_token = 'access_token'
    fake_token.client_credentials.return_value = {'access_token': access_token}
    domain = 'mmm-id.auth0.com'
    client_id = 'client_id'
    secret = 'secret'

    fake_auth0.authenticate(domain, client_id, secret)
    get_token.assert_called_with(domain)
    auth0_obj.assert_called_with(domain, access_token)


def test_resource(fake_auth0):
    """Test for creating a resource"""
    url = 'url.mmm.com'
    name = 'name'
    client_id = 'client_id'
    client_secret = 'client_secret'
    resource_id = 'resource_id'
    grant_id = 'grant_id'
    fake_auth0.auth0.clients.create.return_value = {
        'client_id': client_id, 'client_secret': client_secret}
    fake_auth0.auth0.resource_servers.create.return_value = {
        'id': resource_id}
    fake_auth0.auth0.client_grants.create.return_value = {
        'id': grant_id}
    c_id, c_secret, s_id, g_id = fake_auth0.create_resource(url, name)
    assert client_id == c_id
    assert client_secret == c_secret
    assert resource_id == s_id
    assert grant_id == g_id


@patch('src.auth0.index.time')
def test_get_resource_server(_, fake_auth0):
    """Test for get_resource_server"""
    url = 'url.mmm.com'
    server_id = 'server_id'
    fake_auth0.auth0.resource_servers.get_all.side_effect = [
        [{'identifier': 'wrong.url.com'}],
        [{'identifier': url, 'id': server_id}]
    ]
    assert server_id == fake_auth0.get_resource_server(url)
    fake_auth0.auth0.resource_servers.get_all.assert_called_with(
        page=1, per_page=50)

    fake_auth0.auth0.resource_servers.get_all.side_effect = [
        [{'identifier': 'wrong.url.com'}],
        []
    ]
    assert fake_auth0.get_resource_server(url) is None

    fake_auth0.auth0.resource_servers.get_all.side_effect = [
        [{'identifier': 'wrong.url.com'}],
        [{'identifier': 'wrong.url.com'}],
    ]
    assert fake_auth0.get_resource_server(url) is None

    fake_auth0.auth0.resource_servers.get_all.side_effect = [
        [{'identifier': i}] for i in range(index.PAGE_LIMIT+1)]
    assert fake_auth0.get_resource_server(url) is None

def test_rotate_client_secret(fake_auth0):
    """Test for rotate_client_secret"""
    client_id = 'client_id'
    new_secret = 'new_secret'
    fake_auth0.auth0.clients.rotate_secret.return_value = {
        'client_secret': new_secret}
    assert new_secret == fake_auth0.rotate_client_secret(client_id)
    fake_auth0.auth0.clients.rotate_secret.assert_called_with(client_id)


def test_update_resource(fake_auth0):
    """Test for update_resource"""
    # Update doesn't do anything at the moment
    fake_auth0.update_resource()


def test_delete_resource(fake_auth0):
    """Test for delete_resource"""
    resource_id = 'resource_id'
    client_id = 'client_id'
    fake_auth0.delete_resource(resource_id, client_id)
    fake_auth0.auth0.clients.delete.assert_called_with(client_id)
    fake_auth0.auth0.resource_servers.delete.assert_called_with(resource_id)
