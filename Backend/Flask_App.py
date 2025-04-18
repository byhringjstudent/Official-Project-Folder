from flask import Flask, jsonify, session
from flask_cors import CORS
from flask_session import Session
from AccountRegistrationLogin import account_routes 
from BlogStructure import blog_routes
from EmailVerification import email_verification_routes
from flaskAppConfig import Config
import os
import psycopg2

def create_app(config_class=Config): # creating the app with the config class
    app = Flask(__name__)
    app.config.from_object(config_class) # loading the config class

    Session(app)
    CORS(app, origins = ["http://localhost:5173"], supports_credentials= True, ) # enabling CORS for the app
    app.register_blueprint(account_routes.app_bp, url_prefix='/account') # registering the account routes blueprint
    app.register_blueprint(blog_routes.app_bp, url_prefix='/blog') # registering the blog routes blueprint
    app.register_blueprint(email_verification_routes.app_bp, url_prefix='/email')# registering the email verification routes blueprint

    return app # app instance

app = create_app() # creating the app instance

@app.route('/') # home route
def home():
    print(f"Session ID: {session.get('accountid')}") # print the session ID for debugging
    if session.get('accountid'): # check if the user is logged in
        # if the user is logged in, show the welcome back message
        return jsonify({"message": 'Welcome back!', 
                        "version": ['beta'],
                        'available_routes': ['/blog/readposts', '/blog/createposts', '/account/viewAccountDetails']}), 200
    else:# if the user is not logged in, show the welcome message
        return jsonify({"message": 'Welcome to LegacyIQ!',
                        "version": ['beta'],
                        'available_routes': ['/account/register', '/account/login']}), 200


if __name__ == '__main__': # run the app
    app.run(debug=True)
