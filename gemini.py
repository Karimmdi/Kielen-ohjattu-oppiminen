import os
import pandas as pd
from google import genai
from dotenv import load_dotenv

load_dotenv()

client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])
MODEL_NAME = "gemini-2.5-flash"
SENTENCE_HISTORY_FILE = "languages/sentence_history.csv"


def get_learned_words(n=10):
    """Return the last n learned words."""
    try:
        df = pd.read_csv("languages/learned_words.csv", on_bad_lines="skip")
        df = df[["Finnish", "English"]]
        return df.tail(n).to_dict(orient="records")
    except FileNotFoundError:
        return []


def load_sentence_history():
    """Load previously generated Finnish sentences to avoid duplicates."""
    if os.path.exists(SENTENCE_HISTORY_FILE):
        df = pd.read_csv(SENTENCE_HISTORY_FILE, on_bad_lines="skip")
        return set(df["Finnish"].tolist())
    return set()


def save_sentence_history(sentence):
    """Append a new sentence to history file."""
    df_new = pd.DataFrame([{"Finnish": sentence["Finnish"], "English": sentence["English"]}])
    if os.path.exists(SENTENCE_HISTORY_FILE):
        df_new.to_csv(SENTENCE_HISTORY_FILE, mode="a", header=False, index=False)
    else:
        df_new.to_csv(SENTENCE_HISTORY_FILE, index=False)


def generate_sentence():
    """Generate a simple Finnish sentence using recent words without repeating previous sentences."""
    words = get_learned_words(n=10)
    if not words:
        return None

    finnish_words = [w["Finnish"] for w in words]
    word_list_str = ", ".join(finnish_words)

    used_sentences = load_sentence_history()

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
        response = client.models.generate_content(
            model=MODEL_NAME,
            contents=[
                genai.types.Content(
                    role="user",
                    parts=[genai.types.Part(text=prompt)]
                )
            ]
        )
        text = response.text.strip()
        lines = text.splitlines()
        sentence = {}
        for line in lines:
            if line.startswith("Finnish:"):
                sentence["Finnish"] = line.replace("Finnish:", "").strip()
            elif line.startswith("English:"):
                sentence["English"] = line.replace("English:", "").strip()

        # Skip if empty or already used
        if not sentence or "Finnish" not in sentence or "English" not in sentence:
            return None
        if sentence["Finnish"] in used_sentences:
            return None

        save_sentence_history(sentence)
        return sentence
    except Exception as e:
        print(f"Gemini API error: {e}")
        return None


if __name__ == "__main__":
    s = generate_sentence()
    if s:
        print(s)