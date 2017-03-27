from googleapiclient.discovery import build
from config import CLIENT_ID, CLIENT_SECRET
from oauth2client import tools
from oauth2client.file import Storage
from oauth2client.client import AccessTokenRefreshError
from oauth2client.client import OAuth2WebServerFlow
import httplib2

scope = 'https://www.googleapis.com/auth/gmail.readonly'
redirect_uri = 'urn:ietf:wg:oauth:2.0:oob'
flow = OAuth2WebServerFlow(CLIENT_ID, CLIENT_SECRET, scope)

storage = Storage('credentials.dat')
credentials = storage.get()

if credentials is None or credentials.invalid:
	credentials = tools.run_flow(flow, storage, tools.argparser.parse_args())
