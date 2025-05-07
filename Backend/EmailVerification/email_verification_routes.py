#created: 04/01/2025 by jaden
#purpose: implementing email verification using python, flask, and sendgrid

import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from flask import render_template, url_for, Blueprint
from itsdangerous import URLSafeTimedSerializer
from dotenv import load_dotenv
from .email_verification_db_functions import *

app_bp = Blueprint('email_verification_routes', __name__)  #creating a blueprint for the email verification routes

dotenv_path = os.path.join(os.path.dirname(__file__), 'flask-app.env') #loading the environment variables from the .env file
load_dotenv(dotenv_path) 

app_secret_key = os.getenv("SECRET_KEY")#loading the secret key from the .env file


#settingup sendgrid
SENDGRID_API_KEY = os.getenv("SENDGRID_API_KEY") #Switch back to 'SENDGRID_API_KEY' when deploying, This is just for testing and not wasting emails on actualy sendgrid account. 
sg = SendGridAPIClient(SENDGRID_API_KEY) #creating a sendgrid client

#generate email verification token
def generate_token(email):
    serializer = URLSafeTimedSerializer(app_secret_key) #creating a serializer object
    return serializer.dumps(email, salt = 'email-confirmation') #creating a token for the email address

#send verification email from legacyiqdevteam@outlook.com
def send_verification_email(email):
    #print("function called")
    token = generate_token(email) #generating the token for the email address
    verification_url = url_for('email_verification_routes.verify_email', token = token, _external = True) #creating the verification url

    message = Mail( #creating the mail object
        from_email = 'legacyiqdevteam@outlook.com', 
        to_emails = email,
        subject = 'Please verify your email address',
        html_content = f'Click here to verify email address: {verification_url}'
    )

    try:
        response = sg.send(message) #sending the email
        if response.status_code == 202: #checking if the email was sent successfully
            print("Email sent successfully")#debugging code
        else:
            print("Failed to send email")#debugging code
        return f"A verification email was sent to {str(email)}, your action is needed."
    except Exception as e:
        return f"We encountered an error while sending your verification email: {str(e)}"

#sending verification email to the user
@app_bp.route('/send_verification_email/<email>') #route to send verification email
def send_verification(email): #sending verification email to the user
    return send_verification_email(email)

#confirming verification token
@app_bp.route('/verify_email/<token>') #route to verify email
def verify_email(token): 
    email = confirm_token(token) #confirming the token
    if email: #checking if the token is valid
        result = verify_email_in_db(email)
        if result['status'] == 'success':
            first_name = result['firstname']
            return render_template('verification_success.html', message=f"Congratulations {first_name}! Your email at: {email}, has been successfully verified!")
        else:
            return render_template('verification_error.html', message=f"Sorry {first_name} , your verification link is invalid or expired.")
    else:
        return render_template('verification_error.html', message="Sorry, your verification link is invalid or expired.")
 
def confirm_token(token, expiration = 3600): #confirming the token
    try:
        serializer = URLSafeTimedSerializer(app_secret_key) #creating a serializer object
        return serializer.loads(token, salt = 'email-confirmation', max_age = expiration) #loading the token
    except:
        return None

