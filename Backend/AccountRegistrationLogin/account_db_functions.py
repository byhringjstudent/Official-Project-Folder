import psycopg2
from psycopg2 import sql
from utils import create_unique_id
from flaskAppConfig import db_info
import bcrypt
from EmailVerification.email_verification_routes import send_verification_email

#Purpose: This function creates a new user in the database.
# It takes the user's email, hashed password, first name, and last name as input.
def create_user(email, hashed_password_str, firstName, lastName):
    try:
    # Connect to the PostgreSQL database
        conn = psycopg2.connect(**db_info) #connect to the database
        cur = conn.cursor()
        #check if the email already exists in the database
        query = sql.SQL("SELECT accountid FROM users WHERE email = %s")
        cur.execute(query, (email,))
        result = cur.fetchone()
        if result:
            #if the email already exists return jsonify with error message and 409 status code
            return {'status': 'error', 'message': 'Email already exists'}, 409
        #if the email does not exist insert the new user into the database
        accountid = create_unique_id()#generate a unique account ID
        cur.execute("INSERT INTO account (accountid, accounttype, orgid) VALUES (%s, %s, %s)", (accountid, "Free", create_unique_id()))
        cur.execute("INSERT INTO users (userid, email, password, firstname, lastname, accountid) VALUES (%s, %s, %s, %s, %s, %s)", (create_unique_id(), email, hashed_password_str, firstName, lastName, accountid))
        conn.commit()
        cur.close()
        conn.close()
        return {'status': 'success', 'accountid': accountid, 'userid': create_unique_id()}, 201
    except psycopg2.Error as e:
        print("Database error:", e)
        return {'status': 'error', 'message': 'Database error'}, 500
    finally:
        if cur:
            cur.close()
        if conn:
            conn.close()


#Purpose: This function logs in a user by checking their email and password.
# It retrieves the hashed password from the database and compares it with the provided password.
# If the password matches, it fetches the account ID and user ID from the database.
def login_user(email, password):
    try:
        conn = psycopg2.connect(**db_info)
        cur = conn.cursor()
        
        # Step 1: Get the hashed password
        cur.execute(sql.SQL("SELECT password FROM users WHERE email = %s"), (email,))
        result = cur.fetchone()
        
        if not result:
            # No such email
            return {'status': 'error', 'message': 'Email not found'}, 404
        
        stored_hash = result[0]
        
        # Step 2: Verify password
        if not bcrypt.checkpw(password.encode('utf-8'), stored_hash.encode('utf-8')):
            return {'status': 'error', 'message': 'Incorrect password'}, 401
        
        # Step 3: Fetch accountid and userid
        cur.execute(sql.SQL("SELECT accountid, userid FROM users WHERE email = %s"), (email,))
        accountid, userid = cur.fetchone()
        
        return {
            'status': 'success',
            'accountid': accountid,
            'userid': userid
        }, 200
        
    except psycopg2.Error as e:
        print("Database error:", e)
        return {'status': 'error', 'message': 'Database error'}, 500
    
    finally:
        if cur:
            cur.close()
        if conn:
            conn.close()




#Purpose: This function retrieves user information based on the account ID.
# It fetches the user's email, first name, last name, and verified email status from the database.
def get_user_info(accountid):  
    try:
        conn = psycopg2.connect(**db_info)
        cur = conn.cursor()
        
        # Fetch user information based on accountid
        cur.execute(sql.SQL("SELECT email, firstname, lastname, verifiedemail FROM users WHERE accountid = %s"), (accountid,))
        result = cur.fetchone()
        
        if not result:
            return {'status': 'error', 'message': 'User not found'}, 404
        
        email, firstname, lastname, verifiedemail = result
        
        return {
            'status': 'success',
            'email': email,
            'firstName': firstname,
            'lastName': lastname,
            'verifiedemail': verifiedemail  
        }, 200
        
    except psycopg2.Error as e:
        print("Database error:", e)
        return {'status': 'error', 'message': 'Database error'}, 500
    
    finally:
        if cur:
            cur.close()
        if conn:
            conn.close()




#Purpose: This function retrieves all blogs associated with a specific user based on their account ID.
# It fetches the blog ID, title, content, date posted, status, short description, and tags from the database.
def get_user_blogs(accountid):  
    try:
        conn = psycopg2.connect(**db_info)
        cur = conn.cursor()
        
        # Fetch user blogs based on accountid
        cur.execute("SELECT blogid, blogtitle, dbinstance, dateposted, status, shortdescription, tags FROM blog WHERE accountid = %s ORDER BY dateposted DESC", (accountid,))
        posts = cur.fetchall()
        
        if not posts:
            return {'status': 'error', 'message': 'No blogs found'}, 404
        
        posts_data = [{"blogID": post[0], "title": post[1], "content": post[2], "date": post[3].strftime("%B %d, %Y"), "status": post[4], "shortdescription": post[5], "tags": post[6]} for post in posts] #format the result into a list of dictionaries
        
        return {'status': 'success','blogs': posts_data }, 200
        
    except psycopg2.Error as e:
        print("Database error:", e)
        return {'status': 'error', 'message': 'Database error'}, 500
    
    finally:
        if cur:
            cur.close()
        if conn:
            conn.close()




#Purpose: This function retrieves all draft blog posts from a specific user based on their account ID.
# It fetches the blog ID, title, content, date posted, status, short description, and tags from the database.
def get_user_drafts(accountid):  
    try:
        conn = psycopg2.connect(**db_info)
        cur = conn.cursor()
        
        # Fetch user blogs based on accountid
        cur.execute("SELECT blogid, blogtitle, dbinstance, dateposted, status, shortdescription, tags FROM blog WHERE accountid = %s AND status = 'Draft' ORDER BY dateposted DESC", (accountid,))
        posts = cur.fetchall()
        
        if not posts:
            return {'status': 'error', 'message': 'No drafts found'}, 404
        
        posts_data = [{"blogID": post[0], "title": post[1], "content": post[2], "date": post[3].strftime("%B %d, %Y"), "status": post[4], "shortdescription": post[5], "tags": post[6]} for post in posts] #format the result into a list of dictionaries
        
        return {
            'status': 'success',
            'drafts': posts_data  
        }, 200
        
    except psycopg2.Error as e:
        print("Database error:", e)
        return {'status': 'error', 'message': 'Database error'}, 500
    
    finally:
        if cur:
            cur.close()
        if conn:
            conn.close()




#Purpose: This function updates users information in the database.
#It allows updating the user's first name, last name, and email address.
# It checks if the new email already exists in the database before updating.
def update_user_info(accountid, firstName, lastName, email):
    try:
        conn = psycopg2.connect(**db_info)
        cur = conn.cursor()
        if not firstName and not lastName and not email:
            return {'status': 'error','message': f'Error Updating Account: No Information Provided.'}, 400 
        
        if firstName:
            query = sql.SQL("UPDATE users set firstname = %s WHERE accountid = %s") #query to update the first name in the database
            cur.execute(query, (firstName, accountid)) #execute the query with the new first name and account ID as parameters
        
        if lastName:
            query = sql.SQL("UPDATE users set lastname = %s WHERE accountid = %s") #query to update the last name in the database
            cur.execute(query, (lastName, accountid)) #execute the query with the new last name and account ID as parameters

        
        if email:
            cur.execute("SELECT email FROM users WHERE email = %s", (email,)) #check if the new email already exists in the database
            result = cur.fetchone() #get the result of the query
            if result: #check if the result is not empty
                #if the result is not empty return jsonify with error message and 409 status code
                return {'status': 'error', 'message': 'Email already exists.'}, 409
            query = sql.SQL("UPDATE users set email = %s WHERE accountid = %s") ##query to update the email in the database
            cur.execute(query, (email, accountid)) ##execute the query with the new email and account ID as parameters
            cur.execute("UPDATE users SET verifiedemail = FALSE WHERE accountid = %s", (accountid,)) #set the verified email to false in the database
            send_verification_email(email) #send confirmation email to the new email address. Function located in email_verification_routes.py
        conn.commit()

        return {'status': 'success', 'message': 'User information updated successfully'}, 200
        
    except psycopg2.Error as e:
        print("Database error:", e)
        return {'status': 'error', 'message': 'Database error'}, 500
    
    finally:
        if cur:
            cur.close()
        if conn:
            conn.close()



#Purpose: This function updates the user's password in the database.
# It hashes the new password and updates it in the database.
# It also checks if the new password is the same as the old password before updating.
def update_user_password(accountid, oldPassword, newPassword):
    try:
        conn = psycopg2.connect(**db_info)
        cur = conn.cursor()
        
        # Step 1: Get the hashed password
        cur.execute(sql.SQL("SELECT password FROM users WHERE accountid = %s"), (accountid,))
        result = cur.fetchone()
        
        if not result:
            return {'status': 'error', 'message': 'Account not found'}, 404
        
        stored_hash = result[0]
        
        # Step 2: Verify old password
        if not bcrypt.checkpw(oldPassword.encode('utf-8'), stored_hash.encode('utf-8')):
            return {'status': 'error', 'message': 'Incorrect old password'}, 401
        
        # Step 3: Check if new password is the same as old password
        if bcrypt.checkpw(newPassword.encode('utf-8'), stored_hash.encode('utf-8')):
            return {'status': 'error', 'message': 'New password cannot be the same as old password'}, 400
        
        # Step 4: Hash new password and update in database
        hashed_new_password = bcrypt.hashpw(newPassword.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        
        cur.execute(sql.SQL("UPDATE users SET password = %s WHERE accountid = %s"), (hashed_new_password, accountid))
        conn.commit()
        
        return {'status': 'success', 'message': 'Password updated successfully'}, 200
        
    except psycopg2.Error as e:
        print("Database error:", e)
        return {'status': 'error', 'message': 'Database error'}, 500
    
    finally:
        if cur:
            cur.close()
        if conn:
            conn.close()



#Purpose: This function deletes a user from the database based on their account ID.
# It deletes the user from the users table, the account from the account table, and their blogs from the blog table.
# It also checks if the account ID exists in the database before deleting.
# Deletion is done with SQL cascading in postgresql.
def delete_user(accountid,password):
    try:
        conn = psycopg2.connect(**db_info)
        cur = conn.cursor()
        
        if not accountid:
            return {'status': 'error', 'message': 'Account not found'}, 404
        
        # Delete user blogs
        cur.execute(sql.SQL("SELECT password FROM users WHERE accountid = %s"), (accountid,))
        resultPassword = cur.fetchone()
        if resultPassword:
            stored_hash = resultPassword[0]
            if bcrypt.checkpw(password.encode('utf-8'), stored_hash.encode('utf-8')): #check if the input password matches the stored password
                #if the password matches hash the new password and update it in the database
                deleteAccount =sql.SQL("DELETE FROM account WHERE accountid = %s") #query to delete the account from the database
                cur.execute(deleteAccount, (accountid,)) ##delete the account from the database
                conn.commit()
                return {'status': 'success', 'message': 'User deleted successfully'}, 200
            else:
                return {'status': 'error', 'message': 'Incorrect password'}, 401
        else:
            return {'status': 'error', 'message': 'Account not found'}, 404
    except psycopg2.Error as e:
        return {'status': 'error', 'message': 'Database error'}, 500
    
    finally:
        if cur:
            cur.close()
        if conn:
            conn.close()