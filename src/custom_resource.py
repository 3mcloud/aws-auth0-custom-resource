"""
Handler for a authentication custom resource. This custom resource will live
under the platform level visible to the user, and create apps for them.

Using this repo as reference arch: https://github.com/binxio/cfn-auth0-provider
"""
import os
import logging
from typing import Any
import boto3
from crhelper import CfnResource
from .lambdatype import LambdaDict, LambdaContext
from .utils import config
from . import application, api, grant

logger = logging.getLogger()  # pylint: disable=invalid-name
logger.setLevel(logging.INFO)  # set info level by default

# Setup the client
secrets_client = boto3.client('secretsmanager')  # pylint: disable=invalid-name
helper = CfnResource(  # pylint: disable=invalid-name
    json_logging=False,
    log_level='DEBUG',
    boto_level='CRITICAL',
    sleep_on_delete=120,
    polling_interval=2,
)

RESOURCES = {
    'Authn_Application': application,
    'Authn_Api': api,
    'Authn_Grant': grant,
}


def get_resource(event: LambdaDict) -> Any:
    """
    get_resource determines which type of
    resource is being invoked and returns that
    python file for execution
    """
    resource_type = event['ResourceType'].split(':')[-1]
    if resource_type not in RESOURCES:
        raise KeyError(
            '{} not a valid name in {}'.format(
                resource_type,
                ','.join(RESOURCES.keys())
            )
        )

    return RESOURCES[resource_type]


@helper.create
def create(event: LambdaDict, context: LambdaContext) -> str:
    """
    Optionally return an ID that will be used for the resource PhysicalResourceId,
    if None is returned an ID will be generated. If a poll_create function is defined
    return value is placed into the poll event as event['CrHelperData']['PhysicalResourceId']
    """
    logger.info('CREATE')
    logger.info(event)
    config.set_tags(helper, event)
    return get_resource(event).create(event, context, helper)


@helper.update
def update(event: LambdaDict, context: LambdaContext):
    """
    If the update resulted in a new resource being created, return an id for the new resource.
    CloudFormation will send a delete event with the old id when stack update completes
    """
    logger.info('UPDATE')
    logger.info(event)
    config.set_tags(helper, event)
    return get_resource(event).update(event, context, helper)


@helper.delete
def delete(event: LambdaDict, context: LambdaContext):
    """ Delete function """
    logger.info('DELETE')
    logger.info(event)
    return get_resource(event).delete(event, context, helper)


def poll_create(event: LambdaDict, context: LambdaContext):
    """poll create sets a delay in response for the create"""
    logger.info('POLL CREATE')
    logger.debug('poll event %s\ncontext: %s', event, context)
    try:
        client = boto3.client('cloudformation')
        events = client.describe_stack_events(
            StackName=event['StackId'],
            NextToken=event['RequestId'],
        )
        if stack_is_failing(events):
            logger.warning('Stack is in failing state, tearing down resource')
            event['PhysicalResourceId'] = event['CrHelperData']['PhysicalResourceId']
            delete(event, context)
    except Exception as err: # pylint: disable=broad-except
        logger.error(err)

    return event['CrHelperData']['PhysicalResourceId']

def stack_is_failing(events):
    """iterate stack events, determine if resource creation failed"""
    failed = False
    failure_modes = ('CREATE_FAILED', 'UPDATE_ROLLBACK_IN_PROGRESS')
    for event in events['StackEvents']:
        if event['ResourceStatus'] in failure_modes:
            failed = True
        if event.get('ResourceStatusReason') == "User Initiated":
            break
    return failed



def lambda_handler(event: LambdaDict, context: LambdaContext):
    """ Simply instantiates the cfn helper library """
    # Set up logging based on the LOGGING_LEVEL environment variable
    level_str = os.getenv('LOGGING_LEVEL', 'INFO')
    config.set_logging_level(logger, level_str)
    logger.debug('Event: %s', event)
    logger.debug('Context: %s', context)
    # Manually enable polling for create if the resource type not grant
    if event['RequestType'] == 'Create' and 'Authn_Grant' not in event['ResourceType']:
        helper._poll_create_func = poll_create # pylint: disable=protected-access
    helper(event, context)
