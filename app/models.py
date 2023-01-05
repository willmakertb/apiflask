from flask_login import UserMixin
from .auth.model import get_users
class UserData:
    def __init__(self, username, password ):
        self.username = username
        self.password = password

class UserModel(UserMixin):
    def __init__(self, user_data):
        self.id = user_data.username
        self.password = user_data.password


    @staticmethod
    def query(user_id):
        user_doc = get_users(user_id)
        user_data = UserData(
            username = user_doc.username,
            password = user_doc.to_dict()['password']
        )
        return UserModel(user_data)