from __future__ import print_function
import pickle
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient import errors
from email.mime.text import MIMEText
import base64
import configparser


SCOPES = ['https://www.googleapis.com/auth/gmail.send']

screds = None
# The file token.pickle stores the user's access and refresh tokens, and is
# created automatically when the authorization flow completes for the first
# time.
if os.path.exists('token.pickle'):
    with open('token.pickle', 'rb') as token:
        creds = pickle.load(token)
# If there are no (valid) credentials available, let the user log in.
if not creds or not creds.valid:
    if creds and creds.expired and creds.refresh_token:
        creds.refresh(Request())
    else:
        flow = InstalledAppFlow.from_client_secrets_file(
            'credentials.json', SCOPES)
        creds = flow.run_local_server(port=0)
    # Save the credentials for the next run
    with open('token.pickle', 'wb') as token:
        pickle.dump(creds, token)
service = build('gmail', 'v1', credentials=creds)

config = configparser.ConfigParser()

config.read("hids.ini")

#email = config.get("Email","email")

def create_message(to):
    """Create a message for an email.
      Args:
          sender: Email address of the sender.
          to: Email address of the receiver.
          subject: The subject of the email message.
          message_text: The text of the email message.
      Returns:
          An object containing a base64url encoded email object.
    """
    msg = MIMEText("It's a test")
    msg['From'] = 'ssii.gr2@gmail.com'
    msg['To'] = to
    msg['Subject'] = 'Report diary'
    return {'raw': base64.urlsafe_b64encode(msg.as_bytes()).decode()}


def send_message(service, user_id, message):
    """Send an email message.
      Args:
          service: Authorized Gmail API service instance.
          user_id: User's email address. The special value "me"
          can be used to indicate the authenticated user.
          message: Message to be sent.
      Returns:
          Sent Message.
    """
    try:
        message = (service.users().messages().send(userId=user_id, body=message).execute())
    except:
        print('An error occurred error')

raw_text = create_message('example@gmail.com')
send_message(service, 'me', raw_text)