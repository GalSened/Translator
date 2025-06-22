#!/usr/bin/env python3
# file: semantic_translator.py

import sys
from sentence_transformers import SentenceTransformer, util

# מילון דוגמאות בעברית ואנגלית עם כוונה
semantic_dict = {
    "en": {
        "freedom": "חופש",
        "responsibility": "אחריות",
        "sad": "עצוב",
        "excited": "נרגש",
        "friend": "חבר",
    },
    "he": {
        "חופש": "freedom",
        "אחריות": "responsibility",
        "עצוב": "sad",
        "נרגש": "excited",
        "חבר": "friend",
    }
}

# טעינת מודל סמנטי
model = SentenceTransformer('distiluse-base-multilingual-cased-v1')

def detect_language(word: str) -> str:
    return "he" if any("\u0590" <= c <= "\u05EA" for c in word) else "en"

def semantic_translate(word: str) -> str:
    lang = detect_language(word)
    opposite_lang = "he" if lang == "en" else "en"
    
    # יצירת embedding עבור המילה
    source_embedding = model.encode(word, convert_to_tensor=True)

    # מציאת המילה הכי קרובה סמנטית במילון
    best_match = None
    best_score = -1
    for target_word in semantic_dict[opposite_lang].keys():
        target_embedding = model.encode(target_word, convert_to_tensor=True)
        score = util.pytorch_cos_sim(source_embedding, target_embedding).item()
        if score > best_score:
            best_match = target_word
            best_score = score

    return best_match

def main():
    if len(sys.argv) < 2:
        print("Usage: python semantic_translator.py <word or phrase>")
        sys.exit(1)

    phrase = " ".join(sys.argv[1:])
    translated = semantic_translate(phrase)
    print(f"Semantic translation: {translated}")

if __name__ == "__main__":
    main()
