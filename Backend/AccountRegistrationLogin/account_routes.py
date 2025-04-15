from flask import request, jsonify, session, Blueprint, redirect, url_for, flash, make_response
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

#Unique ID generator for account and user IDs. Class in utils.py    
idGen = uniqueID(10000, 99999, db_info)

#create blueprint for account routes
app_bp = Blueprint('account_routes', __name__)

#register user route
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
    
    try:
        conn = psycopg2.connect(**db_info) #connect to the database
        cur = conn.cursor()
        #check if the email already exists in the database
        query = sql.SQL("SELECT accountid FROM users WHERE email = %s")
        cur.execute(query, (email,))
        result = cur.fetchone()
        if result:
            #if the email already exists return jsonify with error message and 409 status code
            return jsonify({'message': 'Email already exists.'}), 409
        #if the email does not exist insert the new user into the database
        accountid = idGen.genID()#generate a unique account ID
        cur.execute("INSERT INTO account (accountid, accounttype, orgid) VALUES (%s, %s, %s)", (accountid, "Free", idGen.genID()))
        cur.execute("INSERT INTO users (userid, email, password, firstname, lastname, accountid) VALUES (%s, %s, %s, %s, %s, %s)", (idGen.genID(), email, hashed_password_str, firstName, lastName, accountid))
        conn.commit()
        cur.close()
        conn.close()
        #send confirmation email to newly created account. Function located in email_verification_routes.py
        send_verification_email(email)
                 
        
        return jsonify({'message': 'User created successfully. You will be recieving a confirmation email soon!'}), 201
    except Exception as e: 
        return jsonify({'message': f'Error creating user: {str(e)}'}),500


#login user route
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
    
    #hash the input password using bcrypt to compare to database password   
    hashed_password=bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    
    try:
        conn = psycopg2.connect(**db_info)#connect to the database
        cur = conn.cursor()#
        query = sql.SQL("SELECT password FROM users WHERE email = %s")# query to get the password from the database
        cur.execute(query, (email,))#execute the query with the email as a parameter
        resultPassword = cur.fetchone()#get the result of the query
        
        if resultPassword: #check if the result is not empty
            #if the result is not empty get the password from the result
            stored_hash= resultPassword[0]
            if bcrypt.checkpw(password.encode('utf-8'), stored_hash.encode('utf-8')):#check if the input password matches the stored password
                #if the password matches get the account ID and user ID from the database
                userAccountIDQuery = sql.SQL("SELECT accountid FROM users WHERE email = %s")
                userIDQuery = sql.SQL("SELECT userid FROM users WHERE email = %s")
                cur.execute(userAccountIDQuery, (email,))
                accountid = cur.fetchone()[0] #get the account ID from the result
                cur.execute(userIDQuery, (email,))
                userid = cur.fetchone()[0] #get the user ID from the result
                cur.close()
                conn.close()
                session['accountid'] = accountid #set the account ID in the session
                session['userid'] = userid #set the user ID in the session
                #print(accountid)
                #print(userid)
                #print(userAccountid)
                #return jsonify({'message': 'Correct login credentials.'}),200 #return success message
                return jsonify({'message': 'User logged in successfully'}), 201 #return success message if the user is logged in successfully
            else:
                return jsonify({'message': 'Incorrect Password'}), 401 #return error message if the password does not match
        else:
            return jsonify({'message': 'Email not found'}), 404 #return error message if the email is not found
        
    except Exception as e: 
        return jsonify({'message': f'Error logging in user: {str(e)}'}), 500 #return error message if there is an error logging in the user
    
#debug route to check if the user is logged in
@app_bp.route('/sessionCheck', methods = ['GET'])
def sessionCheck():
    if 'accountid' in session and 'userid' in session:
        #if the user is logged in return jsonify with success message and 200 status code
        return jsonify({'message': 'User is logged in', 'accountid': session['accountid'], 'userid': session['userid']}), 200
    else:
        #if the user is not logged in return jsonify with error message and 401 status code
        return jsonify({'message': 'no active session'}), 401




#logout user route
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
    

#view account details route
@app_bp.route('/viewAccountDetails', methods = ['GET'])
def viewAccountDetails():
    conn = psycopg2.connect(**db_info) #connect to the database
    cur = conn.cursor()
    accountid = session.get('accountid')#get the account ID from the session
    #print(accountid) #debugging statement to check if the account ID is in the session
    
    if not accountid: ##check if the account ID is not in the session
        #if the account ID is not in the session return jsonify with error message and 401 status code
        return jsonify({'message': 'User not logged in'}), 401
    
    try:
        query = sql.SQL("SELECT email, firstname, lastname, verifiedemail FROM users WHERE accountid = %s") #query to get the email, first name and last name from the database
        cur.execute(query, (accountid,))
        userDetails = cur.fetchone() #get the result of the query
        
        if userDetails: #check if the result is not empty
            #if the result is not empty get the email, first name and last name from the result
            email, firstName, lastName, verifiedemail = userDetails
            cur.close()
            conn.close()
            return jsonify({'email': email, 'firstName': firstName, 'lastName': lastName, 'verified email status': verifiedemail}), 200 #return success message with the user details
        else:
            return jsonify({'message': 'User not found'}), 404 #return error message if the user is not found
    except Exception as e: 
        return jsonify({'message': f'Error retrieving account details: {str(e)}'}),500 #return error message if there is an error retrieving the account details

@app_bp.route('/blog-posts', methods = ['get'])
def get_blog_posts():
    accountid = session.get('accountid') #get the account ID from the session
    if not accountid: #check if the account ID is not in the session    
        return jsonify({'message': 'User not logged in'}), 401 #if the account ID is not in the session return jsonify with error message and 401 status code
    try:
        conn = psycopg2.connect(**db_info)
        cur = conn.cursor()
        cur.execute("SELECT blogid, blogtitle, dbinstance, dateposted, status FROM blog WHERE accountid = %s", (accountid,)) #query to get the blog posts from the database
        posts = cur.fetchall() #get the result of the query
        cur.close()
        conn.close()
        posts_data = [{"blogID": post[0], "title": post[1], "content": post[2], "date": post[3].strftime("%Y-%m-%d"), "status": post[4]} for post in posts] #format the result into a list of dictionaries
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
        posts_data = [{"blogID": post[0], "title": post[1], "content": post[2], "date": post[3].strftime("%Y-%m-%d"), "status": post[4]} for post in posts] #format the result into a list of dictionaries
        return jsonify(posts_data), 200 #return success message with the blog posts 
    except Exception as e:
        return jsonify({'message': f'Error retrieving blog posts: {str(e)}'}), 500
       


    

#edit account details route    
@app_bp.route('/edit', methods = ['PUT'])
def editAccountDetails():
    data = request.get_json() #get json data from request
    #currentEmail = data.get('currentEmail') #get current email from request data
    newEmail = data.get('newEmail') #get new email from request data
    newPassword = data.get('password') #get new password from request data
    newFirstName = data.get('firstName') #get new first name from request data
    newLastName = data.get('lastName') #get new last name from request data
    accountid = session.get('accountid') #get the account ID from the session
    
    conn = psycopg2.connect(**db_info)
    cur = conn.cursor()
    
    if newPassword: ##check if the new password is provided
        #if the new password is provided hash the new password using bcrypt
        try:
            new_hashed_password = bcrypt.hashpw(newPassword.encode('utf-8'), bcrypt.gensalt())
            new_hashed_password_str = new_hashed_password.decode('utf-8')
            query = sql.SQL("UPDATE users set password = %s WHERE accountid = %s") #query to update the password in the database
            cur.execute(query, (new_hashed_password_str, accountid)) #execute the query with the new password and account ID as parameters
            conn.commit()
            return jsonify({'message': 'Password updated successfully'}), 201
        except Exception as e: 
            return jsonify({'message': f'Error updating password: {str(e)}'}),500
            
    if newFirstName: ##check if the new first name is provided
        try:
            query = sql.SQL("UPDATE users set firstname = %s WHERE accountid = %s") #query to update the first name in the database
            cur.execute(query, (newFirstName, accountid)) #execute the query with the new first name and account ID as parameters
            conn.commit()
            return jsonify({'message': 'First name updated successfully'}), 201
        except Exception as e: 
            return jsonify({'message': f'Error updating first name: {str(e)}'}),500
            
    if newLastName:
        try:
            query = sql.SQL("UPDATE users set lastname = %s WHERE accountid = %s") #query to update the last name in the database
            cur.execute(query, (newLastName, accountid)) #execute the query with the new last name and account ID as parameters
            conn.commit()
            return jsonify({'message': 'Last name updated successfully'}), 201
        except Exception as e: 
            return jsonify({'message': f'Error updating last name: {str(e)}'}),500
    
    if newEmail:
        try:
            query = sql.SQL("UPDATE users set email = %s WHERE accountid = %s") ##query to update the email in the database
            cur.execute("SELECT email FROM users WHERE email = %s", (newEmail,)) #check if the new email already exists in the database
            result = cur.fetchone() #get the result of the query
            if result: #check if the result is not empty
                #if the result is not empty return jsonify with error message and 409 status code
                return jsonify({'message': 'Email already exists.'}), 409
            cur.execute(query, (newEmail, accountid)) ##execute the query with the new email and account ID as parameters
            cur.execute("UPDATE users SET verifiedemail = FALSE WHERE accountid = %s", (accountid,)) #set the verified email to false in the database
            conn.commit()
            send_verification_email(newEmail) #send confirmation email to the new email address. Function located in email_verification_routes.py
            return jsonify({'message': 'Email updated successfully. You will be recieving a confirmation email.'}), 201
        except Exception as e: 
            return jsonify({'message': f'Error updating Email: {str(e)}'}),500
    
    #if no new email, password, first name or last name is provided return jsonify with error message
    cur.close()
    conn.close() 
    return jsonify({'message': 'No new email, password, first name or last name provided to update.'}), 400
  
    
#delete account route
@app_bp.route('/deleteAccount', methods = ['POST'])
def deleteAccount():
    conn = psycopg2.connect(**db_info) #connect to the database
    cur = conn.cursor() 
    accountid = session.get('accountid') #get the account ID from the session
    
    try:
        deleteUser = sql.SQL("DELETE FROM users WHERE accountid = %s") #query to delete the user from the database
        deleteAccount =sql.SQL("DELETE FROM account WHERE accountid = %s") #query to delete the account from the database
        deleteBlog = sql.SQL("DELETE FROM blog WHERE accountid= %s") #query to delete the blogs from the database
    
        cur.execute(deleteUser, (accountid,)) #delete the user from the database
        cur.execute(deleteBlog, (accountid,)) ##delete the blogs from the database
        cur.execute(deleteAccount, (accountid,)) ##delete the account from the database
        
        conn.commit()
        cur.close()
        conn.close()
        return jsonify({'message' : 'Account was successfully deleted'}),204
    
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
    #curl -X POST http://127.0.0.1:5000/account/login -H "Content-Type: application/json" -d "{\"email\": \"mahermikey71@gmail.com\", \"password\": \"what\"}" -c cookies.txt
    #curl -i -X POST http://127.0.0.1:5000/account/logout -b cookies.txt -c cookies.txt
    #curl -X GET http://127.0.0.1:5000/account/viewAccountDetails -b cookies.txt

#TESTING BLOG COMMANDS
    #curl -X POST http://127.0.0.1:5000/blog/createposts -H "Content-Type: application/json" -d "{\"title\": \"My New Blog Post\", \"content\": \"This is the content of the blog post.\", \"status\": \"draft\"}" -b cookies.txt
    #curl -X PUT http://127.0.0.1:5000/blog/updateposts -H "Content-Type: application/json" -d "{\"title\": \"My New Blog Post\", \"content\": \"This is the content of the blog post.\"}" -b cookies.txt
    #curl -X PUT http://127.0.0.1:5000/blog/updateposts/24726 -H "Content-Type: application/json" -d "{\"title\": \"My Updated blog Post\", \"content\": \"Updated content for the blog post.\"}"
    #curl -X DELETE http://127.0.0.1:5000/blog/deleteposts/24726 

#HOME COMMANDS
    #curl -X GET http://localhost:5000/
    #curl -X GET http://localhost:5000/ -b cookies.txt
    #curl -X GET http://localhost:5000/ -b cookies.txt -c cookies.txt





