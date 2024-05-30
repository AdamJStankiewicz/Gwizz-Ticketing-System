from flask import *
from flask_socketio import SocketIO, emit

import hashlib
import uuid
import sqlite3
import os

main_storage_path = 'admin_info.json'

app = Flask(__name__)
socketio = SocketIO(app)

connection = sqlite3.connect('gts.db', check_same_thread=False)
cursor = connection.cursor()


def init():
    if not os.path.exists('gts.db'):
        connection.execute("CREATE TABLE admin_info (password)")
        connection.commit()

    admin_info = {}
    if not os.path.exists(main_storage_path):
        password = input("Enter an admin password: ")
        admin_info['password'] = security.new_password(password)
    
    print("G.T.S. INITIATED")

class security:
    def valid_password(password):
        admin_info = {}
        if os.path.exists(main_storage_path):
            with open(main_storage_path, 'r') as f:
                admin_info = json.load(f)
        password_hash = admin_info['password']
        return security.sha256(password) == password_hash
    
    def new_password(password):
        admin_info = {}
        if os.path.exists(main_storage_path):
            with open(main_storage_path, 'r') as f:
                admin_info = json.load(f)
        admin_info['password'] = security.sha256(password)
        with open(main_storage_path, 'w') as f:
            json.dump(admin_info, f)
        
        return admin_info

    def sha256(string):
        encoded_string = string.encode()
        sha256_hash = hashlib.sha256()
        sha256_hash.update(encoded_string)
        result = sha256_hash.hexdigest()
        
        return result

class db:
    def initiate_db():
        sql_command = """CREATE TABLE emp (
        UUID VARCHAR(36),
        desc VARCHAR(300),
        email VARCHAR(50)
        );"""
        cursor.execute(sql_command)
        print("DATABASE INITIATED")

    def print_db():
        cursor.execute("SELECT * FROM emp")
        ans = cursor.fetchall()

        return ans
    
    def store_ticket(new_id,new_ticket):
        id = new_id
        desc = new_ticket["desc"]
        email = new_ticket["email"]
        db.insert(id,desc,email)

    def delete_ticket_by_id(id):
        if not db.exists(id):
            return
        cursor.execute("DELETE FROM emp WHERE UUID = (?)", (id,))
        print("Ticket removed from database!")
        connection.commit()
        return str("Ticket with id " + id + " was removed from the database")

    def delete_ticket_by_email(email):
        if not db.exists("",email):
            return
        id = ticket.get_ticket_by_email(email)["id"]
        cursor.execute("DELETE FROM emp WHERE UUID = (?)", (id,))
        print("Ticket removed from database!")
        connection.commit()
        return str("Ticket with id " + id + " was removed from the database")

    def insert(id,desc,email):
        cursor.execute("INSERT INTO emp VALUES (?, ?, ?)", (id, desc, email))
        print("New ticket added to database!")
        connection.commit()
    
    def exists(id="",email=""):
        cursor.execute("""SELECT UUID
                            ,email
                    FROM emp
                    WHERE UUID=?
                        OR email=?""",
                    (id, email))
        
        result = cursor.fetchone()
        return result

class ticket:
    def create_ticket(data):
        ticket_data = data
        new_id = ticket.create_uuid()
        new_email = data["email"]

        res = {}

        if db.exists(new_id,new_email):
            res["status"] = "1"
            print(ticket.get_ticket_by_email(new_email))
            res["id"] = ticket.get_ticket_by_email(new_email)["id"]
            return res
            
        db.store_ticket(new_id, ticket_data)
        res["status"] = "0"
        res["id"] = new_id
        res["ticket"] = ticket_data
        
        return res

    def get_ticket_by_id(id):
        cursor.execute("SELECT desc, email FROM emp WHERE UUID = ?",(id,))
        
        result = cursor.fetchone()
        print("RESULT: ", result)
        if result:
            res = {"desc" : result[0],
                   "email" : result[1]}
            return res
        return None

    def get_ticket_by_email(email):
        cursor.execute("SELECT desc, UUID FROM emp WHERE email = ?",(email,))

        result = cursor.fetchone()
        print("RESULT: ", result)
        if result:
            res = {"desc" : result[0],
                   "id" : result[1]}
            return res
        return str("EMAIL: " + email + " Was not found in the database")

    def get_email(email):
        exists = db.exists("",email)

        if exists:
            return exists[1]
        return None

    def get_uuid(id):
        exists = db.exists(id,"")

        if exists:
            return exists[0]
        return None

    def remove_ticket(data):
        if not security.valid_password(data["password"]):
            return "ERROR: INVALID ADMIN PASSWORD"

        if data["email"]:
            if ticket.get_email(data["email"]):
                return db.delete_ticket_by_email(data["email"])
            return "ERROR: EMAIL NOT FOUND"
        elif data["id"]:
            if ticket.get_id(data["id"]):
                return db.delete_ticket_by_id(data["id"])
            return "ERROR: ID NOT FOUND"
        else:
            return "ERROR: Invalid input. Please enter a valid ID or Email."

    def create_uuid():
        id = str(uuid.uuid1())
        return id

@app.route('/', methods=['GET'])
def main():
    return "GTS Online"

@app.route('/tickets/', methods=['GET'])
def get_tickets():
    return db.print_db()

@app.route('/ticket_by_id/<string:id>/', methods=['GET'])
def get_ticket(id):
    return ticket.get_ticket_by_id(id)

@app.route('/ticket_by_email/<string:email>/', methods=['GET'])
def get_ticket_by_email(email):
    return ticket.get_ticket_by_email(email)

@app.route('/upload', methods=['GET','POST'])
def upload_ticket():
    return ticket.create_ticket(request.json)

@app.route('/remove_ticket/', methods=['GET','POST'])
def remove_ticket():
    return ticket.remove_ticket(request.json)


init()
#print("poopymonkey: ", security.string_to_sha256("poopymonkey"))
#app.run()
socketio.run(app,host='0.0.0.0',port=1477, allow_unsafe_werkzeug=True, debug=False)