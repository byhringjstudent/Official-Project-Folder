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

#class DevelopmentConfig(Config): # Development configuration class
#   DEBUG = True # Enable debug mode
#    ENV = 'development' # Environment type

#class ProductionConfig(Config): # Production configuration class
#    DEBUG = False # Disable debug mode
#    ENV = 'production' # Environment type
#    SESSION_COOKIE_SECURE = True

#class TestingConfig(Config): # Testing configuration class
#    DEBUG = True # Enable debug mode
#    TESTING = True # Enable testing mode
#    ENV = 'testing'

#database connection information
db_info ={'host': "localhost",
    'port': "5432",
    'database' : "LegacyIQ",
    'user' : "postgres",
    'password':"password123"}

