#!/usr/bin/env python3
# file: semantic_translator_openai.py

import os
import sys
import openai

# מפתח API מהסביבה (הגדר עם export OPENAI_API_KEY=your-key)
openai.api_key = os.getenv("OPENAI_API_KEY")

def detect_language(text: str) -> str:
    return "he" if any("\u0590" <= c <= "\u05EA" for c in text) else "en"

def create_prompt(phrase: str, source_lang: str) -> str:
    target_lang = "עברית" if source_lang == "en" else "English"
    return (
        f"Translate the following {source_lang.upper()} word or phrase to {target_lang} "
        f"by finding the closest word with the same meaning or intention, not necessarily literal:\n"
        f"{phrase}"
    )

def semantic_translate_openai(phrase: str) -> str:
    source_lang = detect_language(phrase)
    prompt = create_prompt(phrase, source_lang)

    response = openai.ChatCompletion.create(
        model="gpt-4",  # או "gpt-3.5-turbo" אם אתה רוצה לחסוך בעלויות
        messages=[
            {"role": "system", "content": "You are a semantic translator that translates by understanding intent, not word-for-word."},
            {"role": "user", "content": prompt}
        ],
        temperature=0.3,
        max_tokens=60
    )

    return response.choices[0].message.content.strip()

def main():
    if len(sys.argv) < 2:
        print("Usage: python semantic_translator_openai.py <word or phrase>")
        sys.exit(1)

    phrase = " ".join(sys.argv[1:])
    translation = semantic_translate_openai(phrase)
    print(f"\n🧠 Semantic Translation:\n{translation}")

if __name__ == "__main__":
    main()
