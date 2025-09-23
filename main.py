clean_words = []
import random
from models.word import WordManager, Word
from ui.flashcard_ui import FlashcardUI
from services.ai_service import AIService

class FlashcardApp:
  def __init__(self):
    self.word_manager = WordManager()
    self.ai_service = AIService()
    self.words_to_learn = self.word_manager.load_words_to_learn()
    self.ui = FlashcardUI(self.mark_as_known, self.mark_as_unknown)
  
  def mark_as_known(self):
    """When right button is pressed."""
    if not self.ui.current_word:
      return
    
    # Don't mark sentences as learned, just go to next word
    if self.ui.current_word.is_sentence:
      self.next_word()
      return
    
    self.word_manager.mark_word_as_learned(self.ui.current_word)
    self.words_to_learn = [w for w in self.words_to_learn if w != self.ui.current_word]
    
    print(f"You learned: {self.ui.current_word.finnish} -> {self.ui.current_word.english}")
    self.next_word()
    
  def mark_as_unknown(self):
    """When wrong button is pressed - just go to next word without learning"""
    self.next_word()
  
  def next_word(self):
    if not self.words_to_learn and not self.ai_service.sentence_queue:
      self.ui.show_completion()
      return
    
    # Check if we should show a sentence
    if self.ai_service.should_generate_sentence():
      sentence_word = self.ai_service.get_sentence_if_available()
      if sentence_word:
        print(f"Practice sentence: {sentence_word.finnish} -> {sentence_word.english}")
        self.ui.show_word(sentence_word)
        return
    
    # Show regular word
    if self.words_to_learn:
      word = random.choice(self.words_to_learn)
      self.ui.show_word(word)
    else:
      self.ui.show_completion()
  
  def run(self):
    self.next_word()
    self.ui.run()

if __name__ == "__main__":
  app = FlashcardApp()
  app.run()