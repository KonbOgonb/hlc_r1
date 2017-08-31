PATH_TO_DATA = "../tmp/data/data.zip"
USERS_PREFIX = "users"
VISITS_PREFIX = "visits"
LOCATIONS_PREFIX = "locations"
ALL_PREFIXES = [USERS_PREFIX, VISITS_PREFIX, LOCATIONS_PREFIX]
WORKIGN_DIRECTORY = "./local_temp"

from zipfile import ZipFile
import json
from os import listdir
from os.path import isfile, join, exists
from model import User, Location, Visit
from repository import UserRepository, VisitRepository, LocationRepository
import time

class Payload(object):
    def __init__(self, j):
        self.__dict__ = json.loads(j)

def read_all_data():
    with ZipFile(PATH_TO_DATA) as inputzip:
        inputzip.extractall(WORKIGN_DIRECTORY)

    process_all(WORKIGN_DIRECTORY + "/data")
    process_all(WORKIGN_DIRECTORY)

def process_all(path):
    if not exists(path):
        return

    files = [f for f in listdir(path) if isfile(join(path, f))]

    users_files = [f for f in files if f.startswith(USERS_PREFIX)]
    locations_files = [f for f in files if f.startswith(LOCATIONS_PREFIX)]
    visits_files = [f for f in files if f.startswith(VISITS_PREFIX)]

    user_repository = UserRepository()
    location_repository = LocationRepository()  
    visit_repository = VisitRepository()  

    print("started loading users", time.time())

    for file_name in users_files:
        with open(join(path, file_name), encoding='utf-8') as f:
            p = Payload(f.read())
            user_repository.add_multi(p.users)

    print("started loading locations", time.time())

    user_repository.get_item("location1")

    for file_name in locations_files:
        with open(join(path, file_name), encoding='utf-8') as f:
            p = Payload(f.read())
            location_repository.add_multi(p.locations)

    print("started loading visits", time.time())

    for file_name in visits_files:
        with open(join(path, file_name), encoding='utf-8') as f:
            print(file_name)
            p = Payload(f.read())
            visit_repository.add_multi(p.visits)

            users_to_update = {}
            locations_to_update = {}
            for x in p.visits:
                visit = Visit(x)
                if visit.user in users_to_update:
                    users_to_update[visit.user].append(visit.id)
                else:
                    users_to_update[visit.user] = [visit.id]
                if visit.location in locations_to_update:
                    locations_to_update[visit.location].append(visit.id)
                else:
                    locations_to_update[visit.location] = [visit.id]

            users = user_repository.get_multi(users_to_update.keys())
            locations = location_repository.get_multi(locations_to_update.keys())

            for k,v in users_to_update.items():
                user = users[user_repository.get_key(k)]
                if not user.visits:
                    user.visits = v
                else:
                    user.visits += v
            for k,v in locations_to_update.items():
                location = locations[location_repository.get_key(k)]
                if not location.visits:
                    location.visits = v
                else:
                    location.visits += v

            location_repository.update_multi(locations)
            user_repository.update_multi(users)

    print("finished loading data", time.time())

read_all_data()