import json

class ModelEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, ModelBase):
            return obj.__dict__

        return json.JSONEncoder.default(self, obj)

class ModelBase(object):
    def __init__(self, dct):
        if "id" not in dct or not isinstance(dct["id"], int):
            raise ValueError()

        self.id = dct["id"]

    def to_json(self):
        fields = {v:self.__dict__[v] for v in self.__dict__ if v != 'visits'}
        return json.dumps(fields, ensure_ascii=False)

class User(ModelBase):
    def __init__(self, dct):
        self.set_first_name(dct["first_name"])
        self.set_last_name(dct["last_name"])
        self.set_gender(dct["gender"])
        self.set_email(dct["email"])
        self.set_birth_date(dct["birth_date"])
        self.visits = []

        super(User, self).__init__(dct)

    def update(self, dct):
        if "first_name" in dct:
            self.set_first_name(dct["first_name"])

        if "last_name" in dct:
            self.set_last_name(dct["last_name"])

        if "gender" in dct:
            self.set_gender(dct["gender"])

        if "email" in dct:
            self.set_email(dct["email"])

        if "birth_date" in dct:
            self.set_birth_date(dct["birth_date"])

    def set_first_name(self, value):
        if not isinstance(value, str):
            raise ValueError()

        self.first_name = value

    def set_last_name(self, value):
        if not isinstance(value, str):
            raise ValueError()

        self.last_name = value

    def set_email(self, value):
        if not isinstance(value, str):
            raise ValueError()

        self.email = value

    def set_birth_date(self, value):
        if not isinstance(value, int):
            raise ValueError()

        self.birth_date = value

    def set_gender(self, value):
        if value not in ['f', 'm']:
            raise ValueError()

        self.gender = value


class Location(ModelBase):
    def __init__(self, dct):
        self.set_distance(dct["distance"])
        self.set_city(dct["city"])
        self.set_place(dct["place"])
        self.set_country(dct["country"])
        self.visits = []

        super(Location, self).__init__(dct)

    def update(self, dct):
        if "distance" in dct:
            self.set_distance(dct["distance"])

        if "city" in dct:
            self.set_city(dct["city"])

        if "place" in dct:
            self.set_place(dct["place"])

        if "country" in dct:
            self.set_country(dct["country"])

    def set_distance(self, value):
        if not isinstance(value, int):
            raise ValueError()

        self.distance = value

    def set_country(self, value):
        if not isinstance(value, str):
            raise ValueError()

        self.country = value

    def set_place(self, value):
        if not isinstance(value, str):
            raise ValueError()

        self.place = value

    def set_city(self, value):
        if not isinstance(value, str):
            raise ValueError()

        self.city = value

class Visit(ModelBase):
    def __init__(self, dct):
        self.set_user(dct["user"])
        self.set_location(dct["location"])
        self.set_visited_at(dct["visited_at"])
        self.set_mark(dct["mark"])

        super(Visit, self).__init__(dct)

    def update(self, dct):
        if "user" in dct:
            self.set_user(dct["user"])

        if "location" in dct:
            self.set_location(dct["location"])

        if "visited_at" in dct:
            self.set_visited_at(dct["visited_at"])

        if "mark" in dct:
            self.set_mark(dct["mark"])

    def set_mark(self, value):
        if not isinstance(value, int):
            raise ValueError()

        self.mark = value

    def set_location(self, value):
        if not isinstance(value, int):
            raise ValueError()

        self.location = value

    def set_user(self, value):
        if not isinstance(value, int):
            raise ValueError()

        self.user = value

    def set_visited_at(self, value):
        if not isinstance(value, int):
            raise ValueError()

        self.visited_at = value

