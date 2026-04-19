import json
import random
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

from utils.preprocessing import preprocess
from utils.keyword_map import KEYWORD_MAP
from utils.greetings import cek_sapaan, cek_greeting_biasa
from utils.troubleshooting import handle_troubleshooting
from utils.persiapan_kuliah import proses_persiapan_kuliah
from utils.context import context, update_context, reset_context
from utils.troubleshooting import handle_follow_up
from model.rekomendasi_jurusan import (
    rekomendasi_dari_pertanyaan, 
    get_info_jurusan
)

# =========================
# LOAD DATA
# =========================
with open("model/dataset.json", "r", encoding="utf-8") as f:
    data = json.load(f)

# =========================
# BUILD DATASET
# =========================
patterns = []
labels = []
responses = {}

for intent in data["intents"]:
    tag = intent["tag"]
    responses[tag] = intent["responses"]
    for p in intent["patterns"]:
        patterns.append(preprocess(p))
        labels.append(tag)

# =========================
# TF-IDF VECTORIZER
# =========================
vectorizer = TfidfVectorizer(ngram_range=(1, 2))
tfidf_matrix = vectorizer.fit_transform(patterns)

# =========================
# HELPER FUNCTIONS
# =========================
def rule_engine(text):
    text_lower = text.lower()
    best_match = None
    best_match_length = 0
    
    for tag, keywords in KEYWORD_MAP.items():
        for keyword in keywords:
            if keyword in text_lower:
                if len(keyword) > best_match_length:
                    best_match_length = len(keyword)
                    best_match = tag
    return best_match

def exact_pattern_match(text):
    text_clean = preprocess(text)
    for i, pattern in enumerate(patterns):
        if pattern == text_clean or text_clean in pattern or pattern in text_clean:
            return labels[i]
    return None

def resolve_conflict(best_label, text):
    text_lower = text.lower()
    
    if any(k in text_lower for k in ["jadwal kuliah", "jam kuliah"]):
        return "jadwal_kuliah"
    if any(k in text_lower for k in ["fasilitas", "lab", "wifi"]):
        return "fasilitas"
    if any(k in text_lower for k in ["biaya", "ukt"]):
        return "biaya"
    if any(k in text_lower for k in ["prodi", "jurusan"]):
        return "program_studi"
    if any(k in text_lower for k in ["jaringan", "network", "server"]):
        return "teknologi_informasi"
    if any(k in text_lower for k in ["coding", "programmer", "ngoding"]):
        return "ti"
    
    return best_label

# =========================
# CHATBOT CORE
# =========================
def chatbot(user_input):
    if not user_input or not user_input.strip():
        return "Halo! Ada yang bisa saya bantu?"
    
    text = user_input.lower()
    text_clean = preprocess(text)
    
    # PRIORITY 1: TROUBLESHOOTING
    
    follow_up = handle_follow_up(user_input)
    if follow_up:
        return follow_up
    
    # PRIORITY 1: TROUBLESHOOTING
    troubleshooting = handle_troubleshooting(user_input)
    if troubleshooting:
        return troubleshooting
    
    # PRIORITY 2: DETEKSI "TIDAK ADA", "TIDAK", "SELESAI" (KONFIRMASI AKHIR PERCAKAPAN)
    if any(kata in text for kata in ["tidak ada", "tidak", "nggak ada", "gak ada", "selesai", "cukup", "itu saja", "sudah selesai", "udah", "ya udah"]):
        # Reset context jika masih dalam mode troubleshooting
        if context.get("troubleshoot_step", 0) > 0:
            context["troubleshoot_step"] = 0
            context["troubleshoot_type"] = None
        return "Baik, terima kasih sudah menggunakan PENUSA Bot. 😊\n\nJika ada pertanyaan lain, silakan tanyakan kapan saja. Semoga membantu!"
    
    # PRIORITY 3: CEK SAPAAN
    sapaan = cek_sapaan(text)
    if sapaan:
        return sapaan
    
    # PRIORITY 4: GREETING BIASA
    greeting = cek_greeting_biasa(text)
    if greeting:
        return greeting
    
    # PRIORITY 5: PERSIAPAN KULIAH
    persiapan = proses_persiapan_kuliah(text)
    if persiapan:
        return persiapan
    
    # PRIORITY 6: INFO JURUSAN
    if any(kata in text for kata in ["teknik informatika", "ti itu apa", "jurusan ti", "info ti", "apa itu teknik informatika"]):
        info = get_info_jurusan("teknik informatika")
        if info:
            return info
    
    if any(kata in text for kata in ["teknologi informasi", "jurusan jaringan", "info ti jaringan", "apa itu teknologi informasi"]):
        info = get_info_jurusan("teknologi informasi")
        if info:
            return info
    
    if any(kata in text for kata in ["bisnis digital", "jurusan bisnis", "info bisnis digital", "apa itu bisnis digital"]):
        info = get_info_jurusan("bisnis digital")
        if info:
            return info
    
    # PRIORITY 7: REKOMENDASI JURUSAN
    rekomendasi = rekomendasi_dari_pertanyaan(text)
    if rekomendasi:
        update_context("rekomendasi")
        return rekomendasi
    
    # PRIORITY 8: EXACT PATTERN MATCH
    exact_match = exact_pattern_match(text)
    if exact_match and exact_match in responses:
        update_context(exact_match)
        return random.choice(responses[exact_match])
    
    # PRIORITY 9: RULE ENGINE
    rule = rule_engine(text)
    if rule and rule in responses:
        update_context(rule)
        return random.choice(responses[rule])
    
    # PRIORITY 10: TF-IDF SIMILARITY
    if len(patterns) > 0:
        vec = vectorizer.transform([text_clean])
        sims = cosine_similarity(vec, tfidf_matrix)[0]
        
        best_idx = np.argmax(sims)
        best_score = sims[best_idx]
        best_label = labels[best_idx]
        
        if best_score >= 0.25:
            best_label = resolve_conflict(best_label, text)
            if best_label in responses:
                update_context(best_label)
                return random.choice(responses[best_label])
    
    # PRIORITY 11: FALLBACK
    return "Maaf, saya belum paham 😅 \n\n💡 Coba tanyakan:\n- biaya kuliah\n- jadwal kuliah\n- fasilitas kampus\n- alamat kampus\n- daftar jurusan\n- kontak kampus\n- pendaftaran\n- rekomendasi jurusan\n- persiapan kuliah"

# =========================
# MAIN LOOP (CLI)
# =========================
if __name__ == "__main__":
    print("=" * 55)
    print("PENUSA Bot 🤖 siap membantu!")
    print("💬 Ketik 'quit' atau 'exit' untuk keluar")
    print("💬 Ketik 'reset' untuk mereset context")
    print("=" * 55)
    
    while True:
        user_input = input("\n👤 Kamu: ").strip()
        
        if user_input.lower() in ['quit', 'exit', 'keluar']:
            print("🤖 PENUSA Bot: Terima kasih! 👋")
            break
        
        if user_input.lower() == 'reset':
            reset_context()
            print("🤖 PENUSA Bot: Context telah direset.")
            continue
        
        response = chatbot(user_input)
        print(f"🤖 PENUSA Bot: {response}")