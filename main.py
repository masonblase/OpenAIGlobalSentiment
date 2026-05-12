# -- Prerequisites --
# pip install deep_translator
# pip install newsapi-python
# pip install pandas
# pip install requests

from deep_translator import (GoogleTranslator)
from newsapi import NewsApiClient
import pandas as pd
import requests

# Extract data from NewsAPI
newsapi = NewsApiClient(api_key = NEWSAPI_KEY"")
all_articles = newsapi.get_everything(q = "OpenAI")

# Normalize data and clean data
df = pd.json_normalize(all_articles["articles"])
df = df.drop("urlToImage", axis = 1)

# Translate content
df["content"] = df["content"].str[:5000]
df["content"] = GoogleTranslator(source = "auto", target = "en").translate(text = df["content"]) 
print(df["content"])
