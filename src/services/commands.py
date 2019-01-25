from . import db

platform_list = ['instagram', 'reddit', 'twitter']
available_commands = ['add', 'remove', 'list']

def parse_command(event):
    # example command:
    # <@UDGM60HRR> add instagram account dallasdevs
    input_string = event['event']['text']
    input_arr = input_string.split()
    command = input_arr[1]
    platform = input_arr[2]
    account = input_arr[4]
    channel = event['event']['channel']
    team = event['team_id']

    return command, platform, account, channel, team

def command_switch(event):
    #parse command
    command, platform, account, channel, team = parse_command(event)

    # pass command through switch
    if command == 'add': return add_account(platform, account, channel, team)
    if command == 'remove': return remove_account(platform, account, channel, team)
    if command == 'list': return list_accounts()

    # fallback message
    return 'Invalid command'

def add_account(platform, account, channel, team):
    # validate platform
    platform_normalized = platform.lower()
    invalid_platform = False if platform_normalized in platform_list else True
    if invalid_platform: return 'Invalid platform'

    # validate account
    account_record = db.get_account(platform, account, channel, team)
    account_exists = bool(account_record)
    if account_exists: return 'Account already added'

    # run command
    db.add_account(platform, account, channel, team)
    return 'Account added'

def remove_account(platform, account, channel, team):
    # validate account
    account_record = db.get_account(platform, account, channel, team)
    account_missing = not bool(account_record)
    if account_missing: return 'Account does not exist'

    # run command
    db.remove_account(platform, account, channel, team)
    return 'Account removed'

def list_accounts():
    # run command
    accounts = db.get_all_accounts()
    return str(accounts)
