from flask import request, jsonify, session, Blueprint, render_template
from flaskAppConfig import db_info
from datetime import datetime, timezone
from pytz import timezone
from zoneinfo import ZoneInfo
from psycopg2 import sql
import psycopg2
from utils import uniqueID

idGen = uniqueID(10000, 99999, db_info)

app_bp = Blueprint('blog_routes', __name__)

#create new blog post
@app_bp.route('/createposts', methods = ['POST'])
def create_post():
    userAccountid = session.get('accountid')
    #print(f"Account ID in session: {userAccountid}")
    data = request.get_json()
    title = data.get('title')
    content = data.get('content')
    status = data.get('status', 'draft')
    created_at = datetime.now(timezone('America/Chicago'))

    if not title or not content:
        return jsonify({'message': 'Title and content are required!'}), 400

    try: 
        conn = psycopg2.connect(**db_info)
        cur = conn.cursor()
        #userAccountid = session.get('accountid')
        cur.execute("INSERT INTO blog (blogid, blogtitle, dbinstance, dateposted, accountid, status) VALUES (%s, %s, %s, %s, %s, %s)", (idGen.genID(), title, content, created_at, userAccountid, status ))
        conn.commit()
        cur.close()
        conn.close()
        if status == 'published':
            return jsonify({'message': 'Post successfully created!'}), 201
        else:
            return jsonify({'message': 'Post successfully created but not published!'}), 201
    except Exception as e:
        return jsonify({'message': f'Error creating post: {str(e)}'}), 500
    

#read all blog posts
@app_bp.route('/readposts', methods = ['GET'])
def get_posts():
    try:
        conn = psycopg2.connect(**db_info)
        cur = conn.cursor()
        cur.execute("SELECT blogtitle, dbinstance, dateposted, users.firstName, users.lastName FROM blog JOIN users on blog.accountid = users.accountid WHERE status = 'published' ORDER by dateposted DESC")
        posts = cur.fetchall()
        cur.close()
        conn.close()
        posts_data = [{"title": post[0], "content": post[1], "date": post[2].strftime("%B %d, %Y"), "firstName": post[3], "lastName": post[4]} for post in posts]
        return jsonify(posts_data), 200
    except Exception as e:
        return jsonify({'message': f'Error retrieving posts: {str(e)}'}), 500

#read last 3 blog posts
@app_bp.route('/read-latest-posts', methods = ['GET'])
def get_latest_posts():
    try:
        conn = psycopg2.connect(**db_info)
        cur = conn.cursor()
        cur.execute("SELECT blogtitle, dbinstance, dateposted, users.firstName, users.lastName FROM blog JOIN users on blog.accountid = users.accountid WHERE status = 'published' ORDER by dateposted DESC")
        posts = cur.fetchmany(size=3)
        cur.close()
        conn.close()
        posts_data = [{"title": post[0], "content": post[1], "date": post[2].strftime("%B %d, %Y"), "firstName": post[3], "lastName": post[4]} for post in posts]
        return jsonify(posts_data), 200
    except Exception as e:
        return jsonify({'message': f'Error retrieving posts: {str(e)}'}), 500
    
@app_bp.route('/get-single-post/<int:id>', methods = ['GET'])
def single_post(id):
    accountid = session.get('accountid')
    try:
        conn = psycopg2.connect(**db_info)
        cur = conn.cursor()
        cur.execute("SELECT blogtitle, dbinstance, status FROM blog WHERE blogid = %s AND accountid = %s",(id, accountid))
        post = cur.fetchone()
        cur.close()
        conn.close()
        if post:
            return jsonify({"title": post[0],"content": post[1],"status": post[2]}), 200
        else:
            return jsonify({'message': 'Post not found'}), 404
    except Exception as e:
        return jsonify({'message': f'Error retrieving post: {str(e)}'}), 500
   

#update existing blog post
@app_bp.route('/updateposts/<int:id>', methods = ['PUT'])
def update_post(id):
    data = request.get_json()
    new_title = data.get('title')
    new_content = data.get('content')
    if not new_title and not new_content:
        return jsonify({'message': 'Need to update title or content to update blog post!'}), 400
    
    utc_time_updated = datetime.now(timezone.utc)
    time_updated = utc_time_updated.astimezone(ZoneInfo("America/Chicago"))
    try:
        conn = psycopg2.connect(**db_info)
        cur = conn.cursor()
        if new_title:
            cur.execute("UPDATE blog SET blogtitle = %s WHERE blogid = %s", (new_title, id))
        if new_content:
            cur.execute("UPDATE blog SET dbinstance = %s WHERE blogid = %s", (new_content, id))
        cur.execute("UPDATE blog SET dateposted = %s WHERE blogid = %s", (time_updated, id))
        conn.commit()
        cur.close()
        conn.close()
        return jsonify({'message': 'Post updated successfully'}), 200
    except Exception as e:
        return jsonify({'message': f'Error updating post: {str(e)}'}), 500
    

#delete existing blog post
@app_bp.route('/deleteposts/<int:id>', methods = ['DELETE'])
def delete_post(id):
    try:
        conn = psycopg2.connect(**db_info)
        cur = conn.cursor()
        cur.execute("DELETE FROM blog WHERE blogid = %s", (id,))
        conn.commit()
        cur.close()
        conn.close()
        return jsonify({'message': 'Post deleted successfully'}), 200
    except Exception as e:
        return jsonify({'message': f'Error deleting post: {str(e)}'}), 500
   