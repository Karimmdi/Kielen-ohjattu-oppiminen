from tkinter import *
from typing import Callable, Optional
from models.word import Word

class FlashcardUI:
  def __init__(self, on_known: Callable, on_unknown: Callable):
    self.on_known = on_known
    self.on_unknown = on_unknown
    self.current_word: Optional[Word] = None
    self.flip_timer = None
    self._setup_ui()
  
  def _setup_ui(self):
    self.window = Tk()
    self.window.title("Learn new languages with Flashcards")
    self.window.config(padx=50, pady=50, bg="#B1DDC6")
    
    # Canvas setup
    self.canvas = Canvas(width=800, height=526, bg="#B1DDC6", highlightthickness=0)
    self.card_front_img = PhotoImage(file="images/card_front.png")
    self.card_back_img = PhotoImage(file="images/card_back.png")
    
    self.card_background = self.canvas.create_image(400, 263, image=self.card_front_img)
    self.card_title = self.canvas.create_text(400, 150, text="", font=("Arial", 40, "italic"))
    self.card_word = self.canvas.create_text(400, 263, text="", font=("Arial", 60, "bold"))
    self.canvas.grid(row=0, column=0, columnspan=2)
    
    # Buttons
    check_image = PhotoImage(file="images/right.png")
    self.known_button = Button(image=check_image, highlightthickness=0, command=self.on_known)
    self.known_button.grid(row=1, column=0)
    
    cross_image = PhotoImage(file="images/wrong.png")
    self.unknown_button = Button(image=cross_image, highlightthickness=0, command=self.on_unknown)
    self.unknown_button.grid(row=1, column=1)
  
  def show_word(self, word: Word):
    self.current_word = word
    if self.flip_timer:
      self.window.after_cancel(self.flip_timer)
    
    self.canvas.itemconfig(self.card_title, text="Finnish", fill="black")
    self.canvas.itemconfig(self.card_word, text=word.finnish, fill="black")
    self.canvas.itemconfig(self.card_background, image=self.card_front_img)
    
    self.flip_timer = self.window.after(3000, self.flip_card)
  
  def flip_card(self):
    if self.current_word:
      self.canvas.itemconfig(self.card_title, text="English", fill="white")
      self.canvas.itemconfig(self.card_word, text=self.current_word.english, fill="white")
      self.canvas.itemconfig(self.card_background, image=self.card_back_img)

  def show_completion(self):
    if self.flip_timer:
      self.window.after_cancel(self.flip_timer)
    self.canvas.itemconfig(self.card_title, text="Done!", fill="black")
    self.canvas.itemconfig(self.card_word, text="You learned all words 🎉", fill="black")
    self.canvas.itemconfig(self.card_background, image=self.card_front_img)
  
  def run(self):
    self.window.mainloop()