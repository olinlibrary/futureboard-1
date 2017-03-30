"""
A Flask server that presents a minimal browsable interface for the Olin course catalog.

author: Oliver Steele <oliver.steele@olin.edu>
date  : 2017-01-18
license: MIT
"""

import os
import json
import re
from datetime import datetime
from bson import json_util

from flask import Flask, redirect, render_template, request, url_for
from jinja2 import evalcontextfilter, Markup, escape
from pymongo import MongoClient

from factory import create_app
from models import get_date_format

_paragraph_re = re.compile(r'(?:\r\n|\r|\n){2,}')

CLIENT = MongoClient('localhost', 27017)
DB = CLIENT["carpe"]
EMAIL_COLLECTION = DB["emails"]


def gmail_to_mongo(email_data):
    """
    This will be updated to actually parse data
    coming from Google once we have GMail API set up.
    """
    data = {
        "message_id": email_data["id"],
        "text": email_data["text"],
        "subject": email_data["subject"],
        "date": get_date_format(re.split('\s\-|\s\+', email_data["date"])[0]),
        "author_email": email_data["author_email"],
        "author_name": email_data["author_name"],
        "replying_to": email_data["replying_to"]
    }
    EMAIL_COLLECTION.insert_one(data)


app = create_app()


@app.route('/health')
def health():
    return 'ok'


@app.template_filter()
@evalcontextfilter
def nl2br(eval_ctx, value):
    result = u'\n\n'.join(u'<p>%s</p>' % p.replace('\n', Markup('<br>\n')) for p in _paragraph_re.split(escape(value)))
    if eval_ctx.autoescape:
        result = Markup(result)
    return result


@app.route('/')
def home_page():
    dates = sorted(set(map(lambda fname: re.findall('\d+', fname)[0], os.listdir('parsed_data'))))
    return render_template('list.html', dates=dates)


@app.route('/email/<id>')
def single_email_view(id):
    email = EMAIL_COLLECTION.find_one({"message_id": id})
    return render_template('single.html', email=email)


@app.route('/emails', methods=["POST"])
def filter_emails():
    dates = request.form.get("date_range", "01/01/2005 - 01/31/2005").split(" - ")  # sets default to Jan 2005
    start_date, end_date = datetime.strptime(dates[0], '%m/%d/%Y'), datetime.strptime(dates[1], '%m/%d/%Y')
    emails = EMAIL_COLLECTION.find({"date": {"$gt": start_date, "$lt": end_date}})
    return json.dumps([email for email in emails], default=json_util.default)


@app.route('/random-email')
def random_email():
    most_recent_email = EMAIL_COLLECTION.aggregate([{
        "$group": {"_id": "date", "date": {"$max": "$date"}}
    }]).next()
    earliest_email = EMAIL_COLLECTION.aggregate([{
        "$group": {"_id": "date", "date": {"$min": "$date"}}
    }]).next()
    random_email = EMAIL_COLLECTION.aggregate([{"$sample": {"size": 1}}]).next()
    data = {
        "email": random_email,
        "max_date": most_recent_email["date"],
        "min_date": earliest_email["date"]
    }
    print data["max_date"], data["min_date"]
    return json.dumps(data, default=json_util.default)


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    host = "127.0.0.1" if port == 5000 else "0.0.0.0"
    app.run(host=host, debug=True, port=port)
