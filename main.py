__author__ = 'Zachery Thomas'


from tweepy.streaming import StreamListener
from tweepy import OAuthHandler
from tweepy import Stream
from haiku import haiku
from config import *
import unicodedata
import threading
import time


def no_unicode(data):
    return unicodedata.normalize('NFKD' , data).encode('ascii', 'ignore')


class WorkerThread (threading.Thread):
    def __init__(self, text, author):
        threading.Thread.__init__(self)
        self.text = text
        self.author = author

    def run(self):
        # Links aren't cool
        if 'http' in self.text: exit()

        # Don't want @'s
        if '@' in self.text: exit()

        result = haiku(self.text)
        if result:
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

while 1:
    try:
        stream.sample()
    except Exception as e:
        print e
    time.sleep(1)