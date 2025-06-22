import os
import tkinter as tk
from tkinter import messagebox, ttk
import requests

# Detect language
def detect_language(text: str) -> str:
    return "he" if any("\u0590" <= c <= "\u05EA" for c in text) else "en"

# Create improved prompt for Ollama
def create_prompt(text: str, lang: str) -> str:
    if lang == "en":
        return (
            "You are a professional Hebrew translator. Translate the following English word or phrase to accurate and fluent Hebrew based on its intended meaning and context.\n"
            f"Text: {text}\n"
            "Only return the Hebrew translation."
        )
    else:
        return (
            "You are a professional English translator. Translate the following Hebrew word or phrase to accurate and fluent English based on its intended meaning and context.\n"
            f"Text: {text}\n"
            "Only return the English translation."
        )

# Translate using Ollama local model
def translate_with_ollama(prompt, model):
    try:
        # check if Ollama server is running
        ping = requests.get("http://localhost:11434")
        if ping.status_code != 200:
            raise Exception("Ollama server is not responding.")

        response = requests.post(
            'http://localhost:11434/api/generate',
            json={"model": model, "prompt": prompt, "stream": False},
            timeout=30
        )
        response.raise_for_status()
        return response.json()["response"].strip()
    except requests.exceptions.ConnectionError:
        raise Exception("Ollama is not running. Please start it with: ollama serve")
    except requests.exceptions.RequestException as e:
        raise Exception(f"Ollama request failed: {e}")

# Perform translation
def perform_translation():
    phrase = input_entry.get().strip()
    if not phrase:
        messagebox.showwarning("Missing Input", "Please enter a word or phrase to translate.")
        return

    source_lang = detect_language(phrase)
    prompt = create_prompt(phrase, source_lang)
    selected_model = model_var.get()

    try:
        result = translate_with_ollama(prompt, selected_model)
        output_text.delete("1.0", tk.END)
        output_text.insert(tk.END, result)

    except Exception as e:
        tk.messagebox.showerror("Translation Error", f"An error occurred: {str(e)}")

# GUI Setup
root = tk.Tk()
root.title("Semantic Translator (Ollama)")

input_frame = tk.Frame(root)
input_frame.pack(pady=(10, 0))
tk.Label(input_frame, text="Enter word or phrase:").pack(side=tk.LEFT)
input_entry = tk.Entry(input_frame, width=60)
input_entry.pack(side=tk.LEFT, padx=5)

# Model selection dropdown
model_var = tk.StringVar(value="mistral")
tk.Label(root, text="Select model:").pack()
model_dropdown = ttk.Combobox(root, textvariable=model_var, values=["mistral", "llama3", "gemma:2b", "mixtral"])
model_dropdown.pack(pady=5)

translate_button = tk.Button(root, text="Translate", command=perform_translation)
translate_button.pack(pady=10)

output_label = tk.Label(root, text="Translation:")
output_label.pack()
output_text = tk.Text(root, height=4, width=60)
output_text.pack(pady=5)

# Bind Enter key
root.bind('<Return>', lambda event: perform_translation())

root.mainloop()
