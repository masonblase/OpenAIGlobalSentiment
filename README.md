# OpenAIGlobalSentiment
Program that obtains sentiment data about OpenAI from news articles written in a variety of languages. Upon termination, the data frame is exported into a csv file, which can be used for further analysis or in a preferred data visualization software.

Default language of articles is French. The source language can be changed by swapping the two-letter ISO-639-1 language code in the 'language' parameter of the newsapi.get_everything() function on line 37.

The supported languages and their respective codes are listed below:
Arabic - "ar"
German - "de"
English - "en"
French - "fr"
Hebrew - "he"
Italian - "it"
Dutch/Flemish - "nl"
Norwegian - "no"
Portuguese - "pt"
Russian - "ru"
Swedish - "sv"
Chinese - "zh"
