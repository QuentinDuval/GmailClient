from __future__ import print_function

from gclient.authentication import *
from googleapiclient.discovery import build
from typing import List


class Classification:
    def __init__(self):
        self.creds = get_credentials()
        self.service = build('gmail', 'v1', credentials=self.creds)

    def get_all_labels(self) -> List[str]:
        """
        Returns all the labels used to classify mails
        """
        results = self.service.users().labels().list(userId='me').execute()
        return list(results.get('labels', []))

    def list_unread_messages(self, batch_size=500):
        """
        Query GMAIL API to get the list of messages matching the "is unread" criteria
        """
        answer = self.service.users().messages().list(userId='me', q='is:unread', maxResults=batch_size).execute()
        while answer['messages']:
            yield answer
            if 'nextPageToken' not in answer:
                break

            next_page_token = answer['nextPageToken']
            answer = self.service.users().messages().list(userId='me', pageToken=next_page_token).execute()

    def mark_as_read(self, message_ids: List[str]):
        """
        Ask the GMAIL API to mark as "read" all the messages given as parameters
        """
        return self.service.users().messages().batchModify(userId='me', body={
            "removeLabelIds": ["UNREAD"],
            "ids": message_ids,
            "addLabelIds": []
        }).execute()

    def mark_all_as_read(self):
        for answer in self.list_unread_messages():
            message_ids = [message['id'] for message in answer['messages']]
            print("Marked", message_ids)
            self.mark_as_read(message_ids)


if __name__ == '__main__':
    classifier = Classification()
    print(classifier.get_all_labels())
    print(classifier.mark_all_as_read())
