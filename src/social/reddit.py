# import from system
import time
import json

# iimport from dependencies
import requests
import yaml

# import config
from .. import config

# module constants
REDDIT_ICON = 'https://www.redditstatic.com/desktop2x/img/favicon/favicon-32x32.png'
SLEEP_TIME = config['app']['sleep_time']
REQ_HEADERS = { 'User-Agent': 'S.T.A.L.K.E.R. by mikeydunn' }

class Reddit:

    def __init__(self, user):

        # initialize class props
        self.user = user

    def scrape(self):

        # build request url
        url = f'https://www.reddit.com/user/{self.user}.json'

        # request users posts
        # use unique headers for reddit throttling
        response = requests.get(url, headers=REQ_HEADERS)
        response.raise_for_status()
        json = response.json()

        # filter list of new posts
        posts = json['data']['children']
        new_posts = list(filter(self._is_new, posts))
        # return list of new raw posts
        return new_posts

    def message(self, post):
        # storing json objects for building message
        post_data = post['data']
        screen_name = post_data['author']
        author_name = f'u/{screen_name}'
        footer = post_data['subreddit_name_prefixed']
        ts = post_data['created_utc']
        permalink = post_data["permalink"]
        pretext = f'https://reddit.com{permalink}'
        parent_id = post_data.get('parent_id', '')

        # if post_data_hint exists, use submission keys
        # Might be able to do this by looking at the type prefix ('t1_', 't3_', etc)
        # https://www.reddit.com/dev/api/#fullnames
        if 'post_data_hint' in post_data or 'post_hint' in post_data:
            title = post_data['title']
            title_link = post_data['url']
            text = post_data['selftext']
            thumb_url = post_data['thumbnail']

        # else use comment keys
        else:
            title = post_data['link_title']
            title_link = post_data['link_url']
            text = post_data['body']
            thumb_url = ''

        # Start building the message
        attachments = list()

        # Append message header
        attachments.append({
            'pretext': pretext,
            'title': title,
            'title_link': title_link,
            'thumb_url': thumb_url,
        })

        # Append original comment, if it exists
        if parent_id and parent_id.startswith('t1_'):
            # t1_ means the parent is a comment, so lets get that text too
            parent_comment_url = f"https://www.reddit.com/api/info.json?id={parent_id}"
            response = requests.get(parent_comment_url, headers=REQ_HEADERS)
            response.raise_for_status()
            parent = response.json()['data']['children'][0]['data']
            parent_author = f'Original comment by u/{parent["author"]}'
            parent_text = parent['body']

            attachments.append({
                'author_name': parent_author,
                'text': parent_text,
                'color': 'good',
            })

        # Append target's comment
        attachments.append({
            'author_name': author_name,
            'text': text,
            'color': 'danger',
        })

        # Append footer
        attachments.append({
            'thumb_url': thumb_url,
            'footer': footer,
            'footer_icon': REDDIT_ICON,
            'ts': ts
        })

        # return formatted message
        return dict(attachments=attachments)

    def _is_new(self, post):

        # if invalid dict return false
        if 'created_utc' not in post['data']:
            return False

        # calculate times for check
        post_time = post['data']['created_utc']
        current_time = time.time()
        last_check_time = current_time - SLEEP_TIME

        # if the post time is larger, its newer than last check
        return True if post_time > last_check_time else False
