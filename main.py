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

global api

def no_unicode(data):
    return unicodedata.normalize('NFKD' , data).encode('ascii', 'ignore')


class WorkerThread (threading.Thread):
    def __init__(self, text, author):
        threading.Thread.__init__(self)
        self.text = text
        self.author = author

    def run(self):
        if not re.match("""^[A-Za-z0-9 _.,!"'/$]*$""", self.text): exit()

        # Links aren't cool
        if 'http' in self.text: exit()

        result = haiku(self.text)
        if result:
            api.update_status(result)
            print result
            print '  -@%s' % self.author
            print


class HaikuStreamListener (StreamListener):
    def on_status(self, status):
        if no_unicode(status.lang) == 'en':
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
    time.sleep(1)