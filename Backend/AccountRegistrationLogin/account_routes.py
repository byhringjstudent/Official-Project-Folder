from flask import request, jsonify, session, Blueprint, redirect, url_for, flash
import psycopg2
from psycopg2 import sql
import bcrypt
import random
import os
from dotenv import load_dotenv
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from flaskAppConfig import db_info
from utils import uniqueID
from EmailVerification.email_verification_routes import send_verification_email

dotenv_path = os.path.join(os.path.dirname(__file__), 'flask-app.env')
load_dotenv(dotenv_path)

idGen = uniqueID(10000, 99999, db_info)
#print(idGen.genID())



app_bp = Blueprint('account_routes', __name__)

@app_bp.route('/register', methods=['POST'])
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
        cur.execute("INSERT INTO account (accountid, accounttype, orgid) VALUES (%s, %s, %s)", (accountid, "Free", idGen.genID()))
        cur.execute("INSERT INTO users (userid, email, password, firstname, lastname, accountid) VALUES (%s, %s, %s, %s, %s, %s)", (idGen.genID(), email, hashed_password_str, firstName, lastName, accountid))
        conn.commit()
        cur.close()
        conn.close()
        #send confirmation email to newly created account. 
        send_verification_email(email)
                 
        
        return jsonify({'message': 'User created successfully. You will be recieving a confirmation email soon!'}), 201
    except Exception as e: 
        return jsonify({'message': f'Error creating user: {str(e)}'}),500

    
@app_bp.route('/login', methods = ['POST'])

def userLogin():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')
    if session.get('accountid'):
        return jsonify({"message": 'User already logged in'}), 401
    
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
                userAccountIDQuery = sql.SQL("SELECT accountid FROM users WHERE email = %s")
                userIDQuery = sql.SQL("SELECT userid FROM users WHERE email = %s")
                cur.execute(userAccountIDQuery, (email,))
                accountid = cur.fetchone()[0]
                cur.execute(userIDQuery, (email,))
                userid = cur.fetchone()[0]
                cur.close()
                conn.close()
                session['accountid'] = accountid
                session['userid'] = userid
                #print(accountid)
                #print(userid)
                #print(userAccountid)
                return jsonify({'message': 'Correct login credentials.'}),200
            else:
                 jsonify({'message': 'Incorrect Password'}), 401 
        else:
            return jsonify({'message': 'Email not found'}), 404
    

        
        return jsonify({'message': 'User logged in successfully'}), 201
    except Exception as e: 
        return jsonify({'message': f'Error logging in user: {str(e)}'}),500

@app_bp.route('/logout', methods = ['POST'])
def userLogout():
    try:
        session.clear()
        #flash('You have been logged out.')
        print('User logged out successfully', dict(session))
        return jsonify({'message': 'Logged out successfully'})
        return redirect(url_for('login'))    
    except Exception as e:
        return jsonify({'message': 'Log out unsuccessful'}), 500   

@app_bp.route('/viewAccountDetails', methods = ['GET'])
def viewAccountDetails():
    conn = psycopg2.connect(**db_info)
    cur = conn.cursor()
    accountid = session.get('accountid')
    
    if not accountid:
        return jsonify({'message': 'User not logged in'}), 401
    
    try:
        query = sql.SQL("SELECT email, firstname, lastname FROM users WHERE accountid = %s")
        cur.execute(query, (accountid,))
        userDetails = cur.fetchone()
        
        if userDetails:
            email, firstName, lastName = userDetails
            cur.close()
            conn.close()
            return jsonify({'email': email, 'firstName': firstName, 'lastName': lastName}), 20
        else:
            return jsonify({'message': 'User not found'}), 404
    except Exception as e: 
        return jsonify({'message': f'Error retrieving account details: {str(e)}'}),500

    


@app_bp.route('/edit', methods = ['PUT'])
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
            
    if newLastName:
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
    
    
@app_bp.route('/deleteAccount', methods = ['POST'])
def deleteAccount():
    conn = psycopg2.connect(**db_info)
    cur = conn.cursor()
    data = request.get_json()
    email = data.get('email')
    
    try:
        accountidQuery = sql.SQL("SELECT accountid FROM users WHERE email = %s")
        cur.execute(accountidQuery, (email,))
        accountid = cur.fetchone()
    
        
        deleteUser = sql.SQL("DELETE FROM users WHERE accountid = %s")
        deleteAccount =sql.SQL("DELETE FROM account WHERE accountid = %s")
        deleteBlog = sql.SQL("DELETE FROM blog WHERE accountid= %s")
        
        cur.execute(deleteUser, (accountid,))
        cur.execute(deleteBlog, (accountid,))
        cur.execute(deleteAccount, (accountid,))
        
        conn.commit()
        cur.close()
        conn.close()
        return jsonify({'message' : 'Account was successfully deleted'}),204
    
    except Exception as e: 
        return jsonify({'message': f'Error deleting account: {str(e)}'}),500
        
#Code to test in CMD 
#curl -X POST http://localhost:5000/account/register -H "Content-Type: application/json" -d "{\"email\": \"mikeymaher71@gmail.com\",\"password\":\"what\",\"firstName\":\"Michael\",\"lastName\":\"Simko\"}"
#edit account details 
#curl -X PUT http://127.0.0.1:5000/account/edit -H "Content-Type: application/json" -d "{\"currentEmail\": \"testing@test.com\", \"password\": \"newpassword123\"}"
#curl -X PUT http://127.0.0.1:5000/account/edit -H "Content-Type: application/json" -d "{\"currentEmail\": \"mikeymaher07@live.com\", \"firstName\": \"Michael\"}"
#curl -X PUT http://127.0.0.1:5000/account/edit -H "Content-Type: application/json" -d "{\"currentEmail\": \"testing@test.com\", \"lastName\": \"Maher\"}"
#curl -X PUT http://127.0.0.1:5000/account/edit -H "Content-Type: application/json" -d "{\"currentEmail\": \"testing@test.com\", \"newEmail\": \"newemail@example.com\"}"
#curl -X POST http://127.0.0.1:5000/account/deleteAccount -H "Content-Type: application/json" -d "{\"email\": \"mikeymaher71@gmail.com\"}"
#curl -X POST http://127.0.0.1:5000/account/login -H "Content-Type: application/json" -d "{\"email\": \"mahermikey71@gmail.com\", \"password\": \"what\"}" -c cookies.txt
#curl -i -X POST http://127.0.0.1:5000/account/logout - b cookies.txt
#Testing blog Features
#curl -X POST http://127.0.0.1:5000/blog/createposts -H "Content-Type: application/json" -d "{\"title\": \"My New Blog Post\", \"content\": \"This is the content of the blog post.\"}" -b cookies.txt
#curl -X PUT http://127.0.0.1:5000/blog/updateposts -H "Content-Type: application/json" -d "{\"title\": \"My New Blog Post\", \"content\": \"This is the content of the blog post.\"}" -b cookies.txt
#curl -X PUT http://127.0.0.1:5000/blog/updateposts/24726 -H "Content-Type: application/json" -d "{\"title\": \"My Updated blog Post\", \"content\": \"Updated content for the blog post.\"}"
#curl -X DELETE http://127.0.0.1:5000/blog/deleteposts/24726 




