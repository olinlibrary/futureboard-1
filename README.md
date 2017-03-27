# CarpFace
Data visualization for the carpediem email list at Olin

## Installing

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

After that, run `python wrangle.py` which will do a rough parse of all the scraped data and make it accessible to the web app. Then you're ready to go! Just run `python server.py` and visit `localhost:5000`.
