# -- PREREQUISITES
# pip install customtkinter

import customtkinter

def button_callback():
    print("button pressed")

app = customtkinter.CTk()
app.title("OpenAI Global Sentiment")
app.geometry("400x150")
app.grid_columnconfigure(0, weight = 1)

button = customtkinter.CTkButton(app, text = "Write csv", command = button_callback)
button.grid(row = 0, column = 0, padx = 20, pady = 20, sticky = "ew")

arabic = customtkinter.CTkCheckBox(app, text = "Arabic")
arabic.grid(row = 1, column = 0, padx = 20, pady = (0, 20), sticky = "w")
german = customtkinter.CTkCheckBox(app, text = "German")
german.grid(row = 1, column = 1, padx = 20, pady = (0, 20), sticky = "w")

app.mainloop()
