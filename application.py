from flask import Flask
from flask_restful import Api
from flask_jwt_extended import JWTManager
from sqlalchemy.exc import OperationalError

from models import db
from controls import secret_manager_keys
from sqlalchemy import text
from controllers import initialize_routes


# set up flask server
application = Flask(__name__)
api = Api(application)
jwt = JWTManager(application)
# set up keys from aws secret manager
application.config['SECRET_KEY'] = secret_manager_keys.get('secret_key')
application.config["JWT_SECRET_KEY"] = secret_manager_keys.get('jwt_key')

# Database configuration
application.config['SQLALCHEMY_DATABASE_URI'] = secret_manager_keys.get('my_sql_connection')
application.config['SQLALCHEMY_TRAjwtCK_MODIFICATIONS'] = False

# initialize db
db.init_app(application)


def check_sql_connection():
    """Func to check MySQL database connection"""
    try:
        with application.app_context():
            db.session.execute(text('SELECT 1'))
        print("Database connection successful.")

    except OperationalError as e:
        print(f"Database connection failed: {e}")

# routes initialize
initialize_routes(api)


if __name__ == '__main__':
    # check sql connection
    with application.app_context():
        check_sql_connection()
    # application run
    application.run(debug=True, port=5000)
