import re
import collections,itertools
import tweepy
import logging
import time
import pandas as pd
from config import create_api
import matplotlib.pyplot as plt
from nltk.corpus import stopwords

api = create_api()
stop_words =set(stopwords.words('english'))

def process(tweets):
    replies = []
    for i in tweets:
        replies.append(' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)"," ",str(i)).split()))
    return replies

def words_data(tweet_replies):
    """
    Tweets fetch and count analysis
    Parameters - company and number of tweets to be fetched.
    returns cleaned twitter data.
    """
    words_in_tweet = [tweet.lower().split() for tweet in tweet_replies]
    tweets_nsw = [[word for word in tweet_words if not word in stop_words] for tweet_words in words_in_tweet]

    all_words_nsw = list(itertools.chain(*tweets_nsw))
    counts_nsw = collections.Counter(all_words_nsw)
    clean_tweets_nsw = pd.DataFrame(counts_nsw.most_common(15), columns=['words', 'count'])
    return clean_tweets_nsw

def matplot(tweet_replies):
    """
    Creates a Matplot lib chart
    Returns fig object
    """
    data = words_data(tweet_replies)
    fig, ax = plt.subplots(figsize=(8, 8))
    data.sort_values(by='count').plot.barh(x='words', y='count', ax=ax, color="purple")

    ax.set_title("Common Words Found in Tweets (Without Stop Words)")
    return fig

def fetch_comments(tweet_link):
    """
    
    """
    name = re.search('^(?:.*twitter\.com/|@?)(\w{1,15})(?:$|/.*$)', tweet_link).group(1)
    tweet_id = re.search('/status/(\d+)(?#)', tweet_link).group(1)
    replies=[]
    reply = tweepy.Cursor(api.search,q='to:'+name, timeout=999999).items(1000)
    while True:
        try:
            tweet = reply.next()
            if hasattr(tweet, 'in_reply_to_status_id_str'):
                if (tweet.in_reply_to_status_id_str==tweet_id):
                    replies.append(tweet.text)
        except tweepy.RateLimitError as e:
            logging.error("Twitter api rate limit reached".format(e))
            time.sleep(60)
            continue

        except tweepy.TweepError as e:
            logging.error("Tweepy error occured:{}".format(e))
            break

        except StopIteration:
            break

        except Exception as e:
            logging.error("Failed while fetching replies {}".format(e))
            break
    tweets_data = pd.DataFrame(process(replies),columns=['Tweets'])
    return tweets_data


    
