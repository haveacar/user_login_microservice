from flask import request, current_app
from flask_restful import Resource
from sqlalchemy.exc import IntegrityError
from marshmallow import ValidationError
from serializers import UserRegistrationSchema
from models import Users, db

class RegisterResource(Resource):
    """New user Registration"""

    def post(self):
        # Data serialization
        schema = UserRegistrationSchema()
        try:
            data = schema.load(request.json)
        except ValidationError as err:
            return err.messages, 400

        # Check if email already exists
        if Users.query.filter_by(email=data['email']).first():
            return {'message': 'Email already exists'}, 400

        # Check if username already exists
        if Users.query.filter_by(username=data['username']).first():
            return {'message': 'Username already exists'}, 400

        # create instance users
        user = Users(**data)

        try:
            # write to db
            db.session.add(user)
            db.session.commit()

            # # Extract the domain from the current request's URL.
            # domain = request.url_root
            #
            # # send confirmation email
            # token = self.generate_confirmation_token(user.email)
            # confirm_url = f"{domain}confirm-email/{token}"
            # html = HTML_CONFIRM.format(confirm_url)
            #
            # subject = 'Please Confirm your Email on Coart'
            #
            # if send_email_smtp(user.email, subject, html) == 200:  # call the send_email function
            #     user = UserR.query.filter_by(email=email).first()

            return {'message': 'User created successfully. Please confirm your email.',
                        'userId': user.user_id}, 201

        except IntegrityError:
            db.session.rollback() # session rollback
            return {'message': 'A user with this email or username already exists.'}, 409  # 409 Conflict

        except Exception as err:
            db.session.rollback()  # session rollback
            return {'message': f'An error occurred while creating new user: {err}'}, 500

    # def generate_confirmation_token(self, email):
    #     s = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])
    #     return s.dumps(email, salt='confirm_email')