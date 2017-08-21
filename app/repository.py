from model import User, Location, Visit

class RepositoryBase(object):
    def __init__(self, items):
        items_with_keys = [(item.id, item) for item in items]
        self.items = {key: item for (key, item) in  items_with_keys}

    def add_item(self, data):
        new_item = self.create_item(data)
        new_id = max(self.items.keys()) + 1
        new_item.id = new_id
        self.items[new_id] = new_item

        return new_item

    def update_item(self, id, data):
        if id not in self.items:
            return 404

        user = self.items[id]
        user.update(data)

    def get_item(self, id):
        if id in self.items:
            return self.items[id]

class UserRepository(RepositoryBase):
    def __init__(self, data):
        users = data["users"]
        super(UserRepository, self).__init__(users)

    def create_item(self, data):
        return User(data)

class LocationsRepository(RepositoryBase):
    def __init__(self, data):
        users = data["locations"]
        super(LocationsRepository, self).__init__(users)

    def create_item(self, data):
        return Location(data)

class VisitsRepository(RepositoryBase):
    def __init__(self, data):
        users = data["visits"]
        super(VisitsRepository, self).__init__(users)

    def create_item(self, data):
        return Visit(data)