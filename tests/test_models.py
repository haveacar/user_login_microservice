import pytest
from models import db, Users

@pytest.fixture
def user():
    user = Users(username='testuser', email='test@example.com', password='securepassword')
    return user

def test_new_user(user):
    assert user.username == 'testuser'
    assert user.email == 'test@example.com'
    assert user.check_password('securepassword')