# FUTUREBOARD ![build](https://travis-ci.org/aidankmcl/carpe-learning.svg?branch=master)
A simple, interactive way to surface a community’s culture. We want to make it easy for people to share ideas and events with each other.
[Play with it here](http://futureboard.herokuapp.com/)

![A snapshot of the future](https://github.com/aidankmcl/futureboard/blob/master/screenshots/futureboard.png)
<Add a bunch of cool pictures here>

### Table of Contents
* [Current Status](#status)
  * [License](#license)
  * [Future Work](#future-work)
  * [Credits](#credits)
* [Make Your Own](#make-your-own)
  * [Setup](#setup)
  * [Development](#development)
* [Contributing](#contributing)
  * [Edit](#edit)
  * [Commit](#commit)
* [Operating](#operating)
* [Directory Structure](#directory-structure)
  * [Scraping](#scraping)
  * [Server](#server)
  * [Styling](#styling)

## Status
Probably the best way to explain would be to go to [the site](https://futureboard.herokuapp.com) and text the number in the top left of the screen. You'll be sent some information about using the service - as of May 1, 2017 it said the following:

>WELCOME TO FUTUREBOARD
>
>Thanks for the text! To use FUTUREBOARD, write me words or feed me a link (I'll read anything from Youtube, Vimeo or URLs that end in .jpg, .png, and of course .gif).
>
>Got some feedback? Email aidan.mclaughlin@students.olin.edu :)

As mentioned, we currently handle some video links and common image formats.

### License
This project is licensed under the MIT License, a ["short and simple permissive license with conditions only requiring preservation of copyright and license notices."](https://github.com/aidankmcl/futureboard/blob/master/LICENSE)

### Future Work
Our biggest interests right now revolve around input streams and the ability to build up content threads over time. The board does not support any native content from mobile (such as sending images or videos in MMS). It'd also be nice to include links to articles, however `iframe`s can be tricky when it comes to cross-origin content. One way around this could be scraping articles for their title and text to display here.

As for threads, we want to explore an interface for adding information to items on the board for others to access later on. This could involve uploading links, images and videos all related to a certain event or theme.

### Credits
Thank you to Emily, Jeff and Oliver from the library along with the HtL students for all of their input over the course of this project. This project was started by Sean and Aidan but we hope to see it built upon by others in the near future :)

## Make Your Own
### Setup
To install your own version of FUTUREBOARD: fork this repo, clone it so you have local access, enter the directory (`cd futureboard`) and then run `pip install -r requirements.txt` ([virtual environment](http://python-guide-pt-br.readthedocs.io/en/latest/dev/virtualenvs/) recommended). This project was deployed with [Heroku](https://heroku.com) using a Mongo database hosted by [mLab](https://mlab.com/). The texting interface was implemented using [Twilio](https://www.twilio.com/), so if you'd like to run your own version of the site, you'll need to make an account with each of these services (except mLab if you create a mongo instance through Heroku). As a heads up, Twilio costs $1 per phone number and $0.0075 per SMS sent or received, for MMS it's $0.01 to receive and $0.02 to send.

Once you have accounts with these services, you'll need a phone number that can handle SMS (and one day MMS!) from Twilio and a free mLab instance (sandbox). Our app is set to access these services using keys stored as environment variables. You'll need to run the following code with each variable replaced with your real key.

```
export MONGODB_URI="<Get this from mLab instance>";
export TWILIO_ACCOUNT_SID="<Get this from Twilio dashboard>";
export TWILIO_AUTH_TOKEN="<Get this from Twilio dashboard>";
```

NOTE: You'll need to [add these as environment variables to your Heroku instance](https://devcenter.heroku.com/articles/heroku-local#set-up-your-local-environment-variables) as well. Depending on your setup, you may want to have a separate database for local vs. production, but for just getting the app running it's not a crime to use the same.

Now that you've got these variables set, you need to get the [Heroku toolbelt](https://devcenter.heroku.com/articles/getting-started-with-python#set-up) set up. Once logged in through the command line interface, run `heroku git:remote -a <YOUR PROJECT NAME>`. Now when you've committed changes to Github, you can [push to Heroku](https://devcenter.heroku.com/articles/getting-started-with-python#push-local-changes) by running `git push heroku master`. If everything was done correctly, your app should deploy and you can access it at `<YOUR PROJECT NAME>.herokuapp.com`.

### Development
A tricky part about working with Twilio is that you need a publicly accessible URL for them to send texts to, so you need to have some form of staging server or tunneling software like Ngrok ([tutorial for using Ngrok with Twilio](https://www.twilio.com/blog/2013/10/test-your-webhooks-locally-with-ngrok.html)). The latter is recommended as it makes development more natural (test changes without new deployment) but is less permanent than a staging server managed by Heroku. A combination is ideal but extra work, that's all up to you!

As far as database administration, a pro of using mLab is having an interface for sifting through db records and doing general management rather than through the command line.

## Contributing
Setup is very similar to the standalone [setup shown above](#setup) however you can just clone the repository directly. The added complication however is that you'll need to be added to the various services by somebody who's worked on this project before. If you have any questions, feel free to reach out to [aidan.mclaughlin@students.olin.edu](mailto:aidan.mclaughlin@students.olin.edu). You would then use the variables of the main project for connecting to staging database and server. We have a pipeline set up in Heroku that allows us to work on staging until we feel good about it and then easily push those changes to the main server.

### Edit
[Directory Structure](#directory-structure) provides a roadmap to the modules and their functions. Once you are familiar with the layout, check out the [to-do list](#to-do), and then do some coding!

### Commit
Submit a pull request detailing what you did and why. Once the code has been reviewed, the problem will be removed from the to-do list, and your feature will be merged into master and pushed to production.

### To-Do
- Implement change log
- Spread the gospel of FUTUREBOARD
- Remove obsolete files and directories


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
Html templates are stored in [`/app/templates`](../master/app/templates), and [`/app/static`](../master/app/static) contains the CSS, fonts, and JavaScript required to render the board.

[`layout.html`](../master/app/templates/layout.html) contains styling for the whole site.

[`board.html`](../master/app/templates/board.html) extends `layout.html` and runs the custom scripts required to use the main board.

Other templates are no longer used and should be removed in future boards.

## Change Log
To be implemented

## Email Data
This project includes utilities for acquiring Olin mailing list data. If you'd like to access CarpeDiem emails, you'll need an Olin email and a subscription to the list. Once you've signed up, follow the instructions in the `scrape.js` file:
```
To use, install casperjs (npm install -g casperjs) and run:
casperjs scrape.js <arg1> <arg2>
where arg1 is your email for carpe and arg2 is your password for carpe.

If you don't think you have a password for carpe, you do but it's randomly
generated. You'll need to visit the carpediem list at lists.olin.edu to
get it reset.
```
After that, run `python wrangle.py` which will do a rough parse of all the scraped data and make it accessible to the web app. Finally, run `models.py` to add the parsed emails to the remote database your app will use. Note that `models.py` resets the database; see the [operators section](#operating) for information on database setup.

If you intend to use this feature, please know that it is your responsibility to [never commit any of this data](https://help.github.com/articles/ignoring-files/) to a public repository like Github or disclose the identity of Olin students if creating a public app. Please be respectful of our community and its data!

