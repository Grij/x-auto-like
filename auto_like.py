import tweepy
import os
from datetime import datetime
import json

with open("config.json", "r") as f:
    config = json.load(f)
MAX_LIKES_PER_DAY = config["max_likes_per_day"]
SEARCH_QUERY = config["search_query"]
# Налаштування API X
API_KEY = os.getenv("API_KEY")
API_SECRET = os.getenv("API_SECRET")
ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")
ACCESS_TOKEN_SECRET = os.getenv("ACCESS_TOKEN_SECRET")
BEARER_TOKEN = os.getenv("BEARER_TOKEN")

# Ініціалізація клієнта
client = tweepy.Client(
    bearer_token=BEARER_TOKEN,
    consumer_key=API_KEY,
    consumer_secret=API_SECRET,
    access_token=ACCESS_TOKEN,
    access_token_secret=ACCESS_TOKEN_SECRET
)

# Налаштування пошуку
SEARCH_QUERY = "#python OR from:elonmusk -is:retweet"  # Змініть на ваші ключові слова
MAX_LIKES_PER_DAY = 10
LIKED_TWEETS_FILE = "liked_tweets.txt"

def load_liked_tweets():
    try:
        with open(LIKED_TWEETS_FILE, "r") as f:
            return [int(line.strip()) for line in f if line.strip()]
    except FileNotFoundError:
        return []

def save_liked_tweets(tweet_id):
    with open(LIKED_TWEETS_FILE, "a") as f:
        f.write(f"{tweet_id}\n")

def like_tweets():
    print(f"Запуск скрипта: {datetime.now()}")
    liked_tweets = load_liked_tweets()
    
    # Пошук постів
    try:
        tweets = client.search_recent_tweets(query=SEARCH_QUERY, max_results=MAX_LIKES_PER_DAY)
    except Exception as e:
        print(f"Помилка при пошуку постів: {e}")
        return
    
    if not tweets.data:
        print("Не знайдено постів за запитом.")
        return
    
    # Лайкання постів
    for tweet in tweets.data:
        if tweet.id not in liked_tweets:
            try:
                client.like(tweet.id)
                print(f"Лайкнуто пост: {tweet.id} - {tweet.text[:50]}...")
                liked_tweets.append(tweet.id)
                save_liked_tweets(tweet.id)
            except Exception as e:
                print(f"Помилка при лайканні поста {tweet.id}: {e}")
    
    print(f"Лайкнуто {len(tweets.data)} постів.")

if __name__ == "__main__":
    like_tweets()
