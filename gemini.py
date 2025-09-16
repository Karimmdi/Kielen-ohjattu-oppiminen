from google import genai
import random
import os
from dotenv import load_dotenv
import pandas as pd

load_dotenv()


def get_learned_words():
    df = pd.read_csv("languages/learned_words.csv")
    return df.to_dict(orient="records")


def should_generate_sentence(n=5):
    learned = get_learned_words()
    return len(learned) % n == 0 and len(learned) > 0



client = genai.Client(api_key=os.environ["GEMINI_API_KEY"])
model="gemini-2.5-flash"



def generate_sentence():
    words = get_learned_words()
    print(f"learned words: {words}")

    #word = random.choice(words)  # pick one learned word

    finnish_words = [word['Finnish'] for word in words]
    word_list_str = ", ".join(finnish_words)

    prompt = f"""
    Create a simple Finnish sentence using only from this list but choose a word randomly:"{word_list_str}".
    Then provide the English translation.
    Format the output as:
    Finnish: <sentence>
    English: <translation>
    """

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=[
            genai.types.Content(
                role="user",
                parts=[genai.types.Part(text=prompt)]
            )
        ]
    )

    text = response.text.strip()
    finnish = ""
    english = ""

    for line in text.splitlines():
        if line.startswith("Finnish:"):
            finnish = line.replace("Finnish:", "").strip()
        elif line.startswith("English:"):
            english = line.replace("English:", "").strip()

    print(finnish, english)

    return {"Finnish": finnish, "English": english}


generate_sentence()