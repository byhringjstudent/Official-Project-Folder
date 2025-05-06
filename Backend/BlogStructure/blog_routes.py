from flask import request, jsonify, session, Blueprint
from flaskAppConfig import db_info
from datetime import datetime, timezone
from pytz import timezone
import psycopg2
from utils import create_unique_id
from werkzeug.utils import secure_filename
import os
import json
from .blog_db_functions import *



app_bp = Blueprint('blog_routes', __name__)

#Purpose: This route allows users to create blog posts. Users will include a title, short description of the blog, the content
#of the blog, tags, and an image. 
#The image will be saved in the static/uploads folder.  
# The blog post will be saved in the database with a status of either draft or published.
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
    result, status_code = create_blog_post(title, content, shortDescription, status, created_at, tags, userAccountid, image_url)
    if result['status'] == 'success':
        return jsonify({'message': result['message']}), status_code 
    else:
        return jsonify({'message': result['message']}), status_code
    
    

#purpose: This route allows users to view all blog posts.
# Users will be able to view all blog posts that are published.
@app_bp.route('/readposts', methods = ['GET'])
def get_posts():
    result, status_code = get_all_blog_posts()
    if result['status'] == 'success':
        return jsonify({'posts': result['posts']}), status_code
    else:
        return jsonify({'message': result['message']}), status_code


#Purpose: This route allows users to view the latest blog posts.
# Users will be able to view the 2 latest blog posts that are published.
@app_bp.route('/read-latest-posts', methods = ['GET'])
def get_latest_posts():
    result, status_code = get_latest_blog_posts()
    if result['status'] == 'success':
        return jsonify({'posts': result['posts']}), status_code
    else:
        return jsonify({'message': result['message']}), status_code
    

#Purpose: allow users to view one of their posts 
# Users will be able to view one of their posts by using the blog id.
# The blog id will be passed in the URL.
@app_bp.route('/get-single-post/<uuid:id>', methods = ['GET'])
def single_post(id):
    accountid = session.get('accountid')
    if not accountid:
        return jsonify({'message': 'User not logged in!'}), 401
    result, status_code = get_blog_post_by_id(id)
    if result['status'] == 'success':
        return jsonify({'post': result['post']}), status_code
    else:
        return jsonify({'message': result['message']}), status_code
   

#Purpose: update existing blog post
# Users will be able to update their blog post by using the blog id.
# The blog id will be passed in the URL.
@app_bp.route('/updateposts/<uuid:id>', methods = ['PUT'])
def update_post(id):
    new_title = request.form.get('title')
    new_content = request.form.get('content')
    new_status = request.form.get('status')
    new_shortdescription = request.form.get('shortdescription')
    new_tags = json.loads(request.form.get('tags')) if request.form.get('tags') else []  # Ensure tags are JSON    
    image_url = None
    
  
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
            #print(f"Image path: {image_path}")
            
            # Check if the image exists and delete it
            if os.path.exists(image_path):
                #print(f"Image exists, attempting to delete: {image_path}")
                os.remove(image_path)
                #print(f"Image successfully deleted: {image_path}")
            else:
                print(f"Image not found at path: {image_path}")
        
        if not new_title and not new_content and not new_status and not new_shortdescription and not new_tags:
            return jsonify({'message': 'Need to update title, content, status, short description, or tags to update blog post!'}), 400
    
    #print(f"this is the new image_url: {image_url}")
    updated_at = datetime.now(timezone('America/Chicago'))
    result, status_code = update_blog_post(id, new_title, new_content, new_shortdescription, new_status, updated_at, new_tags, image_url)
    if result['status'] == 'success':
        return jsonify({'message': result['message']}), status_code
    else:   
        return jsonify({'message': result['message']}), status_code


#delete existing blog post
@app_bp.route('/deleteposts/<uuid:id>', methods = ['DELETE'])
def delete_post(id):
    result, status_code = delete_blog_post(id)
    if result['status'] == 'success':
        return jsonify({'message': result['message']}), status_code
    else:
        return jsonify({'message': result['message']}), status_code

#purpose: Allow user to search for specific blogs, based on tags, title, or short description. 
#this route is specifically for the blog page, it will only return publshed blogs.
@app_bp.route('/search-published-post', methods = ['GET'])
def search_published_blogs():
    query = request.args.get('q', '').strip()
    result, status_code = search_published_posts(query)
    if result['status'] == 'success':
        return jsonify({'status': 'success','post': result['post']}), status_code
    else:
        return jsonify({'status': 'error','message': result['message']}), status_code
    
    
#purpose: Allow user to search for specific blogs, based on tags, title, or short description. 
#this route is specifically for the acount portal page, it will return all blogs whether publshed or saved as draft.
@app_bp.route('/search-all-post', methods = ['GET'])
def search_all_blogs():
    accountid = session.get('accountid')
    query = request.args.get('q', '').strip()
    result, status_code = search_all_posts(query,accountid)
    if result['status'] == 'success':
        return jsonify({'status': 'success','post': result['post']}), status_code
    else:
        return jsonify({'status': 'error','message': result['message']}), status_code
    
   