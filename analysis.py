import cv2
import numpy as np
import requests
import random
import os   # ⬅️ TAMBAHKAN

API_KEY = os.getenv("WEATHER_API_KEY")
CITY = os.getenv("WEATHER_CITY", "Yogyakarta")


# =========================
# AUTO DETEKSI JENIS DAUN
# =========================
def detect_leaf_type(image):
    # Validasi input: pastikan image adalah array NumPy
    if not isinstance(image, np.ndarray):
        return "Error: Input bukan gambar valid"
    
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (5, 5), 0)

    _, thresh = cv2.threshold(
        blur, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU
    )

    contours, _ = cv2.findContours(
        thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE
    )

    if not contours:
        return "Tidak Terdeteksi"

    cnt = max(contours, key=cv2.contourArea)
    area = cv2.contourArea(cnt)

    x, y, w, h = cv2.boundingRect(cnt)
    ratio = h / w if w != 0 else 0

    # 🔥 LOGIKA BARU (LEBIH AMAN)
    if ratio > 2.8 and area < 0.15 * (image.shape[0] * image.shape[1]):
        return "Padi"
    elif ratio > 1.5:
        return "Cabai"
    else:
        return "Singkong"

# =========================
# ANALISIS TANAMAN
# =========================
def analyze_plant(image_path):
    # Baca gambar dari path
    image = cv2.imread(image_path)
    if image is None:
        return {"error": "Gambar tidak dapat dibaca. Periksa path file."}
    
    skor = random.randint(60, 95)  # Simulasi; ganti dengan analisis gambar jika perlu

    status = "Sehat" if skor >= 75 else "Perlu Perhatian"

    if skor >= 85:
        nutrisi = "Optimal"
        kondisi = "Hijau Segar"
        risiko = "Rendah"
    elif skor >= 70:
        nutrisi = "Cukup"
        kondisi = "Sedikit Pucat"
        risiko = "Sedang"
    else:
        nutrisi = "Kurang"
        kondisi = "Menguning"
        risiko = "Tinggi"

    rekomendasi = [
        "Pastikan penyiraman rutin",
        "Gunakan pupuk NPK seimbang",
        "Pantau kondisi daun setiap hari"
    ]

    return {
        "jenis_tanaman": detect_leaf_type(image),  # Diperbaiki: panggil fungsi yang benar
        "status": status,
        "skor": skor,
        "kondisi_daun": kondisi,
        "nutrisi": nutrisi,
        "risiko_penyakit": risiko,
        "rekomendasi": rekomendasi
    }

# =========================
# CUACA REALTIME
# =========================
def get_weather_data():
    try:
        res = requests.get(
            "https://api.openweathermap.org/data/2.5/weather",
            params={
                "q": CITY,
                "appid": API_KEY,
                "units": "metric",
                "lang": "id"
            },
            timeout=5
        ).json()

        humidity = res["main"]["humidity"]

        return {
            "temp": f"{round(res['main']['temp'])}°C",
            "humidity": f"{humidity}%",
            "condition": res["weather"][0]["description"].capitalize(),
            "advice": (
                "Waspadai jamur karena kelembaban tinggi"
                if humidity > 80 else
                "Cuaca cukup baik untuk tanaman"
            )
        }
    except Exception:
        return {
            "temp": "28°C",
            "humidity": "75%",
            "condition": "Cerah Berawan",
            "advice": "Data cuaca default"
        }
    
def get_weather_forecast():
    try:
        res = requests.get(
            "https://api.openweathermap.org/data/2.5/forecast",
            params={
                "q": CITY,
                "appid": API_KEY,
                "units": "metric",
                "lang": "id"
            },
            timeout=5
        ).json()

        forecast = []
        for item in res["list"][::8]:  # ambil per hari
            forecast.append({
                "date": item["dt_txt"].split(" ")[0],
                "temp": f"{round(item['main']['temp'])}°C",
                "condition": item["weather"][0]["description"].capitalize()
            })

        return forecast[:3]

    except Exception as e:
        print("Forecast error:", e)
        return []

# Contoh penggunaan (untuk testing)
if __name__ == "__main__":
    # Ganti dengan path gambar daun yang valid
    image_path = "path/to/your/leaf_image.jpg"  # Contoh: "leaf.jpg"
    
    # Analisis tanaman
    result = analyze_plant(image_path)
    print("Analisis Tanaman:", result)
    
    # Data cuaca
    weather = get_weather_data()
    print("Cuaca Saat Ini:", weather)
    
    # Forecast
    forecast = get_weather_forecast()
    print("Forecast 3 Hari:", forecast)