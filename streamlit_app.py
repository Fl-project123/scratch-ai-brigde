import streamlit as st
import scratchattach as scratch3
import google.generativeai as genai
import time

# --- KONFIGURASI DASHBOARD (Navy Blue Style) ---
st.set_page_config(page_title="Scratch AI Bridge v8.2", layout="centered")
st.title("🚀 AI Bridge Dashboard (Anti-Crash Mode)")

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
        st.success("Radar Aktif! Memantau sinyal tanpa membebani server...")
        
        # Konfigurasi Gemini
        genai.configure(api_key=GEMINI_KEY)
        model = genai.GenerativeModel('gemini-1.5-flash')
        
        st.info("Menunggu game Scratch mengirimkan Status = 2...")
        terakhir_diproses = ""
        
        while True:
            try:
                # FIX BUG: Perkecil limit menjadi 2 agar paket data sangat ringan
                data_cloud = scratch3.get_cloud_logs(PROJECT_ID, limit=2)
                
                status_terdeteksi = False
                nilai_cloud_ask = ""
                
                for log in data_cloud:
                    if log['name'] == "☁ Status" and str(log['value']) == "2":
                        status_terdeteksi = True
                    if log['name'] == "☁ CloudAsk":
                        nilai_cloud_ask = str(log['value'])
                
                if status_terdeteksi and nilai_cloud_ask and nilai_cloud_ask != "0" and nilai_cloud_ask != terakhir_diproses:
                    terakhir_diproses = nilai_cloud_ask
                    
                    st.write("🎯 **Sinyal Diterima! Menghubungi Gemini AI...**")
                    pertanyaan = dekripsi(nilai_cloud_ask)
                    st.write(f"💬 **Pertanyaan:** \"{pertanyaan}\"")
                    
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
                
            # FIX BUG: Naikkan jeda waktu tidur menjadi 5 detik agar tidak memicu proteksi auto-stop MIT
            time.sleep(5)
