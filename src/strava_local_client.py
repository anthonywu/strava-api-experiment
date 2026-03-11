#!/usr/bin/env python

"""
Strava Development Sandbox.

Get your *Client ID* and *Client Secret* from https://www.strava.com/settings/api

Usage:
  strava_local_client.py get_write_token <client_id> <client_secret> [options]
  strava_local_client.py find_settings

Options:
  -h --help      Show this screen.
  --port=<port>  Local port for OAuth client [default: 8000].
"""

import stravalib
from flask import Flask, request

app = Flask(__name__)

API_CLIENT = stravalib.Client()
WRITE_SCOPES = ["activity:write", "activity:read_all", "profile:read_all"]

# set these in __main__
CLIENT_ID = None
CLIENT_SECRET = None

@app.route("/auth")
def auth_callback():
    oauth_error = request.args.get('error')
    if oauth_error:
        return {'error': oauth_error, 'state': request.args.get('state')}, 400

    code = request.args.get('code')
    if not code:
        return {'error': 'missing_code', 'state': request.args.get('state')}, 400

    token_response = API_CLIENT.exchange_code_for_token(
        client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET,
        code=code
        )
    if isinstance(token_response, tuple):
        access_info = token_response[0]
    else:
        access_info = token_response
    return access_info


if __name__ == '__main__':
    import docopt
    import subprocess
    import sys
    from blessings import Terminal

    args = docopt.docopt(__doc__)
    t = Terminal()

    if args['get_write_token']:
        CLIENT_ID = int(args['<client_id>'])
        CLIENT_SECRET = args['<client_secret>']
        auth_url = API_CLIENT.authorization_url(
            client_id=CLIENT_ID,
            redirect_uri='http://127.0.0.1:{port}/auth'.format(port=args['--port']),
            scope=WRITE_SCOPES,
            state='from_cli'
            )
        if sys.platform == 'darwin':
            print(t.green('On OS X - launching {0} at default browser'.format(auth_url)))
            subprocess.call(['open', auth_url])
        else:
            print(t.red('Go to {0} to authorize access: '.format(auth_url)))
        app.run(port=int(args['--port']))
    elif args['find_settings']:
        subprocess.call(['open', 'https://www.strava.com/settings/api'])
