# Auth Applications Custom Resource

A cloudformation custom resource for setting up an application and scoping it

## Usage

> This custom resource must exist in your account before you can use it. See how to [add to your account](#adding-to-your-account)

To create an auth resource, include the following in your cloudformation template:

### Create an API

```yaml
  AuthApi:
    Type: Custom::Authn_Api
    Properties:
      ServiceToken: !ImportValue pr-aws-cr-authn:LambdaArn
      Name: example-name
      Tenant: my-tenant.auth0.com
      Audience: https://example-url.com
```

### Create an Application

```yaml
  AuthApp:
    Type: Custom::Authn_Application
    DependsOn:
      - AuthApi # See why this is required below
    Properties:
      ServiceToken: !ImportValue pr-aws-cr-authn:LambdaArn
      Name: example-name
      Tenant: my-tenant.auth0.com
      Type: spa # (spa, m2m, web, native)
      Description: "My example"
```

### Associate the Application to the API

```yaml
  AuthGrant:
    Type: Custom::Authn_Grant
    Properties:
      ServiceToken: !ImportValue pr-aws-cr-authn:LambdaArn
      # Use the Audience return value from the AuthApi
      Audience: !GetAtt AuthApi.Audience
      Tenant: my-tenant.auth0.com
      # Use the ClientId return value from the AuthApp
      ApplicationId: !GetAtt AuthApp.ClientId
```

### Other properties

```yaml
    Provider: auth0 # optional (default auth0)
```

## Examples

See the [examples folder](examples/api).

### Warning

If you have more than one API or Application in your template, use `DependsOn` to make sure they do not execute in parallel. If one of them fails to create, the other will not properly delete in the CloudFormation rollback without this.

Also, make sure to use `!GetAtt` on your Application and API when creating a grant so that updating the Application or API also updates the grant.

### Managing An Application

The complete list of configurable properties for an application. For more information on what
these properties are you can refer to the [management API](https://auth0.com/docs/api/management/v2#!/Clients/get_clients) documentation or the Auth0 console if you have access.

```yaml
AuthResource:
  Type: Custom::Authn_Application
  Properties:
    ServiceToken: !ImportValue pr-aws-cr-authn:LambdaArn
    Name: example-name
    Tenant: my-tenant.auth0.com
    Type: spa # required (spa, m2m, web, native)
    Description: "" # required
    AllowAdGroups: [""] # list of AD groups that can generate tokens for your app

    # optional configuration below
    Connections: [""] # IDs of connections to enable such as Azure AD integration
    CallbackUrls: [""]
    LogoutUrls: [""]
    WebOrigins: [""]
    AllowedOrigins: [""] # CORS (default: all CallbackUrls)
    JWTConfiguration:
      LifetimeInSeconds: 3600 # 1 hour
      Scopes: # dict
      Alg: ""
    GrantTypes: [""] # implicit,authorization_code,refresh_token,client_credentials

    LogoUri: ""
    AuthMethod: "" # None, Post, Basic (default: None)
    LoginURI: "" # initiate_login_uri
    ClientMetadata: # dict
    Mobile:
      Android:
        AppPackageName: ""
        Sha256CertFingerprints: [""]
      Ios:
        TeamId: ""
        AppBundleIdentifier: ""
    AllowedClients: [""]
    OidcConformant: False
    CrossOriginLoc: ""

    # SPA/Web/Native only
    RefreshToken:
      RotationType: "" # rotating, non-rotating
      ExpirationType: "" # expiring, non-expiring
      Leeway: 0
      TokenLifetime: 1800

    # Refresh AD Access token for the Azure AD connection (only for MMM tenant).
    ClientMetadata:
      RefreshGraphTokenRule: True # if not enabled, token is only refreshed on user login.

    # Native only
    NativeSocialLogin:
      Apple: # dict
      Facebook: # dict
```

#### Application Attributes

Use CloudFormation GetAtt or Sub to access the following properties

| name         | description                                                                         |
|--------------|-------------------------------------------------------------------------------------|
| Arn          | The Arn of the secrets manager secret with your auth0 client id, secret, and tenant |
| Name         | The name of the secrets manager secret                                              |
| ClientId     | The Auth0 client_id                                                                 |
| ClientSecret | SSM Param location of the client secret (non-m2m apps)                              |

### Managing An API

The complete list of configurable properties for an API. For more information on what
these properties are you can refer to the [management API](https://auth0.com/docs/api/management/v2#!/Resource_Servers/get_resource_servers) documentation or the Auth0 console if you have access.

```yaml
AuthResource:
  Type: Custom::Authn_Api
  Properties:
    Tenant: my-tenant.auth0.com
    ServiceToken: !ImportValue pr-aws-cr-authn:LambdaArn
    Audience: http://my-api.com # required (url starting with https:// or http://)

    # optional configuration below
    Name: example-name
    Scopes: [""] # list of scopes available for this Api
    SigningAlg: "" # HS256 or RS256
    SigningSecret: ""
    AllowOfflineAccess: True # boolean, True or False
    TokenLifetime: 3600 # 1 hour
    TokenDialect: "" # access_token or access_token_authz
    SkipConsentForVerifiableFirstPartyClients: True # boolean
    EnforcePolicies: True # boolean
```

#### API Attributes

Use cloudformation GetAtt or Sub to access the following properties

| name  | description                |
|-------|----------------------------|
| ApiId | The ID of the API in Auth0 |


## Rotation

Secrets Manager handles rotation automatically.

## Common Problems

I get the error `No export named pr-aws-cr-authn:LambdaArn found`. See [adding to your account](#adding-to-your-account)

I can't push a branch to this repository or the drone policy. [Fork the repository](https://docs.github.com/en/free-pro-team@latest/github/getting-started-with-github/fork-a-repo) and push your changes there. Then open a pull request into the main repo.
