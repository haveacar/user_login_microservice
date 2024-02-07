from flask import Flask
from flask_restful import Api
from flask_cors import CORS
from flask_jwt_extended import JWTManager

from models import db
from controls import secret_manager_keys

# set up flask server
application = Flask(__name__)
CORS(application)
api = Api(application)
jwt = JWTManager(application)
# set up keys from aws secret manager
application.config['SECRET_KEY'] = secret_manager_keys.get('secret_key')
application.config["JWT_SECRET_KEY"] = secret_manager_keys.get('jwt_key')

# Database configuration
application.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://your_user:your_password@your_host/your_database'
application.config['SQLALCHEMY_TRAjwtCK_MODIFICATIONS'] = False

# initialize db
db.init_app(application)

if __name__ == '__main__':
    application.run(debug=True, port=5000)
