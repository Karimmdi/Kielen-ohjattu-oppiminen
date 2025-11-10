import random
from tkinter import *
from models.word import WordManager
from services.ai_service import AIService

from ui.flashcard_ui import FlashcardUI
from ui.main_menu_ui import MainMenuUI
from ui.words_ui import WordsUI
from ui.sentence_ui import SentencesUI

from config.settings import config

class FlashcardApp:
  def __init__(self):
    # Only one root window
    self.root = Tk()
    self.root.title("Learn new languages with Flashcards")
    self.root.configure(bg=config.BACKGROUND_COLOR, padx=50, pady=50)
    
    # Grid a home button in the top-left corner
    self.home_button = Button(self.root, text="🏠 Home", command=self.show_menu, font=("Arial", 12, "bold"),
                              bg=config.BACKGROUND_COLOR, fg="#444444", relief="flat",
                              activebackground="#E8E8E8", activeforeground="#000000")
    self.home_button.place(x=-35, y=-35) # Easy fix to move the button to the padding zone
    self.home_button.lift()   
    
    # Single container for stacked screens
    self.container = Frame(self.root, bg=config.BACKGROUND_COLOR)
    self.container.grid(row=0, column=0, sticky="nsew")
    
    # Do NOT resize the container for children
    self.container.config(width=config.APP_WIDTH, height=config.APP_HEIGHT)
    self.container.grid_propagate(False)
    
    self.root.grid_rowconfigure(0, weight=1)
    self.root.grid_columnconfigure(0, weight=1)
    
    # Services and state
    self.word_manager = WordManager()
    self.ai_service = AIService()
    self.words_to_learn = self.word_manager.load_words_to_learn()
    
    # Screens
    self.menu_screen = MainMenuUI(self.container, on_start_flashcards=self.show_flashcards, on_show_words=self.show_words, on_show_sentences=self.show_sentences)
    self.flashcard_screen = FlashcardUI(self.container, on_known=self.mark_as_known,
                                        on_unknown=self.mark_as_unknown, on_back=self.show_menu,)
    self.word_screen = WordsUI(self.container, word_manager=self.word_manager, on_back=self.show_menu)
    self.sentence_screen = SentencesUI(self.container, on_back=self.show_menu)
  
  # Navigation
  def show_menu(self):
    self.flashcard_screen.hide()
    self.word_screen.hide()
    self.sentence_screen.hide()
    self.menu_screen.show()
    self.home_button.lift()

  def show_flashcards(self):
    self.menu_screen.hide()
    self.word_screen.hide()
    self.sentence_screen.hide()
    self.flashcard_screen.show()
    self.home_button.lift()
    self.next_word()
    
  def show_words(self):
    self.menu_screen.hide()
    self.flashcard_screen.hide()
    self.sentence_screen.hide()
    self.word_screen.show()
    self.home_button.lift()
    
  def show_sentences(self):
    self.menu_screen.hide()
    self.flashcard_screen.hide()
    self.word_screen.hide()
    self.sentence_screen.show()
    self.home_button.lift()
    
  def mark_as_known(self):
    """When right button is pressed."""
    if not self.flashcard_screen.current_word:
      return
    
    # Don't mark sentences as learned, just go to next word
    if self.flashcard_screen.current_word.is_sentence:
      self.next_word()
      return
    
    self.word_manager.mark_word_as_learned(self.flashcard_screen.current_word)
    self.words_to_learn = [w for w in self.words_to_learn if w != self.flashcard_screen.current_word]
    
    print(f"You learned: {self.flashcard_screen.current_word.finnish} -> {self.flashcard_screen.current_word.english}")
    self.next_word()
    
  def mark_as_unknown(self):
    """When wrong button is pressed - just go to next word without learning"""
    self.next_word()
  
  def next_word(self):
    if not self.words_to_learn and self.ai_service.sentence_queue.empty():
      self.flashcard_screen.show_completion()
      return
    
    # Check if we should show a sentence
    if self.ai_service.should_generate_sentence():
      sentence_word = self.ai_service.get_sentence_if_available()
      if sentence_word:
        print(f"Practice sentence: {sentence_word.finnish} -> {sentence_word.english}")
        self.flashcard_screen.show_word(sentence_word)
        return
    
    # Show regular word
    if self.words_to_learn:
      word = random.choice(self.words_to_learn)
      self.flashcard_screen.show_word(word)
    else:
      self.flashcard_screen.show_completion()

  def run(self):
    # Start the app at the menu
    self.show_menu()
    self.root.mainloop()

if __name__ == "__main__":
  app = FlashcardApp().run()