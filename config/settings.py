import os
from dataclasses import dataclass
from dotenv import load_dotenv

load_dotenv()

@dataclass
class Config:
  BACKGROUND_COLOR: str = "#B1DDC6"
  CARD_FLIP_DELAY: int = 3000
  DATA_DIR: str = "languages"
  IMAGES_DIR: str = "images"

  # AI Configuration
  GEMINI_API_KEY: str = os.getenv("GEMINI_API_KEY", "")
  GEMINI_MODEL: str = "gemini-2.5-flash"
  PRELOAD_MIN_SENTENCES: int = 3
  SENTENCE_INTERVAL: int = 5
  WORD_BATCH_SIZE: int = 10
  SYSTEM_INSTRUCTIONS: str ="You are a bilingual sentence generator and translator. Your task is to generate natural, " \
  "grammatically correct sentences in both Finnish and English. " \
  "Each sentence must:Follow the standard grammar and syntax rules of both languages." \
  "Use appropriate verb forms, tenses, and word order." \
  "Be contextually relevant and culturally appropriate." \
  "Maintain the same meaning, tone, and nuance in both languages."
config = Config()