import os 
from datetime import timedelta
from dotenv import load_dotenv

dotenv_path = os.path.join(os.path.dirname(__file__), 'flask-app.env')
load_dotenv(dotenv_path)

class Config: # Base configuration class
    SECRET_KEY = os.getenv('SECRET_KEY') # Secret key for session management
    SESSION_TYPE = 'filesystem' # Session type
    SESSION_COOKIE_SECURE = False # Set to True in production for HTTPS
    SESSION_COOKIE_HTTPONLY = True
    PERMANENT_SESSION_LIFETIME = timedelta(days=7) # Session lifetime

#database connection information
db_info ={'host': "192.168.1.221",
    'port': "5432",
    'database' : "LegacyIQ",
    'user' : "postgres",
    'password':"password123"}

