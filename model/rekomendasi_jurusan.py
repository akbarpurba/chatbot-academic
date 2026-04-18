# =========================
# REKOMENDASI JURUSAN - DATA & FUNGSI
# =========================

import re

# =========================
# STATE MANAGEMENT UNTUK PERSIAPAN KULIAH
# =========================

_menunggu_jurusan_persiapan = False

def reset_persiapan_state():
    """Reset state persiapan kuliah"""
    global _menunggu_jurusan_persiapan
    _menunggu_jurusan_persiapan = False

def get_persiapan_state():
    """Mendapatkan status state persiapan (untuk debugging)"""
    global _menunggu_jurusan_persiapan
    return _menunggu_jurusan_persiapan

# Data jurusan lengkap
DATA_JURUSAN = {
    "teknik_informatika": {
        "nama": "Teknik Informatika",
        "emoji": "💻",
        "cocok_untuk": ["coding", "program", "ngoding", "pemrograman", "aplikasi", "software", "developer", "web", "mobile", "android", "ios", "javascript", "python", "java", "php", "ai", "data science", "machine learning", "game", "gaming", "main game", "buat game", "bikin game", "buat web", "bikin web", "hacker", "hacking", "hengker", "haker", "cyber", "otak atik komputer", "bongkar komputer", "matematika", "logika", "algoritma", "data", "big data", "keamanan siber", "bug", "exploit", "op warnet", "admin warnet", "jaga warnet", "guru rpl", "ngajar rpl", "rpl"],
        "deskripsi": "Fokus pada pemrograman, pengembangan software, AI, keamanan siber, dan game development.",
        "mata_kuliah": "Pemrograman Web, Mobile Development, AI, Machine Learning, Struktur Data, Algoritma, Matematika Diskrit, Kriptografi, Keamanan Siber",
        "prospek_kerja": "Software Engineer, Web Developer, Mobile Developer, Data Scientist, AI Engineer, Game Developer, Cyber Security Analyst, Ethical Hacker",
        "alasan": "Kamu suka coding, bikin web, bikin aplikasi, bikin game, matematika, otak-atik komputer, atau jadi hacker."
    },
    "teknologi_informasi": {
        "nama": "Teknologi Informasi",
        "emoji": "📡",
        "cocok_untuk": ["jaringan", "network", "server", "infrastruktur", "admin server", "it support", "troubleshooting", "kabel", "wifi", "internet", "router", "switch", "database", "dbadmin", "cloud", "cloud computing", "buat kabel", "crimping", "otak atik jaringan", "instalasi jaringan", "op warnet", "admin warnet", "jaga warnet", "teknisi jaringan", "guru tkj", "ngajar tkj", "tkj"],
        "deskripsi": "Fokus pada jaringan komputer, administrasi server, database, cloud computing, dan IT support.",
        "mata_kuliah": "Jaringan Komputer, Administrasi Server, Database, Keamanan Jaringan, Cloud Computing, Tata Kelola TI",
        "prospek_kerja": "Network Engineer, Database Administrator, IT Support, System Administrator, Cloud Engineer, Teknisi Jaringan, Admin Warnet",
        "alasan": "Kamu suka jaringan, server, cloud, atau otak-atik kabel."
    },
    "bisnis_digital": {
        "nama": "Bisnis Digital",
        "emoji": "📊",
        "cocok_untuk": ["bisnis", "jualan", "entrepreneur", "wirausaha", "startup", "usaha", "marketing", "pemasaran", "dagang", "e-commerce", "toko online", "desain", "design", "ui", "ux", "multimedia", "grafis", "gambar", "konten", "creative", "trading", "saham", "investasi", "crypto", "forex", "analisis pasar", "keuangan", "ekonomi", "akuntansi", "guru", "mengajar", "pendidikan", "dosen", "pengajar", "guru bisnis", "guru pemasaran", "kerja sendiri", "usaha sendiri", "wirausaha"],
        "deskripsi": "Menggabungkan ilmu bisnis dengan teknologi digital, fokus pada e-commerce, digital marketing, dan trading online.",
        "mata_kuliah": "E-commerce, Digital Marketing, Manajemen Startup, UI/UX Design, Content Marketing, Analisis Pasar Digital, Cryptocurrency, Kewirausahaan",
        "prospek_kerja": "Digital Marketer, E-commerce Specialist, Social Media Strategist, Pengusaha Startup, Trader, Financial Analyst, Dosen Bisnis, Guru SMK Pemasaran",
        "alasan": "Kamu suka bisnis, ekonomi, trading, desain, atau ingin kerja sendiri."
    }
}

# =========================
# DETEKSI JAWABAN TERSTRUKTUR (1. guru, 2. depan komputer, 3. jaringan)
# =========================

def deteksi_jawaban_terstruktur(user_input):
    """Deteksi jawaban user dengan format seperti '1.guru, 2.depan komputer, 3.jaringan'"""
    text = user_input.lower()
    
    jawaban = {1: "", 2: "", 3: ""}
    
    # Cari pola 1.xxx, 2.xxx, 3.xxx
    pattern = r'(\d+)[\.\)]\s*([^,;\n]+)'
    matches = re.findall(pattern, text)
    
    for num, value in matches:
        idx = int(num)
        if idx in jawaban:
            jawaban[idx] = value.strip()
    
    # Jika tidak ada jawaban terstruktur, return None
    if not any(jawaban.values()):
        return None
    
    # Ekstrak informasi dari jawaban
    jawaban1 = jawaban.get(1, '')
    jawaban2 = jawaban.get(2, '')
    jawaban3 = jawaban.get(3, '')
    
    # Cek kata kunci
    mau_jadi_guru = any(kata in jawaban1 for kata in ["guru", "mengajar", "ngajar", "pendidik"])
    mau_jadi_hacker = any(kata in jawaban1 for kata in ["hacker", "hengker", "cyber", "keamanan"])
    mau_jadi_op_warnet = any(kata in jawaban1 for kata in ["warnet", "op warnet", "admin warnet"])
    
    suka_depan_komputer = any(kata in jawaban2 for kata in ["komputer", "depan komputer", "pc", "coding"])
    
    minat_jaringan = any(kata in jawaban3 for kata in ["jaringan", "network", "server", "kabel", "wifi", "internet", "router"])
    minat_coding = any(kata in jawaban3 for kata in ["coding", "program", "ngoding", "pemrograman", "software", "aplikasi"])
    minat_bisnis = any(kata in jawaban3 for kata in ["bisnis", "jualan", "marketing", "pemasaran", "e-commerce", "trading", "ekonomi"])
    
    # Rekomendasi berdasarkan jawaban
    if mau_jadi_guru:
        if minat_jaringan:
            return "👨‍🏫 Berdasarkan jawaban kamu:\n\n1️⃣ Cita-cita: Jadi guru\n2️⃣ Suka kerja: Di depan komputer\n3️⃣ Minat bidang: Jaringan\n\n📌 Rekomendasi: 📡 Teknologi Informasi\n\n🎯 Kenapa? Jurusan ini cocok untuk jadi guru TKJ (Teknik Komputer dan Jaringan).\n\n✅ Prospek kerja: Guru SMK TKJ, Instruktur Jaringan, Teknisi IT"
        
        elif minat_coding:
            return "👨‍🏫 Berdasarkan jawaban kamu:\n\n1️⃣ Cita-cita: Jadi guru\n2️⃣ Suka kerja: Di depan komputer\n3️⃣ Minat bidang: Coding\n\n📌 Rekomendasi: 💻 Teknik Informatika\n\n🎯 Kenapa? Jurusan ini cocok untuk jadi guru RPL (Rekayasa Perangkat Lunak).\n\n✅ Prospek kerja: Guru SMK RPL, Dosen, Instruktur Programming"
        
        elif minat_bisnis:
            return "👨‍🏫 Berdasarkan jawaban kamu:\n\n1️⃣ Cita-cita: Jadi guru\n2️⃣ Suka kerja: Di depan komputer\n3️⃣ Minat bidang: Bisnis/Ekonomi\n\n📌 Rekomendasi: 📊 Bisnis Digital\n\n🎯 Kenapa? Jurusan ini cocok untuk jadi guru Pemasaran atau Bisnis Digital.\n\n✅ Prospek kerja: Guru SMK Pemasaran, Dosen Bisnis, Digital Marketer"
        
        else:
            return "👨‍🏫 Berdasarkan jawaban kamu ingin jadi guru.\n\nTapi saya perlu tahu minat kamu di bidang apa:\n• Jaringan → 📡 Teknologi Informasi (jadi guru TKJ)\n• Coding → 💻 Teknik Informatika (jadi guru RPL)\n• Bisnis/Ekonomi → 📊 Bisnis Digital (jadi guru Pemasaran)\n\n📝 Coba tulis ulang dengan format: '1.guru, 2.depan komputer, 3.jaringan'"
    
    if mau_jadi_hacker:
        return "🔒 Rekomendasi: 💻 Teknik Informatika (peminatan Cyber Security)\n\n🎯 Kenapa? Kamu akan belajar Ethical Hacking, Keamanan Jaringan, Kriptografi, dan Pemrograman.\n\n✅ Prospek kerja: Cyber Security Analyst, Ethical Hacker, Security Engineer\n\n⚠️ Ingat: Ilmu hacking digunakan untuk melindungi sistem, bukan merusak!"
    
    if mau_jadi_op_warnet:
        return "🖥️ Rekomendasi: 📡 Teknologi Informasi\n\n🎯 Kenapa? Kamu akan belajar manajemen jaringan, instalasi PC, troubleshooting, dan administrasi server.\n\n✅ Prospek kerja: Admin Warnet, Teknisi Jaringan, IT Support"
    
    if suka_depan_komputer and minat_jaringan:
        return "📡 Rekomendasi: 📡 Teknologi Informasi\n\n🎯 Kenapa? Jurusan ini fokus pada jaringan komputer, administrasi server, database, cloud computing, dan IT support.\n\n✅ Prospek kerja: Network Engineer, IT Support, Cloud Engineer, Teknisi Jaringan"
    
    if suka_depan_komputer and minat_coding:
        return "💻 Rekomendasi: 💻 Teknik Informatika\n\n🎯 Kenapa? Jurusan ini fokus pada pemrograman, pengembangan aplikasi web/mobile, AI, dan game development.\n\n✅ Prospek kerja: Software Engineer, Web Developer, Mobile Developer, Data Scientist"
    
    if suka_depan_komputer and minat_bisnis:
        return "📊 Rekomendasi: 📊 Bisnis Digital\n\n🎯 Kenapa? Jurusan ini menggabungkan bisnis dengan teknologi digital: e-commerce, digital marketing, startup.\n\n✅ Prospek kerja: Digital Marketer, E-commerce Specialist, Pengusaha Startup, Trader"
    
    return None

# =========================
# RESPONSE DENGAN \n UNTUK JS
# =========================

def get_response_bingung():
    return "🤔 Wajar kok bingung pilih jurusan!\n\nCoba jawab beberapa pertanyaan ini ya:\n\n1️⃣ Apa cita-cita atau minat kamu?\n   Contoh: mau jadi hacker, mau jadi guru, mau jadi op warnet, suka coding, suka buat web, suka buat aplikasi, suka buat game, suka jaringan, suka bisnis, suka ekonomi, suka desain\n\n2️⃣ Suka kerja di depan komputer atau berinteraksi dengan orang?\n\n3️⃣ Lebih suka hal teknis (coding/jaringan) atau bisnis/pemasaran?\n\n💡 Contoh cerita:\n   - 'suka buat web' → Teknik Informatika\n   - 'suka buat aplikasi' → Teknik Informatika\n   - 'suka buat game' → Teknik Informatika\n   - 'suka jaringan' → Teknologi Informasi\n   - 'suka bisnis, suka ekonomi, mau usaha sendiri' → Bisnis Digital\n\n📌 Atau kamu bisa sebutkan minatmu, nanti saya rekomendasikan jurusan yang cocok!"

def get_response_gatau_minat():
    return "🤔 Tenang, wajar kok kalau masih bingung dengan minat dan hobi!\n\nYuk, kita cari tahu potensi diri kamu dengan jawab pertanyaan sederhana ini:\n\n📌 Pertanyaan 1: Waktu luang kamu biasa ngapain?\n   A. Main game / buat game\n   B. Bongkar-bongkar HP / komputer\n   C. Jualan online / scroll Shopee\n   D. Desain gambar / edit video / buat website\n   E. Belajar coding / buat aplikasi\n\n📌 Pertanyaan 2: Pelajaran apa yang paling kamu suka di sekolah?\n   A. Matematika / Fisika\n   B. TIK / Komputer / Informatika\n   C. Ekonomi / Bisnis / Akuntansi\n   D. Seni Budaya / Prakarya\n\n📌 Pertanyaan 3: Kalau disuruh kerja, lebih suka:\n   A. Di depan komputer terus (ngoding, desain, dll)\n   B. Keluar lapangan ketemu orang\n   C. Kerja sendiri di rumah / usaha sendiri\n\n💡 Tulis jawaban kamu seperti: 'saya suka buat aplikasi, suka matematika, dan suka di depan komputer'"

# =========================
# REKOMENDASI MINAT KHUSUS (BUAT WEB, APLIKASI, GAME, DLL)
# =========================

def get_rekomendasi_buat_web():
    return "💻 Rekomendasi: Teknik Informatika\n\n📌 Alasan: Kamu suka membuat website. Teknik Informatika akan mengajarkan pemrograman web (frontend & backend) dan pengembangan aplikasi web.\n\n📖 Deskripsi: Fokus pada pemrograman web, pengembangan software, dan teknologi internet.\n\n📚 Mata kuliah:\n   • Pemrograman Web (HTML, CSS, JavaScript)\n   • Backend Development (PHP, Python, Node.js)\n   • Database (MySQL, PostgreSQL)\n   • Framework (Laravel, React, Vue.js)\n\n💼 Prospek kerja: Web Developer, Frontend Developer, Backend Developer, Fullstack Developer"

def get_rekomendasi_buat_aplikasi():
    return "📱 Rekomendasi: Teknik Informatika\n\n📌 Alasan: Kamu suka membuat aplikasi. Teknik Informatika akan mengajarkan pemrograman untuk mengembangkan aplikasi mobile (Android/iOS), desktop, dan web.\n\n📖 Deskripsi: Fokus pada pemrograman, pengembangan software, dan aplikasi mobile.\n\n📚 Mata kuliah:\n   • Mobile Development (Android/iOS)\n   • Pemrograman Desktop\n   • Pemrograman Web\n   • Basis Data\n   • UI/UX Design\n\n💼 Prospek kerja: Mobile Developer, Android Developer, iOS Developer, Software Engineer"

def get_rekomendasi_buat_game():
    return "🎮 Rekomendasi: Teknik Informatika (peminatan Game Development)\n\n📌 Alasan: Kamu suka membuat game. Teknik Informatika dengan peminatan Game Development akan mengajarkan cara membuat game dari nol.\n\n📖 Deskripsi: Fokus pada pengembangan game, animasi, dan pemrograman game.\n\n📚 Mata kuliah:\n   • Game Development\n   • Animasi 3D\n   • Pemrograman Game (Unity, Unreal Engine)\n   • Desain Game\n   • Grafika Komputer\n\n💼 Prospek kerja: Game Developer, Game Programmer, Unity Developer, Game Designer"

def get_rekomendasi_teknik_informatika():
    return "💻 Rekomendasi: Teknik Informatika\n\n📌 Alasan: Kamu suka coding, matematika, otak-atik komputer, bikin web, bikin aplikasi, bikin game, atau jadi hacker. Jurusan ini akan mengasah skill pemrograman dan keamanan sibermu.\n\n📖 Deskripsi: Fokus pada pemrograman, pengembangan software, AI, keamanan siber, dan game development.\n\n📚 Mata kuliah:\n   • Pemrograman Web\n   • Mobile Development\n   • AI dan Machine Learning\n   • Game Development\n   • Struktur Data dan Algoritma\n   • Keamanan Siber\n\n💼 Prospek kerja: Software Engineer, Web Developer, Mobile Developer, Game Developer, Data Scientist, AI Engineer, Cyber Security Analyst"

def get_rekomendasi_teknologi_informasi():
    return "📡 Rekomendasi: Teknologi Informasi\n\n📌 Alasan: Kamu suka jaringan, server, cloud, atau otak-atik kabel. Jurusan ini tepat untukmu yang suka infrastruktur IT.\n\n📖 Deskripsi: Fokus pada jaringan komputer, administrasi server, database, cloud computing, dan IT support.\n\n📚 Mata kuliah:\n   • Jaringan Komputer\n   • Administrasi Server\n   • Database\n   • Cloud Computing\n   • Keamanan Jaringan\n\n💼 Prospek kerja: Network Engineer, Database Administrator, IT Support, Cloud Engineer, Teknisi Jaringan"

def get_rekomendasi_bisnis_digital():
    return "📊 Rekomendasi: Bisnis Digital\n\n📌 Alasan: Kamu suka bisnis, ekonomi, trading, desain, atau ingin kerja sendiri. Jurusan ini akan membekalimu skill digital business.\n\n📖 Deskripsi: Menggabungkan ilmu bisnis dengan teknologi digital, fokus pada e-commerce, digital marketing, dan trading online.\n\n📚 Mata kuliah:\n   • E-commerce\n   • Digital Marketing\n   • Manajemen Startup\n   • UI/UX Design\n   • Kewirausahaan\n   • Analisis Pasar Digital\n\n💼 Prospek kerja: Digital Marketer, E-commerce Specialist, Social Media Strategist, Pengusaha Startup, Trader, Financial Analyst"

def get_rekomendasi_hengker():
    return "🔒 Rekomendasi: 💻 Teknik Informatika (peminatan Cyber Security)\n\n📌 Alasan: Untuk jadi hacker profesional, kamu perlu belajar Ethical Hacking, Keamanan Jaringan, Kriptografi, dan Pemrograman.\n\n✅ Prospek kerja: Cyber Security Analyst, Ethical Hacker, Security Engineer\n\n⚠️ Ingat: Ilmu hacking digunakan untuk melindungi sistem, bukan merusak!"

def get_rekomendasi_op_warnet():
    return "🖥️ Rekomendasi: 📡 Teknologi Informasi\n\n📌 Alasan: Jadi OP Warnet butuh skill manajemen jaringan, instalasi PC, troubleshooting, dan administrasi server.\n\n✅ Prospek kerja: Admin Warnet, Teknisi Jaringan, IT Support"

def get_rekomendasi_guru_rpl():
    return "👨‍🏫 Rekomendasi: 💻 Teknik Informatika\n\n📌 Untuk jadi guru RPL (Rekayasa Perangkat Lunak), kamu perlu menguasai pemrograman, web, mobile, dan database.\n\n✅ Prospek: Guru SMK RPL, Dosen, Instruktur Programming"

def get_rekomendasi_guru_tkj():
    return "👨‍🏫 Rekomendasi: 📡 Teknologi Informasi\n\n📌 Untuk jadi guru TKJ (Teknik Komputer dan Jaringan), kamu perlu menguasai jaringan, server, dan instalasi PC.\n\n✅ Prospek: Guru SMK TKJ, Instruktur Jaringan, Teknisi IT"

def get_rekomendasi_guru_bisnis():
    return "👨‍🏫 Rekomendasi: 📊 Bisnis Digital\n\n📌 Untuk jadi guru Pemasaran atau Bisnis Digital, kamu perlu menguasai e-commerce, digital marketing, dan startup.\n\n✅ Prospek: Guru SMK Pemasaran, Dosen Bisnis, Digital Marketer"

# =========================
# PERSIAPAN KULIAH
# =========================

def get_persiapan_kuliah(jurusan):
    persiapan = {
        "teknik_informatika": "💻 Persiapan masuk Teknik Informatika:\n\n📚 Persiapan Akademik:\n1. Pelajari dasar-dasar pemrograman (Python, JavaScript, atau Java)\n2. Latihan logika dan algoritma\n3. Pelajari konsep matematika dasar\n\n🖥️ Perlengkapan yang Disarankan:\n• Laptop RAM 8GB (rekomendasi 16GB)\n• Prosesor Intel i5/Ryzen 5 ke atas\n• Storage SSD 256GB\n• Software: VS Code, XAMPP, Git, Figma\n\n🎯 Tips: Biasakan coding setiap hari!",
        
        "teknologi_informasi": "📡 Persiapan masuk Teknologi Informasi:\n\n📚 Persiapan Akademik:\n1. Pelajari dasar-dasar jaringan komputer\n2. Kenali sistem operasi (Windows, Linux)\n3. Pelajari dasar-dasar database (SQL)\n\n🖥️ Perlengkapan yang Disarankan:\n• Laptop RAM 8GB\n• Prosesor Intel i3/Ryzen 3 ke atas\n• Storage 256GB\n• Software: Cisco Packet Tracer, VirtualBox, Wireshark\n\n🎯 Tips: Banyak praktik konfigurasi jaringan!",
        
        "bisnis_digital": "📊 Persiapan masuk Bisnis Digital:\n\n📚 Persiapan Akademik:\n1. Pelajari dasar-dasar pemasaran digital\n2. Kenali platform e-commerce (Shopee, Tokopedia, dll)\n3. Pelajari cara membuat konten media sosial\n4. Pelajari dasar-dasar ekonomi dan bisnis\n\n🖥️ Perlengkapan yang Disarankan:\n• Laptop RAM 8GB\n• Prosesor Intel i3/Ryzen 3\n• Storage 256GB\n• Software/aplikasi yang perlu:\n  - Canva atau Adobe Photoshop (desain)\n  - CapCut atau Adobe Premiere (edit video)\n  - Meta Business Suite (kelola social media)\n\n🎯 Tips Tambahan:\n• Mulai buat konten di media sosial\n• Coba jualan online kecil-kecilan\n• Ikuti perkembangan tren digital marketing"
    }
    return persiapan.get(jurusan.lower(), "Jurusan tidak ditemukan. Coba pilih: teknik informatika, teknologi informasi, atau bisnis digital.")

def deteksi_persiapan_kuliah(user_input):
    global _menunggu_jurusan_persiapan
    text = user_input.lower()
    
    kata_persiapan = ["persiapan", "siap", "perlengkapan", "persiapan masuk", "apa yang disiapkan", "syarat masuk"]
    
    # Jika sedang menunggu jawaban jurusan
    if _menunggu_jurusan_persiapan:
        _menunggu_jurusan_persiapan = False
        if "teknik informatika" in text or "ti" in text or "informatika" in text:
            return get_persiapan_kuliah("teknik_informatika")
        elif "teknologi informasi" in text or "jaringan" in text:
            return get_persiapan_kuliah("teknologi_informasi")
        elif "bisnis digital" in text or "bisnis" in text:
            return get_persiapan_kuliah("bisnis_digital")
        else:
            return "📚 Maaf, saya tidak mengenali jurusan tersebut.\n\nSebutkan jurusanmu:\n• Teknik Informatika\n• Teknologi Informasi\n• Bisnis Digital"
    
    # Deteksi awal pertanyaan persiapan
    if any(kata in text for kata in kata_persiapan):
        if "teknik informatika" in text or "ti" in text or "informatika" in text:
            return get_persiapan_kuliah("teknik_informatika")
        elif "teknologi informasi" in text or "jaringan" in text:
            return get_persiapan_kuliah("teknologi_informasi")
        elif "bisnis digital" in text or "bisnis" in text:
            return get_persiapan_kuliah("bisnis_digital")
        else:
            _menunggu_jurusan_persiapan = True
            return "📚 Persiapan kuliah tergantung jurusan yang dipilih.\n\nSebutkan jurusanmu:\n• Teknik Informatika (coding, programming)\n• Teknologi Informasi (jaringan, server)\n• Bisnis Digital (digital marketing, e-commerce)\n\nContoh: 'bisnis digital'"
    
    return None

def get_all_minat(text):
    text_lower = text.lower()
    minat_terdeteksi = []
    for jurusan_key, data in DATA_JURUSAN.items():
        for kata in data["cocok_untuk"]:
            if kata in text_lower:
                if jurusan_key not in minat_terdeteksi:
                    minat_terdeteksi.append(jurusan_key)
                break
    return minat_terdeteksi

# =========================
# FUNGSI UTAMA REKOMENDASI
# =========================

def rekomendasi_dari_pertanyaan(user_input):
    text = user_input.lower()
    
    # PRIORITAS TERTINGGI: Deteksi jawaban terstruktur
    jawaban_terstruktur = deteksi_jawaban_terstruktur(user_input)
    if jawaban_terstruktur:
        return jawaban_terstruktur
    
    # BAPER
    if any(kata in text for kata in ["suka kamu", "suka bot", "baper"]):
        return "☺️ Wah, makasih ya! Tapi jangan baper dulu, yuk fokus cari info kampus! 😊"
    
    # GATAU MINAT
    if any(kata in text for kata in ["gatau", "ga tau", "gada minat", "ga suka apa-apa", "kosong"]):
        return get_response_gatau_minat()
    
    # =========================
    # DETEKSI MINAT KHUSUS (PRIORITAS TINGGI)
    # =========================
    
    # BUAT WEB
    if any(kata in text for kata in ["buat web", "bikin web", "membuat web", "develop web", "web developer", "website", "desain web", "frontend", "backend", "fullstack"]):
        return get_rekomendasi_buat_web()
    
    # BUAT APLIKASI
    if any(kata in text for kata in ["buat aplikasi", "bikin aplikasi", "membuat aplikasi", "develop aplikasi", "bikin app", "buat app", "mobile developer", "android", "ios"]):
        return get_rekomendasi_buat_aplikasi()
    
    # BUAT GAME
    if any(kata in text for kata in ["buat game", "bikin game", "membuat game", "develop game", "game developer"]):
        return get_rekomendasi_buat_game()
    
    # HENGKER
    if any(kata in text for kata in ["hengker", "hacker", "jadi hengker"]):
        return get_rekomendasi_hengker()
    
    # OP WARNET
    if any(kata in text for kata in ["op warnet", "admin warnet", "jadi op warnet"]):
        return get_rekomendasi_op_warnet()
    
    # GURU SPESIFIK
    if "guru rpl" in text or "ngajar rpl" in text:
        return get_rekomendasi_guru_rpl()
    if "guru tkj" in text or "ngajar tkj" in text:
        return get_rekomendasi_guru_tkj()
    if "guru bisnis" in text or "guru pemasaran" in text:
        return get_rekomendasi_guru_bisnis()
    
    # GURU UMUM
    if any(kata in text for kata in ["guru", "jadi guru", "mau jadi guru"]):
        if "rpl" in text:
            return get_rekomendasi_guru_rpl()
        elif "tkj" in text:
            return get_rekomendasi_guru_tkj()
        else:
            return "👨‍🏫 Mau jadi guru?\n\n📌 Guru RPL → 💻 Teknik Informatika\n📌 Guru TKJ → 📡 Teknologi Informasi\n📌 Guru Pemasaran/Bisnis → 📊 Bisnis Digital\n\nSebutkan 'guru rpl' atau 'guru tkj' ya!"
    
    # =========================
    # DETEKSI SEMUA MINAT (MENGHITUNG SKOR)
    # =========================
    
    # Deteksi minat dari Pertanyaan 1 (Waktu luang)
    minat_game = any(kata in text for kata in ["main game", "game", "gaming", "nonton youtube", "nonton", "buat game", "bikin game", "membuat game", "develop game"])
    minat_buat_web = any(kata in text for kata in ["buat web", "bikin web", "membuat web", "develop web", "web developer", "website", "desain web"])
    minat_buat_aplikasi = any(kata in text for kata in ["buat aplikasi", "bikin aplikasi", "membuat aplikasi", "develop aplikasi", "bikin app", "buat app", "mobile developer"])
    minat_bongkar = any(kata in text for kata in ["bongkar hp", "bongkar komputer", "otak atik", "bongkar"])
    minat_jualan = any(kata in text for kata in ["jualan online", "scroll shopee", "jualan", "shopee", "tokopedia", "e-commerce"])
    minat_desain = any(kata in text for kata in ["desain gambar", "edit video", "desain", "gambar", "edit", "ui", "ux"])
    
    # Deteksi minat dari Pertanyaan 2 (Pelajaran favorit)
    minat_matematika = any(kata in text for kata in ["matematika", "fisika", "mtk", "hitungan"])
    minat_tik = any(kata in text for kata in ["tik", "komputer", "informatika", "programming", "coding", "ngoding"])
    minat_ekonomi = any(kata in text for kata in ["ekonomi", "bisnis", "akuntansi", "keuangan", "marketing", "pemasaran"])
    minat_seni = any(kata in text for kata in ["seni budaya", "seni", "prakarya", "kriya"])
    
    # Deteksi minat dari Pertanyaan 3 (Cara kerja)
    minat_depan_komputer = any(kata in text for kata in ["depan komputer", "komputer", "pc", "coding", "ngoding"])
    minat_keluar = any(kata in text for kata in ["keluar lapangan", "ketemu orang", "lapangan", "outdoor"])
    minat_kerja_sendiri = any(kata in text for kata in ["kerja sendiri", "usaha sendiri", "wirausaha", "entrepreneur", "rumah", "sendiri"])
    
    # =========================
    # HITUNG SKOR UNTUK SETIAP JURUSAN
    # =========================
    skor = {
        "teknik_informatika": 0,
        "teknologi_informasi": 0,
        "bisnis_digital": 0
    }
    
    # Penambahan skor untuk Teknik Informatika
    if minat_game or minat_buat_web or minat_buat_aplikasi:
        skor["teknik_informatika"] += 3
    if minat_bongkar:
        skor["teknik_informatika"] += 2
    if minat_matematika:
        skor["teknik_informatika"] += 2
    if minat_tik:
        skor["teknik_informatika"] += 3
    if minat_depan_komputer:
        skor["teknik_informatika"] += 2
    
    # Penambahan skor untuk Teknologi Informasi
    if minat_bongkar:
        skor["teknologi_informasi"] += 2
    if minat_tik:
        skor["teknologi_informasi"] += 3
    if minat_depan_komputer:
        skor["teknologi_informasi"] += 2
    if "jaringan" in text or "network" in text or "server" in text:
        skor["teknologi_informasi"] += 3
    
    # Penambahan skor untuk Bisnis Digital
    if minat_jualan:
        skor["bisnis_digital"] += 2
    if minat_desain:
        skor["bisnis_digital"] += 2
    if minat_ekonomi:
        skor["bisnis_digital"] += 3
    if minat_keluar:
        skor["bisnis_digital"] += 2
    if minat_kerja_sendiri:
        skor["bisnis_digital"] += 3
    if "trading" in text or "saham" in text or "crypto" in text:
        skor["bisnis_digital"] += 2
    
    # =========================
    # TAMPILKAN REKOMENDASI BERDASARKAN SKOR TERTINGGI
    # =========================
    
    # Cari skor tertinggi
    max_skor = max(skor.values())
    
    # Jika ada skor yang sama (imbang), tampilkan semua
    if max_skor > 0:
        jurusan_teratas = [j for j, s in skor.items() if s == max_skor]
        
        # Buat daftar minat yang terdeteksi
        minat_terdeteksi = []
        if minat_game: minat_terdeteksi.append("🎮 main/buat game")
        if minat_buat_web: minat_terdeteksi.append("🌐 buat web")
        if minat_buat_aplikasi: minat_terdeteksi.append("📱 buat aplikasi")
        if minat_bongkar: minat_terdeteksi.append("🔧 bongkar komputer")
        if minat_jualan: minat_terdeteksi.append("🛒 jualan online")
        if minat_desain: minat_terdeteksi.append("🎨 desain")
        if minat_matematika: minat_terdeteksi.append("🧮 matematika")
        if minat_tik: minat_terdeteksi.append("💻 TIK/Komputer")
        if minat_ekonomi: minat_terdeteksi.append("📊 ekonomi/bisnis")
        if minat_seni: minat_terdeteksi.append("🎭 seni budaya")
        if minat_depan_komputer: minat_terdeteksi.append("🖥️ depan komputer")
        if minat_keluar: minat_terdeteksi.append("🚶 keluar lapangan")
        if minat_kerja_sendiri: minat_terdeteksi.append("🏠 kerja sendiri")
        
        minat_str = ", ".join(minat_terdeteksi) if minat_terdeteksi else "minat yang kamu sebutkan"
        
        if len(jurusan_teratas) == 1:
            if jurusan_teratas[0] == "teknik_informatika":
                return f"📊 Analisis minat kamu: {minat_str}\n\n💻 Rekomendasi: Teknik Informatika\n\n📌 Alasan: Jurusan ini paling cocok dengan kombinasi minatmu karena fokus pada pemrograman, pembuatan web, aplikasi, game, dan teknologi.\n\n📖 Deskripsi: Fokus pada pemrograman, pengembangan software, AI, keamanan siber, dan game development.\n\n📚 Mata kuliah:\n   • Pemrograman Web\n   • Mobile Development\n   • Game Development\n   • AI dan Machine Learning\n   • Struktur Data dan Algoritma\n\n💼 Prospek kerja: Software Engineer, Web Developer, Mobile Developer, Game Developer, Data Scientist"
            
            elif jurusan_teratas[0] == "teknologi_informasi":
                return f"📊 Analisis minat kamu: {minat_str}\n\n📡 Rekomendasi: Teknologi Informasi\n\n📌 Alasan: Jurusan ini paling cocok dengan kombinasi minatmu karena fokus pada jaringan komputer dan infrastruktur IT.\n\n📖 Deskripsi: Fokus pada jaringan komputer, administrasi server, database, cloud computing, dan IT support.\n\n📚 Mata kuliah:\n   • Jaringan Komputer\n   • Administrasi Server\n   • Database\n   • Cloud Computing\n   • Keamanan Jaringan\n\n💼 Prospek kerja: Network Engineer, IT Support, Cloud Engineer, Database Administrator"
            
            elif jurusan_teratas[0] == "bisnis_digital":
                return f"📊 Analisis minat kamu: {minat_str}\n\n📊 Rekomendasi: Bisnis Digital\n\n📌 Alasan: Jurusan ini paling cocok dengan kombinasi minatmu karena fokus pada bisnis, ekonomi, digital marketing, dan kewirausahaan.\n\n📖 Deskripsi: Menggabungkan ilmu bisnis dengan teknologi digital, fokus pada e-commerce, digital marketing, dan trading online.\n\n📚 Mata kuliah:\n   • E-commerce\n   • Digital Marketing\n   • Manajemen Startup\n   • Kewirausahaan\n   • Analisis Pasar Digital\n\n💼 Prospek kerja: Digital Marketer, E-commerce Specialist, Pengusaha Startup, Financial Analyst, Trader"
        
        else:
            rekom_list = []
            if "teknik_informatika" in jurusan_teratas:
                rekom_list.append("💻 Teknik Informatika (coding, web, aplikasi, game, AI)")
            if "teknologi_informasi" in jurusan_teratas:
                rekom_list.append("📡 Teknologi Informasi (jaringan, server, IT support)")
            if "bisnis_digital" in jurusan_teratas:
                rekom_list.append("📊 Bisnis Digital (bisnis online, digital marketing, startup)")
            
            return f"📊 Analisis minat kamu: {minat_str}\n\n🎯 Berdasarkan minatmu, ada beberapa jurusan yang cocok:\n\n" + "\n".join(rekom_list) + "\n\nKamu tertarik dengan yang mana? Coba tanyakan lebih detail tentang jurusannya ya!"
    
    # BINGUNG PILIH JURUSAN
    if any(kata in text for kata in ["bingung", "rekomendasi jurusan", "pilih jurusan", "jurusan apa"]):
        return get_response_bingung()
    
    return None

def get_info_jurusan(jurusan_nama):
    for key, data in DATA_JURUSAN.items():
        if jurusan_nama.lower() in data['nama'].lower():
            return f"{data['emoji']} {data['nama']}\n\n📖 Deskripsi: {data['deskripsi']}\n\n📚 Mata kuliah: {data['mata_kuliah']}\n\n💼 Prospek kerja: {data['prospek_kerja']}"
    return None