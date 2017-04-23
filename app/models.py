
from datetime import datetime
import json
import os
import re

from pymongo import MongoClient

CLIENT = MongoClient(os.environ.get('MONGODB_URI', ''))
EMAIL_COLLECTION = CLIENT['futureboard']['emails']
EVENT_COLLECTION = CLIENT['futureboard']['events']

# Characters we don't want in our message ids
DEL_CHARS = ''.join(c for c in map(chr, range(256)) if not c.isalnum())
DATE_FORMATS = ['%a %b %d %X %Y', '%a, %d %b %Y %X', '%d %b %Y %X']


def read_emails(fpath):
    """Fetches a particular month from parsed_data and returns it as a JSON
    """
    with open(os.path.join(os.path.dirname(__file__), '..', 'parsed_data/', fpath), 'r') as emails:
        return json.loads(emails.read())


def get_date_format(date_string):
    for time_format in DATE_FORMATS:
        try:
            return datetime.strptime(date_string, time_format)
        except:
            pass


def get_email_model(email_json):
    """Converts a JSON representation of an email message to a dictionary representation
    """
    return {
        "message_id": email_json["id"],
        "text": email_json["text"],
        "subject": email_json["subject"],
        "date": get_date_format(re.split('\s\-|\s\+', email_json["date"])[0]),
        "author_email": email_json["author_email"],
        "author_name": email_json["author_name"],
        "replying_to": email_json["replying_to"]
    }

def identify_events(data, src_id, date, collection):
    """Finds dates in the subjects of emails or texts, and creates events from those dates. Data is a string, src_id is the 
    unique id associated with the email or text in its respective collection, and date is the datetime the email or text was sent,
    and collection is the collection the email or text goes into 
    """
    event_date = cal.parseDT(data, date)
    if event_date[1]:
        if not EVENT_COLLECTION.find({"src_id": src_id}):
            EVENT_COLLECTION.insert({'data': data, 'date': event_date, 'collection': collection, 'src_id': src_id})

def add_emails(date=None):
    """Adds emails from parsed_data directory to the database. If no date is specified, it will add every month."""
    if date:
        emails = [get_email_model(email) for email in read_emails(os.path.join(os.path.dirname(__file__), '..', 'parsed_data/'+date+".json"))]
        print(EMAIL_COLLECTION.insert_many(emails).inserted_ids)
    else:
        for email_chunk in os.listdir(os.path.join(os.path.dirname(__file__), '..', 'parsed_data/')):
            print(email_chunk)
            emails = [get_email_model(email) for email in read_emails(email_chunk)]
            EMAIL_COLLECTION.insert_many(emails).inserted_ids

# def parse_events(data=None):
#     """Finds dates in the subjects of emails or texts, and creates events from those dates. Data is a list of id's; if not
#     specified, parses all emails in EMAIL_COLLECTION and TEXT_COLLECTION
#     """
#     if data:
#         # Find id's in database, update in database
#         emails = EMAIL_COLLECTION.find({"_id": {"$in": data}})
#         texts = TEXT_COLLECTION.find({"_id": {"$in": data}})
#     else:
#         emails = EMAIL_COLLECTION.find()
#         texts = TEXT_COLLECTION.find()
    
#     for email in emails:
#         # If the subject is not in EVENTS, strip out an event and add that and the subject to EVENTS
#         if not EVENT_COLLECTION.find({"src_id": emai['_id']}):
#             EVENT_COLLECTION.insert({"subject": email['subject'], "body": email['text'], "type": 'email', "src_id": email["_id"]})
#     for text in texts:
#         # If the text is not in TEXTS, strip out an event and add that and the text to EVENTS
#         if not EVENT_COLLECTION.find({"src_id": text['_id']}):
#             EVENT_COLLECTION.insert({"body": text['body'], "type": 'text', "src_id": text["_id"]})



def reset_db():
    """
    Resets the database and adds all the JSONs stored in the parsed_data directory
    """
    EMAIL_COLLECTION.delete_many({})
    add_emails()

if __name__ == "__main__":
    reset_db()
