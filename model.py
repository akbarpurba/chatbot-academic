import json
import numpy as np
import re
import random
from collections import Counter
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from Levenshtein import distance

from Sastrawi.Stemmer.StemmerFactory import StemmerFactory
from Sastrawi.StopWordRemover.StopWordRemoverFactory import StopWordRemoverFactory

# === LOAD SLANG JSON ===
with open('slang.json') as f:
    slang_dict = json.load(f)

def normalize(text):
    return " ".join([slang_dict.get(word, word) for word in text.split()])


# === INIT NLP ===
factory = StemmerFactory()
stemmer = factory.create_stemmer()

stop_factory = StopWordRemoverFactory()
stopword_remover = stop_factory.create_stop_word_remover()


# === TYPO CORRECTION (DIPERBAIKI) ===
kamus = set()

def correct_typo(word):
    # lindungi hasil slang
    if word in slang_dict.values():
        return word

    kandidat = []
    for k in kamus:
        if abs(len(k) - len(word)) <= 2:
            kandidat.append(k)

    if not kandidat:
        return word

    terbaik = min(kandidat, key=lambda x: distance(word, x))

    if distance(word, terbaik) <= 2:
        return terbaik

    return word


# === FINAL PREPROCESS (URUTAN SUDAH BENAR) ===
def preprocess(text):
    text = text.lower()
    text = re.sub(r'[^a-zA-Z0-9\s]', '', text)  # 1. hapus simbol dulu
    text = normalize(text)  # 2. slang

    words = text.split()
    words = [correct_typo(w) for w in words]  # 3. typo correction
    text = " ".join(words)

    text = stemmer.stem(text)  # 4. stemming
    text = stopword_remover.remove(text)  # 5. stopword

    return text


# === LOAD DATASET ===
with open('dataset.json') as file:
    data = json.load(file)

pertanyaan = []
labels = []
responses = {}

for intent in data['intents']:
    for pattern in intent['patterns']:
        pertanyaan.append(pattern)  # ❗ TIDAK langsung preprocess
        labels.append(intent['tag'])
    responses[intent['tag']] = intent['responses']


# === BANGUN KAMUS UNTUK TYPO ===
for kalimat in pertanyaan:
    kalimat = preprocess(kalimat)
    for kata in kalimat.split():
        kamus.add(kata)

for kata in slang_dict.values():
    kamus.add(kata)


# === TF-IDF ===
processed_pertanyaan = [preprocess(q) for q in pertanyaan]

vectorizer = TfidfVectorizer(ngram_range=(1, 2))
X = vectorizer.fit_transform(processed_pertanyaan)


# === CHATBOT ===
def chatbot(user_input, k=3, threshold=0.35):
    user_input_clean = preprocess(user_input)

    input_vec = vectorizer.transform([user_input_clean])
    similarity = cosine_similarity(input_vec, X)[0]

    if similarity.max() < threshold:
        return random.choice([
            "Kurang paham, coba jelasin lagi.",
            "Maksudnya apa ya? Coba ulang.",
            "Belum ngerti, bisa diperjelas?"
        ])

    top_k_idx = np.argsort(similarity)[-k:][::-1]
    kandidat_label = [labels[i] for i in top_k_idx]

    hasil = Counter(kandidat_label).most_common(1)[0][0]

    return random.choice(responses[hasil])


# === LOOP CHAT ===
while True:
    user = input("Akbar: ")
    print("Bot:", chatbot(user))