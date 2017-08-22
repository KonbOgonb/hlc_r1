from repository import UserRepository, VisitsRepository, LocationsRepository
from dataImporter import read_all_data
from error import Error
from messageBus import MessageBus
from datetime import datetime
import time

PATH_TO_DATA = "../tmp/data/data.zip"

class DataService(object):
    def __init__(self):
        data = read_all_data(PATH_TO_DATA)
        self.users_repository = UserRepository(data)
        self.locations_repository = LocationsRepository(data)
        self.visits_repository = VisitsRepository(data)

        self.repositories = {"users": self.users_repository,
                "locations" : self.locations_repository,
                "visits" : self.visits_repository}

        self.messageBus = MessageBus()
        self.messageBus.register_handler(("add", "visits"), self.add_visit_handler)
        self.messageBus.register_handler(("update", "visits"), self.update_visit_handler)

    def add_visit_handler(self, visit):
        user = self.users_repository.get_item(visit.user)

        if not user:
            return Error.DATA_ERROR

        if visit.id not in user.visits:
            user.visits.append(visit.id)

        location = self.locations_repository.get_item(visit.location)

        if not location:
            return Error.DATA_ERROR

        if visit.id not in location.visits:
            location.visits.append(visit.id)

    def update_visit_handler(self, visit_id, data):
        visit = self.visits_repository.get_item(visit_id)
        if not visit:
            raise KeyError
        if "user" in data:
            old_user = self.users_repository.get_item(visit.user)
            old_user.visits.remove(visit_id)
            new_user = self.users_repository.get_item(data["user"])
            new_user.visits.append(visit_id)
        if "location" in data:
            old_location = self.locations_repository.get_item(visit.location)
            old_location.visits.remove(visit_id)
            new_location = self.locations_repository.get_item(data["location"])
            new_location.visits.append(visit_id)

    def get(self, entityType, id):
        if entityType not in self.repositories:
            return Error.NOT_FOUND

        repository = self.repositories[entityType]
        item = repository.get_item(id)

        if not item:
            return Error.NOT_FOUND

        return item

    def add(self, entityType, data):
        if entityType not in self.repositories:
            return Error.NOT_FOUND

        repository = self.repositories[entityType]

        try:
            result = repository.add_item(data)
            self.messageBus.fire_event(("add", entityType), visit=result)
        except:
            return Error.DATA_ERROR


    def update(self, entityType, id, data):
        if entityType not in self.repositories:
            return Error.NOT_FOUND

        repository = self.repositories[entityType]

        try:
            self.messageBus.fire_event(("update", entityType), visit_id=id, data=data)
            repository.update_item(id, data)
        except KeyError:
            return Error.NOT_FOUND
        except:
            return Error.DATA_ERROR

    def get_user_visits(self, user_id, args):
        user = self.users_repository.get_item(user_id)

        if not user:
            return Error.NOT_FOUND

        try:
            filters = [self.create_filter(k,v) for (k,v) in args.items()]

            result = []
            for visitId in user.visits:
                visit = self.visits_repository.get_item(visitId)
                location = self.locations_repository.get_item(visit.location)
                failed = False
                for f in filters:
                    if not f({"visit":visit, "location":location, "user":user}):
                        failed = True
                if not failed:
                    result.append({"mark":visit.mark, "place":location.place, "visited_at":visit.visited_at})
        except:
            return Error.DATA_ERROR

        return sorted(result, key = lambda x : x["visited_at"])

    def get_location_average(self, location_id, args):
        location = self.locations_repository.get_item(location_id)

        if not location:
            return Error.NOT_FOUND
        try:
            filters = [self.create_filter(k,v) for (k,v) in args.items()]

            result = []
            for visitId in location.visits:
                visit = self.visits_repository.get_item(visitId)
                user = self.users_repository.get_item(visit.user)
                failed = False

                for f in filters:
                    if not f({"visit":visit, "user":user}):
                        failed = True
                if not failed:
                    result.append(visit.mark)
        except:
            return Error.DATA_ERROR

        if len(result) > 0:
            return sum(result) / len(result)

        return 0

    def create_filter(self, key, value):
        def from_date():
            converted_value = int(value)
            return lambda x: converted_value < x["visit"].visited_at

        def to_date():
            converted_value = int(value)
            return lambda x: converted_value > x["visit"].visited_at

        def gender():
            if value not in ["f", "m"]:
                raise ValueError

            return lambda x: x["user"].gender == value

        def country():
            return lambda x: x["location"].country == value

        def toDistance():
            converted_value = int(value)
            return lambda x: converted_value > x["location"].distance 

        def fromAge():
            limit = int(value) * 31540000
            return lambda x: limit < time.time() - x["user"].birth_date

        def toAge():
            limit = int(value) * 31540000
            return lambda x: limit > time.time() - x["user"].birth_date

        dct = {"fromDate" : from_date,
                "toDate" : to_date,
                "gender" : gender,
                "country" : country,
                "toDistance" : toDistance,
                "fromAge":fromAge,
                "toAge":toAge}

        return dct[key]()

