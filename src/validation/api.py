"""
Validate and coerce event resource parameters
"""
from . import AuthnValidator, to_bool

auth0 = {  # pylint: disable=invalid-name
    'tenant': {'type': 'string', 'readonly': True, 'empty': False},
    'service_token': {'type': 'string', 'readonly': True},
    'name': {'type': 'string'},
    'audience': {'type': 'string', 'rename': 'identifier', 'required': True},
    'scopes': {
        'type': 'list',
        'schema': {'type': 'string'}
    },
    'signing_alg': {
        'type': 'string',
        'allowed': ['HS256', 'RS256']
    },
    'signing_secret': {'type': 'string'},
    'allow_offline_access': {'type': 'boolean', 'coerce': to_bool},
    'token_lifetime': {'type': 'integer', 'coerce': int},
    'token_dialect': {
        'type': 'string',
        'allowed': ['access_token', 'access_token_authz']
    },
    'skip_consent_for_verifiable_first_party_clients': {'type': 'boolean', 'coerce': to_bool},
    'enforce_policies': {'type': 'boolean', 'coerce': to_bool},
    # 'client': {'type': 'dict'} don't allow client, force the use of Authn_Grant
}

auth0Validator = AuthnValidator(  # pylint: disable=invalid-name
    auth0,
)
