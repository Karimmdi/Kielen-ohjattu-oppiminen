from google import genai
import random
import os
from models.word import Word, WordManager
from config.settings import config

class AIService:
  def __init__(self):
    self.client = genai.Client(api_key=config.GEMINI_API_KEY)
    self.word_manager = WordManager()
  
  def should_generate_sentence(self) -> bool:
    learned = self.word_manager.get_learned_words()
    return len(learned) % config.SENTENCE_GENERATION_INTERVAL == 0 and len(learned) > 0
  
  def generate_sentence(self) -> Optional[Word]:
    words = self.word_manager.get_learned_words()
    if not words:
      return None
    
    finnish_words = [word.finnish for word in words]
    word_list_str = ", ".join(finnish_words)
    
    prompt = f"""
    Create a simple Finnish sentence using only from this list: "{word_list_str}".
    Then provide the English translation.
    Format the output as:
    Finnish: <sentence>
    English: <translation>
    """
    
    try:
      response = self.client.models.generate_content(
        model=config.GEMINI_MODEL,
        contents=[genai.types.Content(
          role="user",
          parts=[genai.types.Part(text=prompt)]
        )]
      )
      
      return self._parse_response(response.text.strip())
    except Exception as e:
      print(f"Error generating sentence: {e}")
      return None
  
  def _parse_response(self, text: str) -> Optional[Word]:
    finnish = ""
    english = ""
    
    for line in text.splitlines():
      if line.startswith("Finnish:"):
        finnish = line.replace("Finnish:", "").strip()
      elif line.startswith("English:"):
        english = line.replace("English:", "").strip()
    
    if finnish and english:
      return Word(finnish, english)
    return None