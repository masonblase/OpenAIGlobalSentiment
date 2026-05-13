# -- PREREQUISITES --
# pip install deep_translator
# pip install newsapi-python
# pip install pandas
# pip install requests

from deep_translator import (GoogleTranslator)
from newsapi import NewsApiClient
import pandas as pd
import requests

# -- FUNCTIONS --
def translate_column(df, column, target_lang = "en", source_lang = "auto"):
    translator = GoogleTranslator(source = source_lang, target = target_lang)
    
    texts = df[column].fillna("").astype(str).tolist()
    translated = translator.translate_batch(texts)

    df[f"translated_{column}"] = translated
    return df

# Extract data from NewsAPI
newsapi = NewsApiClient(api_key = NEWSAPI_KEY"")
all_articles = newsapi.get_everything(q = "OpenAI", language="fr")

# Normalize data and clean data
df = pd.json_normalize(all_articles["articles"])
df = df.drop("urlToImage", axis = 1)

# Translate content
df["content"] = df["content"].str[:5000]
df = translate_column(df, column = "content", target_lang = "en")
print(df)
