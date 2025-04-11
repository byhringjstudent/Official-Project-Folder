from flask import Flask, jsonify, session
from AccountRegistrationLogin import account_routes 
from BlogStructure import blog_routes
from EmailVerification import email_verification_routes
from flaskAppConfig import Config
import os

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    app.register_blueprint(account_routes.app_bp, url_prefix='/account')
    app.register_blueprint(blog_routes.app_bp, url_prefix='/blog')
    app.register_blueprint(email_verification_routes.app_bp, url_prefix='/email')

    return app

app = create_app()

@app.route('/')
def home():
    print(f"Session ID: {session.get('accountid')}")
    if session.get('accountid'):
        return jsonify({"message": 'Welcome back!',
                        "version": ['beta'],
                        'available_routes': ['/blog/readposts', '/blog/createposts', '/account/viewAccountDetails']}), 200
    else:
        return jsonify({"message": 'Welcome to LegacyIQ!',
                        "version": ['beta'],
                        'available_routes': ['/account/register', '/account/login']}), 200


if __name__ == '__main__':
    app.run(debug=True)
