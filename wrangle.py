"""
For digesting mailing list dump data
Aidan McLaughlin - Jan 21, 2017
"""

import re
import os
import json
DATA_DIR = os.path.join(os.path.dirname(__file__), 'data/')


def parse(fname):
    """
    Given a filename in the data folder, creates the following dictionary
    for each email:
        {
            "id":           id assigned by carpediem mail server,
            "text":         raw email text (includes newlines, etc.),
            "subject":      email subject,
            "date":         send date,
            "author_name":  sender name,
            "author_email": sender email,
            "replying_to":  if a reply, the ID of the email being replied to
        }
    """
    clean_messages = []

    with open(os.path.join(DATA_DIR, fname), 'r') as dump:
        text_dump = dump.read()

    # Break apart messages by From line
    raw_messages = re.compile("From\s\w+\.\w+\sat\s.*").split(text_dump)
    for raw_message in raw_messages:
        if not raw_message:
            continue
        data = {}
        m_id = re.search("Message-ID:\s\<(.*)@.*\>", raw_message)
        data["id"] = m_id.group(1) if m_id else False

        # Split between message and metadata
        message_chunks = re.compile("Message-ID:\s\<.*\>").split(raw_message)

        try:
            metadata, text = message_chunks[0], message_chunks[1]
        except Exception as e:
            print(e)
            continue

        author_info = re.search("From:\s(.*)\sat\s(.*)\s\((.*)\)", metadata)
        # From line is the following:
        # From: dredfern.olin at gmail.com (Derek Redfern)
        # First two matches are the username and email server
        data["author_email"] = author_info.group(1) + "@" + author_info.group(2) if author_info else False
        # Last match is for name in parenthesis
        data["author_name"] = author_info.group(3) if author_info else False

        # Subject
        subject = re.search("Subject:\s(.*(\n)*.*)", metadata)
        subject = subject.group(1) if subject else False
        data["subject"] = re.compile("In-Reply-To:|References:").split(subject)[0].replace("\n\t", " ").strip()

        # Date
        date = re.search("Date:\s(.*)", metadata)
        data["date"] = date.group(1) if date else False

        # Get ID of message being replied to if applicable
        replying_to = re.search("In-Reply-To:\s\<(.*)@.*\>", metadata)
        data["replying_to"] = replying_to.group(1) if replying_to else False

        # Email text
        email_body = re.compile("On\s\w+,\s\w+\s\w+,\s\w+\sat\s\w+:\w+\s[A|P]M\s.*\<.*\>").split(text)[0]
        email_body = re.compile("\-+\snext\spart\s\-+").split(email_body)[0]
        data["text"] = email_body

        clean_messages.append(data)
    return clean_messages


if __name__ == "__main__":

    for email_dump in os.listdir(DATA_DIR):
        emails = []
        emails += parse(email_dump)

        with open("parsed_data/" + email_dump.split('.')[0] + ".json", "w") as clean:
            json.dump(emails, clean)
