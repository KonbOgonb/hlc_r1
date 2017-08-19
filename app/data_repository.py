from data_importer import get_users
from data_importer import User

class Data_repository(object):
    def __init__(self, path_to_data):
        users_keys = [(user.id, user) for user in get_users(path_to_data)]        
        self.users = {key: user for (key, user) in  users_keys}

    def add_user(self, data):
        new_user = User(data)
        new_id = max(self.users.keys()) + 1
        new_user.id = new_id
        self.users[new_id] = new_user

    def update_user(self, id, data):
        if id not in self.users:
            return 404

        user = self.users[id]
        user.update(data)

    def get_user(self, id):
        if id in self.users:
            return self.users[id]
