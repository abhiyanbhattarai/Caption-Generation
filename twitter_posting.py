
import tweepy
import os
from dotenv import load_dotenv

def tweet_post(image_path, tweet_text):
    # Load environment variables from creds
    load_dotenv('creds')

    # Access Twitter API credentials
    consumer_key = os.getenv("TWITTER_CONSUMER_KEY")
    consumer_secret = os.getenv("TWITTER_CONSUMER_SECRET")
    access_token = os.getenv("TWITTER_ACCESS_TOKEN")
    access_token_secret = os.getenv("TWITTER_ACCESS_TOKEN_SECRET")

    client = tweepy.Client(consumer_key=consumer_key, consumer_secret=consumer_secret,
                 access_token=access_token,access_token_secret=access_token_secret)
    
    auth = tweepy.OAuth1UserHandler(consumer_key, consumer_secret,access_token, access_token_secret)

    # Create API object
    api = tweepy.API(auth, wait_on_rate_limit=True)


    # Upload image
    media = api.media_upload(filename=image_path)

    # Post tweet with image
    response = client.create_tweet(text=tweet_text, media_ids=[media.media_id])

    return response


