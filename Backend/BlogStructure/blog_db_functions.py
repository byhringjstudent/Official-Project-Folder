import psycopg2
from psycopg2 import sql
from utils import create_unique_id
from flaskAppConfig import db_info
import os

#purpose: This function is for creating a blog post in the database.
def create_blog_post(title, content, shortDescription, status, created_at, tags, accountid, image_url):
    try:
        conn = psycopg2.connect(**db_info) #connect to the database
        cur = conn.cursor()
        cur.execute("INSERT INTO blog (blogid, blogtitle, dbinstance, dateposted, accountid, status, image_url, tags, shortdescription) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)", (create_unique_id(), title, content, created_at, accountid, status, image_url, tags, shortDescription))
        conn.commit()
        cur.close()
        conn.close()
        if status == 'published':
            return {'status': 'success', 'message': 'Blog post created successfully and published.'}, 201
        else:
            return {'status': 'success', 'message': 'Blog post created successfully and saved as draft.'}, 201
        
    except psycopg2.Error as e:
        return {'status': 'error', 'message': str(e)}, 500
    finally:
        if conn:
            conn.close()
        if cur:
            cur.close()

#purpose: This function is for getting all blog posts from the database that are published.
def get_all_blog_posts():
    try:
        conn = psycopg2.connect(**db_info) #connect to the database
        cur = conn.cursor()
        cur.execute("SELECT blogtitle, dbinstance, dateposted, image_url, shortdescription, tags, users.firstName, users.lastName FROM blog JOIN users on blog.accountid = users.accountid WHERE status = 'published' ORDER by dateposted DESC")
        posts = cur.fetchall()
        posts_data = [{"title": post[0], "content": post[1], "date": post[2].strftime("%B %d, %Y"), "image_url" : post[3],"shortdescription" : post[4],"tags" : post[5], "firstName": post[6], "lastName": post[7]} for post in posts]
        return {'status': 'success', 'posts': posts_data}, 200
    except psycopg2.Error as e:
        return {'status': 'error', 'message': str(e)}, 500
    finally:
        if conn:
            conn.close()
        if cur:
            cur.close()

#Purpose: This function is for getting the 2 lates blog posts from the database that are published.
def get_latest_blog_posts():
    try:
        conn = psycopg2.connect(**db_info) #connect to the database
        cur = conn.cursor()
        cur.execute("SELECT blogtitle, dbinstance, dateposted, image_url, shortdescription, tags, users.firstName, users.lastName FROM blog JOIN users on blog.accountid = users.accountid WHERE status = 'published' ORDER by dateposted DESC")
        posts = cur.fetchmany(size=2)
        posts_data = [{"title": post[0], "content": post[1], "date": post[2].strftime("%B %d, %Y"), "image_url" : post[3],"shortdescription" : post[4],"tags" : post[5], "firstName": post[6], "lastName": post[7]} for post in posts]
        return {'status': 'success', 'posts': posts_data}, 200
    except psycopg2.Error as e:
        return {'status': 'error', 'message': str(e)}, 500
    finally:
        if conn:
            conn.close()
        if cur:
            cur.close()

#Purpose: This function allows users to get a specific blog post by its ID.
def get_blog_post_by_id(blogid):
    try:
        conn = psycopg2.connect(**db_info) #connect to the database
        cur = conn.cursor()
        cur.execute("SELECT blogtitle, dbinstance, dateposted, image_url, shortdescription, tags, status, users.firstName, users.lastName FROM blog JOIN users on blog.accountid = users.accountid WHERE blogid = %s",(str(blogid),))
        post = cur.fetchone()
        if post:
            post_data = [{"title": post[0],"content": post[1], "date": post[2].strftime("%B %d, %Y"), "image_url" : post[3],"shortdescription" : post[4],"tags" : post[5],"status": post[6]}]
            return {'status': 'success', 'post': post_data}, 200
        else:
            return {'status': 'error', 'message': 'Blog post not found.'}, 404
    except psycopg2.Error as e:
        return {'status': 'error', 'message': str(e)}, 500
    finally:
        if conn:
            conn.close()
        if cur:
            cur.close()

#Purpose: This function allows users to get update a specific blog post by its ID.
def update_blog_post(blogid, title, content, shortDescription, status, updated_at, tags, image_url):
    try:
        conn = psycopg2.connect(**db_info) #connect to the database
        cur = conn.cursor()
        if title:
            cur.execute("UPDATE blog SET blogtitle = %s WHERE blogid = %s", (title, str(blogid)))
        if content:
            cur.execute("UPDATE blog SET dbinstance = %s WHERE blogid = %s", (content, str(blogid)))
        if status:
            cur.execute("UPDATE blog SET status = %s WHERE blogid = %s", (status, str(blogid)))
        if shortDescription:
            cur.execute("UPDATE blog SET shortdescription = %s WHERE blogid = %s", (shortDescription, str(blogid)))
        if tags:
            cur.execute("UPDATE blog SET tags = %s WHERE blogid = %s", (tags, str(blogid)))
        if image_url:
            cur.execute("UPDATE blog SET image_url = %s WHERE blogid = %s", (image_url, str(blogid)))
        cur.execute("UPDATE blog SET dateposted = %s WHERE blogid = %s", (updated_at, str(blogid)))
        conn.commit()
        return {'status': 'success', 'message': 'Blog post updated successfully.'}, 200
    except psycopg2.Error as e:
        return {'status': 'error', 'message': str(e)}, 500
    finally:
        if conn:
            conn.close()
        if cur:
            cur.close()


#Purpose: This function allows users to delete a specific blog post by its ID.
def delete_blog_post(blogid):
    try:
        conn = psycopg2.connect(**db_info) #connect to the database
        cur = conn.cursor()
         # Retrieve the image filename from the database (adjust the column name if needed)
        cur.execute("SELECT image_url FROM blog WHERE blogid = %s", (str(blogid),))
        post = cur.fetchone()
        
        if post:
            image_url = post[0]  # assuming the image URL is in the first column
            
            # Normalize path (convert backslashes to forward slashes)
            
            if image_url:
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
    
        cur.execute("DELETE FROM blog WHERE blogid = %s", (str(blogid),))
        conn.commit()
        return {'status': 'success', 'message': 'Blog post deleted successfully.'}, 200
    except psycopg2.Error as e:
        return {'status': 'error', 'message': str(e)}, 500
    finally:
        if conn:
            conn.close()
        if cur:
            cur.close()


#purpose: this function allows users to search for blogs based on their short description, title, or tags.
#This function will only return posts that are publshed because that is all that
#should be displayed on the blog page. 
def search_published_posts(userSearch):
    try:
        conn = psycopg2.connect(**db_info) #connect to the database
        cur = conn.cursor()
        if userSearch:
            cur.execute("SELECT blogid, blogtitle, dbinstance, dateposted, image_url, shortdescription, tags, users.firstName, users.lastName FROM blog JOIN users on blog.accountid = users.accountid WHERE status = 'published' AND (blogtitle ILIKE %s OR EXISTS (SELECT 1 FROM unnest(tags) AS tag WHERE tag ILIKE %s) OR shortdescription ILIKE %s OR users.firstName ILIKE %s OR users.lastName ILIKE %s) ORDER BY dateposted DESC",(f'%{userSearch}',f'%{userSearch}',f'%{userSearch}',f'%{userSearch}',f'%{userSearch}'))
        else:
            cur.execute("SELECT blogid, blogtitle, dbinstance, dateposted, image_url, shortdescription, tags, users.firstName, users.lastName FROM blog JOIN users on blog.accountid = users.accountid WHERE status = 'published' AND (blogtitle ILIKE %s OR EXISTS (SELECT 1 FROM unnest(tags) AS tag WHERE tag ILIKE %s) OR shortdescription ILIKE %s OR users.firstName ILIKE %s OR users.lastName ILIKE %s) ORDER BY dateposted DESC",(f'%{userSearch}',f'%{userSearch}',f'%{userSearch}',f'%{userSearch}',f'%{userSearch}'))
        posts = cur.fetchall()
        
        if posts:
            #print(posts)
            posts_data = [{"blogID": post[0], "title": post[1],"content": post[2], "date": post[3].strftime("%B %d, %Y"), "image_url" : post[4],"shortdescription" : post[5],"tags" : post[6], "firstName": post[7], "lastName": post[8]} for post in posts]
            return {'status': 'success', 'post': posts_data}, 200
        else:
            return {'status': 'error', 'message': 'No posts found'}, 200
        
    except psycopg2.Error as e:
        #print(str(e))
        return {'status': 'error', 'message': str(e)}, 500
    
    finally:
        if conn:
            conn.close()
        if cur:
            cur.close()
            
#Purpose: Search all posts whether published or a draft.
#This would be used in the account portal when a user is searching their own
#blogs.       
def search_all_posts(userSearch, accountid):
    try:
        conn = psycopg2.connect(**db_info) #connect to the database
        cur = conn.cursor()
        if userSearch:
            cur.execute("SELECT blogtitle, dbinstance, dateposted, image_url, shortdescription, tags, status FROM blog WHERE accountid = %s AND (blogtitle ILIKE %s OR EXISTS (SELECT 1 FROM unnest(tags) AS tag WHERE tag ILIKE %s) OR shortdescription ILIKE %s OR status ILIKE %s) ORDER BY dateposted DESC",(accountid,f'%{userSearch}',f'%{userSearch}',f'%{userSearch}', f'%{userSearch}'))
            posts = cur.fetchall()
            if posts:
                posts_data = [{"title": post[0],"content": post[1], "date": post[2].strftime("%B %d, %Y"), "image_url" : post[3],"shortdescription" : post[4],"tags" : post[5], "status":post[6]}for post in posts]
                return {'status': 'success', 'post': posts_data}, 200
            else:
                return {'status': 'error', 'message': 'No results'}, 500
        else:
            return {'status': 'error', 'message': 'No search given'}, 500
        
    except psycopg2.Error as e:
        print(str(e))
        return {'status': 'error', 'message': str(e)}, 500
    
    finally:
        if conn:
            conn.close()
        if cur:
            cur.close()
        
        

