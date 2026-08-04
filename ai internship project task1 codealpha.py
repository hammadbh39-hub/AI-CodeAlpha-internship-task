import os
import threading
import tkinter as tk
from tkinter import ttk, messagebox

from deep_translator import GoogleTranslator
import pyperclip
import pyttsx3

try:
    from gtts import gTTS
    HAS_GTTS = True
except ImportError:
    HAS_GTTS = False

import winsound

languages = {
    "English": "en",
    "Urdu": "ur",
    "Hindi": "hi",
    "French": "fr",
    "German": "de",
    "Arabic": "ar",
    "Greek": "el",
    "Afrikaans": "af",
    "Pashto": "ps",
    "Punjabi": "pa",
    "Turkish": "tr",
    "Romanian": "ro",
    "Russian": "ru",
    "Nepali": "ne",
    "Luxembourgish": "lb",
    "Korean": "ko",
    "Japanese": "ja",
    "Persian": "fa",
    "Thai": "th",
    "Chinese": "zh-CN"
}

root = tk.Tk()
root.title("Language Translation Tool")
root.geometry("620x700")

def translate_text():
    text = input_text.get("1.0", tk.END).strip()
    
    if not text:
        messagebox.showwarning("Warning", "Please enter some text to translate.")
        return

    try:
        source = languages[from_lang.get()]
        target = languages[to_lang.get()]

        translated = GoogleTranslator(
            source=source,
            target=target
        ).translate(text)

        output_text.delete("1.0", tk.END)
        output_text.insert(tk.END, translated)

    except KeyError:
        messagebox.showerror("Error", "Selected language is not supported.")
    except Exception as e:
        messagebox.showerror("Error", str(e))


def clear_text():
    """ Input aur Output dono Textboxes ko clear karta hai """
    input_text.delete("1.0", tk.END)
    output_text.delete("1.0", tk.END)


def speak_text():
    """ High Quality Online Voice (gTTS) without Pygame + Offline Backup (pyttsx3) """
    translated = output_text.get("1.0", tk.END).strip()
    if not translated:
        messagebox.showwarning("Warning", "Nothing to speak! Please translate something first.")
        return

    target_code = languages.get(to_lang.get())

    def play_audio():
        # Pehle gTTS try karein (Windows command line player ke zariye)
        if HAS_GTTS:
            try:
                engine=pyttsx3.init()
                engine.setProperty('rate',150)
                
                voices=engine.getProperty('voices')
                selected_voice=None
                
                for voice in voices:
                    if target_code.lower() in voice.name.lower() or target_code.lower() in str(voice.languages).lower():
                        selected_voice=voice.id 
                        break
                    if selected_voice:
                        engine.setProperty('voice',selected_voice)
                        
                    engine.say(translated)
                    engine.runAndWait()
            except Exception as e:
                messagebox.showerror("Speech Error",f"Unable to speak text:{str(e)}")

        try:
            engine = pyttsx3.init()
            engine.say(translated)
            engine.runAndWait()
        except Exception as e:
            messagebox.showerror("Speech Error", f"Unable to speak text: {str(e)}")
            
    threading.Thread(target=play_audio, daemon=True).start()


def copy_text():
    """ Output text ko clipboard mein copy karta hai """
    translated = output_text.get("1.0", tk.END).strip()
    if translated:
        pyperclip.copy(translated)
        messagebox.showinfo("Success", "Translated text copied to clipboard!")
    else:
        messagebox.showwarning("Warning", "Nothing to copy!")


def swap_languages():
    """ Languages aur text boxes swap karta hai """
    src_lang = from_lang.get()
    tgt_lang = to_lang.get()
    
    from_lang.set(tgt_lang)
    to_lang.set(src_lang)
    
    input_val = input_text.get("1.0", tk.END).strip()
    output_val = output_text.get("1.0", tk.END).strip()
    
    if output_val:
        input_text.delete("1.0", tk.END)
        input_text.insert(tk.END, output_val)
        
        output_text.delete("1.0", tk.END)
        output_text.insert(tk.END, input_val)



title = tk.Label(root, text="Language Translation Tool", font=("Arial", 18, "bold"))
title.pack(pady=10)

input_label = tk.Label(root, text="Enter Text:", font=("Arial", 11, "bold"))
input_label.pack()

input_text = tk.Text(root, height=5, width=60, font=("Arial", 10))
input_text.pack(pady=5)

# Language Selectors Frame
lang_frame = tk.Frame(root)
lang_frame.pack(pady=5)

# From Language
from_label = tk.Label(lang_frame, text="From:", font=("Arial", 10, "bold"))
from_label.grid(row=0, column=0, padx=5)

from_lang = ttk.Combobox(
    lang_frame,
    values=list(languages.keys()),
    width=15,
    state="readonly"
)
from_lang.grid(row=0, column=1, padx=5)
from_lang.set("English")

swap_btn = tk.Button(
    lang_frame,
    text="🔁 Swap",
    font=("Arial", 9, "bold"),
    bg="#E0E0E0",
    command=swap_languages
)
swap_btn.grid(row=0, column=2, padx=10)

# To Language
to_label = tk.Label(lang_frame, text="To:", font=("Arial", 10, "bold"))
to_label.grid(row=0, column=3, padx=5)

to_lang = ttk.Combobox(
    lang_frame,
    values=list(languages.keys()),
    width=15,
    state="readonly"
)
to_lang.grid(row=0, column=4, padx=5)
to_lang.set("Urdu")

# Main Buttons (Translate & Clear)
btn_frame = tk.Frame(root)
btn_frame.pack(pady=10)

translate_btn = tk.Button(
    btn_frame,
    text="Translate",
    font=("Arial", 11, "bold"),
    bg="#4CAF50",
    fg="white",
    width=12,
    command=translate_text
)
translate_btn.grid(row=0, column=0, padx=10)

clear_btn = tk.Button(
    btn_frame,
    text="Clear All",
    font=("Arial", 11, "bold"),
    bg="#f44336",
    fg="white",
    width=12,
    command=clear_text
)
clear_btn.grid(row=0, column=1, padx=10)

# Output Section
output_label = tk.Label(
    root,
    text="Translated Text:",
    font=("Arial", 11, "bold")
)
output_label.pack()

output_text = tk.Text(
    root, height=5,
    width=60,
    font=("Arial", 10)
)
output_text.pack(pady=5)

# Utility Buttons (Speak & Copy)
utility_frame = tk.Frame(root)
utility_frame.pack(pady=10)

speak_btn = tk.Button(
    utility_frame,
    text="🔊 Speak",
    font=("Arial", 10, "bold"),
    bg="#2196F3",
    fg="white",
    width=12,
    command=speak_text
)
speak_btn.grid(row=0, column=0, padx=10)

copy_btn = tk.Button(
    utility_frame,
    text="📋 Copy Text",
    font=("Arial", 10, "bold"),
    bg="#FF9800",
    fg="white",
    width=12,
    command=copy_text
)
copy_btn.grid(row=0, column=1, padx=10)

root.mainloop()