import uuid
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from werkzeug.security import generate_password_hash
from werkzeug.security import check_password_hash

db = SQLAlchemy()


class Users(db.Model):
    """User model representing a user """
    id = db.Column(db.Integer, primary_key=True)
    # generate unique_id
    user_id = db.Column(db.String(36), unique=True, nullable=False, default=lambda: str(uuid.uuid4()))
    username = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), nullable=False)
    password = db.Column(db.String(255), nullable=False)
    date = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    email_confirmed = db.Column(db.Boolean, default=False)

    def set_password(self, password):
        """
        Create and set the hashed password.
        """
        self.password = generate_password_hash(password) # hash password


    def check_password(self, password):
        """
        Verify if the provided password matches the hashed password.
        """
        return check_password_hash(self.password, password)

    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.set_password(password)
