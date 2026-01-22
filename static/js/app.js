// ===============================
// ELEMENTS (AMAN DI LANDING & DASHBOARD)
// ===============================
const startBtn = document.getElementById("startBtn");
const analysisArea = document.getElementById("analysisArea");
const imageInput = document.getElementById("imageInput");
const preview = document.getElementById("preview");
const analyzeBtn = document.getElementById("analyzeBtn");
const resultArea = document.getElementById("resultArea");

// ===============================
// SHOW ANALYSIS AREA
// ===============================
if (startBtn) {
    startBtn.onclick = () => {
        analysisArea.style.display = "block";
        analysisArea.scrollIntoView({ behavior: "smooth" });
    };
}

// ===============================
// IMAGE PREVIEW
// ===============================
if (imageInput) {
    imageInput.onchange = () => {
        const file = imageInput.files[0];
        if (file) {
            preview.src = URL.createObjectURL(file);
            preview.style.display = "block";
        }
    };
}

// ===============================
// ANALYZE IMAGE
// ===============================
if (analyzeBtn) {
    analyzeBtn.onclick = async () => {
        if (!imageInput.files[0]) {
            alert("Upload gambar terlebih dahulu");
            return;
        }

        analyzeBtn.innerText = "Menganalisis...";
        analyzeBtn.disabled = true;

        const formData = new FormData();
        formData.append("image", imageInput.files[0]);

        try {
            const response = await fetch("/analyze", {
                method: "POST",
                body: formData
            });

            const data = await response.json();

            // ===== HASIL =====
            document.getElementById("resJenis").innerText = data.jenis_tanaman;
            document.getElementById("resStatus").innerText = data.status;
            document.getElementById("resDaun").innerText = data.kondisi_daun;
            document.getElementById("resNutrisi").innerText = data.nutrisi;
            document.getElementById("resRisiko").innerText = data.risiko_penyakit;

            // ===== WARNA STATUS =====
            const statusEl = document.getElementById("resStatus");
            statusEl.style.background =
                data.status === "Sehat" ? "#43a047" : "#f57c00";

            // ===== PROGRESS BAR =====
            const bar = document.getElementById("healthBar");
            if (bar && data.skor !== undefined) {
                bar.style.width = data.skor + "%";
                bar.innerText = data.skor + "%";
            }

            // ===== REKOMENDASI =====
            const recs = document.getElementById("resRecs");
            recs.innerHTML = "";
            data.rekomendasi.forEach(r => {
                recs.innerHTML += `<p>✔ ${r}</p>`;
            });

            resultArea.style.display = "block";
            resultArea.scrollIntoView({ behavior: "smooth" });

            // ===== LOAD HISTORY =====
            loadHistory();

        } catch (err) {
            alert("Gagal menganalisis gambar");
            console.error(err);
        } finally {
            analyzeBtn.innerText = "Analisis";
            analyzeBtn.disabled = false;
        }
    };
}

// ===============================
// WEATHER MODAL (LANDING + DASHBOARD)
// ===============================
async function openWeatherDetail() {
    const modal = document.getElementById("weatherModal");
    if (!modal) return;

    modal.style.display = "flex";

    const now = await fetch("/api/weather").then(r => r.json());
    document.getElementById("weatherNow").innerHTML = `
        <p>🌡 Suhu: <b>${now.temp}</b></p>
        <p>💧 Kelembaban: <b>${now.humidity}</b></p>
        <p>☁️ Kondisi: <b>${now.condition}</b></p>
        <small>${now.advice}</small>
    `;

    const forecast = await fetch("/api/weather/forecast").then(r => r.json());
    const area = document.getElementById("forecastArea");
    area.innerHTML = "";

    forecast.forEach(day => {
        area.innerHTML += `
            <div class="forecast-item">
                <b>${day.date}</b><br>
                ${day.temp}<br>
                ${day.condition}
            </div>
        `;
    });
}

function closeWeatherDetail() {
    const modal = document.getElementById("weatherModal");
    if (modal) modal.style.display = "none";
}

// ===============================
// LOAD HISTORY (AMAN)
// ===============================
async function loadHistory() {
    const list = document.getElementById("historyList");
    if (!list) return;

    const res = await fetch("/api/history");
    const data = await res.json();
    list.innerHTML = "";

    data.forEach(item => {
        list.innerHTML += `
            <div class="history-item">
                🌿 ${item.result.jenis_tanaman} – ${item.result.status}
            </div>
        `;
    });
}
