from flask import *
from flask_socketio import SocketIO, emit

import uuid
from uuid import UUID

import json
import os

main_storage_path = 'storage/storage.json'
email_storage_path = 'storage/emails.json'

app = Flask(__name__)
socketio = SocketIO(app)

class storage:
    data = {}
    email_data = {}

    def store_ticket(id,new_ticket):
        if storage.data == {}:
            storage.retrieve_data()

        storage.data[id] = new_ticket

        if new_ticket["email"] != "":
            storage.email_data[new_ticket["email"]] = id

        with open("storage/storage.json", "w") as outfile:
            json.dump(storage.data,outfile)
        
        with open("storage/emails.json", "w") as outfile:
            json.dump(storage.email_data,outfile)


    def retrieve_data():
        if not os.path.isfile(main_storage_path):
            print("Storage file does not exist. It will be created once the first ticket has been created.")
            return
        
        with open('storage/storage.json', 'r') as openfile:
            json_object = json.load(openfile)
            storage.data = json_object

        if not os.path.isfile(email_storage_path):
            print("Email storage file does not exist. It will be created once the first ticket has been created.")
            return
        
        with open('storage/emails.json', 'r') as openfile:
            json_object = json.load(openfile)
            storage.email_data = json_object


    def check_for_email(email):
        storage.retrieve_data()
        return str(email in storage.email_data)

class ticket:
    def create_ticket(data):
        ticket_data = data
        new_id = ticket.create_uuid()
        res = { "id" : "",
                "status" : "",
                "ticket" : ""}

        if data["email"] != "":
            if data["email"] in storage.email_data:
                res["status"] = "1"
                res["id"] = ticket.retrive_uuid(data["email"])
                res["ticket"] = ticket.read_ticket_by_email(data["email"])
                return res

        storage.store_ticket(new_id, ticket_data)
        res["status"] = "0"
        res["id"] = new_id
        res["ticket"] = ticket_data
        
        return res

    def read_all_tickets():
        storage.retrieve_data()
        return storage.data

    def read_ticket(id):
        storage.retrieve_data()

        if id in storage.data:
            return storage.data[id]

        return str("Ticket with UUID: " + id + " Was not found.")

    def read_ticket_by_email(email):
        storage.retrieve_data()

        if email in storage.email_data:
            return storage.data[storage.email_data[email]]
        
        return str("Ticket with EMAIL: " + email + " Was not found.")

    def retrive_uuid(email):
        storage.retrieve_data()
        if email in storage.email_data:
            return storage.email_data[email]

        return str("Email: " + email + " Was not found.")

    def create_uuid():
        id = str(uuid.uuid1())
        return id

@app.route('/', methods=['GET'])
def main():
    return "GTS Online"

@app.route('/tickets/', methods=['GET'])
def get_tickets():
    ticket.read_all_tickets()

@app.route('/ticket_by_id/<string:id>/', methods=['GET'])
def get_ticket(id):
    return ticket.read_ticket(id)

@app.route('/ticket_by_email/<string:email>/', methods=['GET'])
def get_ticket_by_email(email):
    return ticket.read_ticket_by_email(email)

@app.route('/check_for_email/<string:email>/', methods=['GET'])
def check_for_email(email):
    return storage.check_for_email(email)


@app.route('/upload', methods=['GET','POST'])
def upload_ticket():
    return ticket.create_ticket(request.json)

socketio.run(app,host="0.0.0.0",port=1477, allow_unsafe_werkzeug=True, debug=True)