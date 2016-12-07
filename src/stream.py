import tweepy
import json

# Authentication details. To  obtain these visit dev.twitter.com
consumer_key = '6Px0ha1Dh0bUVaCTQAjoIXD9a'
consumer_secret = '0QabO64g45GtQPigQh89c5JHf1zoQmYHgOpzlKMy6PObHsj0qh'
access_token = '2588377867-aNz4bqRn627zsxwdkntVtWLgep5pI2YcMU8sClc'
access_token_secret = 'crvuZvCab6aAnlLqlUwQg9wHSachjI9Lo0VdMNHEP5zsS'

# This is the listener, resposible for receiving data
class StdOutListener(tweepy.StreamListener):
    def on_data(self, data):
        # Twitter returns data in JSON format - we need to decode it first
        decoded = json.loads(data)

        print decoded
        print ''
        return True

    def on_error(self, status):
        print status

if __name__ == '__main__':
    l = StdOutListener()
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)

    stream = tweepy.Stream(auth, l)
    stream.filter(track=['debate','trump','hillary'])
