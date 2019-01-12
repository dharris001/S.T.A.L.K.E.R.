# import from dependencies
from slackeventsapi import SlackEventAdapter
import requests

# import from app
from ..services.slack import Slack
from ..services.db import Db
from .. import config

# module constants
SLACK_SIGNING_SECRET = config['auth']['slack']['signing_url']

# services
db = Db()
slack = Slack()
slack_events_adapter = SlackEventAdapter(
    SLACK_SIGNING_SECRET,
    endpoint='/webhook/slack')

@slack_events_adapter.on('app_mention')
def _app_mention(event):
    # verify admin request
    user = event['event']['user']
    user_info = slack.get_user(user)
    is_admin = user_info['user']['is_admin']

    # if admin, process command and handle
    if is_admin:
        command_dict = _parse_command(event)
        _command_handler(command_dict)

    # else return error to request
    else:
        channel = event['event']['channel']
        slack.post_message({ 'text': 'User not authorized' }, channel)

def _parse_command(event):
    # example command:
    # <@UDGM60HRR> add instagram account dallasdevs
    input_string = event['event']['text']
    input_arr = input_string.split()

    # return command dictionary
    return {
        'command': input_arr[1],
        'platform': input_arr[2],
        'account': input_arr[4],
        'channel': event['event']['channel']
    }

def _command_handler(command_dict):
    # destructure command
    command = command_dict['command']
    channel = command_dict['channel']

    # pass command through switch
    if command == 'add':
        _add_account(**command_dict)
    elif command == 'remove':
         _remove_account(**command_dict)
    elif command == 'list':
        _list_accounts(**command_dict)
    else:
        slack.post_message({ 'text': 'Invalid command' }, channel)

def _add_account(command, platform, account, channel):
    account_record = db.get_account(platform, account, channel)
    account_exists = bool(account_record)
    platform_list = ['instagram', 'reddit', 'twitter']
    invalid_platform = False if platform in platform_list else True

    if account_exists:
        slack.post_message({ 'text': 'Account already added' }, channel)

    elif invalid_platform:
        slack.post_message({ 'test': 'Invalid platform' }, channel)

    else:
        db.add_account(platform, account, channel)
        slack.post_message({ 'text': 'Account added' }, channel)

def _remove_account(command, platform, account, channel):
    account_record = db.get_account(platform, account, channel)
    account_missing = not bool(account_record)

    if account_missing:
        slack.post_message({ 'text': 'Account does not exist' }, channel)

    else:
        db.remove_account(platform, account, channel)
        slack.post_message({ 'text': 'Account removed' }, channel)

def _list_accounts(command, platform, account, channel):
    accounts = db.get_all_accounts()
    slack.post_message({ 'text': str(accounts) }, channel)
    # TTD build this message

class Webhook:

    def __init__(self):
        # start flask and adapter
        slack_events_adapter.start(host='0.0.0.0', port=80)
