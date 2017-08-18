from flask import Flask
from flask import abort
from flask import jsonify
from flask import request
from data_repository import Data_repository

PATH_TO_DATA = "tmp/data/data.zip"

app = Flask(__name__)

@app.route('/')
def index():
    return "muhahaha"

@app.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    user = repository.get_user(user_id)
    if not user:
        abort(404)

    return user.to_json()

@app.route('/users/new', methods=['POST'])
def add_user():
    result = repository.add_user(request.get_json(force=True))
    if not result:
        return jsonify({}), 200

    return abort(result)


@app.route('/users/<int:user_id>', methods=['POST'])
def update_user(user_id):
    result = repository.update_user(user_id, request.get_json(force=True))
    if not result:
        return jsonify({}), 200
        
    return abort(result)

repository = Data_repository(PATH_TO_DATA)

if __name__ == '__main__':
    app.run(debug=True)
