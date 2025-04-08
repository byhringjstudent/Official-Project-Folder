"""
Author :Jaden
Date   :April 5, 2025
Purpose:This file defines the CRUD operations for the blog post.
"""

from flask import request, jsonify
from app import app, db
from models import BlogPost

#create new blog post
@app.route('/api/posts', methods = ['POST'])
def create_post():
    date = request.get_json()
    new_post = BlogPost(
        title = date['title']
        content = data['content']
    )
#add new post to database and commit the transaction    
    db.session.add(new_post)
    db.session.commit()
    return jsonify({'message': 'Post successfully created!', 'id': new_post.id}), 201

#read all blog posts
@app.route('/api/posts', methods = ['GET'])
def get_posts():
    posts = BlogPost.query.all()
    return jsonify([{
        'id': post.id,
        'title': post.title,
        'content': post.content,
        'created_at': post.created_at
    } for post in posts])

#update existing blog post
@app.route('/api/posts/<int:id>', methods = ['PUT'])
def update_post(id):
    date = request.get_json()
    post = BlogPost.query.get_or_404(id)
    post.title = data['title']
    post.content = data['content']
    db.session.commit()
    return jsonify({'message': 'Post updated successfully'})

#delete existing blog post
@app.route('/api/posts/<int:id>', methods = ['DELETE'])
def delete_post(id):
    post = BlogPost.query.get_or_404(id)
    db.session.delete(post)
    db.session.commit()
    return jsonify({'message': 'Post deleted successfully'})