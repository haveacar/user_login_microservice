from flask import request, current_app
from flask_restful import Resource
from itsdangerous import URLSafeTimedSerializer, SignatureExpired, BadTimeSignature
from sqlalchemy.exc import IntegrityError
from marshmallow import ValidationError
from werkzeug.security import check_password_hash
from datetime import timedelta
from flask_jwt_extended import jwt_required, create_access_token, get_jwt_identity, create_refresh_token

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


class ConfirmEmail(Resource):
    """Handle email confirmation"""

    def get(self, token: str):
        s = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])

        try:

            email = s.loads(token, salt='confirm_email', max_age=600)

        except SignatureExpired:
            return {'message': 'The confirmation link has expired. Please request a new one.'}, 400

        except BadTimeSignature:
            return {'message': 'The confirmation link is invalid.'}, 400

        user = Users.query.filter_by(email=email).first()

        if not user:
            return {'message': 'Invalid request.'}, 400

        if user.email_confirmed:
            return {'message': 'Email already confirmed'}, 400

        # confirm user
        user.email_confirmed = True
        db.session.commit()

        return {'message': 'Email confirmed'}, 200


class SignIn(Resource):
    """Handle in function """

    def post(self, access_exp=timedelta(hours=1), refresh_exp=timedelta(days=30)):
        """
        Authenticate a user and issue JWT access and refresh tokens.
        :param access_exp: specifies the expiration time for the access token. Defaults to 1 hour.
        :param refresh_exp: specifies the expiration time for the refresh token.  Defaults to 30 days.
        :return:
        """
        # get data
        email = request.json.get('email')
        password = request.json.get('password')

        # check user in database
        user = Users.query.filter_by(email=email).first()
        if not user or not check_password_hash(user.password, password) or not user.email_confirmed:
            return {'message': 'Login unsuccessful.'}, 401

        # Create a new token with the user id inside
        access_token = create_access_token(identity=user.user_id, expires_delta=access_exp,
                                           additional_claims={"email": user.email, "username": user.username,
                                                              "id": user.user_id,
                                                              })

        # Create a refresh token
        refresh_token = create_refresh_token(identity=user.user_id, expires_delta=refresh_exp)

        return {
                   'user_id': user.user_id,
                   'email': user.email,
                   'username': user.username,
                   'access_token': access_token,
                   'refresh_token': refresh_token,
                   'is_email_confirmed': user.email_confirmed

               }, 200
