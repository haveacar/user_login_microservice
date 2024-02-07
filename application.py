from flask import Flask

application = Flask(__name__)

# Database configuration
application.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://your_user:your_password@your_host/your_database'
application.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
application.config['SECRET_KEY'] = 'my key from secret manager'


if __name__ == '__main__':
    application.run(debug=False, port=5000)
