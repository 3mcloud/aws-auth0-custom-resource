# API Gateway V2

Create an API Gateway V2 resource with JWT authorizer. This stack creates all the resources you
need to create a gateway with a custom domain using the aws-cr-authn custom resources with Auth0 to authenticate your application.

## Machine To Machine

The example creates a machine to machine application because it's easier for testing. However, if you want to use an SPA type app and allow users to authenticate you can. You would need to:

 - Create a front-end application to allow people to login
 - Get the JWT generated from their login and pass it to the API behind API gateway
 - Change the JWT authorizer in this app to use the SPA generated audience(s)
