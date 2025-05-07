from flask import Flask
from flask_cors import CORS
from flask_session import Session
from AccountRegistrationLogin import account_routes, account_blog_routes, account_details_routes
from BlogStructure import blog_routes, blog_viewing_routes
from EmailVerification import email_verification_routes
from flaskAppConfig import Config


def create_app(config_class=Config): # creating the app with the config class
    app = Flask(__name__)
    app.config.from_object(config_class) # loading the config class

    Session(app)
    CORS(app, origins = ["http://localhost:5173"], supports_credentials= True, ) # enabling CORS for the app
    #/api is important for the frontend to work properly with the relative 
    app.register_blueprint(account_blog_routes.app_bp, url_prefix='/api/account') #registering account blog routes
    app.register_blueprint(account_details_routes.app_bp, url_prefix='/api/account') #registering account details routes
    app.register_blueprint(account_routes.app_bp, url_prefix='/api/account') # registering the account routes blueprint
    app.register_blueprint(blog_routes.app_bp, url_prefix='/api/blog') # registering the blog routes blueprint
    app.register_blueprint(blog_viewing_routes.app_bp, url_prefix='/api/blog') # registering the viewing blog routes blueprint
    app.register_blueprint(email_verification_routes.app_bp, url_prefix='/api/email')# registering the email verification routes blueprint


    return app # app instance

app = create_app() # creating the app instance


if __name__ == '__main__': # run the app
    app.run(debug=True)
