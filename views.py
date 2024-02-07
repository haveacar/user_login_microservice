from flask import request, current_app
from flask_restful import Resource
from sqlalchemy.exc import IntegrityError
from itsdangerous import URLSafeTimedSerializer, SignatureExpired, BadTimeSignature, BadSignature
from models import Users, db

class RegisterResource(Resource):
    """Registration new user"""

    def post(self):
        # get dataa
        fields = ('username', 'email', 'password')
        data = {key:request.json.get(key)for key in fields}

        # Check if email already exists
        if Users.query.filter_by(email=data['email']).first():
            return {'message': 'Email already exists'}, 400

        # Check if username already exists
        if Users.query.filter_by(username=data['username']).first():
            return {'message': 'Username already exists'}, 400

        # create instance users
        user = Users(**data)
        # add user
        try:
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
            return {'message': 'Connection data error'}, 400

    # def generate_confirmation_token(self, email):
    #     s = URLSafeTimedSerializer(current_app.config['SECRET_KEY'])
    #     return s.dumps(email, salt='confirm_email')