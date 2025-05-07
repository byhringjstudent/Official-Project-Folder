from flask import request, jsonify, session, Blueprint
import bcrypt
import os
from dotenv import load_dotenv
from flaskAppConfig import db_info
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
    #get user input from request data
    data = request.get_json()
    email = data.get('email') 
    password = data.get('password')
    firstName = data.get('firstName')
    lastName = data.get('lastName')
    
    #check if all required fields are provided
    if not email or not password or not firstName or not lastName:
        return jsonify({'message': 'Email, password, first and last name are required to register an account.'}), 400
    
    #hash the password using bcrypt
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    hashed_password_str = hashed_password.decode('utf-8')
 
    result, status_code = create_user(email, hashed_password_str, firstName, lastName)
    if result['status'] == 'success':
        send_verification_email(email)#send confirmation email to newly created account. Function located in email_verification_routes.py
        result, status_code = login_user(email, password) #login the user after registration
        if result['status'] == 'success':
            session['accountid'] = result['accountid']
            session['userid'] = result['userid']
            return jsonify({'message': result['message'] if 'message' in result else 'User registered and logged in successfully'}), status_code #return success message if the user is registered and logged in successfully
        else:
            return jsonify({'message': result['message'] if 'message' in result else 'User registered successfully'}), status_code #return success message if the user is registered successfully
    else:
        return jsonify({'message': result['message'] if 'message' in result else 'User not registered successfully'}), status_code


#Purpose: This route is used to login a user in the database. It takes the email and password from the request data and checks if the user exists in the database and verifies the password. 
# If the user exists and the password is correct, it creates a session for the user.
@app_bp.route('/login', methods = ['POST'])
def userLogin():
    #get user input from request data
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')
    if session.get('accountid'):#check if the user is already logged in
        return jsonify({"message": 'User already logged in'}), 401
    if not email or not password: ##check if the email and password are provided
        return jsonify({'message': 'Email and Password are required to login.'}), 400
    
    result, status_code = login_user(email, password)
    if result['status'] == 'success':
        session['accountid'] = result['accountid']
        session['userid'] = result['userid']
    return jsonify({'message': result['message'] if 'message' in result else 'User logged in successfully'}), status_code

#purpose: This route is used to log out a user. It clears the session and returns a success message.
@app_bp.route('/logout', methods = ['POST'])
def userLogout():
    try:
        session.clear()#clear the session to log out the user
        response = jsonify({'message': 'User logged out successfully'})
        response.set_cookie('session', '', expires=0)  #clears cookie
        return response, 200 #return success message if the user is logged out successfully
    except Exception as e:
        return jsonify({'message': f'Log out unsuccessful: {str(e)}'}), 500   #return error message if there is an error logging out the user
         

#Purpose: This route is used to delete the account of a user. It checks if the user is logged in and if they are, it retrieves the account details from the database and deletes them.
# If the user is not logged in, it returns an error message.
@app_bp.route('/deleteAccount', methods = ['POST'])
def deleteAccount():
    data = request.get_json()
    password = data.get('password')
    accountid = session.get('accountid') #get the account ID from the session
    #print(f"Account ID from session: {accountid}")
    status, status_code = delete_user(accountid, password) #get the user info from the database
    if status['status'] == 'success':
        session.clear()
        return jsonify({'message': status['message'] if 'message' in status else 'User account deleted successfully'}), status_code
    else:  
        return jsonify({'message': status['message'] if 'message' in status else 'User account not deleted successfully'}), status_code
        
  
#Purpose: This route is used to check if the user is logged in or not. 
# It checks if the account ID is in the session and if it is, it returns a success
#  message with the account ID.
# If the account ID is not in the session, it returns an error message.
@app_bp.route('/check-auth', methods = ['GET'])
def check_auth():
    if 'accountid' in session:
        return jsonify({'loggedIn': True}), 200
    else:
        return jsonify({'loggedIn': False}), 401