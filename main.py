__author__ = 'Zachery Thomas'


from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
from tweepy import API
from haiku import haiku
from config import *
import unicodedata
import threading
import time
import re

global api, C_TIME, MIN_TO_WAIT
C_TIME = time.time()
MIN_TO_WAIT = 120
SEC_TO_WAIT = MIN_TO_WAIT * 60
tweet_found = False


def no_unicode(data):
    return unicodedata.normalize('NFKD' , data).encode('ascii', 'ignore')



class WorkerThread (threading.Thread):
    def __init__(self, text, author):
        threading.Thread.__init__(self)
        self.text = text
        self.author = author

    def run(self):
        # Make sure there are no special characters
        if not re.match("""^[A-Za-z _.,!"'/$]*$""", self.text): exit()

        # Links aren't cool
        if 'http' in self.text: exit()

        result = haiku(self.text)
        if result:
            api.update_status(result + '\n     -%s' % self.author)
            set_limiter()

            print result + '\n\n     -%s' % self.author
            print

            tweet_found = True

class HaikuStreamListener (StreamListener):
    def on_status(self, status):
        # if a tweet is found, end the stream
        if tweet_found = True:
            return False

        if not is_limited() and no_unicode(status.lang) == 'en':
            wt = WorkerThread(status.text, status.author.screen_name)
            wt.start()

    def on_error(self, status):
        print status


auth = OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

hsl = HaikuStreamListener()
stream = Stream(auth, hsl, timeout=None)

api = API(auth)

while 1:
    try:
        stream.sample()
    except Exception as e:
        print e
    time.sleep(SEC_TO_WAIT)

