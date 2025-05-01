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
    #send confirmation email to newly created account. Function located in email_verification_routes.py
    send_verification_email(email)
    return jsonify({'message': result['message'] if 'message' in result else 'User registered successfully'}), status_code #return success message if the user is registered successfully


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
        response = jsonify({'message': 'User logged out successfully'})
        response.set_cookie('session', '', expires=0)  #clears cookie
        return response, 200 #return success message if the user is logged out successfully
    except Exception as e:
        return jsonify({'message': f'Log out unsuccessful: {str(e)}'}), 500   #return error message if there is an error logging out the user
    

#purpose: This route is used to view the account details of a user. It checks if the user is logged in and if they are, it retrieves the account details from the database and returns them.
# If the user is not logged in, it returns an error message.
@app_bp.route('/viewAccountDetails', methods = ['GET'])
def viewAccountDetails():
    accountid = session.get('accountid')#get the account ID from the session
    if not accountid: ##check if the account ID is not in the session
        return jsonify({'message': 'User not logged in'}), 401
    
    result, status_code = get_user_info(accountid)
    if result['status'] == 'success':
        #if the user is logged in return jsonify with success message and 200 status code
        return jsonify({'email': result['email'], 'firstName': result['firstName'], 'lastName': result['lastName'], 'verifiedemail': result['verifiedemail']}), status_code
        
    return jsonify({'message': result['message'] if 'message' in result else 'User logged in successfully'}), status_code

#Purpose: This route is used to display the blog posts of a user in their account portal.
# It checks if the user is logged in and if they are, it retrieves the blog posts from the database and returns them.
# If the user is not logged in, it returns an error message.
@app_bp.route('/blog-posts', methods = ['get'])
def get_blog_posts():
    accountid = session.get('accountid') #get the account ID from the session
    if not accountid: #check if the account ID is not in the session    
        return jsonify({'message': 'User not logged in'}), 401
    result, status_code = get_user_blogs(accountid) #get the user info from the database
    if result['status'] == 'success':
        #print(result['blogs'])
        return jsonify({'blogs': result['blogs']}), status_code


#Purpose: This route is used to display the draft blog posts of a user in their account portal.
# It checks if the user is logged in and if they are, it retrieves the draft blog posts from the database and returns them.
@app_bp.route('/draft-blog-posts', methods = ['get'])
def get_draft_posts():
    accountid = session.get('accountid') #get the account ID from the session
    if not accountid:    
        return jsonify({'message': 'User not logged in'}), 401 
    
    result, status_code = get_user_drafts(accountid) #get the user info from the database
    if result['status'] == 'success':
        #print(result['blogs'])
        return jsonify({'blogs': result['drafts']}), status_code
       


#Purpose: This route is used to edit the account details of a user. It checks if the user is logged in and if they are,
#it retrieves the account details from the database and updates them.
# If the user is not logged in, it returns an error message.
# It also checks if the new email already exists in the database and if it does, it returns an error message.
@app_bp.route('/edit', methods=['PUT'])
def editAccountDetails():
    data = request.get_json() #get json data from request
    newEmail = data.get('newEmail') 
    newFirstName = data.get('firstName') 
    newLastName = data.get('lastName')
    accountid = session.get('accountid') 
    
    if not accountid:
        #if the account ID is not in the session return jsonify with error message and 401 status code
        return jsonify({'message': 'User not logged in'}), 401
    
    result, status_code = update_user_info(accountid, newFirstName, newLastName, newEmail) #get the user info from the database
    if result['status'] == 'success':
        #if the user is logged in return jsonify with success message and 200 status code
        return jsonify({'message': result['message'] if 'message' in result else 'User information updated successfully'}), status_code
    else:
        
        return jsonify({'message': result['message'] if 'message' in result else 'User information not updated successfully'}), status_code

    
    
#Purpose: This route is used to update the password of a user. It checks if the user is logged in and if they are, it retrieves the account details from the database and updates them.
# If the user is not logged in, it returns an error message.
# It also checks if the new password and current password are provided and if they are not, it returns an error message.
# It also checks if the current password is correct and if it is not, it returns an error message.
@app_bp.route('/updatePassword', methods = ['PUT'])
def updatePassword():
    #get user input from request data
    data = request.get_json()
    currentPassword = data.get('currentPassword') 
    newPassword = data.get('newPassword') 
    accountid = session.get('accountid') 
    
    if not accountid:
        return jsonify({'message': 'User not logged in'}), 401
    
    if not newPassword or not currentPassword:
        return jsonify({'message': 'New password and current password are required to update password.'}), 400

    result, status_code = update_user_password(accountid, currentPassword, newPassword) #get the user info from the database
    if result['status'] == 'success':
        #if the user is logged in return jsonify with success message and 200 status code
        return jsonify({'message': result['message'] if 'message' in result else 'User password updated successfully'}), status_code
    else:
        return jsonify({'message': result['message'] if 'message' in result else 'User password not updated successfully'}), status_code
         

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





