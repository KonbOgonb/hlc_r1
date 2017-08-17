from zipfile import ZipFile
import json
from collections import namedtuple
from os import listdir
from os.path import isfile, join

import json

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
        self.id = dct["id"]

    def toJson(self):
        return json.dumps(self.__dict__, ensure_ascii=False)

users_prefix = "users"
visits_prefix = "visits"
locations_prefix = "locations"
working_directory = "local_temp"

def getUsers(path):
    with ZipFile(path) as inputzip:
        inputzip.extractall(working_directory)

    files = [f for f in listdir(working_directory) if isfile(join(working_directory, f))]

    all_users = []

    for file_name in files:
        if file_name.startswith(users_prefix):
            with open(join(working_directory, file_name), encoding='utf-8') as f:
                p = Payload(f.read())
                all_users += p.users

    return [User(x) for x in all_users]
    