# 🌳 Ancaman Sistemik terhadap Hutan Tropis
## Analisis Spasio-Temporal Deforestasi Sawit Industrial di Indonesia Menggunakan K-Means Clustering dan SARIMA (2001–2024)

![Python](https://img.shields.io/badge/Python-3.12-blue)
![Streamlit](https://img.shields.io/badge/Streamlit-1.35-red)
![License](https://img.shields.io/badge/License-CC%20BY%204.0-green)

---

## 📋 Deskripsi Proyek

Proyek ini membangun aplikasi dashboard visualisasi data spasio-temporal interaktif untuk memetakan, mengklasifikasikan, dan memproyeksikan dinamika deforestasi akibat ekspansi perkebunan sawit industrial di seluruh 514 kabupaten/kota Indonesia selama periode 2001–2024.

**Komponen utama:**
- Peta choropleth interaktif dengan kontrol temporal berbasis slider
- Trajectory-Based K-Means Clustering (k=4) untuk tipologi kabupaten
- SARIMA Forecasting per kluster hingga 2030

**Dibuat oleh:**
| | |
|---|---|
| Nama | Indah Syahfitri |
| NIM | 2311532016 |
| Program Studi | Informatika — Fakultas Teknologi Informasi |
| Universitas | Universitas Andalas (UNAND), Padang |
| Mata Kuliah | Visualisasi Data Spasio-Temporal |
| Tahun | 2025 |

---

## 🗃️ Dataset

| Dataset | Sumber | Lisensi |
|---|---|---|
| Indonesia: Annual Palm Deforestation (Industrial) | [Trase Earth Open Data](https://trase.earth/open-data/datasets/spatial-metrics-indonesia-palm-oil-palm-oil-deforestation-annual) | CC BY 4.0 |

**Referensi:** Gaveau, D. et al. (2022). *Slowing deforestation in Indonesia follows declining oil palm expansion and lower oil prices.* PLOS ONE. DOI: 10.1371/journal.pone.0266178

---

## 🏗️ Struktur Folder

```
deforestasi-sawit/
├── data/
│   ├── raw/
│   │   ├── deforestasi_kabupaten.csv
│   │   └── deforestasi_kabupaten.geojson
│   └── processed/
│       ├── df_wide.csv
│       ├── df_long.csv
│       ├── df_clustered.csv
│       ├── forecast_2025_2030.csv
│       └── evaluasi_sarima.csv
├── notebooks/
│   ├── 01_eda.ipynb
│   ├── 02_clustering.ipynb
│   └── 03_forecasting.ipynb
├── pages/
│   ├── 1_Peta_Deforestasi.py
│   ├── 2_Clustering.py
│   ├── 3_Forecasting.py
│   └── 4_Tentang.py
├── utils/
│   ├── load_data.py
│   ├── map_utils.py
│   └── forecasting_utils.py
├── app.py
├── requirements.txt
└── README.md
```

---

## ⚙️ Instalasi & Menjalankan Aplikasi

### 1. Clone repository
```bash
git clone https://github.com/username/deforestasi-sawit.git
cd deforestasi-sawit
```

### 2. Buat virtual environment
```bash
python -m venv venv
venv\Scripts\activate        # Windows
source venv/bin/activate     # Mac/Linux
```

### 3. Install dependensi
```bash
pip install -r requirements.txt
```

### 4. Jalankan aplikasi
```bash
streamlit run app.py
```

Aplikasi akan terbuka otomatis di browser: `http://localhost:8501`

---

## 🛠️ Tech Stack

| Komponen | Library |
|---|---|
| Dashboard | Streamlit |
| Peta interaktif | Folium + streamlit-folium |
| Visualisasi | Plotly |
| Data processing | Pandas, GeoPandas, NumPy |
| Clustering | Scikit-learn (K-Means) |
| Forecasting | Statsmodels (SARIMA), pmdarima (Auto-ARIMA) |

---

## 🤖 Metodologi Machine Learning

### K-Means Trajectory Clustering (k=4)
- Mengelompokkan 514 kabupaten berdasarkan pola temporal deforestasi 2001–2024
- Normalisasi per baris untuk menangkap pola, bukan besaran nilai
- Evaluasi: **Silhouette Score = 0.795** (struktur kluster baik, >0.7)

| Kluster | Jumlah | Persentase | Karakteristik |
|---|---|---|---|
| 🟢 Zero | 369 | 71,8% | Tidak ada aktivitas deforestasi |
| 🟠 Moderate | 114 | 22,2% | Fluktuasi sedang |
| 🔵 Declining | 21 | 4,1% | Tren menurun |
| 🔴 High | 10 | 1,9% | Deforestasi tinggi konsisten |

### SARIMA Forecasting per Kluster
- Model dipilih otomatis menggunakan Auto-ARIMA (kriteria AIC)
- Training: 2001–2019 | Test: 2020–2024 | Proyeksi: 2025–2030

| Kluster | RMSE (ha) | MAE (ha) |
|---|---|---|
| High | 4.123,53 | 3.390,65 |
| Declining | 1.123,65 | 826,12 |
| Moderate | 2.233,64 | 1.707,43 |

---

## 📄 Lisensi

Dataset: CC BY 4.0 — Trase Earth Open Data  
Kode: MIT License
