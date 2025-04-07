from flask import Flask, request, jsonify
import psycopg2
from psycopg2 import sql
import bcrypt
import random
import os
from dotenv import load_dotenv
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

dotenv_path = os.path.join(os.path.dirname(__file__), 'sendgrid.env')
load_dotenv(dotenv_path)

class uniqueID:
    def __init__(self, minNum, maxNum):
        self.minNum = minNum
        self.maxNum = maxNum
        self.generatedIDs = set()
        
    def genID(self):
        if len(self.generatedIDs) >= (self.maxNum - self.minNum + 1):
            raise ValueError("All possible IDs have been used!")
        
        while True:
            newID = random.randint(self.minNum, self.maxNum)
            if newID not in self.generatedIDs:
                self.generatedIDs.add(newID)
                return newID

idGen = uniqueID(10000, 99999)
#print(idGen.genID())

app = Flask(__name__)

#database connection info 
db_info ={'host': "192.168.1.107",
    'port': "5432",
    'database' : "LegacyIQ",
    'user' : "postgres",
    'password':"password123"}

@app.route('/home')

def home():
    return 'Hello, World!'


@app.route('/register', methods=['POST'])
def register_user():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')
    firstName = data.get('firstName')
    lastName = data.get('lastName')
    
    
    if not email or not password or not firstName or not lastName:
        return jsonify({'message': 'Email, password, first and last name are required to register an account.'}), 400
    
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    hashed_password_str = hashed_password.decode('utf-8')
    
    try:
        conn = psycopg2.connect(**db_info)
        cur = conn.cursor()
        accountid = idGen.genID()
        blogid = idGen.genID()
        cur.execute("INSERT INTO account (accountid, blogid, accounttype, orgid) VALUES (%s, %s, %s, %s)", (accountid, blogid, "Free", idGen.genID()))
        cur.execute("INSERT INTO blog (blogid, accountid) VALUES (%s, %s)", (blogid, accountid))
        cur.execute("INSERT INTO users (userid, email, password, firstname, lastname, accountid) VALUES (%s, %s, %s, %s, %s, %s)", (idGen.genID(), email, hashed_password_str, firstName, lastName, accountid))
        conn.commit()
        cur.close()
        conn.close()
        #send confirmation email to newly created account. 
        message = Mail(
        from_email='Legacyiqdevteam@outlook.com',
        to_emails=(str(email)),
        subject='LegacyIQ Account Created',
        html_content='<strong>aThe Legacy Architects are glad you have joined the LegacyIQ community and we hope you enjoy your time. Thank you for signing up with LegacyIQ!</strong>')
        try:
            sg = SendGridAPIClient(os.environ.get('SENDGRID_API_KEY'))
            response = sg.send(message)
        except Exception as e:
            print(str(e))         
        
        return jsonify({'message': 'User created successfully. You will be recieving a confirmation email soon!'}), 201
    except Exception as e: 
        return jsonify({'message': f'Error creating user: {str(e)}'}),500

    
@app.route('/login', methods = ['POST'])

def userLogin():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')
    
    if not email or not password:
        return jsonify({'message': 'Email and Password are required to login.'}), 400
    
    hashed_password=bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    
    try:
        conn = psycopg2.connect(**db_info)
        cur = conn.cursor()
        query = sql.SQL("SELECT password FROM users WHERE email = %s")
        cur.execute(query, (email,))
        resultPassword = cur.fetchone()
        
        if resultPassword:
            stored_hash= resultPassword[0]
            if bcrypt.checkpw(password.encode('utf-8'), stored_hash.encode('utf-8')):
                return jsonify({'message': 'Correct login credentials.'}),200
            else:
                 jsonify({'message': 'Incorrect Password'}), 401 
        else:
            return jsonify({'message': 'Email not found'}), 404
        cur.close()
        conn.close()
        return jsonify({'message': 'User logged in successfully'}), 201
    except Exception as e: 
        return jsonify({'message': f'Error logging in user: {str(e)}'}),500


@app.route('/edit', methods = ['POST'])
def editAccountDetails():
    data = request.get_json()
    currentEmail = data.get('currentEmail')
    newEmail = data.get('newEmail')
    newPassword = data.get('password')
    newFirstName = data.get('firstName')
    newLastName = data.get('lastName')
    
    conn = psycopg2.connect(**db_info)
    cur = conn.cursor()
    
    if newPassword:
        try:
            new_hashed_password = bcrypt.hashpw(newPassword.encode('utf-8'), bcrypt.gensalt())
            new_hashed_password_str = new_hashed_password.decode('utf-8')
            query = sql.SQL("UPDATE users set password = %s WHERE email = %s")
            cur.execute(query, (new_hashed_password_str, currentEmail))
            conn.commit()
            return jsonify({'message': 'Password updated successfully'}), 201
        except Exception as e: 
            return jsonify({'message': f'Error updating password: {str(e)}'}),500
            
    if newFirstName:
        try:
            query = sql.SQL("UPDATE users set firstname = %s WHERE email = %s")
            cur.execute(query, (newFirstName, currentEmail))
            conn.commit()
            return jsonify({'message': 'First name updated successfully'}), 201
        except Exception as e: 
            return jsonify({'message': f'Error updating first name: {str(e)}'}),500
            
    if newFirstName:
        try:
            query = sql.SQL("UPDATE users set lastname = %s WHERE email = %s")
            cur.execute(query, (newLastName, currentEmail))
            conn.commit()
            return jsonify({'message': 'Last name updated successfully'}), 201
        except Exception as e: 
            return jsonify({'message': f'Error updating last name: {str(e)}'}),500
    
    if newEmail:
        try:
            query = sql.SQL("UPDATE users set email = %s WHERE email = %s")
            cur.execute(query, (newEmail, currentEmail))
            conn.commit()
            return jsonify({'message': 'Email updated successfully'}), 201
        except Exception as e: 
            return jsonify({'message': f'Error updating Email: {str(e)}'}),500
        
    cur.close()
    conn.close()
    
    
@app.route('/deleteAccount', methods = ['POST'])
def deleteAccount():
    conn = psycopg2.connect(**db_info)
    cur = conn.cursor()
    data = request.get_json()
    email = data.get('email')
    
    try:
        accountidQuery = sql.SQL("SELECT accountid FROM users WHERE email = %s")
        cur.execute(accountidQuery, (email,))
        accountid = cur.fetchone()
    
        blogidQuery = sql.SQL("SELECT blogid FROM account WHERE accountid = %s")
        cur.execute(blogidQuery, (accountid,))
        blogid = cur.fetchone()
        
        deleteUser = sql.SQL("DELETE FROM users WHERE email = %s")
        deleteAccount =sql.SQL("DELETE FROM account WHERE accountid = %s")
        deleteBlog = sql.SQL("DELETE FROM blog WHERE blogid = %s")
        
        cur.execute(deleteUser, (email,))
        cur.execute(deleteBlog, (blogid,))
        cur.execute(deleteAccount, (accountid,))
        
        conn.commit()
        cur.close()
        conn.close()
        return jsonify({'message' : 'Account was successfully deleted'}),204
    
    except Exception as e: 
        return jsonify({'message': f'Error deleting account: {str(e)}'}),500
        
if __name__ == '__main__':
    app.run(debug=True)
    
#Code to test in CMD 
#curl -X POST http://localhost:5000/register -H "Content-Type: application/json" -d "{\"email\":\"mikeymaher07@live.com\",\"password\":\"testing\",\"firstName\":\"Michael\",\"lastName\":\"Maher\"}"
#edit account details 
#curl -X POST http://127.0.0.1:5000/edit -H "Content-Type: application/json" -d "{\"currentEmail\": \"testing@test.com\", \"password\": \"newpassword123\"}"
#curl -X POST http://127.0.0.1:5000/edit -H "Content-Type: application/json" -d "{\"currentEmail\": \"testing@test.com\", \"firstName\": \"Danny\"}"
#curl -X POST http://127.0.0.1:5000/edit -H "Content-Type: application/json" -d "{\"currentEmail\": \"testing@test.com\", \"lastName\": \"Maher\"}"
#curl -X POST http://127.0.0.1:5000/edit -H "Content-Type: application/json" -d "{\"currentEmail\": \"testing@test.com\", \"newEmail\": \"newemail@example.com\"}"
#curl -X POST http://127.0.0.1:5000/deleteAccount -H "Content-Type: application/json" -d "{\"email\": \"newemail@example.com\"}"


