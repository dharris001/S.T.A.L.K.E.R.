# import from system
import sqlite3

# create connection to share with classes
dbconn = sqlite3.connect(
    './src/datastore/accounts.db',
    check_same_thread=False)

# generate new table if it doesn't exist
dbconn.cursor().execute(
''' CREATE TABLE IF NOT EXISTS accounts (
    id integer PRIMARY KEY,
    platform text NOT NULL,
    account text NOT NULL,
    channel text NOT NULL,
    team_id text NOT NULL
); ''')

dbconn.cursor().execute(
''' CREATE TABLE IF NOT EXISTS teams (
    id integer PRIMARY KEY,
    access_token text NOT NULL ,
    scope text NOT NULL,
    team_name text NOT NULL,
    team_id text NOT NULL UNIQUE,
    bot_user_id text NOT NULL,
    bot_access_token text NOT NULL
); ''')

def get_all_accounts():
    sql = 'SELECT * FROM accounts'
    cursor = dbconn.cursor()
    cursor.execute(sql)

    return cursor.fetchall()

def get_account(platform, account, channel, team):
    sql = 'SELECT * FROM accounts WHERE platform=? AND account=? AND channel=? AND team_id=?'
    cursor = dbconn.cursor()
    cursor.execute(sql, (platform, account, channel, team))

    return cursor.fetchone()

def add_account(platform, account, channel, team):
    sql = 'INSERT INTO accounts(platform, account, channel, team_id) VALUES(?,?,?,?)'
    cursor = dbconn.cursor()
    cursor.execute(sql, (platform, account, channel, team))
    dbconn.commit()

def remove_account(platform, account, channel, team):
    sql = 'DELETE FROM accounts WHERE platform=? AND account=? AND channel=? AND team_id=?'
    cursor = dbconn.cursor()
    cursor.execute(sql, (platform, account, channel, team))
    dbconn.commit()

def add_team(auth_dict):
    access_token = auth_dict['access_token']
    scope = auth_dict['scope']
    team_name = auth_dict['team_name']
    team_id = auth_dict['team_id']
    bot_user_id = auth_dict['bot']['bot_user_id']
    bot_access_token = auth_dict['bot']['bot_access_token']

    sql = 'INSERT INTO teams(access_token, scope, team_name, team_id, bot_user_id, bot_access_token) VALUES(?,?,?,?,?,?) ON CONFLICT(team_id) DO UPDATE SET access_token=excluded.access_token, scope=excluded.scope, bot_user_id=excluded.bot_user_id, bot_access_token=excluded.bot_access_token'
    cursor = dbconn.cursor()
    cursor.execute(sql, (access_token, scope, team_name, team_id, bot_user_id, bot_access_token))
    dbconn.commit()

def get_team(team):
    sql = 'SELECT * FROM teams WHERE team_id=?'
    cursor = dbconn.cursor()
    cursor.execute(sql, (team,))

    return cursor.fetchone()
