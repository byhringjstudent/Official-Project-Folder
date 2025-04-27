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


if __name__ == '__main__': # run the app
    app.run(debug=True)
