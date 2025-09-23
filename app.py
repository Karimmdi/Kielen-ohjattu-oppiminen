import threading
import queue
from tkinter import *
import pandas as pd
import random
import os
from gemini import generate_sentence

BACKGROUND_COLOR = "#B1DDC6"
SENTENCE_INTERVAL = 5  # joka 5 sanaa näytetään yksi lause
PRELOAD_MIN_SENTENCES = 3  # pidetään aina vähintään 3 lausetta valmiina


if os.path.exists("languages/words_to_learn.csv"):
    df = pd.read_csv("languages/words_to_learn.csv")
else:
    df = pd.read_csv("languages/fi-en-words.csv")

to_learn = df.to_dict(orient="records")
current_word = {}
word_counter = 0
sentence_queue = queue.Queue()


# --- Lausen generatori taustalla ---
def sentence_worker():
    """Continuously generate sentences while keeping queue filled."""
    while True:
        try:
            if sentence_queue.qsize() < PRELOAD_MIN_SENTENCES:
                sentence = generate_sentence()
                if sentence:
                    sentence["is_sentence"] = True
                    sentence_queue.put(sentence)
        except Exception as e:
            print(f"Sentence generation failed: {e}")



def mark_as_known():
    global to_learn, current_word

    if not current_word or current_word.get("is_sentence"):
        next_word()
        return

    to_learn = [w for w in to_learn if w != current_word]
    pd.DataFrame(to_learn).to_csv("languages/words_to_learn.csv", index=False)


    clean_word = {"Finnish": current_word["Finnish"], "English": current_word["English"]}
    df_new = pd.DataFrame([clean_word])
    learned_file = "languages/learned_words.csv"
    if os.path.exists(learned_file):
        df_new.to_csv(learned_file, mode="a", header=False, index=False)
    else:
        df_new.to_csv(learned_file, index=False)

    print(f"You learned: {current_word['Finnish']} -> {current_word['English']}")
    next_word()


def next_word():
    global current_word, flip_timer, word_counter

    window.after_cancel(flip_timer)

    if not to_learn and sentence_queue.empty():
        canvas.itemconfig(card_title, text="Done!", fill="black")
        canvas.itemconfig(card_word, text="You learned all words!", fill="black")
        canvas.itemconfig(card_background, image=card_front_img)
        return


    if word_counter >= SENTENCE_INTERVAL and not sentence_queue.empty():
        current_word = sentence_queue.get()
        word_counter = 0
    else:
        if to_learn:
            current_word = random.choice(to_learn)
            current_word["is_sentence"] = False
            word_counter += 1
        elif not sentence_queue.empty():
            current_word = sentence_queue.get()
            current_word["is_sentence"] = True
        else:
            canvas.itemconfig(card_title, text="Done!", fill="black")
            canvas.itemconfig(card_word, text="You learned all words 🎉", fill="black")
            canvas.itemconfig(card_background, image=card_front_img)
            return

    if current_word.get("is_sentence"):
        canvas.itemconfig(card_title, text="Practice Sentence", fill="black")
    else:
        canvas.itemconfig(card_title, text="Finnish", fill="black")


    configure_card_text(current_word["Finnish"], "black")
    canvas.itemconfig(card_background, image=card_front_img)

    flip_timer = window.after(3000, func=flip_card)


def flip_card():
    if current_word.get("is_sentence"):
        canvas.itemconfig(card_title, text="Translation", fill="white")
    else:
        canvas.itemconfig(card_title, text="English", fill="white")

    # saadaan englanninkielinen teksti
    english_text = current_word["English"]

    # konfataan teksti sopivaksi
    configure_card_text(english_text, "white")

    canvas.itemconfig(card_background, image=card_back_img)


def configure_card_text(text, color):
    """Configure card text with appropriate font size and wrapping."""
    # kordinaatit ja fontin koko
    max_width = 650  # pikseliä

    font_family = "Arial"

    is_long_text = current_word.get("is_sentence") or len(text) > 25

    if is_long_text:
        # lauselle pienempi fontti ja rivitys
        font_size = 35

        # yksinkertainen tekstin rivitysalgoritmi
        words = text.split()
        lines = []
        current_line = ""
        chars_per_line = max_width // (font_size * 0.55)

        for word in words:
            # tarkista, ylittääkö rivin leveyden
            test_line = current_line + (" " if current_line else "") + word
            if len(test_line) > chars_per_line and current_line:
                lines.append(current_line)
                current_line = word
            else:
                current_line = test_line

        if current_line:
            lines.append(current_line)

        # Säädä fontin kokoa rivien määrän mukaan
        if len(lines) > 5:
            font_size = 25
        elif len(lines) > 4:
            font_size = 28
        elif len(lines) > 3:
            font_size = 32

        # Rajoita rivien määrä maksimissaan 6
        if len(lines) > 6:
            lines = lines[:6]
            if not lines[-1].endswith("..."):
                lines[-1] = lines[-1] + "..."

        wrapped_text = "\n".join(lines)

        # siirrä tekstiä hieman ylöspäin, jos rivejä on paljon
        y_offset = 0
        if len(lines) > 3:
            y_offset = -10
        elif len(lines) > 2:
            y_offset = -5

        # Aseta teksti ja sijainti
        canvas.coords(card_word, 400, 263 + y_offset)
        canvas.itemconfig(card_word, text=wrapped_text, fill=color,
                         font=(font_family, font_size, "bold"))

    else:
        # yksinkertaiset sanat tai lyhyet lauseet - dynaaminen fontin koko
        text_length = len(text)

        if text_length > 20:
            font_size = 35
        elif text_length > 15:
            font_size = 45
        elif text_length > 12:
            font_size = 50
        elif text_length > 8:
            font_size = 55
        else:
            font_size = 60

        # nollaa sijainti yksiriviselle tekstille
        canvas.coords(card_word, 400, 263)
        canvas.itemconfig(card_word, text=text, fill=color,
                         font=(font_family, font_size, "bold"))



window = Tk()
window.title("Learn new languages with Flashcards")
window.config(padx=50, pady=50, bg=BACKGROUND_COLOR)

flip_timer = window.after(3000, func=flip_card)

canvas = Canvas(width=800, height=526, bg=BACKGROUND_COLOR, highlightthickness=0)
card_front_img = PhotoImage(file="images/card_front.png")
card_back_img = PhotoImage(file="images/card_back.png")
card_background = canvas.create_image(400, 263, image=card_front_img)
card_title = canvas.create_text(400, 150, text="", font=("Arial", 40, "italic"))
card_word = canvas.create_text(400, 263, text="", font=("Arial", 60, "bold"), width=650)
canvas.grid(row=0, column=0, columnspan=2)

check_image = PhotoImage(file="images/right.png")
known_button = Button(image=check_image, highlightthickness=0, command=mark_as_known)
known_button.grid(row=1, column=0)

cross_image = PhotoImage(file="images/wrong.png")
unknown_button = Button(image=cross_image, highlightthickness=0, command=next_word)
unknown_button.grid(row=1, column=1)

threading.Thread(target=sentence_worker, daemon=True).start()

next_word()
window.mainloop()

