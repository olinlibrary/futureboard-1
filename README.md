# FUTUREBOARD ![build](https://travis-ci.org/aidankmcl/carpe-learning.svg?branch=master)
A simple, interactive way to surface a community’s culture.
[Play with it here](http://futureboard.herokuapp.com/)

![A snapshot of the future](https://github.com/aidankmcl/futureboard/blob/master/screenshots/futureboard.png)
<Add a bunch of cool pictures here>

### Table of Contents
* [Contributing](#contributing)
  * [Setup](#setup)
  * [Edit](#edit)
  * [Build](#build)
  * [Commit](#commit)
* [Operating](#operating)
* [Directory Structure](#directory-structure)
  * [Scraping](#scraping)
  * [Server](#server)
  * [Styling](#styling)


## Contributing
### Setup

To install, start with `pip install -r requirements.txt` (virtual environment recommended).
In order to see any data, you'll need an Olin email and a subscription to the CarpeDiem mailing list. Once you've signed up, follow the instructions in the `scrape.js` file:
```
To use, install casperjs (npm install -g casperjs) and run:
casperjs scrape.js <arg1> <arg2>
where arg1 is your email for carpe and arg2 is your password for carpe.

If you don't think you have a password for carpe, you do but it's randomly
generated. You'll need to visit the carpediem list at lists.olin.edu to
get it reset.
```

After that, run `python wrangle.py` which will do a rough parse of all the scraped data and make it accessible to the web app. Finally, run `models.py` to add the parsed emails to the remote database your app will use. Note that `models.py` resets the database; see the [operators section](#operating) for information on database setup.

### Edit
Directory map
Style guide
To-Do list

### Build

### Commit

## Operating
This project was developed on [Heroku](https://heroku.com) using a Mongo database hosted by [mLab](https://mlab.com/). The texting interface was implemented using [Twilio](https://www.twilio.com/), so if you'd like to run your own version of the site, you'll need to make an account with each of these services (except mLab if you create a mongo instance through Heroku). As a heads up, Twilio costs $1 per phone number and $0.0075 per SMS sent or received, for MMS it's $0.01 to receive and $0.02 to send.

<How to deploy to the cloud. What resources to provision and how to configure them. Does this app depends on third-party services? How are these configured and how is the app configured to point to them?>

<Runbook. How to perform different administrative tasks. What kinds of maintenance have you needed to do? What are some failure modes, and where to look / what to change when these occur?>


## Directory Structure

### Scraping
[`scrape.js`](../master/scrape.js) uses casperjs to scrape email data from the CarpeDiem archives and throw them into text files in the `/data` directory, which is ignored by git.

[`wrangle.py`](../master/wrangle.py) pulls the data from the `/data` directory, parses out critical information, and throws those into a JSON which is then stored in `/parsed_data`, which is ignored by git.

[`fetch_emails.py`](../master/fetch_emails.py) attempts to pull new emails from the CarpeBot gmail account. Currently does not work very well; it will use the gmail account that is currently logged in on the computer. Alternatives should be explored in the future.

### Server
All server files are stored in the [`/app`](../master/app) directory.

[`server.py`](../master/app/server.py) runs a [Flask](http://flask.pocoo.org/docs/0.12/) server. If built directly from the command line, it will default to running on `localhost:5000`; if run within a Heroku app, it will use the settings of that app. It requires the `MONGODB_URI ` environment variable to be set as described in the [operators](#operating) section.

[`models.py`](../master/app/models.py) is responsible for taking the email JSONs in the `/parsed_data` directory and pushing them to a remote database. This module also requires the `MONGODB_URI` environment variable to be set.

[`factory.py`](../master/app/factory.py) sets basic configurations for the Flask app.

### Styling

