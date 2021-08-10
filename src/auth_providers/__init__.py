"""Utility to store the list of providers"""

from src.auth0.index import Auth0Provider
# import b2c

PROVIDERS = {
    'auth0': Auth0Provider
}
