import random

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