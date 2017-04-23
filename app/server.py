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

from bs4 import BeautifulSoup
from flask import Flask, redirect, render_template, request, url_for
from jinja2 import evalcontextfilter, Markup, escape
import requests as r
from pymongo import MongoClient
import parsedatetime as pdt
from pprint import PrettyPrinter
from flask_socketio import SocketIO, emit

from app.factory import create_app
from app.models import get_date_format

pp = PrettyPrinter()

_paragraph_re = re.compile(r'(?:\r\n|\r|\n){2,}')

cal = pdt.Calendar()

MONGO_URI = os.environ.get('MONGODB_URI')
if not MONGO_URI:
    print("MONGODB_URI environment variable not set")
CLIENT = MongoClient(MONGO_URI)
EMAIL_COLLECTION = CLIENT.futureboard.emails
TEXT_COLLECTION = CLIENT.futureboard.texts

GOOGLE_BASE = "https://www.google.com/search?tbm=isch&q=%s"


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
    return data


app = create_app()
socketio = SocketIO(app)
COUNT = 0


@socketio.on('connect', namespace='/text')
def handle_new_connection():
    global COUNT
    COUNT += 1
    emit('connection', {'data': 'Connected', 'count': COUNT})


@socketio.on('disconnect', namespace='/text')
def handle_dropped_connection():
    global COUNT
    COUNT -= 1
    emit('connection', {'data': 'Disconnected', 'count': COUNT})


@socketio.on('my_event', namespace='/text')
def handle_my_custom_event(json):
    emit('response', json)


@app.route('/health')
def health():
    socketio.emit('response',
                  {'data': 'Server is healthy!'},
                  namespace='/text')
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
    # dates = sorted(set(map(lambda fname: re.findall('\d+', fname)[0], os.listdir('parsed_data'))))
    # emails = EMAIL_COLLECTION.find().limit(10)
    return render_template('board.html')


@app.route('/texts')
def get_texts():
    start_date = cal.parseDT(request.args.get('start'))[0]
    end_date = cal.parseDT(request.args.get('end'))[0]
    texts = TEXT_COLLECTION.find({"date": {"$gte": start_date, "$lte": end_date}})
    return json.dumps(list(texts), default=json_util.default)


@app.route('/twilio', methods=["GET", "POST"])
def twilio_text():
    print "\n\n", request.form.get('MediaUrl')
    TEXT_COLLECTION.insert({
        'from': request.form.get('From', ''),
        'data': request.form.get('Body', ''),
        'date': datetime.now()})
    socketio.emit('response',
                  {'data': request.form.get('Body', request.form.values())},
                  namespace='/text')
    return json.dumps(request.form.get('Body'))


@app.route('/test-twilio', methods=["GET", "POST"])
def test_twilio_text():
    TEXT_COLLECTION.insert({
        'from': request.form.get('From'),
        'data': request.form.get('Body'),
        'date': datetime.now()})
    socketio.emit('response',
                  {'data': request.form.get('Body', request.form.values())},
                  namespace='/text')
    return json.dumps(request.form.get('Body'))


@app.route('/images/<search_term>')
def query_google(search_term):
    html_doc = r.get(GOOGLE_BASE % "cats").content
    soup = BeautifulSoup(html_doc, 'html.parser')
    res = soup.find(id="res").find_all('img')[0].attrs.get('src')
    return json.dumps(res)


@app.route('/email/<id>')
def single_email_view(id):
    email = EMAIL_COLLECTION.find_one({"message_id": id})
    return render_template('single.html', email=email)


@app.route('/emails', methods=["POST"])
def filter_emails():
    dates = request.form.get("date_range", "01/01/2005 - 01/31/2005").split(" - ")  # sets default to Jan 2005
    start_date, end_date = datetime.strptime(dates[0], '%m/%d/%Y'), datetime.strptime(dates[1], '%m/%d/%Y')
    emails = EMAIL_COLLECTION.find({"date": {"$gt": start_date, "$lt": end_date}})
    print(type(emails))
    dates = [(email, cal.parseDT(email["subject"], email["date"])) for email in emails]
    pp.pprint([(email[0]['subject'], email[1][0]) for email in dates])
    return json.dumps([email[0] for email in dates], default=json_util.default)


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    host = "127.0.0.1" if port == 5000 else "0.0.0.0"
    # app.run(host=host, debug=True, port=port)
    print("Starting app!")
    socketio.run(app, host=host, port=port)
