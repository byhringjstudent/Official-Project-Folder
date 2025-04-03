import os
from dotenv import load_dotenv
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

dotenv_path = os.path.join(os.path.dirname(__file__), 'sendgrid.env')
load_dotenv(dotenv_path)
#print(os.getenv('SENDGRID_API_KEY'))

message = Mail(
    from_email='Legacyiqdevteam@outlook.com',
    to_emails='', #get email from account details
    subject='Sending with Twilio SendGrid is Fun',
    html_content='<strong>and easy to do anywhere, even with Python</strong>')
try:
    sg = SendGridAPIClient(os.environ.get('SENDGRID_API_KEY'))
    response = sg.send(message)
    print(response.status_code)
    print(response.body)
    print(response.headers)
except Exception as e:
    print(str(e))