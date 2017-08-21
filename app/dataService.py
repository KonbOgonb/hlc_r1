from repository import UserRepository, VisitsRepository, LocationsRepository
from dataImporter import read_all_data
from error import Error
from messageBus import MessageBus

PATH_TO_DATA = "../tmp/data/data.zip"

class DataService(object):
    def __init__(self):
        data = read_all_data(PATH_TO_DATA)
        self.user_repository = UserRepository(data)
        self.locations_repository = LocationsRepository(data)
        self.visits_repository = VisitsRepository(data)

        self.repositories = {"users": self.user_repository,
                "locations" : self.locations_repository,
                "visits" : self.visits_repository}

        self.messageBus = MessageBus()
        self.messageBus.register_handler(("add", "visits"), self.add_visit_handler)

    def add_visit_handler(self, visit):
        user = self.user_repository.get_item(visit.user)

        if not user:
            return Error.DATA_ERROR

        if visit.id not in user.visits:
            user.visits.append(visit.id)

        location = self.locations_repository.get_item(visit.location)

        if not location:
            return Error.DATA_ERROR

        if visit.id not in location.visits:
            location.visits.append(visit.id)

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
        result = repository.add_item(data)

        self.messageBus.fire_event(("add", entityType), visit=result)

    def update(self, entityType, id, data):
        if entityType not in self.repositories:
            return Error.NOT_FOUND

        repository = self.repositories[entityType]
        repository.update_item(id, data)

    def get_user_visits(self, user_id):
        user = self.user_repository.get_item(user_id)

        if not user:
            return Error.NOT_FOUND

        return [self.visits_repository.get_item(v) for v in user.visits]