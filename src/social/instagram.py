# import from system
import json
import time

# import from dependencies
import requests
from bs4 import BeautifulSoup

# import from app
from .. import config

# module constants
BASE_URL = 'https://www.instagram.com/'
SLEEP_TIME = config['app']['sleep_time']

class Instagram:

    def __init__(self, handle):
        # initialize class props
        self.handle = handle

    def __extract_json(self, html):
        soup = BeautifulSoup(html, 'html.parser')
        body = soup.find('body')
        script_tag = body.find('script')
        raw_string = script_tag.text.strip().replace('window._sharedData =', '').replace(';', '')
        return json.loads(raw_string)

    def scrape(self):
        new_posts = []
        profile_url = BASE_URL + f'{self.handle}'

        # request user posts
        response = requests.get(profile_url)
        data = self.__extract_json(response.text)

        # filter list of new posts
        user_profile = data['entry_data']['ProfilePage'][0]['graphql']['user']
        posts = user_profile['edge_owner_to_timeline_media']['edges']
        new_posts = list(filter(self._is_new, posts))

        # return list of new raw posts
        return new_posts


    def message(self, post):
        # storing json objects for building message
        latest_post = post['node']
        shortcode = latest_post["shortcode"]
        message = f'{BASE_URL}p/{shortcode}'

        # return formatted message
        return message

    def _is_new(self, post):
        # if invalid dict return false
        if 'taken_at_timestamp' not in post['node']:
            return False

        # calculate times for check
        post_time = post['node']['taken_at_timestamp']
        current_time = time.time()
        last_check_time = current_time - SLEEP_TIME

        # if the post time is larger, its newer than last check
        return True if post_time > last_check_time else False
