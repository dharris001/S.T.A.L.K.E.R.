# import from system
import functools
import threading
import time

# import from app
from .api import api_server
from .services.runner import Runner
from .services import db
from . import config

# constants
SLEEP_TIME = config['app']['sleep_time']

def main():
    # start api server
    api_server_run = functools.partial(api_server.run, host='0.0.0.0', port=80)
    api_server_thread = threading.Thread(target=api_server_run)
    api_server_thread.start()

    # begin stalking loop
    while True:
        accounts = db.get_all_accounts()

        # start a runner for each account
        for index, platform, account, channel, team in accounts:
            runner = Runner(platform, account, channel, team)
            runner.stalk()

        # wait for next cycle
        time.sleep(SLEEP_TIME)

if __name__ == "__main__":
    main()
