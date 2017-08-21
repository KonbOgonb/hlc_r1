from flask import Flask, abort, request
from dataService import DataService
from model import ModelEncoder
from error import Error
import json
import sys

app = Flask(__name__)

@app.route('/')
def index():
    return "muhahaha"

@app.route('/<string:entityType>/<int:item_id>', methods=['GET'])
def get_item(entityType, item_id):
    result = data_service.get(entityType, item_id)
    if type(result) is Error:
        return handle_error(result)

    return result.to_json()

@app.route('/<string:entityType>/new', methods=['POST'])
def add_item(entityType):
    result = data_service.add(entityType, request.get_json(force=True))
    if type(result) is Error:
        return handle_error(result)

    return json.dumps({}), 200

@app.route('/<string:entityType>/<int:item_id>', methods=['POST'])
def update_item(entityType, item_id):
    result = data_service.update(entityType, item_id, request.get_json(force=True))
    if type(result) is Error:
        return handle_error(result)
    
    return json.dumps({}), 200

@app.route('/users/<int:item_id>/visits', methods=['GET'])
def get_user_visits(item_id):
    result = data_service.get_user_visits(item_id)
    if type(result) is Error:
        return handle_error(result)

    return json.dumps({"visits" : result}, cls=ModelEncoder, ensure_ascii=False)

def handle_error(error):
    if error == Error.NOT_FOUND:
        return abort(404)
    if error == Error.DATA_ERROR:
        return abort(400)

    return abort(500)

startupParams = {"host":"127.0.0.1", "port":5000, "debug":True}
data_service = DataService()

if "docker" in sys.argv:
    startupParams = {"host":"0.0.0.0", "port":80}

if __name__ == '__main__':
    app.run(**startupParams)
