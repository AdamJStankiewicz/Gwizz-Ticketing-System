from flask import *
from flask_socketio import SocketIO, emit

import public_ip as ip
import hashlib
import uuid
import sqlite3
import os

admin_storage_path = 'admin_info.json'

app = Flask(__name__)
socketio = SocketIO(app)

connection = sqlite3.connect('gts.db', check_same_thread=False)
cursor = connection.cursor()


def init():

    admin_info = {}
    if not os.path.exists(admin_storage_path):
        password = input("Enter an admin password: ")
        salt = input("Enter a salt word for better encryption: ")
        security.new_password(password,salt)
        db.initiate_db()
    
    print("G.T.S. INITIATED")
    print("IP: " + ip.get(), "Port: 1477")
    
class security:
    def valid_password(password):
        admin_info = {}
        if os.path.exists(admin_storage_path):
            with open(admin_storage_path, 'r') as f:
                admin_info = json.load(f)
        password_hash = admin_info['password']
        password_salt = admin_info['salt']
        return security.encrypt_password(password,password_salt) == password_hash
    
    def new_password(password,salt):
        admin_info = {}
        if os.path.exists(admin_storage_path):
            with open(admin_storage_path, 'r') as f:
                admin_info = json.load(f)
        admin_info['salt'] = salt
        admin_info['password'] = security.encrypt_password(password,salt)
        with open(admin_storage_path, 'w') as f:
            json.dump(admin_info, f)
        
        return admin_info

    def encrypt_password(password,salt):
        password = password + salt
        print(password)
        encoded_string = password.encode()
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
        res = {}
        for row in ans:
            res[row[0]] = {"desc" : row[1], "email" : row[2]}
        return res
    
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
socketio.run(app,host='0.0.0.0',port=1477, allow_unsafe_werkzeug=True, debug=False)