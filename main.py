from tkinter import *
import random
import pandas as pd

BACKGROUND_COLOR = "#B1DDC6"

window = Tk()
window.title("FLASH CARDS")
window.config(padx=50, pady=50, bg=BACKGROUND_COLOR)

flip_timer = None  # ⏱️ Variable global para guardar el timer actual

def get_random_word():
    global flip_timer

    if flip_timer is not None:
        window.after_cancel(flip_timer)

    data = pd.read_csv("data/french_words.csv")
    words_dictionary = data.to_dict(orient="records")
    random_index = random.randint(0, len(words_dictionary) - 1)  # Incluye el 0 para que pueda elegir toda la lista
    random_row = words_dictionary[random_index]

    french_word = random_row["French"]
    english_word = random_row["English"]
    print(f"FR: {french_word} -> EN: {english_word}")

    ui2.itemconfig(title_text, text="French:", fill="black")
    ui2.itemconfig(word_text, text=f"{french_word}", fill="black")
    ui2.itemconfig(card_image, image=front_img)

    flip_timer = window.after(3000, lambda: flip_card(english_word))

    return random_row

def flip_card(english):
    ui2.itemconfig(title_text, text="English:", fill="white")
    ui2.itemconfig(word_text, text=f"{english}", fill="white")
    ui2.itemconfig(card_image, image=back_img)

def add_to_learn(random_row):
    try:
        df = pd.read_csv("words_to_learn.csv")
    except FileNotFoundError:
        print("Archivo no encontrado. Creando uno nuevo...")
        df = pd.DataFrame(columns=["French", "English"])
        df.to_csv("words_to_learn.csv", index=False)

    # Comprobamos si la fila ya está en el DataFrame
    if not ((df["French"] == random_row["French"]) & (df["English"] == random_row["English"])).any():
        # Creamos un DataFrame temporal con la nueva fila
        new_row_df = pd.DataFrame([random_row])
        # Concatenamos el DataFrame original con el nuevo
        df = pd.concat([df, new_row_df], ignore_index=True)
        df.to_csv("words_to_learn.csv", index=False)
        print("Palabra añadida al archivo.")
    else:
        print("La palabra ya existe en el archivo.")

    return df

# ──────────────────────────── UI SETUP ───────────────────────────── #

back_img = PhotoImage(file="images/card_back.png")
front_img = PhotoImage(file="images/card_front.png")

ui2 = Canvas(width=800, height=526, highlightthickness=0)
card_image = ui2.create_image(400, 263, image=front_img)
title_text = ui2.create_text(400, 150, text="Title:", font=("Ariel", 40, "italic"))
word_text = ui2.create_text(400, 263, text="", font=("Ariel", 40, "bold"))
ui2.config(bg=BACKGROUND_COLOR)
ui2.grid(column=0, row=0, columnspan=2)

# ──────────────────────────── BOTONES ───────────────────────────── #

right_image = PhotoImage(file="images/right.png")
right_button = Button(image=right_image, highlightthickness=0, command=get_random_word)
right_button.grid(column=1, row=1)

wrong_image = PhotoImage(file="images/wrong.png")
wrong_button = Button(image=wrong_image, highlightthickness=0,
                      command=lambda: add_to_learn(get_random_word()))
wrong_button.grid(column=0, row=1)

# ──────────────────────────── INICIO ───────────────────────────── #

get_random_word()
window.mainloop()
