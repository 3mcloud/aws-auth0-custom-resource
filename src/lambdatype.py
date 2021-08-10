''' Note: this code is used only by the static type checker! '''
from typing import (
    Any,
    TypedDict,
)
# pylint: disable=too-few-public-methods
class LambdaDict(TypedDict):
    # pylint: disable=line-too-long
    '''
    Lambda event for custom resource
    See: https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/template-custom-resources.html
    '''
    RequestType: str
    ResponseURL: str
    StackId: str
    RequestId: str
    ResourceType: str
    LogicalResourceId: str
    ResourceProperties: Any
    PhysicalResourceId: str
    OldResourceProperties: Any

# pylint: disable=too-few-public-methods
class LambdaCognitoIdentity():
    '''
    Context type hints for lambda context
    '''
    cognito_identity_id: str
    cognito_identity_pool_id: str

# pylint: disable=too-few-public-methods
class LambdaClientContextMobileClient():
    '''
    Context type hints for lambda context
    '''
    installation_id: str
    app_title: str
    app_version_name: str
    app_version_code: str
    app_package_name: str

# pylint: disable=too-few-public-methods
class LambdaClientContext():
    '''
    Context type hints for lambda context
    '''
    client: LambdaClientContextMobileClient
    custom: LambdaDict
    env: LambdaDict

# pylint: disable=too-few-public-methods
class LambdaContext():
    '''
    Context type hints for lambda context
    '''
    function_name: str
    function_version: str
    invoked_function_arn: str
    memory_limit_in_mb: int
    aws_request_id: str
    log_group_name: str
    log_stream_name: str
    identity: LambdaCognitoIdentity
    client_context: LambdaClientContext

    @staticmethod
    def get_remaining_time_in_millis() -> int:
        '''mock the method for type hint'''
        return 0
