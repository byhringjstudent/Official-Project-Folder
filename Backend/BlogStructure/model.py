"""
Author :Jaden
Date   :April 5, 2025
Purpose:Blog post setup, this will represent blog post in database
"""

from datetime import datetime
from app import db

class BlogPost(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(100), nullable = False)
    content = db.Column(db.Text, nullable = False)
    created_at = db.Column(db.DateTime, default = datetime.utcnow)

    def __repr__(self):
        return f'<BlogPost {self.title}>'