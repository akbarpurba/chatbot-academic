import json #untuk baca JSON (datasettt)
import numpy as np #untuk perhitungan arayyyyyy
import re
from sklearn.feature_extraction.text import TfidfVectorizer #ubah teks jadi angka (Tf idf)
from sklearn.metrics.pairwise import cosine_similarity #hitung kemiripan (cosine similarity)
from collections import Counter #untuk voting hasil similarity
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory
from Sastrawi.StopWordRemover.StopWordRemoverFactory import StopWordRemoverFactory

factory = StemmerFactory()
stemmer = factory.create_stemmer()

stop_factory = StopWordRemoverFactory()
stopword_remover = stop_factory.create_stop_word_remover()

data_uji = [
    ("halo", "salam"),
    ("berapa biaya kuliah", "biaya_kuliah"),
    ("jadwal kuliah dimana", "jadwal_kuliah"),
    ("hai bro", "salam"),
    ("biaya semester berapa", "biaya_kuliah")
]

def preprocess(text):
    text = text.lower()
    text = re.sub(r'[^a-zA-Z0-9\s]', '', text)
    text = stopword_remover.remove(text)
    text = stemmer.stem(text)
    return text

with open('dataset.json') as file: #load dataset
    data = json.load(file)
    
pertanyaan = []
jawaban = []
labels = []

for intent in data['intents']:
    for pattern in intent['patterns']:
        pertanyaan.append(preprocess(pattern)) #simpan pertanyaan
        jawaban.append(intent['responses'][0]) #ambil 1 jawaban
        labels.append(intent['tag'])

vectorizer = TfidfVectorizer(ngram_range=(1,2))
x = vectorizer.fit_transform(pertanyaan) #ubah pertanyaan jadi vector

def prediksi_label(user_input, k=3):
    user_input = preprocess(user_input)
    input_vec = vectorizer.transform([user_input]) #ubah input jadi vector
    similarity = cosine_similarity(input_vec, x)[0] #hitung kemiripan (c_similarity)
    
    top_k = np.argsort(similarity)[-k:]  #ambil k tertinggi
    kandidat = [labels[i] for i in top_k] #ambil label
    hasil = Counter(kandidat).most_common(1) #voting
    return hasil[0][0]

def chatbot(user_input, k=3):
    label = prediksi_label(user_input, k)
    for intent in data['intents']:
        if intent['tag'] == label:
            return intent['responses'][0]

def hitung_akurasi(data_uji, k=3):
    benar = 0

    for text, label_asli in data_uji:
        prediksi = prediksi_label(text, k)

        print(f"Input: {text}")
        print(f"Prediksi: {prediksi} | Asli: {label_asli}\n")

        if prediksi == label_asli:
            benar += 1

    total = len(data_uji)
    akurasi = (benar / total) * 100

    print(f"Akurasi: {akurasi:.2f}%")

for k in [1,3,5]:
    print(f"\nTesting K = {k}")
    hitung_akurasi(data_uji, k)