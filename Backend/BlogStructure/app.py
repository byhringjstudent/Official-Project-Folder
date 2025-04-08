"""
Author :Jaden
Date   :April 5, 2025
Purpose:This is the main flask app for the blog backend.
"""

from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_cors import CORS

app = Flask(__name__)

#postgresql connection (replace with username, password, and database name)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://yourusername:yourpassword@localhost:5432/yourdbname'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

#initialize database
db = SQLAlchemy(app)

#connction to react frontend
CORS(app)