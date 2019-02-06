# import from system
from time import time
import hashlib
import hmac

# import from dependencies
from slackclient import SlackClient

# import from app
from . import db
from .. import config

# module constants
SIGNING_SECRET = config['auth']['slack']['signing_secret']

def post_message(message, channel, team):
    text = False
    attachments = False

    team_record = db.get_team(team)
    access_token = team_record[6]
    slack_client = SlackClient(access_token)

    if (isinstance(message, str)):
        text = message
    else:
        attachments = message

    return slack_client.api_call(
        "chat.postMessage",
        channel=channel,
        text=text,
        attachments=attachments,
        unfurl_links=True,
        unfurl_media=True)

def verify_request(request):
    # verify timestamp
    timestamp = request.headers.get('X-Slack-Request-Timestamp')

    if abs(time() - int(timestamp)) > 60 * 5:
        return False

    # verify signature
    signature = request.headers.get('X-Slack-Signature')
    req = str.encode('v0:' + str(timestamp) + ':') + request.get_data()
    request_hash = 'v0=' + hmac.new(
        str.encode(SIGNING_SECRET),
        req, hashlib.sha256
    ).hexdigest()

    if not hmac.compare_digest(request_hash, signature):
        return False

    # valid request
    return True
