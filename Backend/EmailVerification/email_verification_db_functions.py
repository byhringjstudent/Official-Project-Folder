import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from flask import Flask, render_template, url_for, Blueprint
from itsdangerous import URLSafeTimedSerializer
from dotenv import load_dotenv
from flask import jsonify
from flaskAppConfig import db_info
import psycopg2

#function to check if email is verified
def verify_email_in_db(email):
    try:
        conn = psycopg2.connect(**db_info)  # Connect to the database
        cur = conn.cursor()

        if email:
            # Update the email verification status
            cur.execute("UPDATE users SET verifiedemail = TRUE WHERE email = %s", (email,))
            conn.commit()

            # Fetch the user's first name
            cur.execute("SELECT firstname FROM users WHERE email = %s", (email,))
            user = cur.fetchone()

            if user:
                first_name = user[0]
                return {'status': 'success', 'firstname': first_name}
            else:
                return {'status': 'error', 'message': 'User not found'}

    except Exception as e:
        return {'status': 'error', 'message': str(e)}

    finally:
        # Ensure the cursor and connection are closed properly
        if cur:
            cur.close()
        if conn:
            conn.close()
            
            

            
        