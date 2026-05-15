import customtkinter as ctk

# -- UI CODE --
def openaiglobalsentiment_ui(app, get_newsapi_data):
    app.title("OpenAI Global Sentiment")
    app.geometry("400x150")
    app.grid_columnconfigure(0, weight = 1)

    # Supported languages
    languages = {
    "Arabic": "ar",
    "German": "de",
    "English": "en",
    "French": "fr",
    "Hebrew": "he",
    "Italian": "it",
    "Dutch": "nl",
    "Norwegian": "no",
    "Portuguese": "pt",
    "Russian": "ru",
    "Swedish": "sv",
    "Chinese": "zh",
    }

    # Dropdown menu
    language_combobox = ctk.CTkComboBox(app, values = list(languages.keys()))
    language_combobox.grid(row = 0, column = 1, padx = 20, pady = 20, sticky = "w")

    # Write csv button
    button = ctk.CTkButton(app, text = "Write csv", command = lambda: get_newsapi_data(languages, language_combobox))
    button.grid(row = 0, column = 0, padx = 20, pady = 20, sticky = "ew")