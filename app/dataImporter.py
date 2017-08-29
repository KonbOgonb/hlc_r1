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
from time import sleep

class Payload(object):
    def __init__(self, j):
        self.__dict__ = json.loads(j)

def read_all_data():
    with ZipFile(PATH_TO_DATA) as inputzip:
        inputzip.extractall(WORKIGN_DIRECTORY)

    sleep(1.05)


    process_all(WORKIGN_DIRECTORY + "/data")
    process_all(WORKIGN_DIRECTORY)

def process_all(path):
    if not exists(path):
        return

    files = [f for f in listdir(path) if isfile(join(path, f))]

    all_users = []
    all_locations = []
    all_visits = []
    print(path)
    print(files)

    for file_name in files:
        print(file_name)
        if not any(file_name.startswith(prefix) for prefix in ALL_PREFIXES):
            continue

        with open(join(path, file_name), encoding='utf-8') as f:
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

    print("total users: ", len(all_users))
    print("total locations: ", len(all_locations))
    print("total visits: ", len(all_visits))

    user_repository = UserRepository()
    for user in all_users:
        user_repository.add_item(user)

    location_repository = LocationRepository()  
    for location in all_locations:
        location_repository.add_item(location)

    visit_repository = VisitRepository()  
    for visit in all_visits:
        visit_repository.add_item(visit)

read_all_data()