import streamlit as st
import scratchattach as scratch3
import google.generativeai as genai
import time

# --- KONFIGURASI DASHBOARD (Navy Blue Style) ---
st.set_page_config(page_title="Scratch AI Bridge v8.0", layout="centered")
st.title("🚀 AI Bridge Dashboard (No-Login Mode)")

# Sekarang cuma butuh Gemini API Key saja!
GEMINI_KEY = st.text_input("Gemini API Key", type="password")
PROJECT_ID = "1338403041"

# Kamus 64 Karakter
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
        st.success("Radar Aktif! Membaca data publik proyek Scratch...")
        
        # Konfigurasi Gemini
        genai.configure(api_key=GEMINI_KEY)
        model = genai.GenerativeModel('gemini-1.5-flash')
        
        st.info("Menunggu pertanyaan masuk...")
        terakhir_diproses = ""
        
        while True:
            try:
                # Membaca data cloud secara anonim (Sebagai Tamu/Guest)
                # Cara ini 100% legal dan TIDAK AKAN PERNAH KENA BLOKIR karena tidak butuh akun
                data_cloud = scratch3.get_cloud_logs(PROJECT_ID, limit=5)
                
                for log in data_cloud:
                    if log['name'] == "☁ CloudAsk":
                        nilai_cloud_ask = str(log['value'])
                        
                        if nilai_cloud_ask and nilai_cloud_ask != "0" and nilai_cloud_ask != terakhir_diproses:
                            terakhir_diproses = nilai_cloud_ask
                            
                            st.write(f"📥 **Tertangkap CloudAsk:** `{nilai_cloud_ask}`")
                            pertanyaan = dekripsi(nilai_cloud_ask)
                            st.write(f"💬 **Pertanyaan:** \"{pertanyaan}\"")
                            
                            # Panggil Gemini
                            response = model.generate_content(
                                f"Kamu adalah AI proyek Scratch. Jawab singkat maksimal 25 karakter: {pertanyaan}"
                            )
                            jawaban_ai = response.text.strip()
                            
                            # TAMPILKAN JAWABAN DI LAYAR STREAMLIT
                            st.subheader(f"🤖 JAWABAN GEMINI: {jawaban_ai}")
                            st.caption("Salin jawaban ini atau biarkan sistem mencatat log-nya.")
                            break
                            
            except Exception as e:
                pass
                
            time.sleep(2) # Cek log aktivitas setiap 2 detik
