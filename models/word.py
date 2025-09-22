from dataclasses import dataclass
from typing import List
import pandas as pd
import os

@dataclass
class Word:
  finnish: str
  english: str

class WordManager:
  def __init__(self, data_dir: str = "languages"):
    self.data_dir = data_dir
    self.to_learn_file = f"{data_dir}/words_to_learn.csv"
    self.learned_file = f"{data_dir}/learned_words.csv"
    self.source_file = f"{data_dir}/fi-en-words.csv"
  
  def load_words_to_learn(self) -> List[Word]:
    if os.path.exists(self.to_learn_file):
      df = pd.read_csv(self.to_learn_file)
    else:
      df = pd.read_csv(self.source_file)
    
    return [Word(row['Finnish'], row['English']) for _, row in df.iterrows()]
  
  def mark_word_as_learned(self, word: Word) -> None:
    # Remove from to_learn
    df_to_learn = pd.read_csv(self.to_learn_file)
    df_to_learn = df_to_learn[
      ~((df_to_learn['Finnish'] == word.finnish) & 
        (df_to_learn['English'] == word.english))
    ]
    df_to_learn.to_csv(self.to_learn_file, index=False)
    
    # Add to learned
    new_word_df = pd.DataFrame([{'Finnish': word.finnish, 'English': word.english}])
    if os.path.exists(self.learned_file):
      new_word_df.to_csv(self.learned_file, mode="a", header=False, index=False)
    else:
      new_word_df.to_csv(self.learned_file, index=False)

  def get_learned_words(self) -> List[Word]:
    if not os.path.exists(self.learned_file):
      return []
    df = pd.read_csv(self.learned_file)
    return [Word(row['Finnish'], row['English']) for _, row in df.iterrows()]