#created: 04/01/2025 by jaden
#purpose: implementing email verification using python, flask, and sendgrid

import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from flask import Flask, render_template, request, redirect, url_for, Blueprint
from itsdangerous import URLSafeTimedSerializer
from dotenv import load_dotenv
from flask import jsonify
from flaskAppConfig import db_info
import psycopg2

app_bp = Blueprint('email_verification_routes', __name__)

dotenv_path = os.path.join(os.path.dirname(__file__), 'flask-app.env')
load_dotenv(dotenv_path)

app_secret_key = os.getenv("SECRET_KEY")


#settingup sendgrid
SENDGRID_API_KEY = os.getenv("SENDGRID_API_KEY") #Switch back to SENDGRID_API_KEY when deploying, This is just for testing and not wasting emails on actualy sendgrid account. 
sg = SendGridAPIClient(SENDGRID_API_KEY)

#generate email verification token
def generate_token(email):
    serializer = URLSafeTimedSerializer(app_secret_key)
    return serializer.dumps(email, salt = 'email-confirmation')

#send verification email from legacyiqdevteam@outlook.com
def send_verification_email(email):
    print("function called")
    token = generate_token(email)
    verification_url = url_for('email_verification_routes.verify_email', token = token, _external = True)

    message = Mail(
        from_email = 'legacyiqdevteam@outlook.com', 
        to_emails = email,
        subject = 'Please verify your email address',
        html_content = f'Click here to verify email address: {verification_url}'
    )

    try:
        response = sg.send(message)
        return f"A verification email was sent to {str(email)}, your action is needed."
    except Exception as e:
        return f"We encountered an error while sending your verification email: {str(e)}"

@app_bp.route('/send_verification_email/<email>')
def send_verification(email):
    return send_verification_email(email)

#confirming verification token
@app_bp.route('/verify_email/<token>')
def verify_email(token):
    email = confirm_token(token)
    if email:
        conn = psycopg2.connect(**db_info)
        cur = conn.cursor()
        cur.execute("UPDATE users SET verifiedemail = TRUE WHERE email = %s", (email,))
        conn.commit()
        cur.close()
        conn.close()
        return jsonify({"message": "Your email address has been successfully verified!"})
    else:
        return jsonify({"error":"Sorry, your verification link is invalid or expired."})

def confirm_token(token, expiration = 3600):
    try:
        serializer = URLSafeTimedSerializer(app_secret_key)
        return serializer.loads(token, salt = 'email-confirmation', max_age = expiration)
    except:
        return None


"""
Example of what it might look like to trigger the email verification in the front end (react.js and javaScript)

const sendVirificationEmail = async (email) => {
    const response = await fetch('send_verification_email/${email}');
    const result = await response.text();
    alert(result);
};
"""