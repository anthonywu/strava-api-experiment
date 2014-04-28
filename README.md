# Strava API Experiment

This project is my personal experiment with [Strava's API](http://strava.github.io/api/). As an almost daily user of Strava, I have some ideas for working with my own personal data as well as public community data, but I am not ready to package this tool for public consumption yet (e.g. as a published lib or web app).

### Ideas

* analyze the breakdown between public vs. private activities
* analyze workout vs. commute bike rides

### What's inside so far

* a simple OAuth client to get a write-permission `access_token` (for developer use)
* some starter utilities to analyze my personal ride data

### 3rd Party Dependencies

* [hozn's stravalib](https://github.com/hozn/stravalib)
* Python libs listed in requirements.txt

### Exploring the API for your own data

1. create a new Python [virtualenv](http://www.virtualenv.org/en/latest/) (highly recommended)
2. `git clone git@github.com:anthonywu/strava-api-experiment.git`
3. `cd strava-api-experiment`
4. with the project virtualenv activated: `pip install -r requirements.txt`
6. [Register your app](http://www.strava.com/developers) with Strava, then get the `client_id` and `client_secret` parameters from https://www.strava.com/settings/api
6. `cd src`, examine the source of `./strava_local_client.py` or run `./strava_local_client.py -h` - this is a script that interacts with Strava's OAuth endpoints to give you a write-access token
7. Run the local OAuth client: `./strava_local_client.py get_write_token <client_id> <client_secret>`. The client will provide an url (or on OS X, launch your default browser to that url) which directs you to a strava.com page that lets you authorize write-access to your account. After you authorize the usage, the OAuth callback returns to the `localhost`-hosted client app with a `code` that the client then exchanges for an `access_token`. Your browser should display the `access_token` as the response. You can now use this write-permission `access_token` to view and modify your own user data.
8. Getting on the Python command line to play with the API: `STRAVA_API_TOKEN=<access_token> konch`

Enjoy!
