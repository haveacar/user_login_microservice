import pytest
from application import application, check_sql_connection


@pytest.fixture
def client():
    application.config['TESTING'] = True  # Configure Flask for testing
    with application.test_client() as client:
        with application.app_context():
            yield client

def test_home_route(client):
    response = client.get('/')
    assert response.status_code == 200

def test_check_sql_connection():

    assert check_sql_connection() is None