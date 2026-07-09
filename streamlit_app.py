import streamlit as st
import scratchattach as scratch3
import google.generativeai as genai
import time

# --- KONFIGURASI DASHBOARD (Navy Blue Style) ---
st.set_page_config(page_title="Scratch AI Bridge v8.1", layout="centered")
st.title("🚀 AI Bridge Dashboard (Status 2 Detector)")

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
        st.success("Radar Aktif! Memantau sinyal dari game Scratch...")
        
        # Konfigurasi Gemini
        genai.configure(api_key=GEMINI_KEY)
        model = genai.GenerativeModel('gemini-1.5-flash')
        
        st.info("Menunggu game Scratch mengirimkan Status = 2...")
        
        # Variabel pengunci agar tidak memproses pertanyaan yang sama berulang-ulang
        terakhir_diproses = ""
        
        while True:
            try:
                # Ambil data log aktivitas cloud terbaru (5 aktivitas terakhir)
                data_cloud = scratch3.get_cloud_logs(PROJECT_ID, limit=5)
                
                status_terdeteksi = False
                nilai_cloud_ask = ""
                
                # Scan log untuk memeriksa kondisi Status dan CloudAsk
                for log in data_cloud:
                    if log['name'] == "☁ Status" and str(log['value']) == "2":
                        status_terdeteksi = True
                    if log['name'] == "☁ CloudAsk":
                        nilai_cloud_ask = str(log['value'])
                
                # JIKA GAME KAMU SUDAH MENGIRIM STATUS = 2
                if status_terdeteksi and nilai_cloud_ask and nilai_cloud_ask != "0" and nilai_cloud_ask != terakhir_diproses:
                    terakhir_diproses = nilai_cloud_ask
                    
                    st.write("🎯 **Sinyal Diterima! Game mendeteksi pertanyaan baru (Status = 2).**")
                    st.write(f"📥 **Tertangkap Angka:** `{nilai_cloud_ask}`")
                    
                    # Terjemahkan angka menjadi teks
                    pertanyaan = dekripsi(nilai_cloud_ask)
                    st.write(f"💬 **Teks Pertanyaan:** \"{pertanyaan}\"")
                    
                    # Panggil Gemini AI
                    st.write("⚡ *Menghubungi Gemini...*")
                    response = model.generate_content(
                        f"Kamu adalah AI proyek Scratch. Jawab singkat maksimal 25 karakter: {pertanyaan}"
                    )
                    jawaban_ai = response.text.strip()
                    
                    # TAMPILKAN HASILNYA SECARA JELAS DI LAYAR
                    st.markdown("---")
                    st.subheader(f"🤖 JAWABAN GEMINI:")
                    st.success(f"**{jawaban_ai}**")
                    st.markdown("---")
                    
            except Exception as e:
                # Abaikan eror koneksi kecil agar loop tidak patah
                pass
                
            time.sleep(2) # Beri jeda 2 detik sebelum scan ulang log agar tidak dinilai spam oleh MIT
