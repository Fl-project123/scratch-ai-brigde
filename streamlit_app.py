import streamlit as st
import scratchattach as scratch3
import google.generativeai as genai
import time

# --- KONFIGURASI DASHBOARD (Navy Blue Style) ---
st.set_page_config(page_title="Scratch AI Bridge v9.0", layout="centered")
st.title("🚀 AI Bridge Dashboard (Event Listener Mode)")

GEMINI_KEY = st.text_input("Gemini API Key", type="password")
PROJECT_ID = "1338403041"

kamus = ["a","b","c","d","e","f","g","h","i","j","k","l","m","n","o","p","q","r","s","t","u","v","w","x","y","z","0","1","2","3","4","5","6","7","8","9","?"," ","A","B","C","D","E","F","G","H","I","J","K","L","M","N","O","P","Q","R","S","T","U","V","W","X","Y","Z"]

def dekripsi(data_angka):
    hasil = ""
    for i in range(0, len(data_angka), 2):
        dua_digit = data_angka[i:i+2]
        if dua_digit:
            indeks = int(dua_digit) - 1
            if 0 <= indeks < len(kamus):
                hasil += kamus[indeks]
    return hasil

if st.button("Jalankan Radar Jembatan"):
    if not GEMINI_KEY:
        st.error("API Key Gemini wajib diisi, bro!")
    else:
        st.success("Radar Aktif! Menggunakan Jalur Event Listener Resmi ✅")
        
        # Konfigurasi Gemini
        genai.configure(api_key=GEMINI_KEY)
        model = genai.GenerativeModel('gemini-1.5-flash')
        
        st.info("Mendengarkan perubahan variabel awan dari game Scratch...")
        
        # Membuat handler event listener publik (Tanpa Login, Super Aman)
        events = scratch3.CloudEvents(PROJECT_ID)
        
        # Variabel penampung sementara di memori Streamlit
        if "log_ai" not in st.session_state:
            st.session_state.log_ai = []

        # Fungsi yang otomatis terpicu JIKA ada variabel cloud yang berubah
        @events.event
        def on_set(event):
            # Cek jika ada yang merubah Status menjadi 2
            if event.name == "☁ Status" and str(event.value) == "2":
                try:
                    # Ambil nilai CloudAsk detik itu juga dari data event (Bukan nembak server lagi!)
                    # Kita cari data CloudAsk pendampingnya
                    proyek = scratch3.get_project(PROJECT_ID)
                    nilai_cloud_ask = proyek.get_cloud_variable("CloudAsk")
                    
                    if nilai_cloud_ask and str(nilai_cloud_ask) != "0":
                        pertanyaan = dekripsi(str(nilai_cloud_ask))
                        
                        # Panggil Gemini AI
                        response = model.generate_content(
                            f"Kamu adalah AI proyek Scratch. Jawab singkat maksimal 25 karakter: {pertanyaan}"
                        )
                        jawaban_ai = response.text.strip()
                        
                        # Simpan log ke layar
                        st.session_state.log_ai.append(f"📥 Pertanyaan: {pertanyaan} | 🤖 Gemini: {jawaban_ai}")
                except Exception as err:
                    pass

        # Jalankan listen secara non-blocking
        events.start(thread=True)
        
        # Tampilkan log di layar Streamlit secara dinamis
        placeholder = st.empty()
        while True:
            with placeholder.container():
                for log in reversed(st.session_state.log_ai):
                    st.write(log)
            time.sleep(1)
