from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import pickle
import os.path


# If you modify these scopes, delete the file token.pickle.
# For more information about the SCOPES, see https://developers.google.com/gmail/api/auth/scopes

SCOPES = ['https://www.googleapis.com/auth/gmail.modify']

token_pickle_path = '../secrets/token.pickle'
credentials_path = '../secrets/credentials.json'


def get_credentials():
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.

    if os.path.exists('token.pickle'):
        with open(token_pickle_path, 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(credentials_path, SCOPES)
            creds = flow.run_local_server()

        # Save the credentials for the next run
        with open(token_pickle_path, 'wb') as token:
            pickle.dump(creds, token)
    return creds
