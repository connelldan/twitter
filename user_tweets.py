"""
Help Encapsualte all twitter endpoints
Known Ids:
     Elon Musk: 44196397
"""


import os
import requests
from datetime import date, timedelta
from datetime import datetime as dt

from dotenv import load_dotenv

load_dotenv()

# Dates
today = date.today().strftime("%Y-%m-%d")
yesterday = (date.today() - timedelta(days=1)).strftime("%Y-%m-%d")

class TwitterClient(object):
    """Helps encapsulate twitter functions to share commone elements"""
    def __init__(self):
        """

        """
        bearer_token = os.getenv('TWITTER_BEARER_TOKEN')
        self.auth_header = {"Authorization": f"Bearer {bearer_token}"}
        self.base_url = "https://api.twitter.com"


    def query_user(self, user="elonmusk", start_date=yesterday, end_date=today):
        """
        Retrieves all the tweets from a given user from yesterday to today.

        Args:
            user (str): the twitter handle of a user you would like to pull.
            start_date (str): lookback start date; format "%Y-%m-%d"
            end_date (str): date to look up until; format "%Y-%m-%d"

        Returns:
            list: a list of json (NLJSON) representing [user, create_date, tweet].
        """
        url = f"{self.base_url}/1.1/search/tweets.json"
        query = f"?q=(from%3A{user})%20until%3A{end_date}%20since%3A{start_date}"
        response = requests.get(f'{url}{query}',
                                headers=self.auth_header)

        if response.status_code != 200:
            print(f"TWITTER CLIENT ERROR")
            print(response.content)
            return False

        results = response.json()
        needed = []
        for x in results["statuses"]:
            record = {
                "user": x["user"]["screen_name"],
                "create_date": x["created_at"],
                "tweet": x["text"]
            }
            needed.append(record)
        return needed


    def get_user_id(self, username):
        """
        Helper method to get a user id
        """
        url = f'{self.base_url}/2/users/by/username/{username}'
        response = requests.get(url,
                                headers=self.auth_header)
        if response.status_code != 200:
            print(f"Issure finding id for {username}")
            print(response.content)
            return False
        return response.json()['data']['id']


    def get_timeline_tweets(self, user_id, max_results=10):
        """
        Doc: https://documenter.getpostman.com/view/9956214/T1LMiT5U#daeb8a9f-6dac-4a40-add6-6b68bffb40cc


        Method to get most recent tweets, last 3200 tweets are available. Can
        iteate through them by using the max_results, and then finding oldest
        and newest id. Alot of paramets can be used to fetch more historical
        but it is kind of messy
        """
        url = f'{self.base_url}/2/users/{user_id}/tweets'
        params = {"max_results": max_results,
                  "tweet.fields": "created_at"}

        response = requests.get(url,
                                headers=self.auth_header,
                                params=params)

        if response.status_code != 200:
            print(f"Issue with time tweet fetcher for {user_id}")
            print(response.content)
            return response

        results = response.json()
        if 'data' in results:
            for tweet in results['data']:
                tweet['created_at'] = dt.strptime(tweet['created_at'], '%Y-%m-%dT%H:%M:%S.000Z')

        return results

# Just an example
if __name__ == '__main__':
    client = TwitterClient()
    musk_id = client.get_user_id("elonmusk")
    results = client.get_timeline_tweets(musk_id, 100)
    tweets = results['data']
