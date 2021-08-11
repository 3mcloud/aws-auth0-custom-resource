"""Tests for utils/config"""
from unittest.mock import patch, MagicMock
from src.utils import config
from src.validation.application import tagsValidator

@patch('src.utils.config.PROVIDER')
def test_get_provider(provider, monkeypatch):
    """Test for get_provider"""
    env = 'qa'
    monkeypatch.setenv('ENVIRON', env)
    config.get_provider('my-tenant.auth0.com')
    # pylint: disable=no-member
    provider.assert_called_with(
        f'{config.MANAGEMENT_PREFIX}qa/auth0/tenant/my-tenant',
        'my-tenant.auth0.com'
    )

@patch('src.utils.config.cfn')
def test_set_tags(cfn):
    """test tags"""
    cfn.describe_stacks.return_value = {
        'Stacks': [
            {'Tags': []}
        ],
    }
    helper = MagicMock()
    helper.Data = {}
    event = {'ResourceProperties' : {}}
    config.set_tags(helper, event)
    assert helper.Data['tags'] == {}
    assert helper.Data['stack_tags'] == []

    cfn.describe_stacks.return_value = {
        'Stacks': [
            {'Tags': [
                {'Key': 'foo', 'Value': 'bar'}
            ]}
        ],
    }
    helper.Data = {}
    config.set_tags(helper, event)
    assert helper.Data['tags'] == {'foo': 'bar'}
    assert helper.Data['stack_tags'] == [{'Key': 'foo', 'Value': 'bar'}]

    event['ResourceProperties'] = {
        'AllowAdGroups': ['baz'],
    }
    helper.Data = {}
    config.set_tags(helper, event)
    assert helper.Data['tags'] == {'AllowAdGroups': ['baz'], 'foo': 'bar'}
    assert helper.Data['stack_tags'] == [{'Key': 'foo', 'Value': 'bar'}]

    validated = tagsValidator.validated(helper.Data['tags'])
    assert validated == {'AllowAdGroups': '["baz"]'}
