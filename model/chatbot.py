import json
import random
import numpy as np
import re
import os
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Import file rekomendasi jurusan (hanya yang diperlukan)
from model.rekomendasi_jurusan import (
    rekomendasi_dari_pertanyaan, 
    get_info_jurusan
)

# =========================
# LOAD DATA
# =========================
with open("model/dataset.json", "r", encoding="utf-8") as f:
    data = json.load(f)

try:
    with open("model/slang.json", "r", encoding="utf-8") as f:
        slang = json.load(f)
except FileNotFoundError:
    slang = {}
    print("Peringatan: file slang.json tidak ditemukan")

# =========================
# PREPROCESS
# =========================
def normalize(text):
    words = text.lower().split()
    return " ".join([slang.get(w, w) for w in words])

def preprocess(text):
    text = normalize(text)
    text = re.sub(r'[^a-z0-9\s]', ' ', text)
    text = re.sub(r'\s+', ' ', text).strip()
    return text

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
# TF-IDF
# =========================
vectorizer = TfidfVectorizer(ngram_range=(1,2))
tfidf_matrix = vectorizer.fit_transform(patterns)

# =========================
# CONTEXT MEMORY & STATE
# =========================
context = {"last_intent": None, "mode": None}  # mode: "persiapan", "rekomendasi"

# =========================
# KEYWORD MAP (LENGKAP)
# =========================
KEYWORD_MAP = {
    "jadwal_kuliah": ["jadwal kuliah", "jadwal kelas", "jadwal perkuliahan", "jam kuliah", "kelas hari ini", "jadwal mata kuliah"],
    "biaya": ["biaya", "ukt", "biaya kuliah", "biaya persemester", "berapa biaya"],
    "fasilitas": ["fasilitas", "lab", "wifi", "perpustakaan", "ruang belajar", "mushola"],
    "alamat": ["alamat", "lokasi", "dimana kampus", "letak kampus"],
    "program_studi": ["prodi", "jurusan", "program studi", "daftar jurusan"],
    "kontak": ["kontak", "nomor", "email", "hubungi", "admin"],
    "pendaftaran": ["pendaftaran", "daftar", "registrasi", "pmb"],
    "beasiswa": ["beasiswa", "kip", "kip kuliah"],
    "organisasi": ["organisasi", "ukm", "bem", "rohis", "kmk"],
    "dosen": ["dosen", "pengajar", "tenaga pengajar"],
    "krs": ["krs", "isi krs", "kartu rencana studi"],
    "khs": ["khs", "nilai", "hasil studi", "lihat nilai"],
    "bayar_ukt": ["bayar ukt", "pembayaran", "transfer", "briva"],
    "login_issue": ["login", "gagal login", "tidak bisa login", "gabisa login"],
    "reset_password": ["reset password", "lupa password", "ganti password"],
    "cicilan_ukt": ["cicilan", "cicil", "angsuran", "dicicil"],
    "siakad_error": ["siakad error", "error siakad", "server down"],
    "nilai_tidak_muncul": ["nilai kosong", "nilai belum keluar", "nilai tidak muncul"],
    "terimakasih": ["terima kasih", "makasih", "thanks", "bujur"],
    "penusa_bot": ["penusa bot", "kamu siapa", "bot ini apa"],
    "ti": ["teknik informatika", "ti itu apa", "coding", "programmer"],
    "teknologi_informasi": ["teknologi informasi", "jurusan ti", "jaringan", "network", "server"],
    "bisnis_digital": ["bisnis digital", "jurusan bisnis", "e-commerce", "digital marketing", "startup"],
    "stimik": ["stimik", "stmik", "kepanjangan stimik", "apa itu stimik"],
    "lihat_data_mahasiswa": ["data mahasiswa", "profil mahasiswa", "biodata", "data diri"],
    "akses_siakad": ["akses siakad", "cara login siakad", "login siakad", "edlink"],
    "kalender_akademik": ["kalender akademik", "jadwal akademik", "tanggal penting", "jadwal uts", "jadwal uas"],
    "lihat_ruang_kelas": ["ruang kelas", "lihat ruang", "monitor kampus", "ruang kuliah"],
    "website_kampus": ["website kampus", "pmb.pelitanusantara", "situs kampus"],
    "pujian_bot": ["bot keren", "kamu keren", "pintar bot", "keren bot"],
    "hinaan_kritik": ["goblok", "bodoh", "tolol", "bego", "jelek bot"]
}

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
# CEK SAPAAN
# =========================
def cek_sapaan(text):
    text_lower = text.lower()
    
    if "assalamualaikum" in text_lower or "assalamu'alaikum" in text_lower:
        return "Wa'alaikumsalam! 👋 Ada yang bisa saya bantu? Silakan tanya soal kampus ya."
    
    if "horas" in text_lower:
        return "Horas! 👋 Ada yang bisa saya bantu? Coba tanya soal biaya kuliah atau jadwal pendaftaran ya."
    
    if "mejuah-juah" in text_lower or "mejuah juah" in text_lower:
        return "Mejuah-juah! 😄 Selamat datang. Mau tanya info kampus? Saya siap membantu."
    
    if "ahoii" in text_lower or "ahoi" in text_lower or "hoii" in text_lower:
        return "Ahoii Wakkk! 🔥 Nak tanya soal apeni? Coba tanya tentang SIAKAD, KRS, atau nilai!"
    
    return None

def cek_greeting_biasa(text):
    text_lower = text.lower()
    kata_greeting = ["halo", "hai", "hello", "hi", "pagi", "siang", "malam", "selamat datang", "hey"]
    
    if any(word in text_lower for word in kata_greeting):
        return random.choice([
            "Halo! Ada yang bisa saya bantu? Silakan tanya soal biaya, jadwal kuliah, atau pendaftaran ya.",
            "Hai! Selamat datang di PENUSA Bot. Mau tanya soal kampus? Saya siap membantu.",
            "Selamat datang! Tanya apa saja tentang kampus. Biaya kuliah, alamat, beasiswa, atau KRS?",
            "Halo! Senang bertemu denganmu. Yuk tanya soal perkuliahan, saya akan bantu jawab."
        ])
    return None

# =========================
# FUNGSI PERSIAPAN KULIAH (TANPA DEPENDENSI REKOMENDASI_JURUSAN)
# =========================
def get_persiapan_kuliah(jurusan):
    """Mengembalikan daftar persiapan untuk jurusan tertentu"""
    persiapan = {
        "teknik_informatika": "💻 Persiapan masuk Teknik Informatika:\n\n📚 Persiapan Akademik:\n1. Pelajari dasar-dasar pemrograman (Python, JavaScript, atau Java)\n2. Latihan logika dan algoritma\n3. Pelajari konsep matematika dasar\n\n🖥️ Perlengkapan yang Disarankan:\n• Laptop RAM 8GB (rekomendasi 16GB)\n• Prosesor Intel i5/Ryzen 5 ke atas\n• Storage SSD 256GB\n• Software: VS Code, XAMPP, Git, Figma\n\n🎯 Tips: Biasakan coding setiap hari!",
        
        "teknologi_informasi": "📡 Persiapan masuk Teknologi Informasi:\n\n📚 Persiapan Akademik:\n1. Pelajari dasar-dasar jaringan komputer\n2. Kenali sistem operasi (Windows, Linux)\n3. Pelajari dasar-dasar database (SQL)\n\n🖥️ Perlengkapan yang Disarankan:\n• Laptop RAM 8GB\n• Prosesor Intel i3/Ryzen 3 ke atas\n• Storage 256GB\n• Software: Cisco Packet Tracer, VirtualBox, Wireshark\n\n🎯 Tips: Banyak praktik konfigurasi jaringan!",
        
        "bisnis_digital": "📊 Persiapan masuk Bisnis Digital:\n\n📚 Persiapan Akademik:\n1. Pelajari dasar-dasar pemasaran digital\n2. Kenali platform e-commerce (Shopee, Tokopedia, dll)\n3. Pelajari cara membuat konten media sosial\n4. Pelajari dasar-dasar ekonomi dan bisnis\n\n🖥️ Perlengkapan yang Disarankan:\n• Laptop RAM 8GB\n• Prosesor Intel i3/Ryzen 3\n• Storage 256GB\n• Software/aplikasi yang perlu:\n  - Canva atau Adobe Photoshop (desain)\n  - CapCut atau Adobe Premiere (edit video)\n  - Meta Business Suite (kelola social media)\n\n🎯 Tips Tambahan:\n• Mulai buat konten di media sosial\n• Coba jualan online kecil-kecilan\n• Ikuti perkembangan tren digital marketing"
    }
    return persiapan.get(jurusan.lower(), "Jurusan tidak ditemukan. Coba pilih: teknik informatika, teknologi informasi, atau bisnis digital.")

def proses_persiapan_kuliah(user_input):
    global context
    text = user_input.lower()
    
    # Jika sedang dalam mode persiapan (menunggu user menyebut jurusan)
    if context.get("mode") == "persiapan":
        context["mode"] = None  # Reset mode
        if "teknik informatika" in text or "ti" in text or "informatika" in text:
            return get_persiapan_kuliah("teknik_informatika")
        elif "teknologi informasi" in text or "jaringan" in text:
            return get_persiapan_kuliah("teknologi_informasi")
        elif "bisnis digital" in text or "bisnis" in text:
            return get_persiapan_kuliah("bisnis_digital")
        else:
            # Reset mode dan minta user menyebut jurusan dengan benar
            return "📚 Maaf, saya tidak mengenali jurusan tersebut.\n\nSebutkan jurusanmu:\n• Teknik Informatika\n• Teknologi Informasi\n• Bisnis Digital"
    
    # Deteksi awal pertanyaan persiapan
    kata_persiapan = ["persiapan", "siap", "perlengkapan", "persiapan masuk", "apa yang disiapkan", "syarat masuk"]
    if any(kata in text for kata in kata_persiapan):
        # Cek apakah user langsung menyebut jurusan
        if "teknik informatika" in text or "ti" in text or "informatika" in text:
            return get_persiapan_kuliah("teknik_informatika")
        elif "teknologi informasi" in text or "jaringan" in text:
            return get_persiapan_kuliah("teknologi_informasi")
        elif "bisnis digital" in text or "bisnis" in text:
            return get_persiapan_kuliah("bisnis_digital")
        else:
            # Set mode persiapan dan minta user memilih jurusan
            context["mode"] = "persiapan"
            return "📚 Persiapan kuliah tergantung jurusan yang dipilih.\n\nSebutkan jurusanmu:\n• Teknik Informatika (coding, programming)\n• Teknologi Informasi (jaringan, server)\n• Bisnis Digital (digital marketing, e-commerce)\n\nContoh: 'bisnis digital'"
    
    return None

# =========================
# CHATBOT CORE
# =========================
def chatbot(user_input):
    global context
    
    if not user_input or not user_input.strip():
        return "Halo! Ada yang bisa saya bantu?"
    
    text = user_input.lower()
    text_clean = preprocess(text)
    
    # PRIORITY 1: CEK SAPAAN
    sapaan = cek_sapaan(text)
    if sapaan:
        return sapaan
    
    # PRIORITY 2: GREETING BIASA
    greeting = cek_greeting_biasa(text)
    if greeting:
        return greeting
    
    # PRIORITY 3: PERSIAPAN KULIAH
    persiapan = proses_persiapan_kuliah(text)
    if persiapan:
        return persiapan
    
    # =========================
    # PRIORITY 4: INFO JURUSAN (DIPERBAIKI)
    # =========================
    # Deteksi untuk Teknik Informatika
    if any(kata in text for kata in ["teknik informatika", "ti itu apa", "jurusan ti", "info ti", "apa itu teknik informatika", "info teknik informatika", "jelaskan teknik informatika"]):
        info = get_info_jurusan("teknik informatika")
        if info:
            return info
    
    # Deteksi untuk Teknologi Informasi
    if any(kata in text for kata in ["teknologi informasi", "jurusan jaringan", "info ti jaringan", "apa itu teknologi informasi", "info teknologi informasi"]):
        info = get_info_jurusan("teknologi informasi")
        if info:
            return info
    
    # Deteksi untuk Bisnis Digital
    if any(kata in text for kata in ["bisnis digital", "jurusan bisnis", "info bisnis digital", "apa itu bisnis digital", "info bisnis"]):
        info = get_info_jurusan("bisnis digital")
        if info:
            return info
    
    # PRIORITY 5: REKOMENDASI JURUSAN
    rekomendasi = rekomendasi_dari_pertanyaan(text)
    if rekomendasi:
        context["last_intent"] = "rekomendasi"
        return rekomendasi
    
    # PRIORITY 6: EXACT PATTERN MATCH
    exact_match = exact_pattern_match(text)
    if exact_match and exact_match in responses:
        context["last_intent"] = exact_match
        return random.choice(responses[exact_match])
    
    # PRIORITY 7: RULE ENGINE
    rule = rule_engine(text)
    if rule and rule in responses:
        context["last_intent"] = rule
        return random.choice(responses[rule])
    
    # PRIORITY 8: TF-IDF SIMILARITY
    if len(patterns) > 0:
        vec = vectorizer.transform([text_clean])
        sims = cosine_similarity(vec, tfidf_matrix)[0]
        
        best_idx = np.argmax(sims)
        best_score = sims[best_idx]
        best_label = labels[best_idx]
        
        if best_score >= 0.25:
            best_label = resolve_conflict(best_label, text)
            
            if best_label in responses:
                context["last_intent"] = best_label
                return random.choice(responses[best_label])
    
    # PRIORITY 9: FALLBACK
    return "Maaf, saya belum paham 😅 \n\n💡 Coba tanyakan:\n- biaya kuliah\n- jadwal kuliah\n- fasilitas kampus\n- alamat kampus\n- daftar jurusan\n- kontak kampus\n- pendaftaran\n- rekomendasi jurusan\n- persiapan kuliah"
# =========================
# MAIN LOOP
# =========================
if __name__ == "__main__":
    print("=" * 55)
    print("PENUSA Bot 🤖 siap membantu!")
    print("📚 Fitur: Info Kampus, Rekomendasi Jurusan, Tanya Jawab Akademik")
    print("💬 Ketik 'quit' atau 'exit' untuk keluar")
    print("💬 Ketik 'reset' untuk mereset mode persiapan")
    print("=" * 55)
    
    while True:
        user_input = input("\n👤 Kamu: ").strip()
        
        if user_input.lower() in ['quit', 'exit', 'keluar']:
            print("🤖 PENUSA Bot: Terima kasih telah menggunakan PENUSA Bot! 👋")
            break
        
        # Perintah reset
        if user_input.lower() == 'reset':
            context["mode"] = None
            print("🤖 PENUSA Bot: Mode persiapan telah direset.")
            continue
        
        response = chatbot(user_input)
        print(f"🤖 PENUSA Bot: {response}")