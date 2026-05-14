# -- PREREQUISITES
# pip install customtkinter
# pip install deep_translator
# pip install newsapi-python
# pip install pandas
# pip install protobuf sentencepiece
# pip install requests
# pip install sentencepiece
# pip install torch
# pip install transformers

from ast import literal_eval
import customtkinter as ctk
from deep_translator import (GoogleTranslator)
from newsapi import NewsApiClient
import numpy as np
import pandas as pd
import requests
from transformers import AutoTokenizer, AutoModelForSequenceClassification, pipeline

# -- HELPER FUNCTIONS --
def safe_parse(val):
    if isinstance(val, dict):
        return val
    if isinstance(val, str):
        return literal_eval(val)
    return val

# Translates "content" and puts into new column
def translate_column(df, column, target_lang = "en", source_lang = "auto"):
    translator = GoogleTranslator(source = source_lang, target = target_lang)
    
    texts = df[column].fillna("").astype(str).tolist()
    translated = translator.translate_batch(texts)

    df[f"translated_{column}"] = translated
    return df

# Extract and clean data from NewsAPI
def get_newsapi_data():
    newsapi = NewsApiClient(api_key = NEWSAPI_KEY"")
    language_select = language_combobox.get()
    all_articles = newsapi.get_everything(q = "OpenAI", language = language_select, sort_by = "relevancy")

    # Normalize and clean data
    df = pd.json_normalize(all_articles["articles"])
    df = df.drop(columns = ["urlToImage", "source.id", "source.name"], errors = "ignore")

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
    df.to_csv("openaisentiment.csv", sep = "\t", encoding = "utf-8", index = False, header = True)

# -- UI --
app = ctk.CTk()
app.title("OpenAI Global Sentiment")
app.geometry("400x150")
app.grid_columnconfigure(0, weight = 1)

languages = ["ar", "de", "en", "fr", "he", "it", "nl", "no", "pt", "ru", "sv", "zh"]
language_combobox = ctk.CTkComboBox(app, values = languages)
language_combobox.grid(row = 0, column = 1, padx = 20, pady = 20, sticky = "w")

button = ctk.CTkButton(app, text = "Write csv", command = get_newsapi_data)
button.grid(row = 0, column = 0, padx = 20, pady = 20, sticky = "ew")

app.mainloop()
