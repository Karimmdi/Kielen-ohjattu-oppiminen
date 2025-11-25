import threading
import queue
from google import genai
from google.genai import types
from typing import Optional
from models.word import Word, WordManager
import os
import pandas as pd
from config.settings import config
import time

SENTENCE_HISTORY_FILE = "languages/sentence_history.csv"


class AIService:
    def __init__(self):
        try:
            if not config.GEMINI_API_KEY:
                self.gemini_available = False
                print("GEMINI_API_KEY not found in environment variables")
                return

            self.client = genai.Client(api_key=config.GEMINI_API_KEY)
            self.gemini_available = True
            print("Gemini client initialized successfully")
        except Exception as e:
            self.gemini_available = False
            print(f"Error initializing Gemini: {e}")

        self.word_manager = WordManager()
        self.sentence_queue = queue.Queue()
        self.preload_min_sentences = config.PRELOAD_MIN_SENTENCES
        self.sentence_interval = config.SENTENCE_INTERVAL
        self.word_counter = 0
        self.word_batch_size = config.WORD_BATCH_SIZE

        if self.gemini_available:
            self._start_sentence_worker()

    def _start_sentence_worker(self):
        """Start background thread for sentence generation."""
        def sentence_worker():
            while True:
                try:
                    if self.sentence_queue.qsize() < self.preload_min_sentences:
                        sentence_word = self.generate_sentence()
                        if sentence_word:
                            sentence_word.is_sentence = True
                            self.sentence_queue.put(sentence_word)
                except Exception as e:
                    print(f"Sentence generation failed: {e}")
                time.sleep(2)

        thread = threading.Thread(target=sentence_worker, daemon=True)
        thread.start()

    def should_generate_sentence(self) -> bool:
        if not self.gemini_available:
            return False
        self.word_counter += 1
        return self.word_counter >= self.sentence_interval and not self.sentence_queue.empty()

    def get_sentence_if_available(self) -> Optional[Word]:
        if not self.sentence_queue.empty():
            self.word_counter = 0
            return self.sentence_queue.get()
        return None

    def generate_sentence(self) -> Optional[Word]:
        words = self.word_manager.get_learned_words(self.word_batch_size)
        if not words:
            print("No learned words available for sentence generation")
            return None

        finnish_words = [word.finnish for word in words]
        word_list_str = ", ".join(finnish_words)
        print(f"Using words for sentence: {word_list_str}")

        used_sentences = self._load_sentence_history()
        prompt = (
            f"Create a simple Finnish sentence using only words from this list:\n"
            f"{word_list_str}\n"
            "- Do not repeat sentences you have already generated.\n"
            "- Use at least 2-3 different words if possible.\n"
            "- Keep sentences simple for language learners.\n"
            "Then provide the English translation.\n"
            "Format:\nFinnish: <sentence>\nEnglish: <translation>"
        )

        try:
            response = self.client.models.generate_content(**self._build_payload(prompt))
            text = response.text.strip()
            sentence = self._parse_response(text)

            if not sentence or sentence.finnish in used_sentences:
                print("Generated sentence was empty or duplicate")
                return None

            self._save_sentence_history(sentence)
            print(f"Generated new sentence: {sentence.finnish} -> {sentence.english}")
            return sentence
        except Exception as e:
            print(f"Error generating sentence: {e}")
            return None

    def _build_payload(self, prompt: str) -> dict:
        return {
            "model": config.GEMINI_MODEL,
            "contents": [
                genai.types.Content(role="user", parts=[genai.types.Part(text=prompt)])
            ],
            "config": types.GenerateContentConfig(
                temperature=0.1,
                top_p=1.0,
                top_k=1,
                thinking_config=types.ThinkingConfig(thinking_budget=-1),
                system_instruction=config.SYSTEM_INSTRUCTIONS
            )
        }

    def _parse_response(self, text: str) -> Optional[Word]:
        finnish, english = "", ""
        for line in text.splitlines():
            if line.startswith("Finnish:"):
                finnish = line.replace("Finnish:", "").strip()
            elif line.startswith("English:"):
                english = line.replace("English:", "").strip()
        return Word(finnish, english) if finnish and english else None

    def _load_sentence_history(self) -> set:
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
            print(f"Saved sentence to {SENTENCE_HISTORY_FILE}")
