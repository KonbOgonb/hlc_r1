from model import User, Location, Visit
import pylibmc

mc_write = pylibmc.Client(["127.0.0.1"], binary=True, behaviors={"tcp_nodelay": True})
mc_read = pylibmc.Client(["udp:127.0.0.1"], binary=True, behaviors={"tcp_nodelay": True})

class RepositoryBase(object):
    def add_item(self, data):
        key, item = self.create_item(data)
        mc_write.set(key, item)        

        return item

    def update_item(self, new_item):
        key = self.get_key(new_item.id)
        mc_write.set(key, new_item)

    def update_item_from_dict(self, id, data):
        key = self.get_key(id)
        item = mc_write.get(key)

        if not item:
            raise KeyError()

        item.update(data)
        mc_write.set(key, item)

    def get_item(self, id):
        key = self.get_key(id)
        return mc_read.get(key)

class UserRepository(RepositoryBase):
    def get_key(self, id):
        return "user" + str(id)

    def create_item(self, data):
        user = data if isinstance(data, User) else User(data)
        return self.get_key(user.id), user

class LocationRepository(RepositoryBase):
    def get_key(self, id):
        return "location" + str(id)

    def create_item(self, data):
        location = data if isinstance(data, Location) else Location(data)
        return self.get_key(location.id), location

class VisitRepository(RepositoryBase):
    def get_key(self, id):
        return "visit" + str(id)

    def create_item(self, data):
        visit = data if isinstance(data, Visit) else Visit(data)
        return self.get_key(visit.id), visit