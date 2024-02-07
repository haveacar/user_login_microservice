from flask import request, current_app
from flask_restful import Resource
from itsdangerous import URLSafeTimedSerializer
from sqlalchemy.exc import IntegrityError
from marshmallow import ValidationError

from controls import send_email_smtp
from serializers import UserRegistrationSchema
from models import Users, db
from constants import HTML_CONFIRM, SUBJECT


def generate_confirmation_token(email: str) -> str:
    """
    Generate a secure, time-sensitive token for email confirmation.
    :param email: user email(str)
    :return: token(str)
    """
    s = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])
    return s.dumps(email, salt='confirm_email')


def send_confirmation_email(user_email: str) -> bool:
    """Send a confirmation email to the user."""
    # Extract the domain from the current request's URL.
    domain = request.url_root
    # generate token
    token = generate_confirmation_token(user_email)
    confirm_url = f"{domain}confirm-email/{token}"
    # Assuming HTML_CONFIRM has a placeholder for `url`
    html = HTML_CONFIRM.format(confirm_url)

    if send_email_smtp(user_email, SUBJECT, html) == 200:
        return True
    else:
        return False


class RegisterResource(Resource):
    """Handles new user registration."""

    def post(self):
        # Data serialization
        schema = UserRegistrationSchema()
        try:
            data = schema.load(request.json)
        except ValidationError as err:
            return err.messages, 400

        # Combine checks for existing email or username to reduce database hits
        existing_user = Users.query.filter(
            (Users.email == data['email']) | (Users.username == data['username'])
        ).first()
        if existing_user:
            return {'message': 'Email or Username already exists'}, 400

        try:
            # create instance users
            user = Users(**data)
            # write to db
            db.session.add(user)
            db.session.commit()

            # send email confirmation
            if send_confirmation_email(data['email']):
                return {'message': 'User created successfully. Email confirmation sent'}, 201
            else:
                return {'message': 'User created successfully, but confirmation email could not be sent'}, 202

        except IntegrityError:
            db.session.rollback()  # session rollback
            return {'message': 'A user with this email or username already exists.'}, 409  # 409 Conflict

        except Exception as err:
            db.session.rollback()  # session rollback
            return {'message': f'An error occurred while creating new user: {err}'}, 500


class ResendConfirmationResource(Resource):
    """Handles resending the email confirmation."""

    def post(self):
        email = request.json.get('email')
        if not email:
            return {'message': 'Email is required'}, 400

        user = Users.query.filter_by(email=email).first()
        if not user:
            return {'message': 'User not found'}, 404

        # send email confirmation
        if send_confirmation_email(user.email):
            return {'message': 'Email confirmation sent'}, 200
        else:
            return {'message': 'Failed to send email confirmation'}, 500
