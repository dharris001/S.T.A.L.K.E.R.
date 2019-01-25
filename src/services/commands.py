from . import db

platform_list = ['instagram', 'reddit', 'twitter']
available_commands = ['add', 'remove', 'list']

def add_account(platform, account, channel):
    # validate platform
    platform_normalized = platform.lower()
    invalid_platform = False if platform_normalized in platform_list else True
    if invalid_platform: return 'Invalid platform'

    # validate account
    account_record = db.get_account(platform, account, channel)
    account_exists = bool(account_record)
    if account_exists: return 'Account already added'

    # run command
    db.add_account(platform, account, channel)
    return 'Account added'

def remove_account(platform, account, channel):
    # validate account
    account_record = db.get_account(platform, account, channel)
    account_missing = not bool(account_record)
    if account_missing: return 'Account does not exist'

    # run command
    db.remove_account(platform, account, channel)
    return 'Account removed'

def list_accounts():
    # run command
    accounts = db.get_all_accounts()
    return str(accounts)
