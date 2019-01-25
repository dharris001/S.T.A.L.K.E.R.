# import from system
import threading
import time

# import from app
from .services.runner import Runner
from .services import slack
from .services import db
from . import config

# constants
SLEEP_TIME = config['app']['sleep_time']

def main():
    # start webhook server
    webhook_server = threading.Thread(target=slack.webhook)
    webhook_server.start()

    # begin stalking loop
    while True:
        accounts = db.get_all_accounts()

        # start a runner for each account
        for index, platform, account, channel in accounts:
            runner = Runner(platform, account, channel)
            runner.stalk()

        # wait for next cycle
        time.sleep(SLEEP_TIME)

if __name__ == "__main__":
    main()
