"""Library of auth0 interactions"""
import logging
import json
import time
import boto3
from auth0.v3.authentication import GetToken
from auth0.v3.management import Auth0
from src.utils import secret

logger = logging.getLogger()
logger.setLevel(logging.INFO)

# Page limit for auth0 in case of run-away pagination
PAGE_LIMIT = 60


class Auth0Provider():
    """
    Generic Cloudformation custom resource provider for Auth0 resources.
    """

    def __init__(self, management_secret, tenant):
        """Default constructor

        Args:
            management_secret (str): secrets manager location for the management api credentials
            tenant (str): Auth0 tenant, e.g. mmm-dev
        """
        self.secrets_manager = boto3.client('secretsmanager')
        admin = json.loads(secret.get_secret(
            self.secrets_manager, management_secret, logger))
        self.authenticate(
            tenant,
            admin['AUTH0_CLIENT_ID'],
            admin['AUTH0_CLIENT_SECRET']
        )

    def authenticate(self, tenant, client_id, client_secret):
        """Sets up an authenticated client

        Args:
            tenant (str): tenant name for auth0
            client_id (str): id of the application authorized to use the management api
            client_secret (str): client secret for the above application
        """
        get_token = GetToken(tenant)
        logger.info('Getting token for tenant %s with client %s', tenant, client_id)
        token = get_token.client_credentials(
            client_id, client_secret, 'https://{}/api/v2/'.format(tenant))
        mgmt_api_token = token['access_token']

        self.auth0 = Auth0(tenant, mgmt_api_token)
        return self.auth0

    def create_application(self, **kwargs):
        """Create an Auth0 Application (Client)

        Args:
            name (str): Name of the application, e.g. myapp
            app_type (str): Type of application - spa, m2m, native, or web
        """
        client = self.auth0.clients.create(kwargs)
        return client['client_id'], client['client_secret']

    def create_api(self, **kwargs):
        """Create an Auth0 API (Resource)

        Args:
            name (str): Name of the api, e.g. myapi
            audience (str): Audience url, must include http:// or https://
        """
        server = self.auth0.resource_servers.create(kwargs)
        return server['id']

    def create_grant(self, audience, application_id):
        """Create an Auth0 grant (client_grant)

        Args:
            audience (str): Audience url, must include http:// or https://
            application_id (str): ID of the application
        """
        grant = self.auth0.client_grants.create(
            {'client_id': application_id, 'audience': audience, 'scope': []})
        return grant['id']

    def create_resource(self, url, name):
        """Create an auth0 resource

        Creates a client (application), resource server (api), and a grant for the client to use
        the resource server.

        Args:
            url (str): Url for the API, e.g. appsync url
            name (str): Name for the client and resource server
        """
        client = self.auth0.clients.create(
            {'name': name, 'app_type': 'non_interactive'})
        server = self.auth0.resource_servers.create(
            {'name': name, 'identifier': url})
        grant_id = self.auth0.client_grants.create(
            {'client_id': client['client_id'], 'audience': url, 'scope': []})
        return client['client_id'], client['client_secret'], server['id'], grant_id['id']

    def rotate_client_secret(self, client_id):
        """Rotate a client secret

        Args:
            client_id (str): ID of the client to rotate the secret for
        """
        resp = self.auth0.clients.rotate_secret(client_id)
        return resp['client_secret']

    def update_resource(self):
        """Update a resource"""
        # Nothing to update at the moment

    def update_api(self, audience, **kwargs):
        """Update an api

        Args:
            **kwargs (dict): configuration of the auth0 client
        """
        self.auth0.resource_servers.update(audience, kwargs)

    def get_resource_server(self, url):
        """Gets the id of a resource server based on the audience

        Args:
            url (str): Url associated with the resource server
        """
        page = 0
        prev = []
        while page is not None:
            resource_list = self.auth0.resource_servers.get_all(
                page=page, per_page=50)
            # If there is only one page, get_all will return the same
            # value for every page
            if prev == resource_list:
                break
            prev = resource_list
            if resource_list == []:
                break
            for resource in resource_list:
                if resource['identifier'] == url:
                    return resource['id']
            page += 1
            if page > PAGE_LIMIT:
                break
            time.sleep(1)
        return None

    def get_application(self, client_id, fields=None, include_fields=True):
        """Get an application (client) from auth0 by id"""
        return self.auth0.clients.get(id=client_id, fields=fields, include_fields=include_fields)

    def add_to_connection(self, conn_id, app_id):
        """Enable a connection for an application"""
        connection = self.auth0.connections.get(conn_id, ['enabled_clients'])
        # add the app_id to the list of enabled_clients
        if app_id not in connection['enabled_clients']:
            connection['enabled_clients'].append(app_id)
        # update the connection
        self.auth0.connections.update(conn_id, {'enabled_clients': connection['enabled_clients']})

    def remove_from_connection(self, conn_id, app_id):
        """Disable a connection for an application"""
        connection = self.auth0.connections.get(conn_id, ['enabled_clients'])
        # remove the app_id to the list of enabled_clients
        if app_id in connection['enabled_clients']:
            connection['enabled_clients'].remove(app_id)
        # update the connection
        self.auth0.connections.update(conn_id, {'enabled_clients': connection['enabled_clients']})

    def update_application(self, client_id, **kwargs):
        """Update an Auth0 Application (Client)

        Args:
            client_id (str): ID of the Auth0 Application (client)
            **kwargs (dict): configuration of the auth0 client
        """
        client = self.auth0.clients.update(client_id, kwargs)
        return client['client_id']

    def delete_application(self, app_id):
        """Delete an application

        Args:
            app_id (str): The ID of the application to delete
        """
        return self.auth0.clients.delete(app_id)

    def delete_grant(self, grant_id):
        """Delete a grant

        Args:
            grant_id (str): The ID of the grant to delete
        """
        return self.auth0.client_grants.delete(grant_id)

    def delete_api(self, api_id):
        """Delete an api

        Args:
            api_id (str): The ID of the api to delete
        """
        return self.auth0.resource_servers.delete(api_id)

    def delete_resource(self, resource_id, client_id):
        """Delete a resource

        Deletes the resource server, client, and client grant in the resource

        Args:
            resource_id (str): The ID of the resource_server to delete
            client_id (str): The ID of the client to delete
        """
        self.auth0.clients.delete(client_id)
        # Deleting a client also deletes the grants associated with it
        self.auth0.resource_servers.delete(resource_id)
