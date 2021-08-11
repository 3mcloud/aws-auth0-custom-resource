"""
Holds lists of different types of events
"""

# pylint: disable=line-too-long
def get(ids = False):
    """holds different stack events"""
    cases = [{
        "name": "new_stack_create_failed",
        "success": False,
        "StackEvents": [
            {
                "StackId": "arn:aws:cloudformation:us-east-1:123456789012:stack/qa-cr-authn-failures/fe7f9cb0-1474-11eb-aa91-12cf4a8c2bc2",
                "EventId": "1ca95280-1475-11eb-b0ad-0a374cd00e27",
                "StackName": "qa-cr-authn-failures",
                "LogicalResourceId": "qa-cr-authn-failures",
                "PhysicalResourceId": "arn:aws:cloudformation:us-east-1:123456789012:stack/qa-cr-authn-failures/fe7f9cb0-1474-11eb-aa91-12cf4a8c2bc2",
                "ResourceType": "AWS::CloudFormation::Stack",
                "Timestamp": "2020-10-22T14:44:38.938Z",
                "ResourceStatus": "DELETE_COMPLETE"
            },
            {
                "StackId": "arn:aws:cloudformation:us-east-1:123456789012:stack/qa-cr-authn-failures/fe7f9cb0-1474-11eb-aa91-12cf4a8c2bc2",
                "EventId": "AuthApplication-DELETE_COMPLETE-2020-10-22T14:44:38.097Z",
                "StackName": "qa-cr-authn-failures",
                "LogicalResourceId": "AuthApplication",
                "PhysicalResourceId": "/qa/auth0/authncrregression123456789012",
                "ResourceType": "Custom::Authn_Application",
                "Timestamp": "2020-10-22T14:44:38.097Z",
                "ResourceStatus": "DELETE_COMPLETE",
                "ResourceProperties": "{\"ServiceToken\":\"arn:aws:lambda:us-east-1:123456789012:function:qa-auth-custom-resource\",\"Connections\":[\"con_k4Jtslc6jOQq1rYy\"],\"Type\":\"m2m\",\"Tenant\":\"mmm-qa.auth0.com\",\"Description\":\"A failure to ensure resources aren't orphaned\",\"Name\":\"authn-cr-regression-123456789012\"}"
            },
            {
                "StackId": "arn:aws:cloudformation:us-east-1:123456789012:stack/qa-cr-authn-failures/fe7f9cb0-1474-11eb-aa91-12cf4a8c2bc2",
                "EventId": "AuthApplication-DELETE_IN_PROGRESS-2020-10-22T14:44:35.468Z",
                "StackName": "qa-cr-authn-failures",
                "LogicalResourceId": "AuthApplication",
                "PhysicalResourceId": "/qa/auth0/authncrregression123456789012",
                "ResourceType": "Custom::Authn_Application",
                "Timestamp": "2020-10-22T14:44:35.468Z",
                "ResourceStatus": "DELETE_IN_PROGRESS",
                "ResourceProperties": "{\"ServiceToken\":\"arn:aws:lambda:us-east-1:123456789012:function:qa-auth-custom-resource\",\"Connections\":[\"con_k4Jtslc6jOQq1rYy\"],\"Type\":\"m2m\",\"Tenant\":\"mmm-qa.auth0.com\",\"Description\":\"A failure to ensure resources aren't orphaned\",\"Name\":\"authn-cr-regression-123456789012\"}"
            },
            {
                "StackId": "arn:aws:cloudformation:us-east-1:123456789012:stack/qa-cr-authn-failures/fe7f9cb0-1474-11eb-aa91-12cf4a8c2bc2",
                "EventId": "AuthGrant-DELETE_COMPLETE-2020-10-22T14:44:34.796Z",
                "StackName": "qa-cr-authn-failures",
                "LogicalResourceId": "AuthGrant",
                "PhysicalResourceId": "qa-cr-authn-failures_AuthGrant_WY13MI00",
                "ResourceType": "Custom::Authn_Grant",
                "Timestamp": "2020-10-22T14:44:34.796Z",
                "ResourceStatus": "DELETE_COMPLETE",
                "ResourceProperties": "{\"ServiceToken\":\"arn:aws:lambda:us-east-1:123456789012:function:qa-auth-custom-resource\",\"Tenant\":\"mmm-qa.auth0.com\",\"Audience\":\"https://authn-cr-failure.com\",\"ApplicationId\":\"hmODjO7fRD1rguDAdjcyf67bRZqDu0jF\"}"
            },
            {
                "StackId": "arn:aws:cloudformation:us-east-1:123456789012:stack/qa-cr-authn-failures/fe7f9cb0-1474-11eb-aa91-12cf4a8c2bc2",
                "EventId": "AuthGrant-DELETE_IN_PROGRESS-2020-10-22T14:44:31.962Z",
                "StackName": "qa-cr-authn-failures",
                "LogicalResourceId": "AuthGrant",
                "PhysicalResourceId": "qa-cr-authn-failures_AuthGrant_WY13MI00",
                "ResourceType": "Custom::Authn_Grant",
                "Timestamp": "2020-10-22T14:44:31.962Z",
                "ResourceStatus": "DELETE_IN_PROGRESS",
                "ResourceProperties": "{\"ServiceToken\":\"arn:aws:lambda:us-east-1:123456789012:function:qa-auth-custom-resource\",\"Tenant\":\"mmm-qa.auth0.com\",\"Audience\":\"https://authn-cr-failure.com\",\"ApplicationId\":\"hmODjO7fRD1rguDAdjcyf67bRZqDu0jF\"}"
            },
            {
                "StackId": "arn:aws:cloudformation:us-east-1:123456789012:stack/qa-cr-authn-failures/fe7f9cb0-1474-11eb-aa91-12cf4a8c2bc2",
                "EventId": "09413690-1475-11eb-a91a-0a91287fb5a1",
                "StackName": "qa-cr-authn-failures",
                "LogicalResourceId": "qa-cr-authn-failures",
                "PhysicalResourceId": "arn:aws:cloudformation:us-east-1:123456789012:stack/qa-cr-authn-failures/fe7f9cb0-1474-11eb-aa91-12cf4a8c2bc2",
                "ResourceType": "AWS::CloudFormation::Stack",
                "Timestamp": "2020-10-22T14:44:06.386Z",
                "ResourceStatus": "DELETE_IN_PROGRESS",
                "ResourceStatusReason": "The following resource(s) failed to create: [AuthGrant]. . Delete requested by user."
            },
            {
                "StackId": "arn:aws:cloudformation:us-east-1:123456789012:stack/qa-cr-authn-failures/fe7f9cb0-1474-11eb-aa91-12cf4a8c2bc2",
                "EventId": "AuthGrant-CREATE_FAILED-2020-10-22T14:44:05.641Z",
                "StackName": "qa-cr-authn-failures",
                "LogicalResourceId": "AuthGrant",
                "PhysicalResourceId": "qa-cr-authn-failures_AuthGrant_WY13MI00",
                "ResourceType": "Custom::Authn_Grant",
                "Timestamp": "2020-10-22T14:44:05.641Z",
                "ResourceStatus": "CREATE_FAILED",
                "ResourceStatusReason": "Failed to create resource. 404: No resource with identifier https://authn-cr-failure.com",
                "ResourceProperties": "{\"ServiceToken\":\"arn:aws:lambda:us-east-1:123456789012:function:qa-auth-custom-resource\",\"Tenant\":\"mmm-qa.auth0.com\",\"Audience\":\"https://authn-cr-failure.com\",\"ApplicationId\":\"hmODjO7fRD1rguDAdjcyf67bRZqDu0jF\"}"
            },
            {
                "StackId": "arn:aws:cloudformation:us-east-1:123456789012:stack/qa-cr-authn-failures/fe7f9cb0-1474-11eb-aa91-12cf4a8c2bc2",
                "EventId": "AuthGrant-CREATE_IN_PROGRESS-2020-10-22T14:44:05.495Z",
                "StackName": "qa-cr-authn-failures",
                "LogicalResourceId": "AuthGrant",
                "PhysicalResourceId": "qa-cr-authn-failures_AuthGrant_WY13MI00",
                "ResourceType": "Custom::Authn_Grant",
                "Timestamp": "2020-10-22T14:44:05.495Z",
                "ResourceStatus": "CREATE_IN_PROGRESS",
                "ResourceStatusReason": "Resource creation Initiated",
                "ResourceProperties": "{\"ServiceToken\":\"arn:aws:lambda:us-east-1:123456789012:function:qa-auth-custom-resource\",\"Tenant\":\"mmm-qa.auth0.com\",\"Audience\":\"https://authn-cr-failure.com\",\"ApplicationId\":\"hmODjO7fRD1rguDAdjcyf67bRZqDu0jF\"}"
            },
            {
                "StackId": "arn:aws:cloudformation:us-east-1:123456789012:stack/qa-cr-authn-failures/fe7f9cb0-1474-11eb-aa91-12cf4a8c2bc2",
                "EventId": "AuthGrant-CREATE_IN_PROGRESS-2020-10-22T14:44:01.330Z",
                "StackName": "qa-cr-authn-failures",
                "LogicalResourceId": "AuthGrant",
                "PhysicalResourceId": "",
                "ResourceType": "Custom::Authn_Grant",
                "Timestamp": "2020-10-22T14:44:01.330Z",
                "ResourceStatus": "CREATE_IN_PROGRESS",
                "ResourceProperties": "{\"ServiceToken\":\"arn:aws:lambda:us-east-1:123456789012:function:qa-auth-custom-resource\",\"Tenant\":\"mmm-qa.auth0.com\",\"Audience\":\"https://authn-cr-failure.com\",\"ApplicationId\":\"hmODjO7fRD1rguDAdjcyf67bRZqDu0jF\"}"
            },
            {
                "StackId": "arn:aws:cloudformation:us-east-1:123456789012:stack/qa-cr-authn-failures/fe7f9cb0-1474-11eb-aa91-12cf4a8c2bc2",
                "EventId": "AuthApplication-CREATE_COMPLETE-2020-10-22T14:43:59.095Z",
                "StackName": "qa-cr-authn-failures",
                "LogicalResourceId": "AuthApplication",
                "PhysicalResourceId": "/qa/auth0/authncrregression123456789012",
                "ResourceType": "Custom::Authn_Application",
                "Timestamp": "2020-10-22T14:43:59.095Z",
                "ResourceStatus": "CREATE_COMPLETE",
                "ResourceProperties": "{\"ServiceToken\":\"arn:aws:lambda:us-east-1:123456789012:function:qa-auth-custom-resource\",\"Connections\":[\"con_k4Jtslc6jOQq1rYy\"],\"Type\":\"m2m\",\"Tenant\":\"mmm-qa.auth0.com\",\"Description\":\"A failure to ensure resources aren't orphaned\",\"Name\":\"authn-cr-regression-123456789012\"}"
            },
            {
                "StackId": "arn:aws:cloudformation:us-east-1:123456789012:stack/qa-cr-authn-failures/fe7f9cb0-1474-11eb-aa91-12cf4a8c2bc2",
                "EventId": "AuthApplication-CREATE_IN_PROGRESS-2020-10-22T14:43:58.739Z",
                "StackName": "qa-cr-authn-failures",
                "LogicalResourceId": "AuthApplication",
                "PhysicalResourceId": "/qa/auth0/authncrregression123456789012",
                "ResourceType": "Custom::Authn_Application",
                "Timestamp": "2020-10-22T14:43:58.739Z",
                "ResourceStatus": "CREATE_IN_PROGRESS",
                "ResourceStatusReason": "Resource creation Initiated",
                "ResourceProperties": "{\"ServiceToken\":\"arn:aws:lambda:us-east-1:123456789012:function:qa-auth-custom-resource\",\"Connections\":[\"con_k4Jtslc6jOQq1rYy\"],\"Type\":\"m2m\",\"Tenant\":\"mmm-qa.auth0.com\",\"Description\":\"A failure to ensure resources aren't orphaned\",\"Name\":\"authn-cr-regression-123456789012\"}"
            },
            {
                "StackId": "arn:aws:cloudformation:us-east-1:123456789012:stack/qa-cr-authn-failures/fe7f9cb0-1474-11eb-aa91-12cf4a8c2bc2",
                "EventId": "AuthApplication-CREATE_IN_PROGRESS-2020-10-22T14:43:52.855Z",
                "StackName": "qa-cr-authn-failures",
                "LogicalResourceId": "AuthApplication",
                "PhysicalResourceId": "",
                "ResourceType": "Custom::Authn_Application",
                "Timestamp": "2020-10-22T14:43:52.855Z",
                "ResourceStatus": "CREATE_IN_PROGRESS",
                "ResourceProperties": "{\"ServiceToken\":\"arn:aws:lambda:us-east-1:123456789012:function:qa-auth-custom-resource\",\"Connections\":[\"con_k4Jtslc6jOQq1rYy\"],\"Type\":\"m2m\",\"Tenant\":\"mmm-qa.auth0.com\",\"Description\":\"A failure to ensure resources aren't orphaned\",\"Name\":\"authn-cr-regression-123456789012\"}"
            },
            {
                "StackId": "arn:aws:cloudformation:us-east-1:123456789012:stack/qa-cr-authn-failures/fe7f9cb0-1474-11eb-aa91-12cf4a8c2bc2",
                "EventId": "fe8457a0-1474-11eb-aa91-12cf4a8c2bc2",
                "StackName": "qa-cr-authn-failures",
                "LogicalResourceId": "qa-cr-authn-failures",
                "PhysicalResourceId": "arn:aws:cloudformation:us-east-1:123456789012:stack/qa-cr-authn-failures/fe7f9cb0-1474-11eb-aa91-12cf4a8c2bc2",
                "ResourceType": "AWS::CloudFormation::Stack",
                "Timestamp": "2020-10-22T14:43:48.518Z",
                "ResourceStatus": "CREATE_IN_PROGRESS",
                "ResourceStatusReason": "User Initiated"
            }
        ]
    },{
        "name": "create_success",
        "success": True,
        "StackEvents": [
            {
                "StackId": "arn:aws:cloudformation:us-east-1:123456789012:stack/qa-cr-authn-failures/e289fa60-1473-11eb-80df-0e765a9edd1f",
                "EventId": "ed70f690-1473-11eb-97a1-0a0faac5843d",
                "StackName": "qa-cr-authn-failures",
                "LogicalResourceId": "qa-cr-authn-failures",
                "PhysicalResourceId": "arn:aws:cloudformation:us-east-1:123456789012:stack/qa-cr-authn-failures/e289fa60-1473-11eb-80df-0e765a9edd1f",
                "ResourceType": "AWS::CloudFormation::Stack",
                "Timestamp": "2020-10-22T14:36:10.223Z",
                "ResourceStatus": "CREATE_COMPLETE"
            },
            {
                "StackId": "arn:aws:cloudformation:us-east-1:123456789012:stack/qa-cr-authn-failures/e289fa60-1473-11eb-80df-0e765a9edd1f",
                "EventId": "AuthGrant-CREATE_COMPLETE-2020-10-22T14:36:08.961Z",
                "StackName": "qa-cr-authn-failures",
                "LogicalResourceId": "AuthGrant",
                "PhysicalResourceId": "cgr_zKPHy4Lwx2pxE1Ym",
                "ResourceType": "Custom::Authn_Grant",
                "Timestamp": "2020-10-22T14:36:08.961Z",
                "ResourceStatus": "CREATE_COMPLETE",
                "ResourceProperties": "{\"ServiceToken\":\"arn:aws:lambda:us-east-1:123456789012:function:qa-auth-custom-resource\",\"Tenant\":\"mmm-qa.auth0.com\",\"Audience\":\"https://authn-cr-failure.com\",\"ApplicationId\":\"QNFneHk2WMyjYuWtUvl21xspV0ZxM9Ba\"}"
            },
            {
                "StackId": "arn:aws:cloudformation:us-east-1:123456789012:stack/qa-cr-authn-failures/e289fa60-1473-11eb-80df-0e765a9edd1f",
                "EventId": "AuthGrant-CREATE_IN_PROGRESS-2020-10-22T14:36:08.669Z",
                "StackName": "qa-cr-authn-failures",
                "LogicalResourceId": "AuthGrant",
                "PhysicalResourceId": "cgr_zKPHy4Lwx2pxE1Ym",
                "ResourceType": "Custom::Authn_Grant",
                "Timestamp": "2020-10-22T14:36:08.669Z",
                "ResourceStatus": "CREATE_IN_PROGRESS",
                "ResourceStatusReason": "Resource creation Initiated",
                "ResourceProperties": "{\"ServiceToken\":\"arn:aws:lambda:us-east-1:123456789012:function:qa-auth-custom-resource\",\"Tenant\":\"mmm-qa.auth0.com\",\"Audience\":\"https://authn-cr-failure.com\",\"ApplicationId\":\"QNFneHk2WMyjYuWtUvl21xspV0ZxM9Ba\"}"
            },
            {
                "StackId": "arn:aws:cloudformation:us-east-1:123456789012:stack/qa-cr-authn-failures/e289fa60-1473-11eb-80df-0e765a9edd1f",
                "EventId": "AuthGrant-CREATE_IN_PROGRESS-2020-10-22T14:36:04.804Z",
                "StackName": "qa-cr-authn-failures",
                "LogicalResourceId": "AuthGrant",
                "PhysicalResourceId": "",
                "ResourceType": "Custom::Authn_Grant",
                "Timestamp": "2020-10-22T14:36:04.804Z",
                "ResourceStatus": "CREATE_IN_PROGRESS",
                "ResourceProperties": "{\"ServiceToken\":\"arn:aws:lambda:us-east-1:123456789012:function:qa-auth-custom-resource\",\"Tenant\":\"mmm-qa.auth0.com\",\"Audience\":\"https://authn-cr-failure.com\",\"ApplicationId\":\"QNFneHk2WMyjYuWtUvl21xspV0ZxM9Ba\"}"
            },
            {
                "StackId": "arn:aws:cloudformation:us-east-1:123456789012:stack/qa-cr-authn-failures/e289fa60-1473-11eb-80df-0e765a9edd1f",
                "EventId": "AuthApplication-CREATE_COMPLETE-2020-10-22T14:36:02.350Z",
                "StackName": "qa-cr-authn-failures",
                "LogicalResourceId": "AuthApplication",
                "PhysicalResourceId": "/qa/auth0/authncrregression123456789012",
                "ResourceType": "Custom::Authn_Application",
                "Timestamp": "2020-10-22T14:36:02.350Z",
                "ResourceStatus": "CREATE_COMPLETE",
                "ResourceProperties": "{\"ServiceToken\":\"arn:aws:lambda:us-east-1:123456789012:function:qa-auth-custom-resource\",\"Connections\":[\"con_k4Jtslc6jOQq1rYy\"],\"Type\":\"m2m\",\"Tenant\":\"mmm-qa.auth0.com\",\"Description\":\"A failure to ensure resources aren't orphaned\",\"Name\":\"authn-cr-regression-123456789012\"}"
            },
            {
                "StackId": "arn:aws:cloudformation:us-east-1:123456789012:stack/qa-cr-authn-failures/e289fa60-1473-11eb-80df-0e765a9edd1f",
                "EventId": "AuthApplication-CREATE_IN_PROGRESS-2020-10-22T14:36:01.990Z",
                "StackName": "qa-cr-authn-failures",
                "LogicalResourceId": "AuthApplication",
                "PhysicalResourceId": "/qa/auth0/authncrregression123456789012",
                "ResourceType": "Custom::Authn_Application",
                "Timestamp": "2020-10-22T14:36:01.990Z",
                "ResourceStatus": "CREATE_IN_PROGRESS",
                "ResourceStatusReason": "Resource creation Initiated",
                "ResourceProperties": "{\"ServiceToken\":\"arn:aws:lambda:us-east-1:123456789012:function:qa-auth-custom-resource\",\"Connections\":[\"con_k4Jtslc6jOQq1rYy\"],\"Type\":\"m2m\",\"Tenant\":\"mmm-qa.auth0.com\",\"Description\":\"A failure to ensure resources aren't orphaned\",\"Name\":\"authn-cr-regression-123456789012\"}"
            },
            {
                "StackId": "arn:aws:cloudformation:us-east-1:123456789012:stack/qa-cr-authn-failures/e289fa60-1473-11eb-80df-0e765a9edd1f",
                "EventId": "AuthAPI-CREATE_COMPLETE-2020-10-22T14:36:00.974Z",
                "StackName": "qa-cr-authn-failures",
                "LogicalResourceId": "AuthAPI",
                "PhysicalResourceId": "5f9198cecfc1ff003e0dcd6c",
                "ResourceType": "Custom::Authn_Api",
                "Timestamp": "2020-10-22T14:36:00.974Z",
                "ResourceStatus": "CREATE_COMPLETE",
                "ResourceProperties": "{\"ServiceToken\":\"arn:aws:lambda:us-east-1:123456789012:function:qa-auth-custom-resource\",\"Tenant\":\"mmm-qa.auth0.com\",\"Audience\":\"https://authn-cr-failure.com\",\"Name\":\"authn-cr-regression-api-123456789012\"}"
            },
            {
                "StackId": "arn:aws:cloudformation:us-east-1:123456789012:stack/qa-cr-authn-failures/e289fa60-1473-11eb-80df-0e765a9edd1f",
                "EventId": "AuthAPI-CREATE_IN_PROGRESS-2020-10-22T14:36:00.268Z",
                "StackName": "qa-cr-authn-failures",
                "LogicalResourceId": "AuthAPI",
                "PhysicalResourceId": "5f9198cecfc1ff003e0dcd6c",
                "ResourceType": "Custom::Authn_Api",
                "Timestamp": "2020-10-22T14:36:00.268Z",
                "ResourceStatus": "CREATE_IN_PROGRESS",
                "ResourceStatusReason": "Resource creation Initiated",
                "ResourceProperties": "{\"ServiceToken\":\"arn:aws:lambda:us-east-1:123456789012:function:qa-auth-custom-resource\",\"Tenant\":\"mmm-qa.auth0.com\",\"Audience\":\"https://authn-cr-failure.com\",\"Name\":\"authn-cr-regression-api-123456789012\"}"
            },
            {
                "StackId": "arn:aws:cloudformation:us-east-1:123456789012:stack/qa-cr-authn-failures/e289fa60-1473-11eb-80df-0e765a9edd1f",
                "EventId": "AuthApplication-CREATE_IN_PROGRESS-2020-10-22T14:35:56.779Z",
                "StackName": "qa-cr-authn-failures",
                "LogicalResourceId": "AuthApplication",
                "PhysicalResourceId": "",
                "ResourceType": "Custom::Authn_Application",
                "Timestamp": "2020-10-22T14:35:56.779Z",
                "ResourceStatus": "CREATE_IN_PROGRESS",
                "ResourceProperties": "{\"ServiceToken\":\"arn:aws:lambda:us-east-1:123456789012:function:qa-auth-custom-resource\",\"Connections\":[\"con_k4Jtslc6jOQq1rYy\"],\"Type\":\"m2m\",\"Tenant\":\"mmm-qa.auth0.com\",\"Description\":\"A failure to ensure resources aren't orphaned\",\"Name\":\"authn-cr-regression-123456789012\"}"
            },
            {
                "StackId": "arn:aws:cloudformation:us-east-1:123456789012:stack/qa-cr-authn-failures/e289fa60-1473-11eb-80df-0e765a9edd1f",
                "EventId": "AuthAPI-CREATE_IN_PROGRESS-2020-10-22T14:35:56.291Z",
                "StackName": "qa-cr-authn-failures",
                "LogicalResourceId": "AuthAPI",
                "PhysicalResourceId": "",
                "ResourceType": "Custom::Authn_Api",
                "Timestamp": "2020-10-22T14:35:56.291Z",
                "ResourceStatus": "CREATE_IN_PROGRESS",
                "ResourceProperties": "{\"ServiceToken\":\"arn:aws:lambda:us-east-1:123456789012:function:qa-auth-custom-resource\",\"Tenant\":\"mmm-qa.auth0.com\",\"Audience\":\"https://authn-cr-failure.com\",\"Name\":\"authn-cr-regression-api-123456789012\"}"
            },
            {
                "StackId": "arn:aws:cloudformation:us-east-1:123456789012:stack/qa-cr-authn-failures/e289fa60-1473-11eb-80df-0e765a9edd1f",
                "EventId": "e28c1d40-1473-11eb-80df-0e765a9edd1f",
                "StackName": "qa-cr-authn-failures",
                "LogicalResourceId": "qa-cr-authn-failures",
                "PhysicalResourceId": "arn:aws:cloudformation:us-east-1:123456789012:stack/qa-cr-authn-failures/e289fa60-1473-11eb-80df-0e765a9edd1f",
                "ResourceType": "AWS::CloudFormation::Stack",
                "Timestamp": "2020-10-22T14:35:52.018Z",
                "ResourceStatus": "CREATE_IN_PROGRESS",
                "ResourceStatusReason": "User Initiated"
            }
        ]
    },{
        "name": "stack_update_create_rollback_then_update",
        "success": False,
        "StackEvents": [
            {
                "StackId": "arn:aws:cloudformation:us-east-1:123456789012:stack/qa-cr-authn-failures/82f87f80-148d-11eb-a522-0ea47a628cf7",
                "EventId": "d41285a0-148d-11eb-8203-0a4db9a5d67f",
                "StackName": "qa-cr-authn-failures",
                "LogicalResourceId": "qa-cr-authn-failures",
                "PhysicalResourceId": "arn:aws:cloudformation:us-east-1:123456789012:stack/qa-cr-authn-failures/82f87f80-148d-11eb-a522-0ea47a628cf7",
                "ResourceType": "AWS::CloudFormation::Stack",
                "Timestamp": "2020-10-22T17:41:34.575Z",
                "ResourceStatus": "UPDATE_ROLLBACK_COMPLETE"
            },
            {
                "StackId": "arn:aws:cloudformation:us-east-1:123456789012:stack/qa-cr-authn-failures/82f87f80-148d-11eb-a522-0ea47a628cf7",
                "EventId": "AuthApplication-f2e905ef-c14d-40c4-bd1f-29b18d9de9d3",
                "StackName": "qa-cr-authn-failures",
                "LogicalResourceId": "AuthApplication",
                "PhysicalResourceId": "/qa/auth0/authncrregression123456789012",
                "ResourceType": "AWS::CloudFormation::CustomResource",
                "Timestamp": "2020-10-22T17:41:34.241Z",
                "ResourceStatus": "DELETE_COMPLETE"
            },
            {
                "StackId": "arn:aws:cloudformation:us-east-1:123456789012:stack/qa-cr-authn-failures/82f87f80-148d-11eb-a522-0ea47a628cf7",
                "EventId": "AuthApplication-1506e172-e8cb-4fb9-bc23-ae2608f78549",
                "StackName": "qa-cr-authn-failures",
                "LogicalResourceId": "AuthApplication",
                "PhysicalResourceId": "/qa/auth0/authncrregression123456789012",
                "ResourceType": "AWS::CloudFormation::CustomResource",
                "Timestamp": "2020-10-22T17:41:31.331Z",
                "ResourceStatus": "DELETE_IN_PROGRESS"
            },
            {
                "StackId": "arn:aws:cloudformation:us-east-1:123456789012:stack/qa-cr-authn-failures/82f87f80-148d-11eb-a522-0ea47a628cf7",
                "EventId": "AuthGrant-eb8fd3e8-ea4f-4180-a7d4-dad33ceeb9c2",
                "StackName": "qa-cr-authn-failures",
                "LogicalResourceId": "AuthGrant",
                "PhysicalResourceId": "qa-cr-authn-failures_AuthGrant_721I7XY7",
                "ResourceType": "AWS::CloudFormation::CustomResource",
                "Timestamp": "2020-10-22T17:41:30.436Z",
                "ResourceStatus": "DELETE_COMPLETE"
            },
            {
                "StackId": "arn:aws:cloudformation:us-east-1:123456789012:stack/qa-cr-authn-failures/82f87f80-148d-11eb-a522-0ea47a628cf7",
                "EventId": "AuthGrant-49ffcb53-da68-420b-bc52-eea3b6eefca6",
                "StackName": "qa-cr-authn-failures",
                "LogicalResourceId": "AuthGrant",
                "PhysicalResourceId": "qa-cr-authn-failures_AuthGrant_721I7XY7",
                "ResourceType": "AWS::CloudFormation::CustomResource",
                "Timestamp": "2020-10-22T17:41:28.076Z",
                "ResourceStatus": "DELETE_IN_PROGRESS"
            },
            {
                "StackId": "arn:aws:cloudformation:us-east-1:123456789012:stack/qa-cr-authn-failures/82f87f80-148d-11eb-a522-0ea47a628cf7",
                "EventId": "cf5c5090-148d-11eb-bb65-0e29088293c9",
                "StackName": "qa-cr-authn-failures",
                "LogicalResourceId": "qa-cr-authn-failures",
                "PhysicalResourceId": "arn:aws:cloudformation:us-east-1:123456789012:stack/qa-cr-authn-failures/82f87f80-148d-11eb-a522-0ea47a628cf7",
                "ResourceType": "AWS::CloudFormation::Stack",
                "Timestamp": "2020-10-22T17:41:26.669Z",
                "ResourceStatus": "UPDATE_ROLLBACK_COMPLETE_CLEANUP_IN_PROGRESS"
            },
            {
                "StackId": "arn:aws:cloudformation:us-east-1:123456789012:stack/qa-cr-authn-failures/82f87f80-148d-11eb-a522-0ea47a628cf7",
                "EventId": "bf0a9c60-148d-11eb-9cb5-0ac97ebd7097",
                "StackName": "qa-cr-authn-failures",
                "LogicalResourceId": "qa-cr-authn-failures",
                "PhysicalResourceId": "arn:aws:cloudformation:us-east-1:123456789012:stack/qa-cr-authn-failures/82f87f80-148d-11eb-a522-0ea47a628cf7",
                "ResourceType": "AWS::CloudFormation::Stack",
                "Timestamp": "2020-10-22T17:40:59.276Z",
                "ResourceStatus": "UPDATE_ROLLBACK_IN_PROGRESS",
                "ResourceStatusReason": "The following resource(s) failed to create: [AuthGrant]. "
            },
            {
                "StackId": "arn:aws:cloudformation:us-east-1:123456789012:stack/qa-cr-authn-failures/82f87f80-148d-11eb-a522-0ea47a628cf7",
                "EventId": "AuthGrant-CREATE_FAILED-2020-10-22T17:40:58.114Z",
                "StackName": "qa-cr-authn-failures",
                "LogicalResourceId": "AuthGrant",
                "PhysicalResourceId": "qa-cr-authn-failures_AuthGrant_721I7XY7",
                "ResourceType": "Custom::Authn_Grant",
                "Timestamp": "2020-10-22T17:40:58.114Z",
                "ResourceStatus": "CREATE_FAILED",
                "ResourceStatusReason": "Failed to create resource. 404: No resource with identifier https://authn-cr-failure.com",
                "ResourceProperties": "{\"ServiceToken\":\"arn:aws:lambda:us-east-1:123456789012:function:qa-auth-custom-resource\",\"Tenant\":\"mmm-qa.auth0.com\",\"Audience\":\"https://authn-cr-failure.com\",\"ApplicationId\":\"bD802jihR56shFVTpgA8uznIu8s5fKaI\"}"
            },
            {
                "StackId": "arn:aws:cloudformation:us-east-1:123456789012:stack/qa-cr-authn-failures/82f87f80-148d-11eb-a522-0ea47a628cf7",
                "EventId": "AuthGrant-CREATE_IN_PROGRESS-2020-10-22T17:40:57.958Z",
                "StackName": "qa-cr-authn-failures",
                "LogicalResourceId": "AuthGrant",
                "PhysicalResourceId": "qa-cr-authn-failures_AuthGrant_721I7XY7",
                "ResourceType": "Custom::Authn_Grant",
                "Timestamp": "2020-10-22T17:40:57.958Z",
                "ResourceStatus": "CREATE_IN_PROGRESS",
                "ResourceStatusReason": "Resource creation Initiated",
                "ResourceProperties": "{\"ServiceToken\":\"arn:aws:lambda:us-east-1:123456789012:function:qa-auth-custom-resource\",\"Tenant\":\"mmm-qa.auth0.com\",\"Audience\":\"https://authn-cr-failure.com\",\"ApplicationId\":\"bD802jihR56shFVTpgA8uznIu8s5fKaI\"}"
            },
            {
                "StackId": "arn:aws:cloudformation:us-east-1:123456789012:stack/qa-cr-authn-failures/82f87f80-148d-11eb-a522-0ea47a628cf7",
                "EventId": "AuthGrant-CREATE_IN_PROGRESS-2020-10-22T17:40:53.735Z",
                "StackName": "qa-cr-authn-failures",
                "LogicalResourceId": "AuthGrant",
                "PhysicalResourceId": "",
                "ResourceType": "Custom::Authn_Grant",
                "Timestamp": "2020-10-22T17:40:53.735Z",
                "ResourceStatus": "CREATE_IN_PROGRESS",
                "ResourceProperties": "{\"ServiceToken\":\"arn:aws:lambda:us-east-1:123456789012:function:qa-auth-custom-resource\",\"Tenant\":\"mmm-qa.auth0.com\",\"Audience\":\"https://authn-cr-failure.com\",\"ApplicationId\":\"bD802jihR56shFVTpgA8uznIu8s5fKaI\"}"
            },
            {
                "StackId": "arn:aws:cloudformation:us-east-1:123456789012:stack/qa-cr-authn-failures/82f87f80-148d-11eb-a522-0ea47a628cf7",
                "EventId": "AuthApplication-CREATE_COMPLETE-2020-10-22T17:40:51.431Z",
                "StackName": "qa-cr-authn-failures",
                "LogicalResourceId": "AuthApplication",
                "PhysicalResourceId": "/qa/auth0/authncrregression123456789012",
                "ResourceType": "Custom::Authn_Application",
                "Timestamp": "2020-10-22T17:40:51.431Z",
                "ResourceStatus": "CREATE_COMPLETE",
                "ResourceProperties": "{\"ServiceToken\":\"arn:aws:lambda:us-east-1:123456789012:function:qa-auth-custom-resource\",\"Connections\":[\"con_k4Jtslc6jOQq1rYy\"],\"Type\":\"m2m\",\"Tenant\":\"mmm-qa.auth0.com\",\"Description\":\"A failure to ensure resources aren't orphaned\",\"Name\":\"authn-cr-regression-123456789012\"}"
            },
            {
                "StackId": "arn:aws:cloudformation:us-east-1:123456789012:stack/qa-cr-authn-failures/82f87f80-148d-11eb-a522-0ea47a628cf7",
                "EventId": "AuthApplication-CREATE_IN_PROGRESS-2020-10-22T17:40:51.089Z",
                "StackName": "qa-cr-authn-failures",
                "LogicalResourceId": "AuthApplication",
                "PhysicalResourceId": "/qa/auth0/authncrregression123456789012",
                "ResourceType": "Custom::Authn_Application",
                "Timestamp": "2020-10-22T17:40:51.089Z",
                "ResourceStatus": "CREATE_IN_PROGRESS",
                "ResourceStatusReason": "Resource creation Initiated",
                "ResourceProperties": "{\"ServiceToken\":\"arn:aws:lambda:us-east-1:123456789012:function:qa-auth-custom-resource\",\"Connections\":[\"con_k4Jtslc6jOQq1rYy\"],\"Type\":\"m2m\",\"Tenant\":\"mmm-qa.auth0.com\",\"Description\":\"A failure to ensure resources aren't orphaned\",\"Name\":\"authn-cr-regression-123456789012\"}"
            },
            {
                "StackId": "arn:aws:cloudformation:us-east-1:123456789012:stack/qa-cr-authn-failures/82f87f80-148d-11eb-a522-0ea47a628cf7",
                "EventId": "AuthApplication-CREATE_IN_PROGRESS-2020-10-22T17:40:44.568Z",
                "StackName": "qa-cr-authn-failures",
                "LogicalResourceId": "AuthApplication",
                "PhysicalResourceId": "",
                "ResourceType": "Custom::Authn_Application",
                "Timestamp": "2020-10-22T17:40:44.568Z",
                "ResourceStatus": "CREATE_IN_PROGRESS",
                "ResourceProperties": "{\"ServiceToken\":\"arn:aws:lambda:us-east-1:123456789012:function:qa-auth-custom-resource\",\"Connections\":[\"con_k4Jtslc6jOQq1rYy\"],\"Type\":\"m2m\",\"Tenant\":\"mmm-qa.auth0.com\",\"Description\":\"A failure to ensure resources aren't orphaned\",\"Name\":\"authn-cr-regression-123456789012\"}"
            },
            {
                "StackId": "arn:aws:cloudformation:us-east-1:123456789012:stack/qa-cr-authn-failures/82f87f80-148d-11eb-a522-0ea47a628cf7",
                "EventId": "b303d850-148d-11eb-9afa-0a73682547f5",
                "StackName": "qa-cr-authn-failures",
                "LogicalResourceId": "qa-cr-authn-failures",
                "PhysicalResourceId": "arn:aws:cloudformation:us-east-1:123456789012:stack/qa-cr-authn-failures/82f87f80-148d-11eb-a522-0ea47a628cf7",
                "ResourceType": "AWS::CloudFormation::Stack",
                "Timestamp": "2020-10-22T17:40:39.101Z",
                "ResourceStatus": "UPDATE_IN_PROGRESS",
                "ResourceStatusReason": "User Initiated"
            },
            {
                "StackId": "arn:aws:cloudformation:us-east-1:123456789012:stack/qa-cr-authn-failures/82f87f80-148d-11eb-a522-0ea47a628cf7",
                "EventId": "85137040-148d-11eb-bd1c-0a7162bf9a3d",
                "StackName": "qa-cr-authn-failures",
                "LogicalResourceId": "qa-cr-authn-failures",
                "PhysicalResourceId": "arn:aws:cloudformation:us-east-1:123456789012:stack/qa-cr-authn-failures/82f87f80-148d-11eb-a522-0ea47a628cf7",
                "ResourceType": "AWS::CloudFormation::Stack",
                "Timestamp": "2020-10-22T17:39:22.038Z",
                "ResourceStatus": "CREATE_COMPLETE"
            },
            {
                "StackId": "arn:aws:cloudformation:us-east-1:123456789012:stack/qa-cr-authn-failures/82f87f80-148d-11eb-a522-0ea47a628cf7",
                "EventId": "82fcec50-148d-11eb-a522-0ea47a628cf7",
                "StackName": "qa-cr-authn-failures",
                "LogicalResourceId": "qa-cr-authn-failures",
                "PhysicalResourceId": "arn:aws:cloudformation:us-east-1:123456789012:stack/qa-cr-authn-failures/82f87f80-148d-11eb-a522-0ea47a628cf7",
                "ResourceType": "AWS::CloudFormation::Stack",
                "Timestamp": "2020-10-22T17:39:18.624Z",
                "ResourceStatus": "CREATE_IN_PROGRESS",
                "ResourceStatusReason": "User Initiated"
            }
        ]
    }]
    if ids:
        return [case['name'] for case in cases]
    return cases
