# import from dependencies
from slackclient import SlackClient
from flask import request

# import from app
from ..services import db
from . import api_server
from .. import config

# module constants
CLIENT_ID = config['auth']['slack']['client_id']
CLIENT_SECRET = config['auth']['slack']['client_secret']
OAUTH_SCOPE = config['auth']['slack']['oauth_scope']

# endpoints
@api_server.route('/slack/install')
def _install():
    output = '''
        <a href="https://slack.com/oauth/authorize?scope={0}&client_id={1}">
            Add to Slack
        </a>
    '''.format(OAUTH_SCOPE, CLIENT_ID)

    return output

@api_server.route('/slack/auth')
def _auth():
    # access denied entry
    if 'error' in request.args:
        return 'Access Denied.'

    # authorized entry
    elif 'code' in request.args:
        auth_code = request.args['code']
        slack_client = SlackClient('')

        try:
            auth_response = slack_client.api_call(
                'oauth.access',
                client_id=CLIENT_ID,
                client_secret=CLIENT_SECRET,
                code=auth_code
            )

            # add all info to db
            db.add_team(auth_response)

            return 'Sccesfully installed.'

        except:
            pass

    return 'Error installing.'
