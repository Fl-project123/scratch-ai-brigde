import streamlit as st
import scratchattach as scratch3
import google.generativeai as genai
import time

# --- KONFIGURASI DASHBOARD (Navy Blue Style) ---
st.set_page_config(page_title="Scratch AI Bridge v7.0", layout="centered")
st.title("🚀 AI Bridge Dashboard (Python + Streamlit)")

# Input di Dashboard Streamlit
SESSION_ID = st.text_input("Scratch Session ID", type="password")
GEMINI_KEY = st.text_input("Gemini API Key", type="password")
PROJECT_ID = "1338403041"

# Kamus 44 Karakter kamu
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

def enkripsi(teks_input):
    hasil = ""
    for huruf in teks_input:
        if huruf in kamus:
            posisi = kamus.index(huruf) + 1
            hasil += f"{posisi:02d}"
    return hasil

if st.button("Nyalakan Radar Jembatan AI"):
    if not SESSION_ID or not GEMINI_KEY:
        st.error("Session ID dan Gemini Key wajib diisi, bro!")
    else:
        st.success("Radar Jembatan Aktif! Memantau awan Scratch MIT...")
        
        # Koneksi Resmi via Python
       # --- KODE BARU YANG SUDAH DIPERBAIKI ---
        try:
            # Di versi baru, cukup masukkan Session ID saja
            session = scratch3.Session(SESSION_ID)
            
            # Server akan otomatis membaca username dari Session ID tersebut
            conn = session.connect_cloud(PROJECT_ID)
        except Exception as e:
            st.error(f"Gagal login ke Scratch! Periksa apakah Session ID kamu sudah kedaluwarsa: {e}")
        # Konfigurasi Gemini
        genai.configure(api_key=GEMINI_KEY)
        model = genai.GenerativeModel('gemini-1.5-flash')
        
        st.info("Menunggu pertanyaan dari dalam game Scratch...")
        
        # Variabel pengunci lokal
        terakhir_diproses = ""
        
        # LOOP UTAMA (Berjalan di latar belakang)
        while True:
            try:
                # Ambil nilai CloudAsk langsung dari server MIT secara realtime
                nilai_cloud_ask = scratch3.get_var(PROJECT_ID, "CloudAsk")
                
                if nilai_cloud_ask and nilai_cloud_ask != "0" and nilai_cloud_ask != terakhir_diproses:
                    terakhir_diproses = nilai_cloud_ask
                    
                    st.write(f"📥 **Tertangkap angka masuk:** `{nilai_cloud_ask}`")
                    pertanyaan = dekripsi(str(nilai_cloud_ask))
                    st.write(f"💬 **Pertanyaan Terjemahan:** \"{pertanyaan}\"")
                    
                    # Panggil Gemini
                    response = model.generate_content(
                        f"Kamu adalah AI proyek Scratch. Jawab singkat maksimal 25 karakter: {pertanyaan}"
                    )
                    jawaban_ai = response.text.strip()
                    st.write(f"🤖 **Gemini Menjawab:** \"{jawaban_ai}\"")
                    
                    # Enkripsi & Suntik balik ke Cloud resmi MIT
                    jawaban_encoded = enkripsi(jawaban_ai)
                    conn.set_var("CloudAnswer", jawaban_encoded)
                    time.sleep(0.3)
                    conn.set_var("Status", "1")
                    
                    st.success("✅ Jawaban sukses dipantulkan ke server MIT!")
                    
            except Exception as e:
                st.write(f"⚠️ Ada interupsi data: {e}")
                
            time.sleep(1) # Cek setiap 1 detik sekali agar ramah CPU Celeron
