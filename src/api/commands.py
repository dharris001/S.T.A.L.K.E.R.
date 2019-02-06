# import from dependencies
from flask import request, jsonify
import requests

# import from app
from ..services import slack
from ..services import db
from . import api_server

# module constants
PLATFORM_LIST = ['twitter', 'instagram', 'reddit']

# endpoints
@api_server.route('/slack/add', methods=['POST'])
def _add():
    # validate token
    verified_req = slack.verify_request(request)
    if not verified_req: return 'Invalid request'

    # parse command
    command_dict = request.form.to_dict()
    platform = command_dict['text'].split()[0].lower()
    account = command_dict['text'].split()[1].lower()
    channel = command_dict['channel_id']
    team = command_dict['team_id']

    # validate platform
    invalid_platform = False if platform in PLATFORM_LIST else True
    if invalid_platform: return 'Invalid platform'

    # validate account
    account_record = db.get_account(platform, account, channel, team)
    account_exists = bool(account_record)
    if account_exists: return 'Account already added'

    # run command
    db.add_account(platform, account, channel, team)

    # send responses
    response_url = command_dict['response_url']
    public_message = {
        'response_type': 'in_channel',
        'text': f'Now targeting {account} on {platform}.'
    }
    requests.post(response_url, json=public_message)

    return api_server.response_class(status=200)

@api_server.route('/slack/remove', methods=['POST'])
def _remove():
    # validate token
    verified_req = slack.verify_request(request)
    if not verified_req: return 'Invalid request'

    # parse command
    command_dict = request.form.to_dict()
    platform = command_dict['text'].split()[0].lower()
    account = command_dict['text'].split()[1].lower()
    channel = command_dict['channel_id']
    team = command_dict['team_id']

    # validate account
    account_record = db.get_account(platform, account, channel, team)
    account_missing = not bool(account_record)
    if account_missing: return 'Account does not exist'

    # run command
    db.remove_account(platform, account, channel, team)

    # send responses
    response_url = command_dict['response_url']
    public_message = {
        'response_type': 'in_channel',
        'text': f'Removed {platform} account {account}.'
    }
    requests.post(response_url, json=public_message)

    return api_server.response_class(status=200)
