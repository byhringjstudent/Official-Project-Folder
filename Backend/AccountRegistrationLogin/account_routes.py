from flask import request, jsonify, session, Blueprint, redirect, url_for, flash, make_response
import psycopg2
from psycopg2 import sql
import bcrypt
import os
from dotenv import load_dotenv
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from flaskAppConfig import db_info
from utils import create_unique_id
from EmailVerification.email_verification_routes import send_verification_email
from .account_db_functions import *

dotenv_path = os.path.join(os.path.dirname(__file__), 'flask-app.env')
load_dotenv(dotenv_path)


#create blueprint for account routes
app_bp = Blueprint('account_routes', __name__)

#Puporse: This route is used to register a new user in the database.It takes the email, password, first name and 
# last name from the request data and creates a new user in the database. It also sends a confirmation email to the newly created account.
@app_bp.route('/register', methods=['POST'])
def register_user():
    data = request.get_json()
    email = data.get('email') #get email from request data
    password = data.get('password')#get password from request data
    firstName = data.get('firstName')#get first name from request data
    lastName = data.get('lastName')#get last name from request data
    
    #check if the email, password, first name and last name are provided
    if not email or not password or not firstName or not lastName:
        #if not return jsonify with error message and 400 status code
        return jsonify({'message': 'Email, password, first and last name are required to register an account.'}), 400
    
    #hash the password using bcrypt
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    hashed_password_str = hashed_password.decode('utf-8')
 
    result, status_code = create_user(email, hashed_password_str, firstName, lastName)
    #send confirmation email to newly created account. Function located in email_verification_routes.py
    send_verification_email(email)
    return jsonify({'message': result['message'] if 'message' in result else 'User registered successfully'}), status_code #return success message if the user is registered successfully


#Purpose: This route is used to login a user in the database. It takes the email and password from the request data and checks if the user exists in the database and verifies the password. 
# If the user exists and the password is correct, it creates a session for the user.
@app_bp.route('/login', methods = ['POST'])
def userLogin():
    data = request.get_json()#get json data from request
    email = data.get('email')#get email from request data
    password = data.get('password')#get password from request data
    if session.get('accountid'):#check if the user is already logged in
        #if the user is already logged in return jsonify with error message and 401 status code
        return jsonify({"message": 'User already logged in'}), 401
    if not email or not password: ##check if the email and password are provided
        return jsonify({'message': 'Email and Password are required to login.'}), 400
    
    result, status_code = login_user(email, password)
    if result['status'] == 'success':
        session['accountid'] = result['accountid']
        session['userid'] = result['userid']
    return jsonify({'message': result['message'] if 'message' in result else 'User logged in successfully'}), status_code
    
#purpose: This route is used to check if the user is logged in or not. It checks if the account ID and user ID are in the session. 
# If they are, it returns a success message with the account ID and user ID. If they are not, it returns an error message.
@app_bp.route('/sessionCheck', methods = ['GET'])
def sessionCheck():
    if 'accountid' in session and 'userid' in session:
        #if the user is logged in return jsonify with success message and 200 status code
        return jsonify({'message': 'User is logged in', 'accountid': session['accountid'], 'userid': session['userid']}), 200
    else:
        #if the user is not logged in return jsonify with error message and 401 status code
        return jsonify({'message': 'no active session'}), 401



#purpose: This route is used to log out a user. It clears the session and returns a success message.
@app_bp.route('/logout', methods = ['POST'])
def userLogout():
    try:
        session.clear()#clear the session to log out the user
        #flash('You have been logged out.')
        #print('User logged out successfully', dict(session)) #debugging statement to check if the user is logged out successfully
        response = jsonify({'message': 'User logged out successfully'})
        response.set_cookie('session', '', expires=0)  # optional: clears cookie
        return response, 200 #return success message if the user is logged out successfully
    except Exception as e:
        return jsonify({'message': f'Log out unsuccessful: {str(e)}'}), 500   #return error message if there is an error logging out the user
    

#purpose: This route is used to view the account details of a user. It checks if the user is logged in and if they are, it retrieves the account details from the database and returns them.
# If the user is not logged in, it returns an error message.
@app_bp.route('/viewAccountDetails', methods = ['GET'])
def viewAccountDetails():
    accountid = session.get('accountid')#get the account ID from the session
    if not accountid: ##check if the account ID is not in the session
        #if the account ID is not in the session return jsonify with error message and 401 status code
        return jsonify({'message': 'User not logged in'}), 401
    
    result, status_code = get_user_info(accountid)
    if result['status'] == 'success':
        #if the user is logged in return jsonify with success message and 200 status code
        return jsonify({'email': result['email'], 'firstName': result['firstName'], 'lastName': result['lastName'], 'verifiedemail': result['verifiedemail']}), status_code
        
    return jsonify({'message': result['message'] if 'message' in result else 'User logged in successfully'}), status_code

@app_bp.route('/blog-posts', methods = ['get'])
def get_blog_posts():
    accountid = session.get('accountid') #get the account ID from the session
    if not accountid: #check if the account ID is not in the session    
        return jsonify({'message': 'User not logged in'}), 401 #if the account ID is not in the session return jsonify with error message and 401 status code
    try:
        conn = psycopg2.connect(**db_info)
        cur = conn.cursor()
        cur.execute("SELECT blogid, blogtitle, dbinstance, dateposted, status, shortdescription, tags FROM blog WHERE accountid = %s ORDER BY dateposted DESC", (accountid,)) #query to get the blog posts from the database
        posts = cur.fetchall() #get the result of the query
        cur.close()
        conn.close()
        posts_data = [{"blogID": post[0], "title": post[1], "content": post[2], "date": post[3].strftime("%B %d, %Y"), "status": post[4], "shortdescription": post[5], "tags": post[6]} for post in posts] #format the result into a list of dictionaries
        return jsonify(posts_data), 200 #return success message with the blog posts 
    except Exception as e:
        return jsonify({'message': f'Error retrieving blog posts: {str(e)}'}), 500

@app_bp.route('/draft-blog-posts', methods = ['get'])
def get_draft_posts():
    accountid = session.get('accountid') #get the account ID from the session
    if not accountid: #check if the account ID is not in the session    
        return jsonify({'message': 'User not logged in'}), 401 #if the account ID is not in the session return jsonify with error message and 401 status code
    try:
        conn = psycopg2.connect(**db_info)
        cur = conn.cursor()
        cur.execute("SELECT blogid, blogtitle, dbinstance, dateposted, status FROM blog WHERE accountid = %s AND status = %s", (accountid, 'draft')) #query to get the blog posts from the database
        posts = cur.fetchall() #get the result of the query
        cur.close()
        conn.close()
        posts_data = [{"blogID": post[0], "title": post[1], "content": post[2], "date": post[3].strftime("%B %d, %Y"), "status": post[4]} for post in posts] #format the result into a list of dictionaries
        return jsonify(posts_data), 200 #return success message with the blog posts 
    except Exception as e:
        return jsonify({'message': f'Error retrieving blog posts: {str(e)}'}), 500
       


    

@app_bp.route('/edit', methods=['PUT'])
def editAccountDetails():
    data = request.get_json() #get json data from request
    #currentEmail = data.get('currentEmail') #get current email from request data
    newEmail = data.get('newEmail') #get new email from request data
    newFirstName = data.get('firstName') #get new first name from request data
    newLastName = data.get('lastName') #get new last name from request data
    accountid = session.get('accountid') #get the account ID from the session
    
    conn = psycopg2.connect(**db_info)
    cur = conn.cursor()

    

    try:
        if not newFirstName and not newLastName and not newEmail:
            return jsonify({'message': f'Error updating account'}), 400 
        if newFirstName: ##check if the new first name is provided
            query = sql.SQL("UPDATE users set firstname = %s WHERE accountid = %s") #query to update the first name in the database
            cur.execute(query, (newFirstName, accountid)) #execute the query with the new first name and account ID as parameters
            

        if newLastName:
            query = sql.SQL("UPDATE users set lastname = %s WHERE accountid = %s") #query to update the last name in the database
            cur.execute(query, (newLastName, accountid)) #execute the query with the new last name and account ID as parameters

        
        if newEmail:
            cur.execute("SELECT email FROM users WHERE email = %s", (newEmail,)) #check if the new email already exists in the database
            result = cur.fetchone() #get the result of the query
            if result: #check if the result is not empty
                #if the result is not empty return jsonify with error message and 409 status code
                return jsonify({'message': 'Email already exists.'}), 409
            query = sql.SQL("UPDATE users set email = %s WHERE accountid = %s") ##query to update the email in the database
            cur.execute(query, (newEmail, accountid)) ##execute the query with the new email and account ID as parameters
            cur.execute("UPDATE users SET verifiedemail = FALSE WHERE accountid = %s", (accountid,)) #set the verified email to false in the database
            send_verification_email(newEmail) #send confirmation email to the new email address. Function located in email_verification_routes.py
        
        
        conn.commit()
        return jsonify({'message': "Account updated successfully"}), 200

    except Exception as e:
        conn.rollback()
        return jsonify({'message': f'Error updating account: {str(e)}'}), 500
    finally:
        cur.close()
        conn.close()
    

@app_bp.route('/updatePassword', methods = ['PUT'])
def updatePassword():
    data = request.get_json()
    currentPassword = data.get('currentPassword') #get current password from request data
    newPassword = data.get('newPassword') #get new password from request data
    accountid = session.get('accountid') #get the account ID from the session
    
    if newPassword == currentPassword:
        return jsonify({'message': 'Passwords are the same'}), 401

    conn = psycopg2.connect(**db_info) #connect to db  
    cur = conn.cursor() #create cursor
    try:
        query = sql.SQL("SELECT password FROM users WHERE accountid = %s") #query to get the password from the database
        cur.execute(query, (accountid,)) #execute the query with the account ID as a parameter
        resultPassword = cur.fetchone() #get the result of the query
        
        if resultPassword: #check if the result is not empty
            #if the result is not empty get the password from the result
            stored_hash= resultPassword[0]
            if bcrypt.checkpw(currentPassword.encode('utf-8'), stored_hash.encode('utf-8')): #check if the input password matches the stored password
                #if the password matches hash the new password and update it in the database
                hashed_password = bcrypt.hashpw(newPassword.encode('utf-8'), bcrypt.gensalt())
                hashed_password_str = hashed_password.decode('utf-8')
                query = sql.SQL("UPDATE users SET password = %s WHERE accountid = %s") #query to update the password in the database
                cur.execute(query, (hashed_password_str, accountid)) #execute the query with the new password and account ID as parameters
                conn.commit()
                return jsonify({'message': 'Password updated successfully'}), 201 #return success message if the password is updated successfully
            else:
                return jsonify({'message': 'Incorrect current Password'}), 401 #return error message if the current password does not match
        else:
            return jsonify({'message': 'Account ID not found'}), 404
        
    except Exception as e:
        return jsonify({'message': f'Error updating password: {str(e)}'}), 500
         

    
  
    
#delete account route
@app_bp.route('/deleteAccount', methods = ['POST'])
def deleteAccount():
    data = request.get_json()
    password = data.get('password')
    conn = psycopg2.connect(**db_info) #connect to the database
    cur = conn.cursor() 
    accountid = session.get('accountid') #get the account ID from the session
    print(f"Account ID from session: {accountid}")
    try:
        query = sql.SQL("SELECT password FROM users WHERE accountid = %s") #query to get the password from the database
        cur.execute(query, (accountid,)) #execute the query with the account ID as a parameter
        resultPassword = cur.fetchone() #get the result of the query
        if resultPassword:
            stored_hash = resultPassword[0]
            if bcrypt.checkpw(password.encode('utf-8'), stored_hash.encode('utf-8')): #check if the input password matches the stored password
                #if the password matches hash the new password and update it in the database
                deleteAccount =sql.SQL("DELETE FROM account WHERE accountid = %s") #query to delete the account from the database
                cur.execute(deleteAccount, (accountid,)) ##delete the account from the database
        
                conn.commit()
                cur.close()
                conn.close()
                session.clear()
                response = jsonify({'message': 'Account deleted successfully'})
                response.set_cookie('session', '', expires=0)  # optional: clears cookie
                return response, 200 
            else:   
                return jsonify({'message': 'Incorrect Password'}), 400
        else:
            return jsonify({'message': 'Account ID not found'}), 404
    except Exception as e: 
        return jsonify({'message': f'Error deleting account: {str(e)}'}),500

@app_bp.route('/check-auth', methods = ['GET'])
def check_auth():
    if 'accountid' in session:
        return jsonify({'loggedIn': True}), 200
    else:
        return jsonify({'loggedIn': False}), 401
    

#CURL COMMANDS FOR TESTING DIFFERENT ROUTES 
             
#ACCOUNT COMMANDS
    #curl -X POST http://localhost:5000/account/register -H "Content-Type: application/json" -d "{\"email\": \"mikeymaher71@gmail.com\",\"password\":\"what\",\"firstName\":\"Michael\",\"lastName\":\"Simko\"}"
    #curl -X PUT http://127.0.0.1:5000/account/edit -H "Content-Type: application/json" -d "{\"password\": \"newpassword123\"}"
    #curl -X PUT http://127.0.0.1:5000/account/edit -H "Content-Type: application/json" -d "{\"firstName\": \"Michael\"}"
    #curl -X PUT http://127.0.0.1:5000/account/edit -H "Content-Type: application/json" -d "{\"lastName\": \"Maher\"}"
    #curl -X PUT http://127.0.0.1:5000/account/edit -H "Content-Type: application/json" -d "{\"newEmail\": \"newemail@example.com\"}"
    #curl -X POST http://127.0.0.1:5000/account/deleteAccount -H "Content-Type: application/json" -d "{\"email\": \"mikeymaher71@gmail.com\"}"
    #curl -X POST http://127.0.0.1:5000/account/login -H "Content-Type: application/json" -d "{\"email\": \"opticgorilla34@gmail.com\", \"password\": \"password123\"}" -c cookies.txt
    #curl -i -X POST http://127.0.0.1:5000/account/logout -b cookies.txt -c cookies.txt
    #curl -X GET http://127.0.0.1:5000/account/viewAccountDetails -b cookies.txt
    #curl -X PUT http://127.0.0.1:5000/account/updatePassword -H "Content-Type: application/json" -d "{\"currentPassword\": \"password123\", \"newPassword\": \"newpassword123\"}" -b cookies.txt

#TESTING BLOG COMMANDS
    #curl -X POST http://127.0.0.1:5000/blog/createposts -H "Content-Type: application/json" -d "{\"title\": \"My New Blog Post\", \"content\": \"This is the content of the blog post.\", \"status\": \"draft\"}" -b cookies.txt
    #curl -X PUT http://127.0.0.1:5000/blog/updateposts -H "Content-Type: application/json" -d "{\"title\": \"My New Blog Post\", \"content\": \"This is the content of the blog post.\"}" -b cookies.txt
    #curl -X PUT http://127.0.0.1:5000/blog/updateposts/24726 -H "Content-Type: application/json" -d "{\"title\": \"My Updated blog Post\", \"content\": \"Updated content for the blog post.\"}"
    #curl -X DELETE http://127.0.0.1:5000/blog/deleteposts/24726 

#HOME COMMANDS
    #curl -X GET http://localhost:5000/
    #curl -X GET http://localhost:5000/ -b cookies.txt
    #curl -X GET http://localhost:5000/ -b cookies.txt -c cookies.txt





