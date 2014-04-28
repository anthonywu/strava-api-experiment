# Strava API Experiment

This project is my personal experiment with [Strava's API](http://strava.github.io/api/). As an almost daily user of Strava recording private/commute rides as well as the occassional long weekend workout ride, I have some ideas for working with my own personal data as well as public community data, but I am not ready to package this tool for public consumption yet (e.g. as a published lib or web app).

This is an "afternoon project" for the time being, so I don't guarantee or claim any foresight or quality. Use or borrow this code at your own risk!

### Ideas

* analyze the breakdown between public vs. private activities
* analyze workout vs. commute bike rides

Note: there's a site called [VeloViewer](http://veloviewer.com/) which already does a bunch of fancy analytics and visualizations with your Strava data, so you might want to check that out. However, it's not open source (as far as I can tell).

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

e.g.

```
$ strava-api-experiment/src $ STRAVA_API_TOKEN=<...> konch
utils: <module 'utils' from 'strava-api-experiment/src/utils.pyc'>
client: <utils.MyStravaClient object at 0x10edc9050>

In [1]: client.get_athlete_clubs()
Out[1]:
[<Club id=11111 name=u'BAF' resource_state=2>,
 <Club id=22222 name=u'LS' resource_state=2>]
```

See [stravalib](https://github.com/hozn/stravalib) documentation on how to use the `client` object.

Enjoy!
