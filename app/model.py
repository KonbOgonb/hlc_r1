import json

class ModelEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, ModelBase):
            return obj.__dict__

        return json.JSONEncoder.default(self, obj)

class ModelBase(object):
    def __init__(self, dct):
        if "id" in dct:
            self.id = dct["id"]

    def to_json(self):
        fields = {v:self.__dict__[v] for v in self.__dict__ if v != 'visits'}
        return json.dumps(fields, ensure_ascii=False)

class User(ModelBase):
    def __init__(self, dct):
        self.first_name = dct["first_name"]
        self.last_name = dct["last_name"]
        self.gender = dct["gender"]
        self.email = dct["email"]
        self.birth_date = dct["birth_date"]
        self.visits = []

        super(User, self).__init__(dct)

    def update(self, dct):
        if "first_name" in dct:
            self.first_name = dct["first_name"]

        if "last_name" in dct:
            self.last_name = dct["last_name"]

        if "gender" in dct:
            self.gender = dct["gender"]

        if "email" in dct:
            self.email = dct["email"]

        if "birth_date" in dct:
            self.birth_date = dct["birth_date"]

class Location(ModelBase):
    def __init__(self, dct):
        self.distance = dct["distance"]
        self.city = dct["city"]
        self.place = dct["place"]
        self.country = dct["country"]
        self.visits = []

        super(Location, self).__init__(dct)

    def update(self, dct):
        if "distance" in dct:
            self.distance = dct["distance"]

        if "city" in dct:
            self.city = dct["city"]

        if "place" in dct:
            self.place = dct["place"]

        if "country" in dct:
            self.country = dct["country"]

class Visit(ModelBase):
    def __init__(self, dct):
        self.user = dct["user"]
        self.location = dct["location"]
        self.visited_at = dct["visited_at"]
        self.mark = dct["mark"]

        super(Visit, self).__init__(dct)

    def update(self, dct):
        if "user" in dct:
            self.user = dct["user"]

        if "location" in dct:
            self.location = dct["location"]

        if "visited_at" in dct:
            self.visited_at = dct["visited_at"]

        if "mark" in dct:
            self.mark = dct["mark"]

