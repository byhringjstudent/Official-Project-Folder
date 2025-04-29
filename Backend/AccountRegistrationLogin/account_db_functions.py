import psycopg2
from psycopg2 import sql
from utils import create_unique_id
from flaskAppConfig import db_info
from flask import request, jsonify, session, Blueprint, redirect, url_for, flash, make_response
import bcrypt
from flask import Flask, render_template, request, redirect, url_for, session, flash


#Purpose: This function creates a new user in the database. It takes the user's email, hashed password, first name, and last name as input.
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

#function to check if the user exists in the database and verify the password:  
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

#function to get the user information from the database
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