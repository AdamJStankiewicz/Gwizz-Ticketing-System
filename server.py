from flask import *
from flask_socketio import SocketIO, emit

import uuid
import sqlite3

main_storage_path = 'storage/storage.json'
email_storage_path = 'storage/emails.json'

app = Flask(__name__)
socketio = SocketIO(app)

connection = sqlite3.connect('gts.db', check_same_thread=False)
cursor = connection.cursor()

class db:
    def initiate_db():
        sql_command = """CREATE TABLE emp (
        UUID VARCHAR(36),
        desc VARCHAR(300),
        email VARCHAR(50)
        );"""
        cursor.execute(sql_command)

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
        return id

    def delete_ticket_by_email(email):
        if not db.exists("",email):
            return
        id = ticket.get_ticket_by_email(email)["id"]
        cursor.execute("DELETE FROM emp WHERE UUID = (?)", (id,))
        print("Ticket removed from database!")
        connection.commit()
        return id

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

    def remove_ticket_by_id(id):
        res = db.delete_ticket_by_id(id)
        return str("Removed Ticket: " + res + " From Database")

    def remove_ticket_by_email(email):
        res = db.delete_ticket_by_email(email)
        return str("Removed Ticket: " + res + " From Database")
    
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

@app.route('/remove_ticket_by_id/<string:id>/', methods=['GET','POST'])
def remove_ticket_by_id(id):
    return ticket.remove_ticket_by_id(id)

@app.route('/remove_ticket_by_email/<string:email>/', methods=['GET','POST'])
def remove_ticket_by_email(email):
    return ticket.remove_ticket_by_email(email)


socketio.run(app,host='0.0.0.0',port=1477, allow_unsafe_werkzeug=True, debug=False)
print("GTS RUNNING")