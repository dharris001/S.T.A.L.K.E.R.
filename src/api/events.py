# import from dependencies
from slackeventsapi import SlackEventAdapter
from flask import Flask

# import from app
from ..services import commands
from ..services import slack
from . import api_server
from .. import config

# module constants
SLACK_SIGNING_SECRET = config['auth']['slack']['signing_url']

# services
slack_events = SlackEventAdapter(SLACK_SIGNING_SECRET, '/slack/events', api_server)

# events
@slack_events.on('app_mention')
def _app_mention(event):
    channel = event['event']['channel']
    response = commands.command_switch(event)
    slack.post_message(response, channel)

    # if event_id = Ev0MDYHUEL respond with help commands
