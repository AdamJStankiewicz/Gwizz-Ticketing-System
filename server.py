from flask import Flask, request, jsonify
from flask_socketio import SocketIO, emit
from flask_cors import CORS

import re
import requests
from bs4 import BeautifulSoup
import datetime
import hashlib
import uuid
import sqlite3
import os
import json 

admin_storage_path = 'admin_info.json'

app = Flask(__name__)
CORS(app)
socketio = SocketIO(app)

connection = sqlite3.connect('gts.db', check_same_thread=False)
cursor = connection.cursor()

def init():
    if not os.path.exists(admin_storage_path):
        password = input("Enter an admin password: ")
        salt = input("Enter a salt word for better encryption: ")
        security.new_password(password,salt)
        db.initiate_db()
    
    print("G.T.S. INITIATED")
    print("Current time: " + str(datetime.datetime.now()))
    
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
        email VARCHAR(50),
        time VARCHAR(50),
        completed VARCHAR(1),
        url VARCHAR(50),
        title VARCHAR(50)
        );"""
        cursor.execute(sql_command)
        print("DATABASE INITIATED")

    def print_db():
        cursor.execute("SELECT * FROM emp")
        ans = cursor.fetchall()
        res = {}
        for row in ans:
            res[row[0]] = {"desc" : row[1], "email" : row[2], "time" : row[3], "completed" : row[4], "url" : row[5], "title" : row[6]}
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

    def update_ticket(url, title, id, completed):
        if completed:
            print("ID:", id)
            cursor.execute("UPDATE emp SET completed = ?, url = ?, title = ? WHERE UUID = ?", (1, url, title, id))
            connection.commit()
            return str("Ticket with id: " + id + " has been marked as completed, associated video info has been added")
        else:
            cursor.execute("UPDATE emp SET completed = ?, url = ?, title = ? WHERE UUID = ?", (0, "", "", id))
            connection.commit()
            return "Ticket with id: " + id + " has been marked as uncompleted, associated video info has been removed"

    def insert(id,desc,email):
        cursor.execute("INSERT INTO emp VALUES (?, ?, ?, ?, ?, ?, ?)", (id, desc, email, str(datetime.datetime.now()), 0, "", ""))
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

        if not ticket.valid_email(new_email):
            res["status"] = "1"
            return res

        if db.exists(new_id,new_email):
            res["status"] = "2"
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

    def get_tickets_by_date(date):
        cur_db = db.print_db()
        res = {}
        for ticket in cur_db:
            if date in cur_db[ticket]["time"]:
                res[ticket] = cur_db[ticket]
        return res

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

        if ticket.get_email(data["email"]):
            return db.delete_ticket_by_email(data["email"])
        elif ticket.get_uuid(data["id"]):
            return db.delete_ticket_by_id(data["id"])
        else:
            return "ERROR: Invalid input. Please enter a valid ID or Email."

    def update_ticket(data):
        if not security.valid_password(data["password"]):
            return "ERROR: INVALID ADMIN PASSWORD"
        
        id = data["id"]
        completed = data["completed"]

        if not completed:
             return db.update_ticket("", "", id, completed)

        url = data["url"]
        title = ticket.get_video_title(url)
        
        if ticket.get_uuid(data["id"]):
            id = data["id"]
        elif ticket.get_email(data["email"]):
            id = ticket.get_ticket_by_email(data["email"])["id"]
        else:
            return "ERROR: Invalid input."
        
        return db.update_ticket(url, title, id, completed)

    def get_video_title(url):
        r = requests.get(url)
        soup = BeautifulSoup(r.text,"html.parser")
        link = soup.find_all(name="title")[0]
        res = str(link.text.strip(" - YouTube"))

        return res


    def create_uuid():
        id = str(uuid.uuid1())
        return id


    def valid_email(email):
        return bool(re.search(r"^[\w\.\+\-]+\@[\w]+\.[a-z]{2,3}$", email))    

@app.route('/', methods=['GET'])
def main():
    print("Hello")
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

@app.route('/tickets_by_date/<string:date>', methods=['GET','POST'])
def get_tickets_by_date(date):
    return ticket.get_tickets_by_date(date)

@app.route('/upload', methods=['GET','POST'])
def upload_ticket():
    return ticket.create_ticket(request.json)

@app.route('/remove_ticket/', methods=['GET','POST'])
def remove_ticket():
    return ticket.remove_ticket(request.json)

@app.route('/update_ticket', methods=['GET','POST'])
def update_ticket():
    return ticket.update_ticket(request.json)

init()
socketio.run(app,host='0.0.0.0',port=1477, allow_unsafe_werkzeug=True, debug=False)