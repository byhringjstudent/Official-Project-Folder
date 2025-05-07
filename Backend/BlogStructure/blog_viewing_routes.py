from flask import request, jsonify, session, Blueprint
from .blog_db_functions import *



app_bp = Blueprint('blog_viewing_routes', __name__)

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