# import from dependencies
from slackclient import SlackClient

# import from app
from . import db

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
