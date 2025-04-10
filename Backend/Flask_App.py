from flask import Flask
from AccountRegistrationLogin import account_routes 
from BlogStructure import blog_routes
from flaskAppConfig import Config
import os

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    app.register_blueprint(account_routes.app_bp, url_prefix='/account')
    app.register_blueprint(blog_routes.app_bp, url_prefix='/blog')

    return app

app = create_app()


if __name__ == '__main__':
    app.run(debug=True)
