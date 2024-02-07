from flask import Flask
from flask_restful import Api
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from models import db

# set up flask server
application = Flask(__name__)
CORS(application)
api = Api(application)
jwt = JWTManager(application)
# set up keys from aws secret manager
application.config['SECRET_KEY'] = 'my secret key from secret manager'
application.config["JWT_SECRET_KEY"] = 'my jwt key from secret manager'

# Database configuration
application.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://your_user:your_password@your_host/your_database'
application.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# initialize db
db.init_app(application)

if __name__ == '__main__':
    application.run(debug=True, port=5000)
