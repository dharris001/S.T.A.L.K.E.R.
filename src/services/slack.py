# import from dependencies
import requests

# import from app
from .. import config

# module constants
SLACK_CHAT_URL = 'https://slack.com/api/chat.postMessage'
SLACK_USER_INFO_URL = 'https://slack.com/api/users.info'
SLACK_BOT_TOKEN = config['auth']['slack']['bot_token']

class Slack:

    def post_message(self, message, channel):
        # request options
        message['channel'] = channel
        headers = {
            'Authorization': f'Bearer {SLACK_BOT_TOKEN}',
            'Content-Type': 'application/json'
        }

        try:
            # send post request for chat message
            response = requests.post(
                SLACK_CHAT_URL,
                headers=headers,
                json=message)

            return response.json()

        except Exception as e:
            error_string = str(e)
            print(error_string)

    def get_user(self, user):
        # request options
        params = dict(user=user)
        headers = {
            'Authorization': f'Bearer {SLACK_BOT_TOKEN}',
            'Content-Type': 'application/x-www-form-urlencoded'
        }

        try:
            # send get request for user info
            response = requests.get(
                SLACK_USER_INFO_URL,
                headers=headers,
                params=params)

            return response.json()

        except Exception as e:
            error_string = str(e)
            print(error_string)
