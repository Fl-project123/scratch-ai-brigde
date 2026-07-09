import streamlit as st
import scratchattach as scratch3
import google.generativeai as genai
import time

# --- KONFIGURASI DASHBOARD (Navy Blue Style) ---
st.set_page_config(page_title="Scratch AI Bridge v8.3", layout="centered")
st.title("🚀 AI Bridge Dashboard (Live Scanner)")

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

if st.button("Jalankan Radar Pemantau Publik"):
    if not GEMINI_KEY:
        st.error("API Key Gemini wajib diisi, bro!")
    else:
        st.success("Radar Aktif! Mengunci variabel live proyek...")
        
        # Konfigurasi Gemini
        genai.configure(api_key=GEMINI_KEY)
        model = genai.GenerativeModel('gemini-1.5-flash')
        
        st.info("Menunggu sinyal Status = 2 dari Scratch...")
        terakhir_diproses = ""
        
        while True:
            try:
                # SOLUSI JITU: Langsung tembak nilai variabel aslinya secara live via API publik
                # Ini sangat ringan, tidak bikin crash, dan instan!
                nilai_status = str(scratch3.get_var(PROJECT_ID, "Status"))
                
                # Jika terdeteksi game mengirimkan sinyal Status 2
                if nilai_status == "2":
                    nilai_cloud_ask = str(scratch3.get_var(PROJECT_ID, "CloudAsk"))
                    
                    if nilai_cloud_ask and nilai_cloud_ask != "0" and nilai_cloud_ask != terakhir_diproses:
                        terakhir_diproses = nilai_cloud_ask
                        
                        st.write("🎯 **Sinyal Terkunci! Status = 2 Terdeteksi.**")
                        pertanyaan = dekripsi(nilai_cloud_ask)
                        st.write(f"💬 **Pertanyaan Player:** \"{pertanyaan}\"")
                        
                        # Ambil jawaban dari Gemini
                        response = model.generate_content(
                            f"Kamu adalah AI proyek Scratch. Jawab singkat maksimal 25 karakter: {pertanyaan}"
                        )
                        jawaban_ai = response.text.strip()
                        
                        st.markdown("---")
                        st.subheader(f"🤖 JAWABAN GEMINI:")
                        st.success(f"**{jawaban_ai}**")
                        st.markdown("---")
                        
            except Exception as e:
                pass
                
            # Jeda 1.5 detik sangat aman untuk pembacaan live satu variabel tunggal
            time.sleep(1.5)
