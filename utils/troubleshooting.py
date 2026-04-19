from .context import context

def jawaban_sudah(text):
    text_lower = text.lower()
    kata_sudah = [
        "sudah", "bisa", "iya", "ya", "y", "berhasil", 
        "ok", "oke", "okey", "siap", "done", "selesai",
        "udah", "udh", "sdh", "beres", "berhasil", "lancar",
        "bisa login", "masuk", "berhasil login"
    ]
    return any(kata in text_lower for kata in kata_sudah)

def jawaban_belum(text):
    text_lower = text.lower()
    kata_belum = [
        "belum", "tidak", "nggak", "gak", "ga", "g", "gk", "gx",
        "blm", "blum", "masih", "error", "gagal", "tidak bisa",
        "ga bisa", "gak bisa", "nggak bisa", "belum bisa",
        "belum berhasil", "gagal login", "tidak masuk"
    ]
    return any(kata in text_lower for kata in kata_belum)

def jawaban_ya(text):
    text_lower = text.lower()
    kata_ya = [
        "ya", "iya", "iy", "y", 
        "ada", "ada yang mau ditanyakan", "ada pertanyaan", "ada yang ingin ditanyakan",
        "mau", "mau nanya", "mau tanya", "pengen nanya",
        "tanya", "pertanyaan", "ada yang mau ditanya",
        "tolong", "bisa", "boleh", "siap", "ok", "oke",
        "ada pertanyaan lagi", "masih ada"
    ]
    return any(kata in text_lower for kata in kata_ya)

def jawaban_tidak(text):
    text_lower = text.lower()
    kata_tidak = [
        "tidak", "tidak ada", "tidak mau", "tidak ingin",
        "nggak", "gak", "ga", "g", "gk", "gx",
        "gada", "gk ada", "gak ada", "nggak ada", "ga ada",
        "gk ad", "gak ad", "nggak ad", "gada yang mau ditanyakan",
        "g ada", "tidak ada pertanyaan", "ngga ada",
        "selesai", "cukup", "itu saja", "udah", "sudah",
        "tidak perlu", "ga perlu", "gak perlu", "tidak ada yang mau ditanya",
        "ga ada pertanyaan", "gak ada pertanyaan", "nggak ada pertanyaan",
        "gada pertanyaan", "kosong", "habis", "beres",
        "gak ada yang ditanya", "ga ada yang ditanya", "nggak ada yang ditanya",
        "tidak ada yang ditanya", "gada lagi", "ga ada lagi", "gk ada lagi"
    ]
    return any(kata in text_lower for kata in kata_tidak)

def reset_troubleshoot():
    context["troubleshoot_step"] = 0
    context["troubleshoot_type"] = None
    context["waiting_for_follow_up"] = False


def handle_follow_up(user_input):
    if context.get("waiting_for_follow_up", False):
        if jawaban_ya(user_input):
            context["waiting_for_follow_up"] = False
            return "Silakan tanyakan apa yang ingin Anda ketahui. Saya siap membantu! 😊\n\n💡 Contoh: biaya kuliah, jadwal kuliah, rekomendasi jurusan, persiapan kuliah, dll."
        elif jawaban_tidak(user_input):
            context["waiting_for_follow_up"] = False
            return "Baik, terima kasih sudah menggunakan PENUSA Bot. 😊\n\nJika ada pertanyaan lain, silakan tanyakan kapan saja. Semoga membantu!"
        else:
            return "Maaf, saya kurang paham. Silakan jawab **'ada'** jika masih ada pertanyaan, atau **'tidak'** jika sudah selesai.\n\n❓ Ada yang lain ingin ditanyakan? (jawab 'ada' atau 'tidak')"
    return None


def troubleshoot_login(user_input):
    step = context.get("troubleshoot_step", 0)
    
    if step == 0:
        context["troubleshoot_step"] = 1
        context["troubleshoot_type"] = "login"
        return "🔐 **Masalah Login SIAKAD - Langkah 1/5**\n\n✅ Saran: Pastikan NIM/Email dan password yang Anda masukkan sudah benar. Password bersifat case sensitive (huruf besar/kecil dibedakan).\n\n⚠️ Periksa juga:\n• Caps Lock tidak aktif\n• Tidak ada spasi di awal atau akhir\n• Coba login menggunakan NIM (bukan email) atau sebaliknya\n\n❓ Apakah sudah bisa login? (jawab: 'sudah' atau 'belum')"
    
    elif step == 1:
        if jawaban_sudah(user_input):
            reset_troubleshoot()
            context["waiting_for_follow_up"] = True
            return "✅ **Bagus!** Masalah login Anda sudah terselesaikan. 😊\n\n❓ Ada yang lain ingin ditanyakan? (jawab 'ada' atau 'tidak')"
        elif jawaban_belum(user_input):
            context["troubleshoot_step"] = 2
            return "🔐 **Masalah Login SIAKAD - Langkah 2/5**\n\n✅ Saran: Coba gunakan fitur 'Lupa Password' di halaman login SIAKAD.\n\n📋 Langkah-langkah:\n1. Buka halaman login SIAKAD\n2. Klik tombol 'Lupa Password'\n3. Masukkan email atau NIM yang terdaftar\n4. Klik 'Kirim'\n5. Cek email Anda untuk tautan reset password\n6. Buat password baru (minimal 8 karakter, kombinasi huruf dan angka)\n\n⚠️ Jika tidak menerima email, cek folder Spam atau junk mail.\n\n❓ Apakah sudah bisa login setelah reset password? (jawab: 'sudah' atau 'belum')"
        else:
            return "Maaf, saya kurang paham. Silakan jawab dengan **'sudah'** jika berhasil, atau **'belum'** jika masih gagal.\n\n❓ Apakah sudah bisa login? (jawab: 'sudah' atau 'belum')"
    
    elif step == 2:
        if jawaban_sudah(user_input):
            reset_troubleshoot()
            context["waiting_for_follow_up"] = True
            return "✅ **Bagus!** Masalah login Anda sudah terselesaikan. 😊\n\n❓ Ada yang lain ingin ditanyakan? (jawab 'ada' atau 'tidak')"
        elif jawaban_belum(user_input):
            context["troubleshoot_step"] = 3
            return "🔐 **Masalah Login SIAKAD - Langkah 3/5**\n\n✅ Saran: Bersihkan cache browser atau gunakan mode incognito/private window.\n\n📋 Cara membersihkan cache:\n• **Chrome**: Ctrl+Shift+Delete → Pilih 'Gambar dan file' → Hapus data\n• **Firefox**: Ctrl+Shift+Delete → Pilih 'Cache' → Hapus\n• **Edge**: Ctrl+Shift+Delete → Pilih 'Cache' → Hapus\n\n💡 Atau gunakan mode incognito (Chrome: Ctrl+Shift+N, Firefox: Ctrl+Shift+P)\n\n❓ Apakah sudah bisa login setelah membersihkan cache? (jawab: 'sudah' atau 'belum')"
        else:
            return "Maaf, saya kurang paham. Silakan jawab dengan **'sudah'** jika berhasil, atau **'belum'** jika masih gagal.\n\n❓ Apakah sudah bisa login setelah reset password? (jawab: 'sudah' atau 'belum')"
    
    elif step == 3:
        if jawaban_sudah(user_input):
            reset_troubleshoot()
            context["waiting_for_follow_up"] = True
            return "✅ **Bagus!** Masalah login Anda sudah terselesaikan. 😊\n\n❓ Ada yang lain ingin ditanyakan? (jawab 'ada' atau 'tidak')"
        elif jawaban_belum(user_input):
            context["troubleshoot_step"] = 4
            return "🔐 **Masalah Login SIAKAD - Langkah 4/5**\n\n✅ Saran: Coba gunakan jaringan internet yang berbeda.\n\n📋 Yang bisa dicoba:\n• Ganti dari WiFi ke data seluler (atau sebaliknya)\n• Restart modem/router WiFi\n• Coba akses dari tempat dengan sinyal lebih stabil\n\n❓ Apakah sudah bisa login setelah mengganti jaringan? (jawab: 'sudah' atau 'belum')"
        else:
            return "Maaf, saya kurang paham. Silakan jawab dengan **'sudah'** jika berhasil, atau **'belum'** jika masih gagal.\n\n❓ Apakah sudah bisa login setelah membersihkan cache? (jawab: 'sudah' atau 'belum')"
    
    elif step == 4:
        if jawaban_sudah(user_input):
            reset_troubleshoot()
            context["waiting_for_follow_up"] = True
            return "✅ **Bagus!** Masalah login Anda sudah terselesaikan. 😊\n\n❓ Ada yang lain ingin ditanyakan? (jawab 'ada' atau 'tidak')"
        elif jawaban_belum(user_input):
            context["troubleshoot_step"] = 5
            return "🔐 **Masalah Login SIAKAD - Langkah 5/5 (Terakhir)**\n\n✅ Saran: Coba akses dari perangkat yang berbeda.\n\n📋 Coba login menggunakan:\n• HP/komputer lain\n• Browser yang berbeda (Chrome, Firefox, Edge)\n• Aplikasi EdLink (download di Play Store/App Store)\n\n❓ Apakah sudah bisa login dari perangkat lain? (jawab: 'sudah' atau 'belum')"
        else:
            return "Maaf, saya kurang paham. Silakan jawab dengan **'sudah'** jika berhasil, atau **'belum'** jika masih gagal.\n\n❓ Apakah sudah bisa login setelah mengganti jaringan? (jawab: 'sudah' atau 'belum')"
    
    elif step == 5:
        if jawaban_sudah(user_input):
            reset_troubleshoot()
            context["waiting_for_follow_up"] = True
            return "✅ **Bagus!** Masalah login Anda sudah terselesaikan. 😊\n\n❓ Ada yang lain ingin ditanyakan? (jawab 'ada' atau 'tidak')"
        else:
            reset_troubleshoot()
            context["waiting_for_follow_up"] = True
            return "⚠️ **Mohon maaf, saya sudah memberikan semua langkah yang bisa saya bantu.**\n\nKarena masalah masih belum terselesaikan, silakan:\n\n📞 **Hubungi admin kampus**\n🌐 Website: <a href='https://pmb.pelitanusantara.ac.id' target='_blank'>pmb.pelitanusantara.ac.id</a>\n\n📍 **Atau datang langsung ke kampus**\n• Kampus 1: Jl. Iskandar Muda No. 1 Medan\n• Kampus 2: Jl. Lintas Sumatera, Tj. Garbus Satu, Lubuk Pakam\n🕒 Jam operasional: Senin-Jumat, 08.00-16.00 WIB\n\n💡 **Tips:** Jangan lupa bawa kartu mahasiswa atau identitas diri untuk verifikasi data.\n\n❓ Ada yang lain ingin ditanyakan? (jawab 'ada' atau 'tidak')"


def troubleshoot_lupa_password(user_input):
    step = context.get("troubleshoot_step", 0)
    
    if step == 0:
        context["troubleshoot_step"] = 1
        context["troubleshoot_type"] = "lupa_password"
        return "🔑 **Lupa Password - Langkah 1/3**\n\n✅ Saran: Gunakan fitur 'Lupa Password' di halaman login SIAKAD.\n\n📋 Langkah-langkah:\n1. Buka halaman login SIAKAD\n2. Klik tombol 'Lupa Password'\n3. Masukkan email atau NIM yang terdaftar\n4. Klik 'Kirim'\n5. Cek email Anda untuk tautan reset password\n6. Buat password baru (minimal 8 karakter, kombinasi huruf, angka, dan simbol)\n\n⚠️ Jika tidak menerima email, cek folder Spam atau junk mail.\n\n❓ Apakah sudah berhasil reset password? (jawab: 'sudah' atau 'belum')"
    
    elif step == 1:
        if jawaban_sudah(user_input):
            reset_troubleshoot()
            context["waiting_for_follow_up"] = True
            return "✅ **Bagus!** Password Anda sudah berhasil direset. Silakan login dengan password baru.\n\n❓ Ada yang lain ingin ditanyakan? (jawab 'ada' atau 'tidak')"
        elif jawaban_belum(user_input):
            context["troubleshoot_step"] = 2
            return "🔑 **Lupa Password - Langkah 2/3**\n\n✅ Saran: Pastikan email atau NIM yang Anda masukkan sudah benar dan terdaftar di sistem.\n\n📋 Cek kembali:\n• Email yang digunakan saat pendaftaran\n• NIM yang tertera di kartu mahasiswa\n\n❓ Apakah sudah memasukkan email/NIM yang benar? (jawab: 'sudah' atau 'belum')"
        else:
            return "Maaf, saya kurang paham. Silakan jawab dengan **'sudah'** jika berhasil, atau **'belum'** jika masih gagal.\n\n❓ Apakah sudah berhasil reset password? (jawab: 'sudah' atau 'belum')"
    
    elif step == 2:
        if jawaban_sudah(user_input):
            context["troubleshoot_step"] = 1
            return troubleshoot_lupa_password(user_input)
        elif jawaban_belum(user_input):
            context["troubleshoot_step"] = 3
            return "🔑 **Lupa Password - Langkah 3/3 (Terakhir)**\n\n✅ Saran: Hubungi admin kampus untuk reset password secara manual.\n\n📋 Yang perlu disiapkan saat menghubungi admin:\n• Nama lengkap\n• NIM\n• Program studi\n• Nomor HP aktif\n• Kartu mahasiswa (sebagai bukti)\n\n📞 **Kontak admin:**\n🌐 Website: <a href='https://pmb.pelitanusantara.ac.id' target='_blank'>pmb.pelitanusantara.ac.id</a>\n\n📍 **Atau datang langsung ke kampus:**\n• Kampus 1: Jl. Iskandar Muda No. 1 Medan\n• Kampus 2: Jl. Lintas Sumatera, Tj. Garbus Satu, Lubuk Pakam\n🕒 Jam operasional: Senin-Jumat, 08.00-16.00 WIB\n\n💡 Admin akan memverifikasi identitas Anda dan mereset password akun.\n\n❓ Ada yang lain ingin ditanyakan? (jawab 'ada' atau 'tidak')"
        else:
            return "Maaf, saya kurang paham. Silakan jawab dengan **'sudah'** jika sudah benar, atau **'belum'** jika masih salah.\n\n❓ Apakah sudah memasukkan email/NIM yang benar? (jawab: 'sudah' atau 'belum')"
    
    elif step == 3:
        reset_troubleshoot()
        context["waiting_for_follow_up"] = True
        return "✅ **Baik, semoga segera teratasi.** 😊\n\n❓ Ada yang lain ingin ditanyakan? (jawab 'ada' atau 'tidak')"


def troubleshoot_krs(user_input):
    step = context.get("troubleshoot_step", 0)
    
    if step == 0:
        context["troubleshoot_step"] = 1
        context["troubleshoot_type"] = "krs"
        return "📋 **KRS Tidak Bisa Diisi - Langkah 1/4**\n\n✅ Saran: Pastikan periode pengisian KRS sedang dibuka.\n\n📋 Informasi:\n• Pengisian KRS biasanya dibuka 1-2 minggu sebelum perkuliahan dimulai\n• Cek jadwal pengisian KRS di SIAKAD atau pengumuman kampus\n\n❓ Apakah periode pengisian KRS sedang dibuka? (jawab: 'sudah' atau 'belum')"
    
    elif step == 1:
        if jawaban_belum(user_input):
            reset_troubleshoot()
            context["waiting_for_follow_up"] = True
            return "📋 **Tunggu periode pengisian KRS dibuka.**\n\nInformasi jadwal pengisian KRS biasanya diumumkan melalui:\n• SIAKAD\n• Papan pengumuman kampus\n• Grup WhatsApp kelas\n\nPantau secara berkala agar tidak ketinggalan.\n\n❓ Ada yang lain ingin ditanyakan? (jawab 'ada' atau 'tidak')"
        elif jawaban_sudah(user_input):
            context["troubleshoot_step"] = 2
            return "📋 **KRS Tidak Bisa Diisi - Langkah 2/4**\n\n✅ Saran: Pastikan Anda sudah login ke SIAKAD dengan benar.\n\n📋 Cek:\n• NIM dan password benar\n• Tidak ada masalah login\n• Koneksi internet stabil\n\n❓ Apakah Anda sudah berhasil login ke SIAKAD? (jawab: 'sudah' atau 'belum')"
        else:
            return "Maaf, saya kurang paham. Silakan jawab dengan **'sudah'** jika periode sedang dibuka, atau **'belum'** jika belum.\n\n❓ Apakah periode pengisian KRS sedang dibuka? (jawab: 'sudah' atau 'belum')"
    
    elif step == 2:
        if jawaban_belum(user_input):
            context["troubleshoot_step"] = 0
            return troubleshoot_login(user_input)
        elif jawaban_sudah(user_input):
            context["troubleshoot_step"] = 3
            return "📋 **KRS Tidak Bisa Diisi - Langkah 3/4**\n\n✅ Saran: Pastikan Anda belum melebihi batas maksimal SKS.\n\n📋 Informasi:\n• Maksimal SKS per semester biasanya 24 SKS\n• Cek jumlah SKS yang sudah diambil\n• Jika sudah 24 SKS, tidak bisa tambah mata kuliah lagi\n\n❓ Apakah jumlah SKS yang diambil masih di bawah batas maksimal? (jawab: 'sudah' atau 'belum')"
        else:
            return "Maaf, saya kurang paham. Silakan jawab dengan **'sudah'** jika sudah login, atau **'belum'** jika belum.\n\n❓ Apakah Anda sudah berhasil login ke SIAKAD? (jawab: 'sudah' atau 'belum')"
    
    elif step == 3:
        if jawaban_belum(user_input):
            context["troubleshoot_step"] = 4
            return "📋 **KRS Tidak Bisa Diisi - Langkah 4/4 (Terakhir)**\n\n✅ Saran: Coba konsultasikan dengan dosen pembimbing akademik (PA).\n\n📋 Hal yang bisa dibantu dosen PA:\n• Membuka blokir pengisian KRS\n• Memberi rekomendasi mata kuliah\n• Membantu jika ada kendala teknis\n\n❓ Apakah sudah konsultasi dengan dosen PA? (jawab: 'sudah' atau 'belum')"
        elif jawaban_sudah(user_input):
            reset_troubleshoot()
            context["waiting_for_follow_up"] = True
            return "✅ **Bagus!** Jika masih di bawah batas, seharusnya bisa mengisi KRS.\n\nCoba refresh halaman SIAKAD atau logout lalu login kembali.\n\n❓ Ada yang lain ingin ditanyakan? (jawab 'ada' atau 'tidak')"
        else:
            reset_troubleshoot()
            context["waiting_for_follow_up"] = True
            return "📋 **Silakan cek jumlah SKS Anda di SIAKAD.**\n\nJika sudah melebihi batas, Anda harus membatalkan beberapa mata kuliah terlebih dahulu.\n\n❓ Ada yang lain ingin ditanyakan? (jawab 'ada' atau 'tidak')"
    
    elif step == 4:
        if jawaban_sudah(user_input):
            reset_troubleshoot()
            context["waiting_for_follow_up"] = True
            return "⚠️ **Mohon maaf, saya sudah memberikan semua langkah yang bisa saya bantu.**\n\nKarena masalah masih belum terselesaikan, silakan:\n\n📞 **Hubungi bagian akademik**\n🌐 Website: <a href='https://pmb.pelitanusantara.ac.id' target='_blank'>pmb.pelitanusantara.ac.id</a>\n\n📍 **Atau datang langsung ke kampus**\n• Kampus 1: Jl. Iskandar Muda No. 1 Medan\n• Kampus 2: Jl. Lintas Sumatera, Tj. Garbus Satu, Lubuk Pakam\n🕒 Jam operasional: Senin-Jumat, 08.00-16.00 WIB\n\n💡 Petugas akademik akan membantu pengisian KRS secara manual.\n\n❓ Ada yang lain ingin ditanyakan? (jawab 'ada' atau 'tidak')"
        else:
            reset_troubleshoot()
            context["waiting_for_follow_up"] = True
            return "📋 **Silakan konsultasi dengan dosen pembimbing akademik (PA) Anda.**\n\nDosen PA dapat membantu:\n• Membuka blokir pengisian KRS\n• Memberikan solusi jika ada kendala teknis\n\nJika sudah konsultasi tapi masih tidak bisa, hubungi bagian akademik.\n\n📞 Kontak akademik tersedia di website <a href='https://pmb.pelitanusantara.ac.id' target='_blank'>pmb.pelitanusantara.ac.id</a>\n\n❓ Ada yang lain ingin ditanyakan? (jawab 'ada' atau 'tidak')"


def troubleshoot_nilai(user_input):
    step = context.get("troubleshoot_step", 0)
    
    if step == 0:
        context["troubleshoot_step"] = 1
        context["troubleshoot_type"] = "nilai"
        return "📊 **Nilai Tidak Muncul - Langkah 1/4**\n\n✅ Saran: Pastikan periode pengumuman nilai sudah tiba.\n\n📋 Informasi:\n• Nilai biasanya keluar 2-4 minggu setelah ujian akhir semester\n• Cek jadwal pengumuman nilai di kalender akademik\n\n❓ Apakah sudah melewati batas waktu pengumuman nilai? (jawab: 'sudah' atau 'belum')"
    
    elif step == 1:
        if jawaban_belum(user_input):
            reset_troubleshoot()
            context["waiting_for_follow_up"] = True
            return "📊 **Silakan tunggu hingga periode pengumuman nilai tiba.**\n\nPantau SIAKAD secara berkala. Biasanya nilai keluar 2-4 minggu setelah ujian akhir semester.\n\nCek kalender akademik di SIAKAD untuk jadwal pastinya.\n\n❓ Ada yang lain ingin ditanyakan? (jawab 'ada' atau 'tidak')"
        elif jawaban_sudah(user_input):
            context["troubleshoot_step"] = 2
            return "📊 **Nilai Tidak Muncul - Langkah 2/4**\n\n✅ Saran: Coba refresh halaman atau logout lalu login kembali ke SIAKAD.\n\n📋 Terkadang data nilai perlu di-refresh untuk muncul.\n\n❓ Setelah refresh, apakah nilai sudah muncul? (jawab: 'sudah' atau 'belum')"
        else:
            return "Maaf, saya kurang paham. Silakan jawab dengan **'sudah'** jika sudah melewati batas waktu, atau **'belum'** jika masih dalam batas waktu.\n\n❓ Apakah sudah melewati batas waktu pengumuman nilai? (jawab: 'sudah' atau 'belum')"
    
    elif step == 2:
        if jawaban_sudah(user_input):
            reset_troubleshoot()
            context["waiting_for_follow_up"] = True
            return "✅ **Bagus!** Nilai Anda sudah muncul. 😊\n\n❓ Ada yang lain ingin ditanyakan? (jawab 'ada' atau 'tidak')"
        elif jawaban_belum(user_input):
            context["troubleshoot_step"] = 3
            return "📊 **Nilai Tidak Muncul - Langkah 3/4**\n\n✅ Saran: Cek apakah mata kuliah yang nilainya tidak muncul masih dalam proses penilaian.\n\n📋 Beberapa kemungkinan:\n• Dosen belum selesai mengoreksi ujian\n• Nilai masih dalam proses validasi oleh program studi\n• Ada masalah teknis pada sistem\n\n❓ Apakah nilai mata kuliah lain sudah muncul? (jawab: 'sudah' atau 'belum')"
        else:
            return "Maaf, saya kurang paham. Silakan jawab dengan **'sudah'** jika nilai sudah muncul, atau **'belum'** jika belum.\n\n❓ Setelah refresh, apakah nilai sudah muncul? (jawab: 'sudah' atau 'belum')"
    
    elif step == 3:
        if jawaban_belum(user_input):
            context["troubleshoot_step"] = 4
            return "📊 **Nilai Tidak Muncul - Langkah 4/4 (Terakhir)**\n\n✅ Saran: Hubungi dosen pengampu mata kuliah yang bersangkutan.\n\n📋 Informasi yang perlu disampaikan ke dosen:\n• Nama mata kuliah\n• Semester\n• Kelas\n\n❓ Apakah sudah menghubungi dosen? (jawab: 'sudah' atau 'belum')"
        elif jawaban_sudah(user_input):
            context["troubleshoot_step"] = 4
            return "📊 **Nilai Tidak Muncul - Langkah 4/4 (Terakhir)**\n\n✅ Saran: Hubungi dosen pengampu mata kuliah yang nilainya belum muncul.\n\n📋 Informasi yang perlu disampaikan ke dosen:\n• Nama mata kuliah\n• Semester\n• Kelas\n\n❓ Apakah sudah menghubungi dosen? (jawab: 'sudah' atau 'belum')"
        else:
            return "Maaf, saya kurang paham. Silakan jawab dengan **'sudah'** jika nilai lain sudah muncul, atau **'belum'** jika semua belum muncul.\n\n❓ Apakah nilai mata kuliah lain sudah muncul? (jawab: 'sudah' atau 'belum')"
    
    elif step == 4:
        if jawaban_sudah(user_input):
            reset_troubleshoot()
            context["waiting_for_follow_up"] = True
            return "⚠️ **Mohon maaf, saya sudah memberikan semua langkah yang bisa saya bantu.**\n\nJika sudah menghubungi dosen tapi nilai masih belum muncul, silakan:\n\n📞 **Hubungi bagian akademik**\n🌐 Website: <a href='https://pmb.pelitanusantara.ac.id' target='_blank'>pmb.pelitanusantara.ac.id</a>\n\n📍 **Atau datang langsung ke kampus**\n• Kampus 1: Jl. Iskandar Muda No. 1 Medan\n• Kampus 2: Jl. Lintas Sumatera, Tj. Garbus Satu, Lubuk Pakam\n🕒 Jam operasional: Senin-Jumat, 08.00-16.00 WIB\n\n💡 Petugas akademik akan membantu mengecek nilai Anda.\n\n❓ Ada yang lain ingin ditanyakan? (jawab 'ada' atau 'tidak')"
        else:
            reset_troubleshoot()
            context["waiting_for_follow_up"] = True
            return "📞 **Silakan hubungi dosen pengampu mata kuliah yang bersangkutan.**\n\nDosen dapat memberikan informasi:\n• Apakah nilai sudah diinput\n• Kapan nilai akan keluar\n• Jika ada kendala teknis\n\nJika sudah hubungi dosen tapi masih belum ada perubahan, hubungi bagian akademik.\n\n📞 Kontak akademik tersedia di website <a href='https://pmb.pelitanusantara.ac.id' target='_blank'>pmb.pelitanusantara.ac.id</a>\n\n❓ Ada yang lain ingin ditanyakan? (jawab 'ada' atau 'tidak')"


def troubleshoot_siakad_error(user_input):
    step = context.get("troubleshoot_step", 0)
    
    if step == 0:
        context["troubleshoot_step"] = 1
        context["troubleshoot_type"] = "siakad_error"
        return "⚠️ **Error SIAKAD - Langkah 1/4**\n\n✅ Saran: Coba refresh halaman (tekan F5 atau Ctrl+R). Terkadang error hanya karena loading yang tidak sempurna.\n\n❓ Apakah SIAKAD sudah bisa diakses? (jawab: 'sudah' atau 'belum')"
    
    elif step == 1:
        if jawaban_sudah(user_input):
            reset_troubleshoot()
            context["waiting_for_follow_up"] = True
            return "✅ **Bagus!** SIAKAD sudah bisa diakses. 😊\n\n❓ Ada yang lain ingin ditanyakan? (jawab 'ada' atau 'tidak')"
        elif jawaban_belum(user_input):
            context["troubleshoot_step"] = 2
            return "⚠️ **Error SIAKAD - Langkah 2/4**\n\n✅ Saran: Bersihkan cache dan cookies browser.\n\n📋 Cara: Ctrl+Shift+Delete → Pilih 'Cache' dan 'Cookies' → Hapus data\n\n💡 Alternatif: Gunakan mode incognito/private window.\n\n❓ Apakah SIAKAD sudah bisa diakses? (jawab: 'sudah' atau 'belum')"
        else:
            return "Maaf, saya kurang paham. Silakan jawab dengan **'sudah'** jika bisa, atau **'belum'** jika masih error.\n\n❓ Apakah SIAKAD sudah bisa diakses? (jawab: 'sudah' atau 'belum')"
    
    elif step == 2:
        if jawaban_sudah(user_input):
            reset_troubleshoot()
            context["waiting_for_follow_up"] = True
            return "✅ **Bagus!** SIAKAD sudah bisa diakses. 😊\n\n❓ Ada yang lain ingin ditanyakan? (jawab 'ada' atau 'tidak')"
        elif jawaban_belum(user_input):
            context["troubleshoot_step"] = 3
            return "⚠️ **Error SIAKAD - Langkah 3/4**\n\n✅ Saran: Coba akses dari browser lain (Chrome, Firefox, Edge) atau dari perangkat lain (HP/komputer berbeda).\n\n❓ Apakah SIAKAD sudah bisa diakses? (jawab: 'sudah' atau 'belum')"
        else:
            return "Maaf, saya kurang paham. Silakan jawab dengan **'sudah'** jika bisa, atau **'belum'** jika masih error.\n\n❓ Apakah SIAKAD sudah bisa diakses? (jawab: 'sudah' atau 'belum')"
    
    elif step == 3:
        if jawaban_sudah(user_input):
            reset_troubleshoot()
            context["waiting_for_follow_up"] = True
            return "✅ **Bagus!** SIAKAD sudah bisa diakses. 😊\n\n❓ Ada yang lain ingin ditanyakan? (jawab 'ada' atau 'tidak')"
        elif jawaban_belum(user_input):
            context["troubleshoot_step"] = 4
            return "⚠️ **Error SIAKAD - Langkah 4/4 (Terakhir)**\n\n✅ Saran: Coba gunakan jaringan internet yang berbeda.\n\n❓ Apakah SIAKAD sudah bisa diakses? (jawab: 'sudah' atau 'belum')"
        else:
            return "Maaf, saya kurang paham. Silakan jawab dengan **'sudah'** jika bisa, atau **'belum'** jika masih error.\n\n❓ Apakah SIAKAD sudah bisa diakses? (jawab: 'sudah' atau 'belum')"
    
    elif step == 4:
        if jawaban_sudah(user_input):
            reset_troubleshoot()
            context["waiting_for_follow_up"] = True
            return "✅ **Bagus!** SIAKAD sudah bisa diakses. 😊\n\n❓ Ada yang lain ingin ditanyakan? (jawab 'ada' atau 'tidak')"
        else:
            reset_troubleshoot()
            context["waiting_for_follow_up"] = True
            return "⚠️ **Mohon maaf, saya sudah memberikan semua langkah yang bisa saya bantu.**\n\nKemungkinan SIAKAD sedang dalam masa maintenance atau ada gangguan server. Silakan coba beberapa saat lagi.\n\nJika masalah berlanjut, silakan hubungi admin kampus:\n🌐 <a href='https://pmb.pelitanusantara.ac.id' target='_blank'>pmb.pelitanusantara.ac.id</a>\n\n📍 Atau datang langsung ke administrasi kampus.\n\n❓ Ada yang lain ingin ditanyakan? (jawab 'ada' atau 'tidak')"


def troubleshoot_gagal_daftar(user_input):
    step = context.get("troubleshoot_step", 0)
    
    if step == 0:
        context["troubleshoot_step"] = 1
        context["troubleshoot_type"] = "gagal_daftar"
        return "📝 **Gagal Mendaftar - Langkah 1/4**\n\n✅ Saran: Pastikan semua berkas yang diupload sudah lengkap.\n\n📋 Berkas yang diperlukan:\n• Ijazah/SKHU/SKTL (2 lembar)\n• KTP (2 lembar)\n• KK (2 lembar)\n• Pas foto 3x4 (2 lembar)\n\n❓ Apakah berkas sudah lengkap? (jawab: 'sudah' atau 'belum')"
    
    elif step == 1:
        if jawaban_belum(user_input):
            reset_troubleshoot()
            context["waiting_for_follow_up"] = True
            return "📋 **Silakan lengkapi berkas yang kurang.**\n\nPendaftaran online bisa dilakukan di:\n🌐 <a href='https://pmb.pelitanusantara.ac.id' target='_blank'>pmb.pelitanusantara.ac.id</a>\n\nPastikan semua berkas sudah siap sebelum mendaftar.\n\n❓ Ada yang lain ingin ditanyakan? (jawab 'ada' atau 'tidak')"
        elif jawaban_sudah(user_input):
            context["troubleshoot_step"] = 2
            return "📝 **Gagal Mendaftar - Langkah 2/4**\n\n✅ Saran: Pastikan koneksi internet stabil saat upload berkas.\n\n📋 Coba gunakan jaringan yang lebih cepat atau pindah ke lokasi dengan sinyal lebih baik.\n\n❓ Setelah mencoba, apakah pendaftaran berhasil? (jawab: 'sudah' atau 'belum')"
        else:
            return "Maaf, saya kurang paham. Silakan jawab dengan **'sudah'** jika berkas lengkap, atau **'belum'** jika masih kurang.\n\n✅ Apakah berkas sudah lengkap? (jawab: 'sudah' atau 'belum')"
    
    elif step == 2:
        if jawaban_sudah(user_input):
            reset_troubleshoot()
            context["waiting_for_follow_up"] = True
            return "✅ **Bagus!** Pendaftaran Anda berhasil. 😊\n\n❓ Ada yang lain ingin ditanyakan? (jawab 'ada' atau 'tidak')"
        elif jawaban_belum(user_input):
            context["troubleshoot_step"] = 3
            return "📝 **Gagal Mendaftar - Langkah 3/4**\n\n✅ Saran: Coba gunakan browser yang berbeda atau perangkat yang berbeda untuk mendaftar.\n\n📋 Contoh: Jika pakai Chrome, coba Firefox atau Edge. Jika pakai HP, coba pakai komputer.\n\n❓ Setelah mencoba, apakah pendaftaran berhasil? (jawab: 'sudah' atau 'belum')"
        else:
            return "Maaf, saya kurang paham. Silakan jawab dengan **'sudah'** jika berhasil, atau **'belum'** jika masih gagal.\n\n❓ Setelah mencoba, apakah pendaftaran berhasil? (jawab: 'sudah' atau 'belum')"
    
    elif step == 3:
        if jawaban_sudah(user_input):
            reset_troubleshoot()
            context["waiting_for_follow_up"] = True
            return "✅ **Bagus!** Pendaftaran Anda berhasil. 😊\n\n❓ Ada yang lain ingin ditanyakan? (jawab 'ada' atau 'tidak')"
        elif jawaban_belum(user_input):
            context["troubleshoot_step"] = 4
            return "📝 **Gagal Mendaftar - Langkah 4/4 (Terakhir)**\n\n✅ Saran: Coba bersihkan cache browser atau gunakan mode incognito.\n\n❓ Setelah mencoba, apakah pendaftaran berhasil? (jawab: 'sudah' atau 'belum')"
        else:
            return "Maaf, saya kurang paham. Silakan jawab dengan **'sudah'** jika berhasil, atau **'belum'** jika masih gagal.\n\n❓ Setelah mencoba, apakah pendaftaran berhasil? (jawab: 'sudah' atau 'belum')"
    
    elif step == 4:
        if jawaban_sudah(user_input):
            reset_troubleshoot()
            context["waiting_for_follow_up"] = True
            return "✅ **Bagus!** Pendaftaran Anda berhasil. 😊\n\n❓ Ada yang lain ingin ditanyakan? (jawab 'ada' atau 'tidak')"
        else:
            reset_troubleshoot()
            context["waiting_for_follow_up"] = True
            return "⚠️ **Mohon maaf, saya sudah memberikan semua langkah yang bisa saya bantu.**\n\nJika masih mengalami masalah pendaftaran, silakan:\n\n📞 **Hubungi panitia PMB**\n🌐 Website: <a href='https://pmb.pelitanusantara.ac.id' target='_blank'>pmb.pelitanusantara.ac.id</a>\n\n📍 **Atau datang langsung ke kampus**\n• Kampus 1: Jl. Iskandar Muda No. 1 Medan\n• Kampus 2: Jl. Lintas Sumatera, Tj. Garbus Satu, Lubuk Pakam\n🕒 Jam operasional: Senin-Jumat, 08.00-16.00 WIB\n\n💡 Petugas akan membantu pendaftaran secara offline.\n\n❓ Ada yang lain ingin ditanyakan? (jawab 'ada' atau 'tidak')"


def troubleshoot_lupa_data_login(user_input):
    step = context.get("troubleshoot_step", 0)
    
    if step == 0:
        context["troubleshoot_step"] = 1
        context["troubleshoot_type"] = "lupa_data_login"
        return "🔍 **Lupa Data Login - Langkah 1/2**\n\n✅ Saran: Cek kartu mahasiswa Anda. NIM biasanya tercetak di kartu mahasiswa.\n\n❓ Apakah Anda menemukan NIM di kartu mahasiswa? (jawab: 'sudah' atau 'belum')"
    
    elif step == 1:
        if jawaban_sudah(user_input):
            reset_troubleshoot()
            context["waiting_for_follow_up"] = True
            return "✅ **Bagus!** Silakan gunakan NIM tersebut untuk login SIAKAD.\n\n🔑 **Informasi password default:**\n• Biasanya menggunakan tanggal lahir (format: YYYYMMDD)\n• Contoh: jika lahir 15 Januari 2000 → password: 20000115\n• Atau menggunakan NIM sebagai password default\n\nJika masih tidak bisa login, coba gunakan fitur 'Lupa Password'.\n\n❓ Ada yang lain ingin ditanyakan? (jawab 'ada' atau 'tidak')"
        elif jawaban_belum(user_input):
            context["troubleshoot_step"] = 2
            return "🔍 **Lupa Data Login - Langkah 2/2 (Terakhir)**\n\n✅ Saran: Hubungi admin kampus untuk meminta data login.\n\n📋 Yang perlu disiapkan saat menghubungi admin:\n• Nama lengkap\n• Tanggal lahir\n• Program studi\n• Nomor HP aktif\n\n📞 **Kontak admin:**\n🌐 Website: <a href='https://pmb.pelitanusantara.ac.id' target='_blank'>pmb.pelitanusantara.ac.id</a>\n\n📍 **Atau datang langsung ke kampus:**\n• Kampus 1: Jl. Iskandar Muda No. 1 Medan\n• Kampus 2: Jl. Lintas Sumatera, Tj. Garbus Satu, Lubuk Pakam\n🕒 Jam operasional: Senin-Jumat, 08.00-16.00 WIB\n\n💡 Jangan lupa bawa identitas diri (KTP) untuk verifikasi data.\n\n❓ Ada yang lain ingin ditanyakan? (jawab 'ada' atau 'tidak')"
        else:
            return "Maaf, saya kurang paham. Silakan jawab dengan **'sudah'** jika menemukan NIM, atau **'belum'** jika tidak.\n\n❓ Apakah Anda menemukan NIM di kartu mahasiswa? (jawab: 'sudah' atau 'belum')"
    
    elif step == 2:
        reset_troubleshoot()
        context["waiting_for_follow_up"] = True
        return "✅ **Baik, semoga segera teratasi.** 😊\n\n❓ Ada yang lain ingin ditanyakan? (jawab 'ada' atau 'tidak')"


def handle_troubleshooting(user_input):
    text = user_input.lower()
    
    if context.get("troubleshoot_step", 0) > 0:
        troubleshoot_type = context.get("troubleshoot_type")
        if troubleshoot_type == "login":
            return troubleshoot_login(user_input)
        elif troubleshoot_type == "lupa_password":
            return troubleshoot_lupa_password(user_input)
        elif troubleshoot_type == "krs":
            return troubleshoot_krs(user_input)
        elif troubleshoot_type == "nilai":
            return troubleshoot_nilai(user_input)
        elif troubleshoot_type == "siakad_error":
            return troubleshoot_siakad_error(user_input)
        elif troubleshoot_type == "gagal_daftar":
            return troubleshoot_gagal_daftar(user_input)
        elif troubleshoot_type == "lupa_data_login":
            return troubleshoot_lupa_data_login(user_input)
    
    kata_login = [
        "gagal login", "tidak bisa login", "error login", "login gagal", "tidak dapat masuk",
        "akun tidak bisa diakses", "masuk ke siakad gagal", "login error",
        "ga bisa login", "gabisa login", "gak bisa login", "nggak bisa login",
        "ga bisa masuk", "gabisa masuk", "gak bisa masuk", "nggak bisa masuk",
        "login susah", "susah login", "login error mulu", "error terus",
        "gagal masuk siakad", "tidak bisa akses siakad", "ga bisa akses siakad"
    ]
    if any(kata in text for kata in kata_login):
        return troubleshoot_login(user_input)
    
    kata_lupa_password = [
        "lupa password", "lupa pw", "reset password", "forgot password",
        "lupa sandi", "lupa kata sandi", "ganti password", "ubah password",
        "lupa password siakad", "lupa pw siakad", "reset password siakad",
        "lupa password edlink", "lupa pw edlink", "reset password edlink",
        "tidak bisa ganti password", "gagal ganti password", "error ganti password",
        "lupa password akun", "password lupa", "pw lupa", "sandi lupa"
    ]
    if any(kata in text for kata in kata_lupa_password):
        return troubleshoot_lupa_password(user_input)
    
    kata_krs = [
        "krs tidak bisa", "tidak bisa isi krs", "gagal isi krs", "krs error",
        "krs tidak dapat diajukan", "pengisian krs gagal", "krs tidak tersimpan",
        "krs ga bisa", "krs gak bisa", "krs ngak bisa", "ga bisa isi krs",
        "gak bisa isi krs", "nggak bisa isi krs", "krs error terus",
        "krs ga bisa disimpan", "krs gak bisa diajukan", "isi krs gagal",
        "krs bermasalah", "krs error mulu", "krs lemot"
    ]
    if any(kata in text for kata in kata_krs):
        return troubleshoot_krs(user_input)
    
    kata_nilai = [
        "nilai tidak muncul", "nilai belum keluar", "nilai kosong", "khs kosong",
        "nilai tidak ada", "hasil studi tidak muncul", "transkrip nilai kosong",
        "nilai belum diinput", "khs belum keluar", "nilai belum tampil",
        "nilai ga muncul", "nilai gak muncul", "nilai ngak muncul", "nilai belum ada",
        "nilai kosong semua", "khs ga ada", "khs gak ada", "nilai ga keluar",
        "nilai gak keluar", "nilai belum muncul semua", "khs kosong semua",
        "nilai ga ada", "nilai belum turun", "nilai masih kosong"
    ]
    if any(kata in text for kata in kata_nilai):
        return troubleshoot_nilai(user_input)
    
    kata_siakad_error = [
        "siakad error", "error siakad", "server down", "siakad tidak bisa dibuka",
        "siakad bermasalah", "sistem siakad error", "siakad tidak dapat diakses",
        "siakad sedang error", "website siakad error",
        "siakad ga bisa", "siakad gak bisa", "siakad ngak bisa", "siakad error terus",
        "siakad lemot", "siakad lambat", "siakad loading terus", "siakad blank",
        "siakad putih", "siakad tidak merespon", "siakad ga bisa dibuka",
        "siakad gak bisa dibuka", "siakad error mulu", "siakad hang"
    ]
    if any(kata in text for kata in kata_siakad_error):
        return troubleshoot_siakad_error(user_input)
    
    kata_gagal_daftar = [
        "gagal daftar", "gagal mendaftar", "error pendaftaran", "tidak bisa daftar",
        "pendaftaran error", "pendaftaran gagal", "registrasi gagal",
        "tidak dapat mendaftar", "proses pendaftaran error",
        "ga bisa daftar", "gak bisa daftar", "nggak bisa daftar", "daftar gagal",
        "pendaftaran ga bisa", "pendaftaran gak bisa", "error waktu daftar",
        "gagal waktu daftar", "daftar error", "formulir error", "submit gagal"
    ]
    if any(kata in text for kata in kata_gagal_daftar):
        return troubleshoot_gagal_daftar(user_input)
    
    kata_lupa_data = [
        "lupa nim", "lupa email", "lupa data login", "lupa akun", "lupa username",
        "lupa password", "lupa kata sandi", "tidak ingat nim", "tidak ingat email",
        "nim hilang", "email hilang", "data akun lupa",
        "lupa nim saya", "nim lupa", "email lupa", "lupa password siakad",
        "lupa pw", "lupa sandi", "gatau nim", "gak tau nim", "ga tau nim",
        "lupa akun saya", "nim berapa", "cari nim", "nim saya apa",
        "lupa pw siakad", "lupa password edlink", "lupa pw edlink"
    ]
    if any(kata in text for kata in kata_lupa_data):
        return troubleshoot_lupa_data_login(user_input)
    
    return None