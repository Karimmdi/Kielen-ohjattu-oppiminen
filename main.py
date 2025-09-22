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
    self.ui = FlashcardUI(self.mark_as_known, self.next_word)
  
  def mark_as_known(self):
    if not self.ui.current_word:
      return
    
    self.word_manager.mark_word_as_learned(self.ui.current_word)
    self.words_to_learn = [w for w in self.words_to_learn if w != self.ui.current_word]
    
    # Check if we should generate a sentence
    if self.ai_service.should_generate_sentence():
      sentence_word = self.ai_service.generate_sentence()
      if sentence_word:
        print(f"Generated: {sentence_word.finnish} -> {sentence_word.english}")
    
    self.next_word()
  
  def next_word(self):
    if not self.words_to_learn:
      self.ui.show_completion()
      return
    
    word = random.choice(self.words_to_learn)
    self.ui.show_word(word)
  
  def run(self):
    self.next_word()
    self.ui.run()

if __name__ == "__main__":
  app = FlashcardApp()
  app.run()