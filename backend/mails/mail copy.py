import base64
from email.mime.text import MIMEText
import os
import pickle
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request

SCOPES = ['https://mail.google.com/']
our_email = 'your_gmail@gmail.com'


def create_message(sender, to, subject, message_text):
  """Create a message for an email.

  Args:
    sender: Email address of the sender.
    to: Email address of the receiver.
    subject: The subject of the email message.
    message_text: The text of the email message.

  Returns:
    An object containing a base64url encoded email object.
  """
  message = MIMEText(message_text)
  message['to'] = to
  message['from'] = sender
  message['subject'] = subject
  return {'raw': base64.urlsafe_b64encode(message.as_string())}


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
    print('Message Id: %s' % message['id'])
    return message
  except Exception as error:
    print('An error occurred: %s' % error)


def gmail_authenticate():
    creds = None
    # the file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first time
    if os.path.exists("token.pickle"):
        with open("token.pickle", "rb") as token:
            creds = pickle.load(token)
    # if there are no (valid) credentials availablle, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # save the credentials for the next run
        with open("token.pickle", "wb") as token:
            pickle.dump(creds, token)
    return build('gmail', 'v1', credentials=creds)


def search_messages(service, query):
    result = service.users().messages().list(userId='me',q=query).execute()
    messages = [ ]
    if 'messages' in result:
        messages.extend(result['messages'])
    while 'nextPageToken' in result:
        page_token = result['nextPageToken']
        result = service.users().messages().list(userId='me',q=query, pageToken=page_token).execute()
        if 'messages' in result:
            messages.extend(result['messages'])
    res = set([])
    res.update([i['id'] for i in messages])
    return list(res)

def Sync_mail(service, historyId=None):
  result = None
  res = set([])
  if historyId == None:
    result = service.users().messages().list(maxResults=200,userId='me').execute()
    res.update([msg['id'] for msg in result['messages']])
  else:
    result = service.users().history().list(userId='me',startHistoryId=historyId).execute()
    res.update([msg['id'] for hist in result['history'] for msg in hist['messages']])
  return list(res)


def get_mails(service,ids):
  mails = []
  try:
    for id in ids:
      mail = {}
      txt = service.users().messages().get(userId='me', id=id,format='FULL').execute()
      payload = txt['payload']
      headers = payload['headers']
      # Look for Subject and Sender Email in the headers
      for d in headers:
        if d['name'] == 'Subject':
          mail['subject'] = d['value']
        if d['name'] == 'From':
          mail['sender_mail'] = d['value']
      mail['hidtoryid'] = txt['historyId']
      mail['internalDate'] = txt['internalDate']
      mail['mail_id'] = txt['id']
      mail['thread_id'] = txt['threadId']
      mails.append(mail)
    return mails
  except Exception as error:
    return mails

      





    