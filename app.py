from flask import Flask, render_template, request, jsonify
import os
from analysis import analyze_plant, get_weather_data, get_weather_forecast

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
UPLOAD_FOLDER = os.path.join(BASE_DIR, "uploads")

app = Flask(__name__)
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

# ==========================
# SIMPAN RIWAYAT ANALISIS
# ==========================
analysis_history = []


@app.route("/")
def landing():
    return render_template("landing.html")


@app.route("/dashboard")
def dashboard():
    weather = get_weather_data()
    return render_template("dashboard.html", weather=weather)


# ==========================
# WEATHER API
# ==========================
@app.route("/api/weather")
def api_weather():
    return jsonify(get_weather_data())


@app.route("/api/weather/forecast")
def api_weather_forecast():
    return jsonify(get_weather_forecast())


# ==========================
# HISTORY API
# ==========================
@app.route("/api/history")
def api_history():
    return jsonify(analysis_history[::-1][:5])


# ==========================
# ANALYZE IMAGE
# ==========================
@app.route("/analyze", methods=["POST"])
def analyze():
    if "image" not in request.files:
        return jsonify({"error": "Image tidak ditemukan"}), 400

    image = request.files["image"]
    filename = image.filename
    filepath = os.path.join(app.config["UPLOAD_FOLDER"], filename)
    image.save(filepath)

    result = analyze_plant(filepath)

    analysis_history.append({
        "filename": filename,
        "result": result
    })

    return jsonify(result)


# ==========================
# RUN APP
# ==========================
if __name__ == "__main__":
    app.run()


