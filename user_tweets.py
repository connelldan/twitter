import requests
import os
from datetime import date, timedelta

# Request
ENDPOINT = "https://api.twitter.com/1.1/search/tweets.json"
bearer_token = os.environ['BEARER_TOKEN']
headers = {"Authorization": f"Bearer {bearer_token}"}   

# Dates
today = date.today()
today = today.strftime("%Y-%m-%d")
yesterday = date.today() - timedelta(days=1)
yesterday = yesterday.strftime("%Y-%m-%d")

def query_user(user="elonmusk", start_date=yesterday, end_date=today):

    """Retrieves all the tweets from a given user from yesterday to today.

    Args:
        user (str): the twitter handle of a user you would like to pull.
        start_date (str): lookback start date; format "%Y-%m-%d"
        end_date (str): date to look up until; format "%Y-%m-%d"

    Returns:
        list: a list of json (NLJSON) representing [user, create_date, tweet].
    """
    query = f"?q=(from%3A{user})%20until%3A{end_date}%20since%3A{start_date}%20-filter%3Areplies&count=100" 
    results = requests.get(f'{ENDPOINT}{query}', headers=headers).json() 

    needed = []
    for x in results["statuses"]:
        record = {
            "user": x["user"]["screen_name"],
            "create_date": x["created_at"],
            "tweet": x["text"]
        }
        needed.append(record)
    return needed