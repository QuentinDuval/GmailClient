from __future__ import print_function

from gclient.authentication import *
from googleapiclient.discovery import build


def get_all_labels():
    """
    Returns all the labels used to classify mails
    """
    creds = get_credentials()
    service = build('gmail', 'v1', credentials=creds)
    results = service.users().labels().list(userId='me').execute()
    return list(results.get('labels', []))


if __name__ == '__main__':
    print(get_all_labels())
