from tkinter import *
from typing import Callable, Optional
from models.word import Word
from config.settings import config

class FlashcardUI:
  def __init__(self, master: Frame, on_known: Callable, on_unknown: Callable, on_back: Callable):
    self.on_known = on_known
    self.on_unknown = on_unknown
    self.on_back = on_back
    self.current_word: Optional[Word] = None
    self.flip_timer = None
    
    self.root = master.winfo_toplevel()
    self.frame = Frame(master, bg=config.BACKGROUND_COLOR)
    self.canvas = None
    self.card_front_img = None
    self.card_back_img = None
    self.check_image = None
    self.cross_image = None
    self.card_background = None
    self.card_title = None
    self.card_word = None
    self._build()
  
  def _build(self):
    # Canvas setup
    self.canvas = Canvas(self.frame, width=800, height=526, bg=config.BACKGROUND_COLOR, highlightthickness=0)
    self.card_front_img = PhotoImage(file="images/card_front.png")
    self.card_back_img = PhotoImage(file="images/card_back.png")
    
    self.card_background = self.canvas.create_image(400, 263, image=self.card_front_img)
    self.card_title = self.canvas.create_text(400, 150, text="", font=("Arial", 40, "italic"))
    self.card_word = self.canvas.create_text(400, 263, text="", font=("Arial", 60, "bold"))
    self.canvas.grid(row=0, column=0, columnspan=2)
    
    # Store button images as instance variables to prevent garbage collection
    self.check_image = PhotoImage(file="images/right.png")
    self.cross_image = PhotoImage(file="images/wrong.png")
    
    # Buttons
    self.known_button = Button(self.frame, image=self.check_image, highlightthickness=0, command=self.on_known)
    self.known_button.grid(row=1, column=0)
    
    self.unknown_button = Button(self.frame, image=self.cross_image, highlightthickness=0, command=self.on_unknown)
    self.unknown_button.grid(row=1, column=1)
    
  def _on_back_pressed(self):
  # Cancel pending flip to avoid callbacks after navigation
    if self.flip_timer:
      self.root.after_cancel(self.flip_timer)
      self.flip_timer = None
    self.on_back()
  
  def show_word(self, word: Word):
    self.current_word = word
    if self.flip_timer:
      self.root.after_cancel(self.flip_timer)
    
    # Set title based on whether it's a sentence or word
    if getattr(word, 'is_sentence', False):
      self.canvas.itemconfig(self.card_title, text="Practice Sentence", fill="black")
    else:
      self.canvas.itemconfig(self.card_title, text="Finnish", fill="black")
    
    self._configure_card_text(word.finnish, "black")
    self.canvas.itemconfig(self.card_background, image=self.card_front_img)
    
    self.flip_timer = self.root.after(3000, self.flip_card)
  
  def flip_card(self):
    if self.current_word:
      # Set title based on whether it's a sentence or word
      if getattr(self.current_word, 'is_sentence', False):
        self.canvas.itemconfig(self.card_title, text="Translation", fill="white")
      else:
        self.canvas.itemconfig(self.card_title, text="English", fill="white")
      
      self._configure_card_text(self.current_word.english, "white")
      self.canvas.itemconfig(self.card_background, image=self.card_back_img)
      
  def _configure_card_text(self, text, color):
    """Configure card text with appropriate font size and wrapping."""
    max_width = 650
    font_family = "Arial"
    
    is_long_text = getattr(self.current_word, 'is_sentence', False) or len(text) > 25
    
    if is_long_text:
      # Smaller font and line wrapping for sentences
      font_size = 35
      
      # Simple text wrapping algorithm
      words = text.split()
      lines = []
      current_line = ""
      chars_per_line = max_width // (font_size * 0.55)
      
      for word in words:
        test_line = current_line + (" " if current_line else "") + word
        if len(test_line) > chars_per_line and current_line:
          lines.append(current_line)
          current_line = word
        else:
          current_line = test_line
      
      if current_line:
        lines.append(current_line)
      
      # Adjust font size based on number of lines
      if len(lines) > 5:
        font_size = 25
      elif len(lines) > 4:
        font_size = 28
      elif len(lines) > 3:
        font_size = 32
      
      # Limit maximum lines to 6
      if len(lines) > 6:
        lines = lines[:6]
        if not lines[-1].endswith("..."):
          lines[-1] = lines[-1] + "..."
      
      wrapped_text = "\n".join(lines)
      
      # Move text up slightly if there are many lines
      y_offset = 0
      if len(lines) > 3:
        y_offset = -10
      elif len(lines) > 2:
        y_offset = -5
      
      self.canvas.coords(self.card_word, 400, 263 + y_offset)
      self.canvas.itemconfig(self.card_word, text=wrapped_text, fill=color,
                             font=(font_family, font_size, "bold"))
    else:
      # Dynamic font size for simple words
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
      
      # Reset position for single-line text
      self.canvas.coords(self.card_word, 400, 263)
      self.canvas.itemconfig(self.card_word, text=text, fill=color,
                             font=(font_family, font_size, "bold"))
  
  # Screen control
  def show(self):
    self.frame.grid(row=0, column=0, sticky="nsew")

  def hide(self):
    self.frame.grid_remove()