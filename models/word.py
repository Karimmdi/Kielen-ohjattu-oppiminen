from dataclasses import dataclass
from typing import List
import pandas as pd
import os

@dataclass
class Word:
  finnish: str
  english: str
  is_sentence: bool = False

  def __eq__(self, other):
    if isinstance(other, Word):
      return self.finnish == other.finnish and self.english == other.english
    return False

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
      # Fallback: copy master file to create words_to_learn.csv
      df = pd.read_csv(self.source_file)
      # Create the words_to_learn.csv file for future use
      df.to_csv(self.to_learn_file, index=False)
      print(f"Created {self.to_learn_file} from master dataset")

    return [Word(row['Finnish'], row['English']) for _, row in df.iterrows()]

  def mark_word_as_learned(self, word: Word) -> None:
    # Don't mark sentences as learned
    if word.is_sentence:
      return

    # Remove from to_learn
    if os.path.exists(self.to_learn_file):
      df_to_learn = pd.read_csv(self.to_learn_file)
      df_to_learn = df_to_learn[
        ~((df_to_learn['Finnish'] == word.finnish) &
          (df_to_learn['English'] == word.english))
      ]
      df_to_learn.to_csv(self.to_learn_file, index=False)

    # Add to learned
    clean_word = {"Finnish": word.finnish, "English": word.english}
    new_word_df = pd.DataFrame([clean_word])
    if os.path.exists(self.learned_file):
      new_word_df.to_csv(self.learned_file, mode="a", header=False, index=False)
    else:
      new_word_df.to_csv(self.learned_file, index=False)

  def get_learned_words(self, n: int = None) -> List[Word]:
    if not os.path.exists(self.learned_file):
      return []
    df = pd.read_csv(self.learned_file)
    if n is not None:
      df = df.tail(n)
    return [Word(row['Finnish'], row['English']) for _, row in df.iterrows()]