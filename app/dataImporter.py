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
                for x in p.users:
                    user_repository.add_item(User(x))

    print("started loading locations", time.time())

    for file_name in locations_files:
        with open(join(path, file_name), encoding='utf-8') as f:
            p = Payload(f.read())
                for x in p.locations:
                    location_repository.add_item(Location(x))

    print("started loading visits", time.time())

    for file_name in visits_files:
        with open(join(path, file_name), encoding='utf-8') as f:
            p = Payload(f.read())
                for x in p.visits:
                    visit_repository.add_item(Visit(x))
                    user = user_repository.get_item(visit.user)
                    user.visits.append(visit.id)
                    user_repository.update_item(user)
                    location = location_repository.get_item(visit.location)
                    location.visits.append(visit.id)
                    location_repository.update_item(location)

    print("finished loading visits", time.time())

read_all_data()