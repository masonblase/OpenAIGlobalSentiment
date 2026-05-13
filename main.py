# -- PREREQUISITES --
# pip install deep_translator
# pip install newsapi-python
# pip install pandas
# pip install protobuf sentencepiece
# pip install requests
# pip install sentencepiece
# pip install torch
# pip install transformers

from ast import literal_eval
from deep_translator import (GoogleTranslator)
from newsapi import NewsApiClient
import numpy as np
import pandas as pd
import requests
from transformers import AutoTokenizer, AutoModelForSequenceClassification, pipeline

# -- FUNCTIONS --
def safe_parse(val):
    if isinstance(val, dict):
        return val
    if isinstance(val, str):
        return literal_eval(val)
    return val
def translate_column(df, column, target_lang = "en", source_lang = "auto"):
    translator = GoogleTranslator(source = source_lang, target = target_lang)
    
    texts = df[column].fillna("").astype(str).tolist()
    translated = translator.translate_batch(texts)

    df[f"translated_{column}"] = translated
    return df

# Extract data from NewsAPI
newsapi = NewsApiClient(api_key = NEWSAPI_KEY"")
all_articles = newsapi.get_everything(q = "OpenAI")

# Normalize data and clean data
df = pd.json_normalize(all_articles["articles"])
df = df.drop("urlToImage", axis = 1)

# Translate content and store in a column
df["content"] = df["content"].str[:5000]
df = translate_column(df, column = "content", target_lang = "en")

# Get sentiment and store in a column
sentiment_score = pipeline(
    "sentiment-analysis",
    model = "cardiffnlp/twitter-xlm-roberta-base-sentiment",
    tokenizer = AutoTokenizer.from_pretrained(
        "cardiffnlp/twitter-xlm-roberta-base-sentiment",
        use_fast = False
    )
)

clean_texts = df["translated_content"].dropna().astype(str).tolist()
df["sentiment_placeholder"] = sentiment_score(clean_texts, batch_size = 32)
df = df.join( # Normalize sentiment data
    pd.json_normalize(df["sentiment_placeholder"].map(safe_parse))
).drop("sentiment_placeholder", axis = 1)

conditions = [
    (df["label"] == "negative"),
    (df["label"] == "neutral"),
    (df["label"] == "positive")
]
values = [-1, 0, 1]
df["sentiment_score"] = np.select(conditions, values)
print(df["sentiment_score"])