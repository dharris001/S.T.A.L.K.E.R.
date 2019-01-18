# import from dependencies
from slackeventsapi import SlackEventAdapter
from slackclient import SlackClient

# import from app
from . import commands
from .. import config

# module constants
SLACK_SIGNING_SECRET = config['auth']['slack']['signing_url']
SLACK_BOT_TOKEN = config['auth']['slack']['bot_token']

# services
slack_client = SlackClient(SLACK_BOT_TOKEN)
slack_events = SlackEventAdapter(SLACK_SIGNING_SECRET, endpoint='/webhook/slack')

# event listeners
@slack_events.on('app_mention')
def _app_mention(event):
    channel = event['event']['channel']
    command_dict = _parse_mention(event)
    response = _command_handler(**command_dict)
    post_message(response, channel)

# public functions
def webhook():
    # start flask and adapter
    slack_events.start(host='0.0.0.0', port=80)

def post_message(message, channel):
    text = False
    attachments = False

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

# helper functions
def _parse_mention(event):
    # example command:
    # <@UDGM60HRR> add instagram account dallasdevs
    input_string = event['event']['text']
    input_arr = input_string.split()

    return {
        'command': input_arr[1],
        'platform': input_arr[2],
        'account': input_arr[4],
        'channel': event['event']['channel']
    }

def _command_handler(command, platform, account, channel):

    # pass command through switch
    if command == 'add': return commands.add_account(platform, account, channel)
    if command == 'remove': return commands.remove_account(platform, account, channel)
    if command == 'list': return commands.list_accounts()

    # fallback message
    return 'Invalid command'
