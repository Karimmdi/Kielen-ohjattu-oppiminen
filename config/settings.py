import os
from dataclasses import dataclass
from dotenv import load_dotenv

load_dotenv()

@dataclass
class Config:
  # UI Confihuration
  APP_WIDTH = 800
  APP_HEIGHT = 636
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
  SYSTEM_INSCTRUCTIONS="You are a sentence generator and a translator. Your job is to generate accurate sentences that has both Finnish and English equivalents."

config = Config()