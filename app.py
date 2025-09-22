from tkinter import *
import pandas as pd
import random
import os

BACKGROUND_COLOR = "#B1DDC6"


if os.path.exists("languages/words_to_learn.csv"):
  df = pd.read_csv("languages/words_to_learn.csv")
else:
  df = pd.read_csv("languages/fi-en-words.csv")

to_learn = df.to_dict(orient="records")
current_word = {}


def mark_as_known():
  """Move current_word to learned_words.csv and update words_to_learn.csv."""
  global to_learn, current_word

  if not current_word:
    return

  # remove from to_learn
  to_learn = [w for w in to_learn if w != current_word]
  pd.DataFrame(to_learn).to_csv("languages/words_to_learn.csv", index=False)

  # append to learned_words.csv
  learned_file = "languages/learned_words.csv"
  df_new = pd.DataFrame([current_word])
  if os.path.exists(learned_file):
    df_new.to_csv(learned_file, mode="a", header=False, index=False)
  else:
    df_new.to_csv(learned_file, index=False)

  print(f"You learned: {current_word['Finnish']} -> {current_word['English']}")
  next_word()


def next_word():
  """Show the next word from to_learn or finish if empty."""
  global current_word, flip_timer

  window.after_cancel(flip_timer)

  if not to_learn:
    canvas.itemconfig(card_title, text="Done!", fill="black")
    canvas.itemconfig(card_word, text="You learned all words 🎉", fill="black")
    canvas.itemconfig(card_background, image=card_front_img)
    return

  current_word = random.choice(to_learn)
  canvas.itemconfig(card_title, text="Finnish", fill="black")
  canvas.itemconfig(card_word, text=current_word["Finnish"], fill="black")
  canvas.itemconfig(card_background, image=card_front_img)

  flip_timer = window.after(3000, func=flip_card)


def flip_card():
  """Flip the card to show English translation."""
  canvas.itemconfig(card_title, text="English", fill="white")
  canvas.itemconfig(card_word, text=current_word["English"], fill="white")
  canvas.itemconfig(card_background, image=card_back_img)



window = Tk()
window.title("Learn new languages with Flashcards")
window.config(padx=50, pady=50, bg=BACKGROUND_COLOR)

flip_timer = window.after(3000, func=flip_card)

canvas = Canvas(width=800, height=526, bg=BACKGROUND_COLOR, highlightthickness=0)
card_front_img = PhotoImage(file="images/card_front.png")
card_back_img = PhotoImage(file="images/card_back.png")
card_background = canvas.create_image(400, 263, image=card_front_img)
card_title = canvas.create_text(400, 150, text="", font=("Ariel", 40, "italic"))
card_word = canvas.create_text(400, 263, text="", font=("Ariel", 60, "bold"))
canvas.grid(row=0, column=0, columnspan=2)


check_image = PhotoImage(file="images/right.png")
known_button = Button(image=check_image, highlightthickness=0, command=mark_as_known)
known_button.grid(row=1, column=0)

cross_image = PhotoImage(file="images/wrong.png")
unknown_button = Button(image=cross_image, highlightthickness=0, command=next_word)
unknown_button.grid(row=1, column=1)


next_word()
window.mainloop()