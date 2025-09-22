import os
from dataclasses import dataclass

@dataclass
class Config:
  BACKGROUND_COLOR: str = "#B1DDC6"
  CARD_FLIP_DELAY: int = 3000
  DATA_DIR: str = "languages"
  IMAGES_DIR: str = "images"
  SENTENCE_GENERATION_INTERVAL: int = 5
  
  # AI Configuration
  GEMINI_API_KEY: str = os.getenv("GEMINI_API_KEY", "")
  GEMINI_MODEL: str = "gemini-2.5-flash"

config = Config()