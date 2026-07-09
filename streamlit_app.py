import streamlit as st
import scratchattach as scratch3
import google.generativeai as genai
import time

# --- KONFIGURASI DASHBOARD (Navy Blue Style) ---
st.set_page_config(page_title="Scratch AI Bridge v7.1", layout="centered")
st.title("🚀 AI Bridge Dashboard (Streamlit Cloud)")

# Input di Dashboard Streamlit
SESSION_ID = st.text_input("Scratch Session ID", type="password")
GEMINI_KEY = st.text_input("Gemini API Key", type="password")
PROJECT_ID = "1338403041"

# Kamus 64 Karakter kamu
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
        try:
            # Login versi terbaru yang valid
            session = scratch3.Session(SESSION_ID)
            
            # Membuka koneksi cloud resmi via objek session
            conn = session.connect_cloud(PROJECT_ID)
            st.success("Radar Jembatan Aktif! Memantau awan Scratch MIT...")
            
            # Konfigurasi Gemini
            genai.configure(api_key=GEMINI_KEY)
            model = genai.GenerativeModel('gemini-1.5-flash')
            
            st.info("Menunggu pertanyaan dari dalam game Scratch...")
            terakhir_diproses = ""
            
            # LOOP UTAMA
            while True:
                try:
                    # CARA BARU AMBIL VARIABEL CLOUD (Lewat objek conn, bukan scratch3 langsung)
                    # Kita gunakan fungsi bawaan proyek publik agar lebih aman
                    proyek_publik = scratch3.get_project(PROJECT_ID)
                    nilai_cloud_ask = proyek_publik.get_cloud_variable("CloudAsk")
                    
                    if nilai_cloud_ask and str(nilai_cloud_ask) != "0" and str(nilai_cloud_ask) != terakhir_diproses:
                        terakhir_diproses = str(nilai_cloud_ask)
                        
                        st.write(f"📥 **Tertangkap data masuk:** `{nilai_cloud_ask}`")
                        pertanyaan = dekripsi(str(nilai_cloud_ask))
                        st.write(f"💬 **Pertanyaan Terjemahan:** \"{pertanyaan}\"")
                        
                        # Panggil Gemini
                        response = model.generate_content(
                            f"Kamu adalah AI proyek Scratch. Jawab singkat maksimal 25 karakter: {pertanyaan}"
                        )
                        jawaban_ai = response.text.strip()
                        st.write(f"🤖 **Gemini Menjawab:** \"{jawaban_ai}\"")
                        
                        # Enkripsi & Kirim balik lewat pipa koneksi terotentikasi
                        jawaban_encoded = enkripsi(jawaban_ai)
                        conn.set_var("CloudAnswer", jawaban_encoded)
                        time.sleep(0.5)
                        conn.set_var("Status", "1")
                        
                        st.success("✅ Jawaban sukses dipantulkan!")
                        
                except Exception as e_loop:
                    # Tampilkan eror spesifik di dalam loop jika ada masalah pembacaan
                    pass
                    
                time.sleep(1) # Interval pengecekan awan
                
        except Exception as e:
            st.error(f"Gagal mengunci jaringan Scratch: {e}")
