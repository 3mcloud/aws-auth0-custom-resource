"""Tests for utils/config"""
from unittest.mock import patch, MagicMock
import logging
import src.utils.config as config
from src.utils.config import PROVIDERS
from src.validation.application import tagsValidator


def test_set_logging_level():
    """Test for set_logging_level"""
    cases = {
        'CRITICAL': logging.CRITICAL,
        'ERROR': logging.ERROR,
        'WARNING': logging.WARN,
        'INFO': logging.INFO,
        'DEBUG': logging.DEBUG
    }
    logger = logging.getLogger()
    for level_str in cases:
        config.set_logging_level(logger, level_str)
        assert cases[level_str] == logger.getEffectiveLevel()


def test_get_provider(monkeypatch):
    """Test for get_provider"""
    env = 'qa'
    provider = 'auth0'
    monkeypatch.setenv('ENVIRON', env)
    monkeypatch.setenv('AUTH_PROVIDER', provider)
    with patch.dict(PROVIDERS, {'auth0': MagicMock()}, clear=True):
        config.get_provider('mmm-id.auth0.com')
        # pylint: disable=no-member
        PROVIDERS[provider].assert_called_with(
            f'{config.MANAGEMENT_PREFIX}qa/auth0/tenant/mmm-id',
            'mmm-id.auth0.com'
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
