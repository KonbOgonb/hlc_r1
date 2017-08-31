from model import User, Location, Visit
import pylibmc

mc = pylibmc.Client(["127.0.0.1"], binary=True,
    behaviors={"tcp_nodelay": True})

class RepositoryBase(object):
    def add_item(self, data):
        key, item = self.create_item(data)
        mc.set(key, item)        

        return item

    def add_multi(self, data):
        items = {}
        for x in data:
            k,v = self.create_item(x)
            items[k] = v
        mc.set_multi(items)

    def get_multi(self, data):
        count = 0 
        items = []
        result = {}
        for i in data:
            count += 1
            items.append(i)
            if count == 1000:
                esult.update(mc.get_multi([self.get_key(x) for x in items]))
                count = 0

        result.update(mc.get_multi([self.get_key(x) for x in items]))
        return result

    def update_multi(self, data):
        mc.set_multi(data)

    def update_item(self, new_item):
        key = self.get_key(new_item.id)
        mc.set(key, new_item)

    def update_item_from_dict(self, id, data):
        key = self.get_key(id)
        item = mc.get(key)

        if not item:
            raise KeyError()

        item.update(data)
        mc.set(key, item)

    def get_item(self, id):
        key = self.get_key(id)
        return mc.get(key)

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