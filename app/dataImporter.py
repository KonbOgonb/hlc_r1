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
                all_users += [User(x) for x in p.users]

            if file_name.startswith(LOCATIONS_PREFIX):
                all_locations += [Location(x) for x in p.locations]

            if file_name.startswith(VISITS_PREFIX):
                all_visits += [Visit(x) for x in p.visits]


    users_dict = {user.id: user for user in all_users}
    locations_dict = {location.id: location for location in all_locations}

    for visit in all_visits:
        if visit.user in users_dict:
            users_dict[visit.user].visits.append(visit.id)
        if visit.location in locations_dict:
            locations_dict[visit.location].visits.append(visit.id)

    return {"users": all_users,
            "visits": all_visits,
            "locations": all_locations}
