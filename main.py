import pandas as pd
import requests
from newsapi import NewsApiClient

# Extract data from NewsAPI
newsapi = NewsApiClient(api_key = NEWSAPI_KEY"")
all_articles = newsapi.get_everything(q = "OpenAI")

# Normalize data and put into DataFrame
df = pd.json_normalize(all_articles["articles"])
df = df.drop("urlToImage", axis = 1)
print(df.columns.tolist())
