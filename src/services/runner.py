# import from application
from ..social.instagram import Instagram
from ..social.twitter import Twitter
from ..social.reddit import Reddit
from . import slack

class Runner:

    def __init__(self, platform, account, channel, team):
        # logging
        print(f'{platform} -- {account} -- {channel} -- {team}')

        # store account and platform
        self.platform = platform
        self.account = account
        self.channel = channel
        self.team = team

    def stalk(self):
        # fallback if scrape fails
        post_list = []

        # run social platform specific methods
        if self.platform == 'reddit':
            social = Reddit(self.account)
        elif self.platform == 'twitter':
            social = Twitter(self.account)
        elif self.platform == 'instagram':
            social = Instagram(self.account)
        else:
            return

        # attempt scrape and append to post_list
        try:
            new_posts = social.scrape()
            post_list = post_list + new_posts

        except Exception as e:
            error_string = str(e)
            error_message = f'{self.platform}/{self.account}/{self.team}: {error_string}'
            print(error_message)

        # Iterate through posts returned from scrape
        # build message and post to slack
        for post in post_list:
            message = social.message(post)
            slack.post_message(message, self.channel, self.team)
