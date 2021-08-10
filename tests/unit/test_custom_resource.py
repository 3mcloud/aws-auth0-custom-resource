"""Unit tests for the lambda handler"""
from unittest.mock import patch, MagicMock as Mock
import pytest

from tests.unit.fixtures import stack_events
from src import custom_resource as index

@patch('src.custom_resource.CfnResource._send', Mock())
@patch('src.custom_resource.get_resource')
@patch('src.custom_resource.config')
def test_lambda_handler(_, resource):
    """Test for create events to the lambda handler"""
    new_message = 'new message'
    context = Mock()
    event = {
        'RequestType': 'Create',
        'ResponseURL': 's3::/fake/path',
        'StackId': 'arn:aws',
        'RequestId': 'foobar',
        'ResourceType': 'Custom::Authn_Api',
        'LogicalResourceId': 'foo',
        'ResourceProperties': {}
    }
    resource().create.return_value = new_message
    index.lambda_handler(event, context)

@patch('src.custom_resource.get_resource')
@patch('src.custom_resource.config')
def test_handler_create(_, resource):
    """Test for create events to the lambda handler"""
    new_message = 'new message'
    context = Mock()
    event = {
        'RequestType': 'Create',
        'ResourceType': 'Custom::Authn_Api',
        'ResourceProperties': {},
        'StackId': 'arn:aws',
    }
    resource().create.return_value = new_message
    res = index.create(event, context)

    assert res == new_message


@patch('src.custom_resource.get_resource')
@patch('src.custom_resource.config')
def test_handler_update(_, resource):
    """Test for update events to the lambda handler"""
    message = 'a message'
    new_message = 'new message'
    context = Mock()
    event = {
        'RequestType': 'Update',
        'ResourceProperties': {
            'Message': message
        }
    }
    resource().update.return_value = new_message
    res = index.update(event, context)

    assert res == new_message


@patch('src.custom_resource.get_resource')
@patch('src.custom_resource.config')
def test_handler_delete(_, resource):
    """Test for delete events to the lambda handler"""
    message = 'a message'
    new_message = 'new message'
    context = Mock()
    event = {
        'RequestType': 'Delete',
        'ResourceProperties': {
            'Message': message
        }
    }
    resource().delete.return_value = new_message
    res = index.delete(event, context)

    assert res == new_message


@patch('src.custom_resource.config', Mock())
def test_handler_invalid_type():
    """Test for invalid events to the lambda handler"""
    context = Mock()
    event = {
        'RequestType': 'Invalid',
        'ResourceProperties': {}
    }
    with pytest.raises(KeyError):
        index.create(event, context)

@patch('src.custom_resource.get_resource')
@patch('src.custom_resource.config')
def test_handler_error(_, resource):
    """Test for errors during handling of an event"""
    context = Mock()
    event = {
        'RequestType': 'Delete',
        'ResourceProperties': {}
    }
    resource().delete.side_effect = Exception('Delete failure')
    with pytest.raises(Exception):
        index.delete(event, context)

@pytest.mark.parametrize('event', stack_events.get(), ids=stack_events.get(True))
def test_stack_is_failing(event):
    """test events to see if stack is failing"""

    assert index.stack_is_failing(event) is not event["success"]
