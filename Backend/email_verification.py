#created: 04/01/2025 by jaden
#purpose: implementing email verification using python, flask, and sendgrid

import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
from flask import Flask, render_template, request, redirect, url_for
from itsdangerous import URLSafeTimedSerializer

#randomly generated flask key
app = Flask (__name__)
rand_priv_key = os.urandom(24)
app.config['SECRET_KEY'] = rand_priv_key

#settingup sendgrid
SENDGRID_API_KEY = os.getenv("SENDGRID_API_KEY")
sg = SendGridAPIClient(SENDGRID_API_KEY)

#generate email verification token
def generate_token(email):
    serializer = URLSafeTimedSerializer(app.config['SECRET_KEY'])
    return serializer.dumps(email, salt = 'email-confirmation')

#send verification email from legacyiqdevteam@outlook.com
def send_verification_email(email):
    token = generate_token(email)
    verification_url = url_for('verify_email', token = token, _external = True)

    message = Mail(
        from_email = 'legacyiqdevteam@outlook.com',
        to_emails = email,
        subject = 'Please verify your email address',
        html_content = f'Click here to verify email address: {verification_url}'
    )

    try:
        response = sg.send(message)
        return f"A verification email was sent to {email}, your action is needed."
    except Exception as e:
        return f"We encountered an error while sending your verification email: {str(e)}"

@app.route('/send_verification_email/<email>')
def send_verification(email):
    return send_verification_email(email)

#confirming verification token
@app.route('/verify_email/<token>')
def verify_email(token):
    email = confirm_token(token)
    if email:
        return "Your email address has been successfully verified!"
    else:
        return "Sorry, your verification link is invalid or expired."

def confirm_token(token, expiration = 3600):
    try:
        serializer = URLSafeTimedSerializer(app.config['SECRET_KEY'])
        return serializer.loads(token, salt = 'email-confirmation', max_age = expiration)
    except:
        return None

if __name__ == '__main__':
#running flask in debug mode, turn debug off when we deploy
    app.run(debug = True)

"""
Example of what it might look like to trigger the email verification in the front end (react.js and javaScript)

const sendVirificationEmail = async (email) => {
    const response = await fetch('send_verification_email/${email}');
    const result = await response.text();
    alert(result);
};
"""