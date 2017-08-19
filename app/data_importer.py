USERS_PREFIX = "users"
VISITS_PREFIX = "visits"
LOCATIONS_PREFIX = "locations"
WORKIGN_DIRECTORY = "local_temp"

from zipfile import ZipFile
import json
from os import listdir
from os.path import isfile, join

class Payload(object):
    def __init__(self, j):
        self.__dict__ = json.loads(j)


class User(object):
    def __init__(self, dct):
        self.first_name = dct["first_name"]
        self.last_name = dct["last_name"]
        self.gender = dct["gender"]
        self.email = dct["email"]
        self.birth_date = dct["birth_date"]

        if "id" in dct:
            self.id = dct["id"]

    def to_json(self):
        return json.dumps(self.__dict__, ensure_ascii=False)

    def update(self, dct):
        if "first_name" in dct:
            self.first_name = dct["first_name"]

        if "last_name" in dct:
            self.last_name = dct["last_name"]

        if "gender" in dct:
            self.gender = dct["gender"]

        if "email" in dct:
            self.email = dct["email"]

def get_users(path):
    with ZipFile(path) as inputzip:
        inputzip.extractall(WORKIGN_DIRECTORY)

    files = [f for f in listdir(WORKIGN_DIRECTORY) if isfile(join(WORKIGN_DIRECTORY, f))]

    all_users = []

    for file_name in files:
        if file_name.startswith(USERS_PREFIX):
            with open(join(WORKIGN_DIRECTORY, file_name), encoding='utf-8') as f:
                p = Payload(f.read())
                all_users += p.users

    return [User(x) for x in all_users]
