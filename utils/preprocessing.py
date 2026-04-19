import re
import json
import os

# Load slang.json
try:
    with open("model/slang.json", "r", encoding="utf-8") as f:
        slang = json.load(f)
except FileNotFoundError:
    slang = {}
    print("Peringatan: file slang.json tidak ditemukan")

def normalize(text):
    words = text.lower().split()
    return " ".join([slang.get(w, w) for w in words])

def preprocess(text):
    text = normalize(text)
    text = re.sub(r'[^a-z0-9\s]', ' ', text)
    text = re.sub(r'\s+', ' ', text).strip()
    return text