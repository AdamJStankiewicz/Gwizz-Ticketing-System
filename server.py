from flask import *
from flask_socketio import SocketIO, emit
import uuid
import json
import os

storage_path = 'storage/storage.json'
test_desc = "Djo is such a fucking vibe"
app = Flask(__name__)
socketio = SocketIO(app)

class storage:
    data = {}

    def store_ticket(id,new_ticket):
        if storage.data == {}:
            storage.retrieve_data()

        storage.data[id] = new_ticket
        with open("storage/storage.json", "w") as outfile:
            json.dump(storage.data,outfile)


    def retrieve_data():
        if not os.path.isfile(storage_path):
            print("Storage file does not exist. It will be created once the first ticket has been created.")
            return
        with open('storage/storage.json', 'r') as openfile:
            json_object = json.load(openfile)
        
        storage.data = json_object

class ticket:
    def create_ticket(desc):
        ticket_data = {"desc" : desc}
        new_id = ticket.create_uuid()

        storage.store_ticket(new_id, ticket_data)

    def read_ticket(id):
        if id in storage.data:
            return storage.data[id]
        
        return str("Ticket with UUID: " + id + " Was not found")

    def create_uuid():
        id = str(uuid.uuid1())
        return id


@app.route('/', methods=['GET'])
def main():
    return "GTS Online"

@app.route('/tickets/', methods=['GET'])
def get_tickets():
    storage.retrieve_data()
    return storage.data

@app.route('/tickets/<string:id>/', methods=['GET'])
def get_ticket(id):
    storage.retrieve_data()
    return storage.data[id]

@app.route('/upload', methods=['POST'])
def upload_ticket():
    desc = request.json["desc"]
    ticket.create_ticket(desc)

    return "Ticket uploaded"

socketio.run(app,host="0.0.0.0",port=1477, allow_unsafe_werkzeug=True, debug=True)