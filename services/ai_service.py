from urllib import response
from google import genai
from typing import Optional
from models.word import Word, WordManager
import os
import pandas as pd
from config.settings import config

SENTENCE_HISTORY_FILE = "languages/sentence_history.csv"

class AIService:
  def __init__(self):
    self.client = genai.Client(api_key=config.GEMINI_API_KEY)
    self.word_manager = WordManager()

  def should_generate_sentence(self) -> bool:
    return True

  def generate_sentence(self) -> Optional[Word]:
    words = self.word_manager.get_learned_words()
    if not words:
      return None

    finnish_words = [word.finnish for word in words]
    word_list_str = ", ".join(finnish_words)

    used_sentences = self._load_sentence_history()

    prompt = f"""
    Create a simple Finnish sentence using only words from this list (choose multiple words if possible):
    "{word_list_str}"
    - Do not repeat sentences you have already generated.
    - Use at least 2-3 different words if possible.
    - Keep sentences simple for language learners.
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
      text = response.text.strip()
      sentence = self._parse_response(text)
      # Skip if empty or already used
      if not sentence or sentence.finnish in used_sentences:
        return None
      self._save_sentence_history(sentence)
      return sentence
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

  def _load_sentence_history(self):
    if os.path.exists(SENTENCE_HISTORY_FILE):
      df = pd.read_csv(SENTENCE_HISTORY_FILE, on_bad_lines="skip")
      return set(df["Finnish"].tolist())
    return set()

  def _save_sentence_history(self, sentence: Word):
    df_new = pd.DataFrame([{"Finnish": sentence.finnish, "English": sentence.english}])
    if os.path.exists(SENTENCE_HISTORY_FILE):
      df_new.to_csv(SENTENCE_HISTORY_FILE, mode="a", header=False, index=False)
    else:
      df_new.to_csv(SENTENCE_HISTORY_FILE, index=False)