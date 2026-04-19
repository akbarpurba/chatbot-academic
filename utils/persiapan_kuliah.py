from .context import context

def get_persiapan_kuliah(jurusan):
    persiapan = {
        "teknik_informatika": "💻 Persiapan masuk Teknik Informatika:\n\n📚 Persiapan Akademik:\n1. Pelajari dasar-dasar pemrograman (Python, JavaScript, atau Java)\n2. Latihan logika dan algoritma\n3. Pelajari konsep matematika dasar\n\n🖥️ Perlengkapan yang Disarankan:\n• Laptop RAM 8GB (rekomendasi 16GB)\n• Prosesor Intel i5/Ryzen 5 ke atas\n• Storage SSD 256GB\n• Software: VS Code, XAMPP, Git, Figma\n\n🎯 Tips: Biasakan coding setiap hari!",
        
        "teknologi_informasi": "📡 Persiapan masuk Teknologi Informasi:\n\n📚 Persiapan Akademik:\n1. Pelajari dasar-dasar jaringan komputer\n2. Kenali sistem operasi (Windows, Linux)\n3. Pelajari dasar-dasar database (SQL)\n\n🖥️ Perlengkapan yang Disarankan:\n• Laptop RAM 8GB\n• Prosesor Intel i3/Ryzen 3 ke atas\n• Storage 256GB\n• Software: Cisco Packet Tracer, VirtualBox, Wireshark\n\n🎯 Tips: Banyak praktik konfigurasi jaringan!",
        
        "bisnis_digital": "📊 Persiapan masuk Bisnis Digital:\n\n📚 Persiapan Akademik:\n1. Pelajari dasar-dasar pemasaran digital\n2. Kenali platform e-commerce (Shopee, Tokopedia, dll)\n3. Pelajari cara membuat konten media sosial\n4. Pelajari dasar-dasar ekonomi dan bisnis\n\n🖥️ Perlengkapan yang Disarankan:\n• Laptop RAM 8GB\n• Prosesor Intel i3/Ryzen 3\n• Storage 256GB\n• Software: Canva, CapCut, Meta Business Suite\n\n🎯 Tips: Mulai buat konten di media sosial!"
    }
    return persiapan.get(jurusan.lower(), "Jurusan tidak ditemukan.")

def proses_persiapan_kuliah(user_input):
    global context
    text = user_input.lower()
    
    if context.get("mode") == "persiapan":
        context["mode"] = None
        if "teknik informatika" in text or "ti" in text or "informatika" in text:
            return get_persiapan_kuliah("teknik_informatika")
        elif "teknologi informasi" in text or "jaringan" in text:
            return get_persiapan_kuliah("teknologi_informasi")
        elif "bisnis digital" in text or "bisnis" in text:
            return get_persiapan_kuliah("bisnis_digital")
        else:
            return "📚 Maaf, saya tidak mengenali jurusan tersebut.\n\nSebutkan: Teknik Informatika, Teknologi Informasi, atau Bisnis Digital"
    
    kata_persiapan = ["persiapan", "siap", "perlengkapan", "persiapan masuk", "apa yang disiapkan", "syarat masuk"]
    if any(kata in text for kata in kata_persiapan):
        if "teknik informatika" in text or "ti" in text or "informatika" in text:
            return get_persiapan_kuliah("teknik_informatika")
        elif "teknologi informasi" in text or "jaringan" in text:
            return get_persiapan_kuliah("teknologi_informasi")
        elif "bisnis digital" in text or "bisnis" in text:
            return get_persiapan_kuliah("bisnis_digital")
        else:
            context["mode"] = "persiapan"
            return "📚 Persiapan kuliah tergantung jurusan.\n\nSebutkan jurusanmu:\n• Teknik Informatika (coding)\n• Teknologi Informasi (jaringan)\n• Bisnis Digital (bisnis online)\n\nContoh: 'bisnis digital'"
    
    return None