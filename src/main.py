# import from system
import time
import sys

# import from dependencies
import yaml

# import from app
from services.slack import Slack
from services.runner import Runner

def main():

    # import config
    with open('config.yml', 'r') as config:
        config = yaml.load(config)

    # variable declerations
    social_channels = config['social_channels']
    sleep_time = config['app']['sleep_time']
    slack = Slack()
    start_message = { 'text': 'now stalking...' }
    exit_message = { 'text': 'ending stalk...' }

    # output running status
    slack.post(start_message)

    # loop through runners until killed
    while True:
        try:
            # start cycle of runners
            initialize_runners(social_channels)

            # wait for next cycle
            time.sleep(sleep_time)

        except KeyboardInterrupt:
            # output ending status
            slack.post(exit_message)

            # graceful exit
            sys.exit(0)

def initialize_runners(social_channels):

    # start a runner for each user in a channel
    for channel, users in social_channels.items():
        if isinstance(users, list):
            for user in users:
                runner = Runner(channel, user)
                runner.stalk()

main()