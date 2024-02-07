from flask_restful import Api
from views import RegisterResource


def initialize_routes(api: Api):
    """User Routes"""
    api.add_resource(RegisterResource, '/api/v1/register')  # register user confirmation token, send confirm url(POST)