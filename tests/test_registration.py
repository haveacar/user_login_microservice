import pytest
from flask import Flask
from flask_restful import Api
from sqlalchemy.exc import IntegrityError
from controllers import initialize_routes
from models import db, Users

@pytest.fixture
def app():
    """Create and configure a new app instance for each test."""
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    app.config['TESTING'] = True
    db.init_app(app)
    # Create a context for the app
    with app.app_context():
        db.create_all()
    return app

@pytest.fixture
def client(app):
    api = Api(app)
    initialize_routes(api)
    return app.test_client()

@pytest.fixture
def runner(app):
    return app.test_cli_runner()

# Mock send_confirmation_email function
@pytest.fixture
def mock_send_confirmation_email(monkeypatch):
    monkeypatch.setattr('views.send_confirmation_email', lambda email: True)

# Successful registration
def test_register_success(client, mock_send_confirmation_email):
    response = client.post('/api/v1/register', json={
        'username': 'newuser',
        'email': 'newuser@example.com',
        'password': 'aSecurePassword'
    })
    assert response.status_code == 201
    assert response.json['message'] == 'User created successfully. Email confirmation sent'

# Registration with existing email/username
def test_register_existing_user(client, app, mock_send_confirmation_email):
    with app.app_context():
        user = Users(username='existinguser', email='existing@example.com', password='password123')
        db.session.add(user)
        db.session.commit()

    response = client.post('/api/v1/register', json={
        'username': 'existinguser',
        'email': 'existing@example.com',
        'password': 'password123'
    })
    assert response.status_code == 400
    assert response.json['message'] == 'Email or Username already exists'

# Invalid input data
def test_register_invalid_data(client):
    response = client.post('/api/v1/register', json={
        'username': 'us',  # too short
        'email': 'notanemail',  # invalid format
        'password': 'short'  # too short
    })
    assert response.status_code == 400

# Email send failure scenario
def test_register_email_send_failure(client, monkeypatch):
    monkeypatch.setattr('views.send_confirmation_email', lambda email: False)
    response = client.post('/api/v1/register', json={
        'username': 'userfailmail',
        'email': 'userfailmail@example.com',
        'password': 'aSecurePassword'
    })
    assert response.status_code == 202
    assert response.json['message'] == 'User created successfully, but confirmation email could not be sent'

# Testing database errors (e.g., IntegrityError)
@pytest.fixture
def mock_db_session_add_raise_integrity_error(monkeypatch):
    def mock_add(*args, **kwargs):
        raise IntegrityError('', '', '')
    monkeypatch.setattr(db.session, 'add', mock_add)

def test_register_db_error(client, mock_db_session_add_raise_integrity_error):
    response = client.post('/api/v1/register', json={
        'username': 'userDbError',
        'email': 'userdberror@example.com',
        'password': 'aSecurePassword'
    })
    assert response.status_code == 409
    assert response.json['message'] == 'A user with this email or username already exists.'