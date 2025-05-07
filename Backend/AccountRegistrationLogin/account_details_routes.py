from flask import request, jsonify, session, Blueprint
import bcrypt
import os
from dotenv import load_dotenv
from flaskAppConfig import db_info
from EmailVerification.email_verification_routes import send_verification_email
from .account_db_functions import *

#create blueprint for account routes
app_bp = Blueprint('account_details_routes', __name__)

dotenv_path = os.path.join(os.path.dirname(__file__), 'flask-app.env')
load_dotenv(dotenv_path)   


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
    else:
        #if the user is not logged in return jsonify with error message and 401 status code
        return jsonify({'message': result['message'] if 'message' in result else 'User information not retrieved successfully'}), status_code\


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
