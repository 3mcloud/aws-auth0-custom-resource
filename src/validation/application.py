"""
Validate and coerce event resource parameters
"""
import json
from cerberus import Validator
from . import AuthnValidator, to_bool

APP_TYPE_MAP = {
    'spa': 'spa',
    'native': 'native',
    'm2m': 'non_interactive',
    'web': 'regular_web',
}

AUTH_METHOD_MAP = {
    'None': 'none',
    'Post': 'client_secret_post',
    'Basic': 'client_secret_basic'
}


def to_auth_method_type(val):
    """coerce the auth method to the api value"""
    if not val in AUTH_METHOD_MAP:
        raise ValueError(
            f'method should be one of {",".join(AUTH_METHOD_MAP.keys())}'
        )
    return AUTH_METHOD_MAP[val]


def to_app_type(val):
    """coerce the app type value"""
    if val not in APP_TYPE_MAP:
        raise ValueError(
            'type should be one of {}'.format(','.join(APP_TYPE_MAP.keys()))
        )
    return APP_TYPE_MAP[val]


# pylint: disable=invalid-name
auth0 = {
    'tenant': {
        'type': 'string',
        'readonly': True,
        'empty': False,
    },
    'service_token': {
        'type': 'string',
        'readonly': True,
        'empty': False,
    },
    'name': {
        'type': 'string',
        'required': True,
        'empty': False,
    },
    'description': {
        'type': 'string',
        'required': True,
        'empty': False,
    },
    'logo_uri': {'type': 'string'},
    'type': {
        'rename': 'app_type',
        'required': True,
        'type': 'string',
        'allowed': ['spa', 'native', 'non_interactive', 'regular_web'],
        'coerce': (to_app_type),
    },
    'token_endpoint_auth_method': {
        'type': 'string',
        'allowed': ['None', 'Post', 'Basic'],
        # 'default': 'None',
        'coerce': (to_auth_method_type),
    },
    'auth_method': {
        'rename': 'token_endpoint_auth_method',
        'type': 'string',
    },
    'login_u_r_i': {
        'rename': 'initiate_login_uri',
        'type': 'string',
    },
    'callback_urls': {
        'rename': 'callbacks',
        'type': 'list',
        'schema': {'type': 'string'},
    },
    'logout_urls': {
        'rename': 'allowed_logout_urls',
        'type': 'list',
        'schema': {'type': 'string'}
    },
    'web_origins': {
        'type': 'list',
        'schema': {'type': 'string'}
    },
    'allowed_origins': {
        'type': 'list',
        'schema': {'type': 'string'}
    },
    'j_w_t_configuration': {
        'rename': 'jwt_configuration',
        'schema': {
            'lifetime_in_seconds': {'type': 'integer', 'default': 3600, 'coerce': int},
            'scopes': {'type': 'dict'},
            'alg': {'type': 'string'},
        }
    },

    # SPA/Web/Native only
    'refresh_token': {
        'type': 'dict',
        'dependencies': 'grant_types',
        'schema': {
            'rotation_type': {
                'type': 'string',
                'allowed': ['rotating', 'non-rotating'],
            },
            'expiration_type': {
                'type': 'string',
                'allowed': ['expiring', 'non-expiring'],
            },
            'token_lifetime': {
                'type': 'integer',
                'min': 1800,
                'max': 2592000,
                'coerce': int
            },
        }
    },

    # # Native
    'native_social_login': {
        'type': 'dict',
        'dependencies': {'type': ['native']},
        'schema': {
            'apple': {
                'type': 'dict',
            },
            'facebook': {
                'type': 'dict',
            },
        }
    },

    # # Advanced : Danger Zone

    'client_metadata': {
        'type': 'dict',
        'default': {},
    },
    'mobile': {
        'type': 'dict',
        'schema': {
            'android': {
                'type': 'dict',
                'schema': {
                    'app_package_name': {
                        'type': 'string'
                    },
                    'sha256_cert_fingerprints': {
                        'type': 'list'
                    },
                }
            },
            'ios': {
                'type': 'dict',
                'schema': {
                    'team_id': {
                        'type': 'string'
                    },
                    'app_bundle_identifier': {
                        'type': 'string'
                    },
                },
            }
        },
    },
    'allowed_clients': {
        'type': 'list'
    },
    'oidc_conformant': {
        'type': 'boolean',
        'coerce': to_bool
    },
    # 'cross_origin_loc': '', # Cross-Origin Verification Fallback
    # M2M Only
    'grant_types': {
        'type': 'list',
        'anyof': [
            {
                'dependencies': {'type': 'non_interactive'},
                'allowed': [
                    'client_credentials',
                    'implicit',
                    'authorization_code',
                    'refresh_token',
                    'password',
                    'mfa',
                ],
            },
            {
                'dependencies': {'type': ['spa', 'native', 'regular_web']},
                'allowed': [
                    'implicit',
                    'authorization_code',
                    'refresh_token',
                    'password',
                    'mfa',
                ],
            },
        ],
    },
    'allow_ad_groups': {
        'readonly': True,
        'type': 'list',
        'dependencies': {'type': ['spa', 'native', 'regular_web']},
        'schema': {
            'type': 'string',
        }
    },

    # custom-resource specific
    'connections': {
        'readonly': True,
        'type': 'list',
        'schema': {
            'type': 'string'
        }
    }
}

tags_schema = {
    'ApplicationID': {
        'type': 'string',
    },
    'AllowAdGroups': {
        'type': 'string',
        'coerce': (lambda x: json.dumps(x, separators=(',', ':'))),
        'maxlength': 255,
    }
}

application_defaults = {
    'non_interactive': {
        'grant_types': ['client_credentials'],
        'token_endpoint_auth_method': 'client_secret_post',
    },
    'spa': {
        'grant_types': ['implicit', 'authorization_code', 'refresh_token'],
        'token_endpoint_auth_method': 'none',
    }
}

def with_defaults(document):
    """a function to return defaults on an application type"""
    app_type = document['app_type']
    if app_type not in application_defaults:
        return {}
    return application_defaults[app_type]

auth0Validator = AuthnValidator(
    auth0,
    with_defaults=with_defaults,
)
tagsValidator = Validator(
    tags_schema,
    purge_unknown=True,
)
