"""
Validate and coerce event resource parameters
"""
from . import AuthnValidator

auth0 = {
    'tenant': {'type': 'string', 'readonly': True, 'empty': False},
    'service_token': {'type': 'string', 'readonly': True},
    'application_id': {'type': 'string', 'empty': False},
    'audience': {'type': 'string', 'empty': False},
    'scope': {
        'type': 'list',
        'schema': {'type': 'string'}
    }
}

auth0Validator = AuthnValidator(
    auth0,
    purge_unknown=True,
)
