from flask_admin import Admin, BaseView
from flask_admin.contrib.sqla import ModelView
from views import Users


class UserView(ModelView):
    """hide password"""
    column_formatters = {
        'password': lambda v, c, m, p: '*' * 8  # m is the model instance
    }


def init_admin(application, session):
    """Func to initialize admin"""
    admin = Admin(application, name='Web3m', url='/web3m-admin', template_mode='bootstrap4')
    # Add views
    admin.add_view(UserView(Users, session))