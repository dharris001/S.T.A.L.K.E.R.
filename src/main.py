# import from system
import threading
import time

# import from app
from .services.webhook import Webhook
from .services.runner import Runner
from .services.db import Db
from . import config

# constants
SLEEP_TIME = config['app']['sleep_time']

def main():
    # start webhook server
    webhook_server = threading.Thread(target=Webhook)
    webhook_server.start()

    # begin stalking loop
    while True:
        accounts = Db().get_all_accounts()

        # start a runner for each account
        for index, platform, account, channel in accounts:
            print(f'{platform} -- {account} -- {channel}')
            runner = Runner(platform, account, channel)
            runner.stalk()

        # wait for next cycle
        time.sleep(SLEEP_TIME)

if __name__ == "__main__":
    main()
