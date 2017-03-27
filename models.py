
from datetime import datetime
import json
import os
import re

from pymongo import MongoClient

CLIENT = MongoClient('localhost', 27017)
DB = CLIENT["carpe"]
EMAIL_COLLECTION = DB["emails"]

# Characters we don't want in our message ids
DEL_CHARS = ''.join(c for c in map(chr, range(256)) if not c.isalnum())
DATE_FORMATS = ['%a %b %d %X %Y', '%a, %d %b %Y %X', '%d %b %Y %X']


def read_emails(fpath):
    with open(os.path.join(os.path.dirname(__file__), 'parsed_data/', fpath), 'r') as emails:
        return json.loads(emails.read())


def get_date_format(date_string):
    for time_format in DATE_FORMATS:
        try:
            return datetime.strptime(date_string, time_format)
        except:
            pass


def get_email_model(email_json):
    return {
        "message_id": email_json["id"],
        "text": email_json["text"],
        "subject": email_json["subject"],
        "date": get_date_format(re.split('\s\-|\s\+', email_json["date"])[0]),
        "author_email": email_json["author_email"],
        "author_name": email_json["author_name"],
        "replying_to": email_json["replying_to"]
    }


def add_emails():
    for email_chunk in os.listdir(os.path.join(os.path.dirname(__file__), 'parsed_data/')):
        emails = [get_email_model(email) for email in read_emails(email_chunk)]
        print EMAIL_COLLECTION.insert_many(emails).inserted_ids


def reset_db():
    EMAIL_COLLECTION.delete_many({})
    add_emails()

if __name__ == "__main__":
    reset_db()
