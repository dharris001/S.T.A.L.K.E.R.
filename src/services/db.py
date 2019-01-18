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
    channel text NOT NULL
); ''')

def get_all_accounts():
    sql = 'SELECT * FROM accounts'
    cursor = dbconn.cursor()
    cursor.execute(sql)

    return cursor.fetchall()

def get_account(platform, account, channel):
    sql = 'SELECT * FROM accounts WHERE platform=? AND account=? AND channel=?'
    cursor = dbconn.cursor()
    cursor.execute(sql, (platform, account, channel))

    return cursor.fetchone()

def add_account(platform, account, channel):
    sql = 'INSERT INTO accounts(platform, account, channel) VALUES(?,?,?)'
    cursor = dbconn.cursor()
    cursor.execute(sql, (platform, account, channel))
    dbconn.commit()

def remove_account(platform, account, channel):
    sql = 'DELETE FROM accounts WHERE platform=? AND account=? AND channel=?'
    cursor = dbconn.cursor()
    cursor.execute(sql, (platform, account, channel))
    dbconn.commit()
