import requests
from newsapi import NewsApiClient

newsapi = NewsApiClient(api_key = NEWSAPI_KEY"")

all_articles = newsapi.get_everything(q = "OpenAI")

print(all_articles)

