from flask import request, jsonify, session, Blueprint
import bcrypt
import os
from dotenv import load_dotenv
from EmailVerification.email_verification_routes import send_verification_email
from .account_db_functions import *


#create blueprint for account routes
app_bp = Blueprint('account_blog_routes', __name__)

dotenv_path = os.path.join(os.path.dirname(__file__), 'flask-app.env')
load_dotenv(dotenv_path)     

#Purpose: This route is used to display the blog posts of a user in their account portal.
# It checks if the user is logged in and if they are, it retrieves the blog posts from the database and returns them.
# If the user is not logged in, it returns an error message.
@app_bp.route('/blog-posts', methods = ['get'])
def get_blog_posts():
    try:
        accountid = session.get('accountid') #get the account ID from the session
        if not accountid: #check if the account ID is not in the session    
            return jsonify({'message': 'User not logged in'}), 401
        result, status_code = get_user_blogs(accountid) #get the user info from the database
        if result['status'] == 'success':
            #print(result['blogs'])
            return jsonify({'blogs': result['blogs']}), status_code
        else:
            return jsonify({'message': result['message'] if 'message' in result else 'User blogs not retrieved successfully'}), status_code
    except Exception as e:
        return jsonify({'message': f'Error retrieving blog posts: {str(e)}'}), 500
              

#Purpose: This route is used to display the draft blog posts of a user in their account portal.
# It checks if the user is logged in and if they are, it retrieves the draft blog posts from the database and returns them.
@app_bp.route('/draft-blog-posts', methods = ['get'])
def get_draft_posts():
    accountid = session.get('accountid') #get the account ID from the session
    if not accountid:    
        return jsonify({'message': 'User not logged in'}), 401 
    
    result, status_code = get_user_drafts(accountid) #get the user info from the database
    if result['status'] == 'success':
        #print(result['blogs']) debugging code
        return jsonify({'blogs': result['drafts']}), status_code
    else:
        return jsonify({'message': result['message'] if 'message' in result else 'User blogs not retrieved successfully'}), status_code
