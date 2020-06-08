# -*- coding: utf-8 -*-

import re
import emoji
from nltk.corpus import stopwords
from typing import NoReturn, Text, List

from variables.envs import logger

class TweetCleaner(object):

  def __init__(self,
      language="portuguese",
      remove_stop_words=False,
      remove_retweets=False) -> NoReturn:
    self.stop_words = set(stopwords.words("portuguese")) if remove_stop_words else set()
    self.remove_retweets = remove_retweets

  def give_emoji_free_text(self, text: Text) -> Text:
    allchars = [string for string in text]
    emoji_list = [string for string in allchars if string in emoji.UNICODE_EMOJI]
    return " ".join([string for string in text.split()
      if not any(value in string for value in emoji_list)])

  def get_claned_retweet_text(self, text: Text) -> Text:
    if re.match(r"RT @[_A-Za-z0-9]+:", text):
      if self.remove_retweets: return ""
      retweet_info = text[:text.index(":") + 2]
      text = text[text.index(":")+ 2:]
    else:
      retweet_info = ""
    return retweet_info

  def get_cleaned_text(self, text: Text) -> Text:
    try:
      cleaned_text = text.replace("\n", "").replace('\"','').replace('\'','').replace('-',' ')
      retweet_info = self.get_claned_retweet_text(cleaned_text)
      cleaned_text = re.sub(r"@[a-zA-Z0-9_]+", "", (retweet_info + cleaned_text)).strip()
      cleaned_text = re.sub(r"RT\s:\s", "", cleaned_text).lstrip()
      cleaned_text = cleaned_text[::] if cleaned_text[0] != " " else cleaned_text[1::]
      cleaned_text = self.give_emoji_free_text(cleaned_text)
      cleaned_text = re.sub(r"http\S+", "", cleaned_text)
      cleaned_text = re.sub(r"https\S+", "", cleaned_text)
      return cleaned_text
    except Exception as error:
      logger.error(f"Error get cleaned tweet text - {error}")

  def filter_tweets(self, tweets: List) -> List:
    return [
      { "_id": str(tweet.user.id) if tweet.user.id else "None",
        "name": str(tweet.user.name) if tweet.user.name else "None",
        "screen_name": str(tweet.user.screen_name) if tweet.user.screen_name else "None",
        "description": str(tweet.user.description) if tweet.user.description else "None",
        "followers_count": str(tweet.user.followers_count) if tweet.user.followers_count else "None",
        "friends_count": str(tweet.user.friends_count) if tweet.user.friends_count else "None",
        "location": str(tweet.user.location) if tweet.user.location else "None",
        "full_text": self.get_cleaned_text(tweet.full_text) if tweet.full_text else "None"
      } for tweet in tweets]
