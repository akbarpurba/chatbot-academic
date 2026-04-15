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

for intent in data['intents']:
    for pattern in intent['patterns']:
        pertanyaan.append(preprocess(pattern)) #simpan pertanyaan
        jawaban.append(intent['responses'][0]) #ambil 1 jawaban
        
vectorizer = TfidfVectorizer(ngram_range=(1,2))
x = vectorizer.fit_transform(pertanyaan) #ubah pertanyaan jadi vector

def chatbot(user_input, k=3):
    user_input = preprocess(user_input)
    input_vec = vectorizer.transform([user_input]) #ubah input jadi vector
    similarity = cosine_similarity(input_vec, x)[0] #hitung kemiripan (c_similarity)
    index = similarity.argmax() #voting / ambil nilai tertinggi dari c_similarity
    
    if similarity.max() < 0.3:
        return "Maaf, saya tidak memahami pertanyaan Anda"
    
    top_k = np.argsort(similarity)[-k:]  #ambil k tertinggi
    kandidat = [jawaban[i] for i in top_k] #ambil jawaban
    hasil = Counter(kandidat).most_common(1) #voting
    return hasil[0][0]

while True:
    user = input("Akbar: ")
    print("Bot: ", chatbot(user))