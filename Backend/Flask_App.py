from flask import Flask, send_from_directory
from flask_cors import CORS
from flask_session import Session
from AccountRegistrationLogin import account_routes, account_blog_routes, account_details_routes
from BlogStructure import blog_routes, blog_viewing_routes
from EmailVerification import email_verification_routes
from flaskAppConfig import Config
import os

# Heroku OAuth credentials
client_id = os.getenv("OAUTH_CLIENT_ID")
client_secret = os.getenv("OAUTH_CLIENT_SECRET")

def create_app(config_class=Config):
    app = Flask(__name__, static_folder='dist', static_url_path='')
    app.config.from_object(config_class)

    # Enable CORS for frontend
    CORS(app, origins=[
        "https://your-netlify-app.netlify.app",
        "http://localhost:5173"
    ], supports_credentials=True)

    Session(app)

    # Register Blueprints
    app.register_blueprint(account_blog_routes.app_bp, url_prefix='/api/account')
    app.register_blueprint(account_details_routes.app_bp, url_prefix='/api/account')
    app.register_blueprint(account_routes.app_bp, url_prefix='/api/account')
    app.register_blueprint(blog_routes.app_bp, url_prefix='/api/blog')
    app.register_blueprint(blog_viewing_routes.app_bp, url_prefix='/api/blog')
    app.register_blueprint(email_verification_routes.app_bp, url_prefix='/api/email')

    # Static uploads folder
    upload_folder = os.path.join(app.root_path, 'static', 'uploads')
    os.makedirs(upload_folder, exist_ok=True)
    app.config['UPLOAD_FOLDER'] = upload_folder

    # Serve frontend
    @app.route('/', defaults={'path': ''})
    @app.route('/<path:path>')
    def serve_react(path):
        if path != "" and os.path.exists(os.path.join(app.static_folder, path)):
            return send_from_directory(app.static_folder, path)
        else:
            return send_from_directory(app.static_folder, 'index.html')

    return app

# Expose app instance for gunicorn
app = create_app()

if __name__ == '__main__':
    app.run(debug=True)
