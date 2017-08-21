USERS_PREFIX = "users"
VISITS_PREFIX = "visits"
LOCATIONS_PREFIX = "locations"
ALL_PREFIXES = [USERS_PREFIX, VISITS_PREFIX, LOCATIONS_PREFIX]
WORKIGN_DIRECTORY = "local_temp"

from zipfile import ZipFile
import json
from os import listdir
from os.path import isfile, join
from model import User, Location, Visit

class Payload(object):
    def __init__(self, j):
        self.__dict__ = json.loads(j)

def read_all_data(path):
    with ZipFile(path) as inputzip:
        inputzip.extractall(WORKIGN_DIRECTORY)

    files = [f for f in listdir(WORKIGN_DIRECTORY) if isfile(join(WORKIGN_DIRECTORY, f))]

    all_users = []
    all_locations = []
    all_visits = []

    for file_name in files:
        if not any(file_name.startswith(prefix) for prefix in ALL_PREFIXES):
            continue

        with open(join(WORKIGN_DIRECTORY, file_name), encoding='utf-8') as f:
            p = Payload(f.read())

            if file_name.startswith(USERS_PREFIX):            
                all_users += p.users

            if file_name.startswith(LOCATIONS_PREFIX):
                all_locations += p.locations

            if file_name.startswith(VISITS_PREFIX):
                all_visits += p.visits

    return {"users": [User(x) for x in all_users],
            "visits": [Visit(x) for x in all_visits],
            "locations": [Location(x) for x in all_locations]}
