"""
Verify that deleting invalid resources does
not raise exceptions
"""
import random
import string
from unittest.mock import MagicMock
import src.utils.config as config
import src.grant as grant



def get_random_string(length=8):
    """randome string for tests"""
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(length))

def test_create_grant(monkeypatch):
    """
    Test that we can create an existing grant without failing
    """
    tenant = 'mmm-dev.auth0.com'
    name = f'e2e-test-{get_random_string()}'
    audience = f'https://{name}.co'
    client_id = None
    api_id = None
    monkeypatch.setenv('ENVIRON', 'qa')

    provider = config.get_provider(tenant)


    try:
        client_id, _ = provider.create_application(**{
            'name': name,
            'description': 'e2e test application',
            'app_type': 'spa',
        })

        api_id = provider.create_api(**{
            'name': name,
            'identifier': audience,
        })
        event = {
            'ResourceProperties': {
                'ApplicationId': client_id,
                'Audience': audience,
                'Tenant': tenant,
            }
        }
        grant.create(event, {}, MagicMock())
        grant.update(event, {}, MagicMock())
    except Exception as error:
        print('test is failing')
        teardown_resources(
            provider=provider,
            client_id=client_id,
            api_id=api_id,
        )
        raise error

    teardown_resources(
            provider=provider,
            client_id=client_id,
            api_id=api_id,
        )

def teardown_resources(provider, client_id, api_id):
    """given client id and api id it will try to
    tear these things down"""
    if client_id:
        provider.delete_application(client_id)
    if api_id:
        provider.delete_api(api_id)
