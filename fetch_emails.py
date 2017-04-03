import httplib2, os, base64

from apiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage
from pprint import PrettyPrinter

pp = PrettyPrinter()

try:
    import argparse
    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
    flags = None

# If modifying these scopes, delete your previously saved credentials
# at ~/.credentials/gmail-python-quickstart.json
SCOPES = 'https://www.googleapis.com/auth/gmail.readonly'
CLIENT_SECRET_FILE = 'client_secret.json'
APPLICATION_NAME = 'Gmail API Python Quickstart'


def get_credentials():
    """Gets valid user credentials from storage.

    If nothing has been stored, or if the stored credentials are invalid,
    the OAuth2 flow is completed to obtain the new credentials.

    Returns:
        Credentials, the obtained credential.
    """
    home_dir = os.path.expanduser('~')
    credential_dir = os.path.join(home_dir, '.credentials')
    if not os.path.exists(credential_dir):
        os.makedirs(credential_dir)
    credential_path = os.path.join(credential_dir,
                                   'gmail-python-quickstart.json')

    store = Storage(credential_path)
    credentials = store.get()
    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
        flow.user_agent = APPLICATION_NAME
        if flags:
            credentials = tools.run_flow(flow, store, flags)
        else: # Needed only for compatibility with Python 2.6
            credentials = tools.run(flow, store)
        print('Storing credentials to ' + credential_path)
    return credentials

def main():
    """Shows basic usage of the Gmail API.

    Creates a Gmail API service object and outputs a list of label names
    of the user's Gmail account.
    """
    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    service = discovery.build('gmail', 'v1', http=http)

    results = service.users().messages().list(userId='me').execute()
    # pp.pprint(results)
    for msg_id in results['messages']:
        message = service.users().messages().get(userId='me', id=msg_id['id']).execute()

        email_content = {}

        email_content["id"] = message.get('id', False)
        meta_dict = {meta["name"].lower(): meta["value"] for meta in message["payload"]["headers"] if meta["name"] in ["Subject", "Date", "From"]}
        email_content["subject"] = meta_dict.get("subject", False)
        email_content["date"] = meta_dict.get("date", False)

        # From format is 'John Doe <johny_appleseed@gmail.com>'
        name = re.findall(re.compile('[a-zA-Z]{1,} [a-zA-Z]{1,}'), meta_dict.get("from", ""))
        email = re.findall(re.compile('<.*>'), meta_dict.get("from", "")) 
        email_content["author_name"] = name[0] if name else False
        email_content["author_email"] = email[0].lstrip("<").rstrip(">") if email else False

        email_content["replying_to"] = False

        try:
            body = message['payload']['parts'][0]['parts'][0]['body']['data'].rstrip("=") + "=="
        except KeyError:
            if message['payload']['body']['size'] > 0:
                body = message['payload']['body']['data'].rstrip("=") + "=="
            else:
                body = ""

        try:
            email_content['text'] = base64.b64decode(body).decode(errors="ignore")      # Having unicode errors
        except TypeError:
            print "that's fine"

        month = re.findall(re.compile("[A-Z]{1}[a-z]{2} [0-9]{4}"), meta_dict.get("date", ''))
        month = month[0]
        try:
            emails[month].append(email_content)
        except KeyError:
            emails[month] = [email_content]

    if not emails:
        print("No new emails!")
    else:
        for date, lst_emails in emails.items():
            update_jsons(lst_emails, date)


if __name__ == '__main__':
    main()
