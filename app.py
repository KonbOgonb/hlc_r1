#!flask/bin/python
from flask import Flask
from dataImporter import getUsers


path_to_data = "tmp/data/data.zip"

app = Flask(__name__)

@app.route('/')
def index():	
    return "muhahaha"

@app.route('/users/<int:user_id>', methods=['GET'])
def getUser(user_id):
    user = users[user_id]
    return users[user_id].toJson()

users = {key: user for (key, user) in [(user.id, user) for user in getUsers(path_to_data)]}

if __name__ == '__main__':
    app.run(debug=True)