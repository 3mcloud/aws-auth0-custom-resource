"""
Unit test globals
"""
from unittest import mock
import pytest

@pytest.fixture(scope='session', autouse=True)
def default_session_fixture(request):
    """patch things for every unit test"""
    # Patch boto client to return a magic mock by default during
    # all unit tests
    patched = mock.patch('botocore.client.BaseClient._make_api_call')
    patched.start()
    def unpatch():
        try:
            patched.stop()
        except IndexError:
            pass
    request.addfinalizer(unpatch)
