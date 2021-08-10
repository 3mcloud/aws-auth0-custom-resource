'''End to end test for auth0 resource cycle'''

from src.auth0.index import Auth0Provider


def test_connection():
    '''Test the connection methods'''
    auth0 = Auth0Provider(management_secret='qa/auth0/tenant/mmm-dev', tenant='mmm-dev.auth0.com')
    app_id = 'QqTPi39208tYuf4p7THhdSOUGD1PvGpj'
    conn_id = 'con_WYljqEqcw2L8VU7c'
    start = auth0.auth0.connections.get(conn_id, ['enabled_clients'])
    auth0.add_to_connection(conn_id, app_id)
    mid = auth0.auth0.connections.get(conn_id, ['enabled_clients'])
    auth0.remove_from_connection(conn_id, app_id)
    end = auth0.auth0.connections.get(conn_id, ['enabled_clients'])

    assert start == end
    assert mid != start
