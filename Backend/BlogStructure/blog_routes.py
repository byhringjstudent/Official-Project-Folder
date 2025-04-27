from flask import request, jsonify, session, Blueprint, render_template
from flaskAppConfig import db_info
from datetime import datetime, timezone
from pytz import timezone
from zoneinfo import ZoneInfo
from psycopg2 import sql
import psycopg2
from utils import create_unique_id
from werkzeug.utils import secure_filename
import os
import json
from PIL import Image



app_bp = Blueprint('blog_routes', __name__)

#Purpose: This route allows users to create blog posts. Users will include a title, short description of the blog, the content
#of the blog, tags, and an image. 
UPLOAD_FOLDER = 'static/uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app_bp.route('/createposts', methods = ['POST'])
def create_post():
    userAccountid = session.get('accountid')
    #print(userAccountid)
    title = request.form.get('title')
    content = request.form.get('content')
    shortDescription = request.form.get('shortDescription')
    status = request.form.get('status', 'draft')
    created_at = datetime.now(timezone('America/Chicago'))
    tags = json.loads(request.form.get('tags')) if request.form.get('tags') else []  # Ensure tags are JSON
    
    if not title or not content or not shortDescription or not tags:
        return jsonify({'message': 'Title, content, a short description, and tags are required!'}), 400

    image_url = None
    if 'image' in request.files:
        image = request.files['image']
        if image and allowed_file(image.filename):
            filename = str(create_unique_id()) + os.path.splitext(image.filename)[1]
            filename = secure_filename(filename)
            filepath = os.path.join(UPLOAD_FOLDER, filename)
            image.save(filepath)
            image_url = f"/{filepath}"  # Or generate full URL if needed
        else:
            filename = str(create_unique_id()) + '.jpg'  # Force .jpg extension
            filename = secure_filename(filename)
            filepath = os.path.join(UPLOAD_FOLDER, filename)
            image.save(filepath)
            image_url = f"/{filepath}"
    try: 
        conn = psycopg2.connect(**db_info)
        cur = conn.cursor()
        #userAccountid = session.get('accountid')
        cur.execute("INSERT INTO blog (blogid, blogtitle, dbinstance, dateposted, accountid, status, image_url, tags, shortdescription) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)", (create_unique_id(), title, content, created_at, userAccountid, status, image_url, tags, shortDescription))
        conn.commit()
        cur.close()
        conn.close()
        if status == 'published':
            return jsonify({'message': 'Post successfully created!'}), 201
        else:
            return jsonify({'message': 'Post successfully created but not published!'}), 201
    except Exception as e:
        print(f"Error: {str(e)}")
        return jsonify({'message': f'Error creating post: {str(e)}'}), 500
    
    

#read all blog posts
@app_bp.route('/readposts', methods = ['GET'])
def get_posts():
    try:
        conn = psycopg2.connect(**db_info)
        cur = conn.cursor()
        cur.execute("SELECT blogtitle, dbinstance, dateposted, image_url, shortdescription, tags, users.firstName, users.lastName FROM blog JOIN users on blog.accountid = users.accountid WHERE status = 'published' ORDER by dateposted DESC")
        posts = cur.fetchall()
        cur.close()
        conn.close()
        posts_data = [{"title": post[0], "content": post[1], "date": post[2].strftime("%B %d, %Y"), "image_url" : post[3],"shortdescription" : post[4],"tags" : post[5], "firstName": post[6], "lastName": post[7]} for post in posts]
        return jsonify({"posts": posts_data}), 200
    except Exception as e:
        return jsonify({'message': f'Error retrieving posts: {str(e)}'}), 500

#read last 3 blog posts
@app_bp.route('/read-latest-posts', methods = ['GET'])
def get_latest_posts():
    try:
        conn = psycopg2.connect(**db_info)
        cur = conn.cursor()
        cur.execute("SELECT blogtitle, dbinstance, dateposted, image_url, shortdescription, tags, users.firstName, users.lastName FROM blog JOIN users on blog.accountid = users.accountid WHERE status = 'published' ORDER by dateposted DESC")
        posts = cur.fetchmany(size=3)
        cur.close()
        conn.close()
        posts_data = [{"title": post[0], "content": post[1], "date": post[2].strftime("%B %d, %Y"), "image_url" : post[3],"shortdescription" : post[4],"tags" : post[5], "firstName": post[6], "lastName": post[7]} for post in posts]
        return jsonify({"posts" : posts_data}), 200
    except Exception as e:
        return jsonify({'message': f'Error retrieving posts: {str(e)}'}), 500
    

#allow users to view one of their posts 
@app_bp.route('/get-single-post/<uuid:id>', methods = ['GET'])
def single_post(id):
    accountid = session.get('accountid')
    print(accountid)
    print(id)
    try:
        conn = psycopg2.connect(**db_info)
        cur = conn.cursor()
        cur.execute("SELECT blogtitle, dbinstance, dateposted, image_url, shortdescription, tags, status FROM blog WHERE blogid = %s and accountid = %s",(str(id), str(accountid)))
        post = cur.fetchone()
        cur.close()
        conn.close()
        if post:
            post_data = [{"title": post[0],"content": post[1], "date": post[2].strftime("%B %d, %Y"), "image_url" : post[3],"shortdescription" : post[4],"tags" : post[5],"status": post[6]}]
            return jsonify({"post": post_data}), 200
        else:
            return jsonify({'message': 'Post not found'}), 404
    except Exception as e:
        return jsonify({'message': f'Error retrieving post: {str(e)}'}), 500
   

#update existing blog post
@app_bp.route('/updateposts/<uuid:id>', methods = ['PUT'])
def update_post(id):
    new_title = request.form.get('title')
    new_content = request.form.get('content')
    new_status = request.form.get('status')
    new_shortdescription = request.form.get('shortdescription')
    new_tags = json.loads(request.form.get('tags')) if request.form.get('tags') else []  # Ensure tags are JSON    
    image_url = None
    
    current_image_url = None
    try:
        conn = psycopg2.connect(**db_info)
        cur = conn.cursor()
        cur.execute("SELECT image_url FROM blog WHERE blogid = %s", (str(id),))
        post = cur.fetchone()
        if post:
            current_image_url = post[0]
            print(current_image_url)
        cur.close()
        conn.close()
    except Exception as e:
        return jsonify({'message': f'Error retrieving current image URL: {str(e)}'}), 500
    
    if 'image' in request.files:
        image = request.files['image']
        if image and allowed_file(image.filename):
            filename = str(create_unique_id()) + os.path.splitext(image.filename)[1]
            filename = secure_filename(filename)
            filepath = os.path.join(UPLOAD_FOLDER, filename)
            print(filepath)
            image.save(filepath)
            image_url = f"/{filepath}"  # Or generate full URL if needed
        else:
            filename = str(create_unique_id()) + '.jpg'  # Force .jpg extension
            filename = secure_filename(filename)
            filepath = os.path.join(UPLOAD_FOLDER, filename)
            image.save(filepath)
            image_url = f"/{filepath}"
            
        if current_image_url:            
            # Normalize path (convert backslashes to forward slashes)
            current_image_url = current_image_url.replace("\\", "/")
            if current_image_url.startswith('/static'):
                current_image_url = current_image_url[7:]  # Remove '/static' from the start of the path
                

            
            # Construct the local file path
            # Ensure we get the absolute path to the 'static' folder
            static_folder_path = os.path.abspath('static')
            image_path = os.path.join(static_folder_path, current_image_url.lstrip('/'))  # Remove leading slash from URL
            
            # Log the file path for debugging
            print(f"Image path: {image_path}")
            
            # Check if the image exists and delete it
            if os.path.exists(image_path):
                print(f"Image exists, attempting to delete: {image_path}")
                os.remove(image_path)
                print(f"Image successfully deleted: {image_path}")
            else:
                print(f"Image not found at path: {image_path}")
        
    if not new_title and not new_content and not new_status and not new_shortdescription and not new_tags:
        return jsonify({'message': 'Need to update title, content, status, short description, or tags to update blog post!'}), 400
    
    print(f"this is the new image_url: {image_url}")
    updated_at = datetime.now(timezone('America/Chicago'))
    try:
        conn = psycopg2.connect(**db_info)
        cur = conn.cursor()
        if new_title:
            cur.execute("UPDATE blog SET blogtitle = %s WHERE blogid = %s", (new_title, str(id)))
        if new_content:
            cur.execute("UPDATE blog SET dbinstance = %s WHERE blogid = %s", (new_content, str(id)))
        if new_status:
            cur.execute("UPDATE blog SET status = %s WHERE blogid = %s", (new_status, str(id)))
        if new_shortdescription:
            cur.execute("UPDATE blog SET shortdescription = %s WHERE blogid = %s", (new_shortdescription, str(id)))
        if new_tags:
            cur.execute("UPDATE blog SET tags = %s WHERE blogid = %s", (new_tags, str(id)))
        if image_url:
            cur.execute("UPDATE blog SET image_url = %s WHERE blogid = %s", (image_url, str(id)))
        cur.execute("UPDATE blog SET dateposted = %s WHERE blogid = %s", (updated_at, str(id)))
        conn.commit()
        cur.close()
        conn.close()
        return jsonify({'message': 'Post updated successfully'}), 200
    except Exception as e:
        print(f"Error occurred: {str(e)}")
        return jsonify({'message': f'Error updating post: {str(e)}'}), 500
    

#delete existing blog post
@app_bp.route('/deleteposts/<uuid:id>', methods = ['DELETE'])
def delete_post(id):
    try:
        conn = psycopg2.connect(**db_info)
        cur = conn.cursor()
         # Retrieve the image filename from the database (adjust the column name if needed)
        cur.execute("SELECT image_url FROM blog WHERE blogid = %s", (str(id),))
        post = cur.fetchone()
        
        if post:
            image_url = post[0]  # assuming the image URL is in the first column
            
            # Normalize path (convert backslashes to forward slashes)
            image_url = image_url.replace("\\", "/")
            if image_url.startswith('/static'):
                image_url = image_url[7:]  # Remove '/static' from the start of the path

            
            # Construct the local file path
            # Ensure we get the absolute path to the 'static' folder
            static_folder_path = os.path.abspath('static')
            image_path = os.path.join(static_folder_path, image_url.lstrip('/'))  # Remove leading slash from URL
            
            # Log the file path for debugging
            print(f"Image path: {image_path}")
            
            # Check if the image exists and delete it
            if os.path.exists(image_path):
                print(f"Image exists, attempting to delete: {image_path}")
                os.remove(image_path)
                print(f"Image successfully deleted: {image_path}")
            else:
                print(f"Image not found at path: {image_path}")
    
        cur.execute("DELETE FROM blog WHERE blogid = %s", (str(id),))
        conn.commit()
        cur.close()
        conn.close()
        return jsonify({'message': 'Post deleted successfully'}), 200
    except Exception as e:
        return jsonify({'message': f'Error deleting post: {str(e)}'}), 500
   