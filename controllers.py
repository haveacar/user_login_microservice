from flask_restful import Api
from views import RegisterResource, ResendConfirmationResource, ConfirmEmail


def initialize_routes(api: Api):
    """User Routes"""
    api.add_resource(RegisterResource, '/api/v1/register')  # register user confirmation token, send confirm url(POST)
    api.add_resource(ResendConfirmationResource, '/api/v1/resend-confirmation') # resend email confirmation(POST)
    api.add_resource(ConfirmEmail, '/confirm-email/<token>', endpoint='confirm_email') # email confirmation (GET)