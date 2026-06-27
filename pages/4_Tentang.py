# pages/4_Tentang.py - PERBAIKAN SUMBER DATA

import streamlit as st

st.set_page_config(page_title="Tentang", page_icon="ℹ️", layout="wide")

# ============================================================
# CSS - MODERN UPGRADE
# ============================================================
st.markdown("""
<style>
    /* ===== HEADER ===== */
    .page-header {
        padding: 20px 0 12px 0;
        text-align: center;
    }
    .page-header h1 {
        font-size: 2.4rem;
        font-weight: 800;
        background: linear-gradient(135deg, #0F172A 0%, #2563EB 50%, #7C3AED 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin: 0;
        letter-spacing: -0.5px;
    }
    .page-header .subtitle {
        color: #64748B;
        font-size: 1.05rem;
        margin-top: 6px;
        font-weight: 400;
    }
    
    /* ===== HERO CARD ===== */
    .hero-card {
        background: linear-gradient(135deg, #0F172A 0%, #1E293B 50%, #2563EB 100%);
        border-radius: 20px;
        padding: 36px 40px;
        color: white;
        margin-bottom: 24px;
        position: relative;
        overflow: hidden;
        box-shadow: 0 12px 48px rgba(37,99,235,0.25);
    }
    .hero-card::before {
        content: '🌳';
        position: absolute;
        right: -20px;
        bottom: -40px;
        font-size: 200px;
        opacity: 0.08;
    }
    .hero-card .hero-title {
        font-size: 1.8rem;
        font-weight: 700;
        margin-bottom: 8px;
    }
    .hero-card .hero-title span {
        background: linear-gradient(135deg, #60A5FA, #A78BFA);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    .hero-card .hero-desc {
        color: #94A3B8;
        font-size: 1rem;
        line-height: 1.7;
        max-width: 700px;
    }
    .hero-card .hero-badge {
        display: inline-block;
        background: rgba(255,255,255,0.12);
        padding: 4px 16px;
        border-radius: 20px;
        font-size: 0.75rem;
        color: #94A3B8;
        margin-top: 12px;
        backdrop-filter: blur(4px);
        border: 1px solid rgba(255,255,255,0.06);
    }
    
    /* ===== SECTION CARD ===== */
    .section-card {
        background: #FFFFFF;
        border-radius: 16px;
        padding: 24px 28px;
        border: 1px solid #F1F5F9;
        box-shadow: 0 1px 3px rgba(0,0,0,0.03);
        margin-bottom: 16px;
        transition: all 0.3s ease;
        position: relative;
        overflow: hidden;
    }
    .section-card:hover {
        border-color: #2563EB40;
        box-shadow: 0 8px 32px rgba(37,99,235,0.08);
        transform: translateY(-2px);
    }

    .fade-in {
        animation: fadeInUp 0.8s ease both;
    }

    @keyframes fadeInUp {
        from {
            opacity: 0;
            transform: translateY(14px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    .section-card .card-icon {
        font-size: 1.6rem;
        margin-right: 10px;
    }
    .section-card h3 {
        color: #0F172A;
        margin-top: 0;
        margin-bottom: 14px;
        display: flex;
        align-items: center;
        gap: 10px;
        font-size: 1.1rem;
        font-weight: 700;
        border-bottom: 2px solid #F1F5F9;
        padding-bottom: 12px;
    }
    .section-card h3 .badge {
        font-size: 0.65rem;
        font-weight: 600;
        background: #DBEAFE;
        color: #1E40AF;
        padding: 2px 12px;
        border-radius: 12px;
        margin-left: auto;
    }
    
    /* ===== IDENTITAS ===== */
    .info-grid {
        display: grid;
        grid-template-columns: 1fr 1fr;
        gap: 6px 24px;
    }
    .info-row {
        display: flex;
        padding: 8px 0;
        border-bottom: 1px solid #F8FAFC;
        align-items: center;
    }
    .info-row .label {
        font-weight: 600;
        color: #0F172A;
        width: 130px;
        flex-shrink: 0;
        font-size: 0.85rem;
    }
    .info-row .value {
        color: #475569;
        font-size: 0.85rem;
    }
    .info-row .value .highlight {
        color: #2563EB;
        font-weight: 600;
    }
    
    /* ===== TECH STACK ===== */
    .tech-stack {
        display: flex;
        flex-wrap: wrap;
        gap: 10px;
        margin-top: 6px;
    }
    .tech-item {
        background: #F1F5F9;
        padding: 6px 18px;
        border-radius: 24px;
        font-size: 0.8rem;
        font-weight: 500;
        color: #1E293B;
        transition: all 0.3s ease;
        cursor: default;
        border: 1px solid transparent;
    }
    .tech-item:hover {
        background: #2563EB;
        color: white;
        transform: scale(1.06) translateY(-2px);
        box-shadow: 0 4px 16px rgba(37,99,235,0.3);
        border-color: #2563EB;
    }
    .tech-item .icon {
        margin-right: 4px;
    }
    
    /* ===== TIMELINE ===== */
    .timeline {
        display: flex;
        gap: 12px;
        margin: 12px 0 4px 0;
    }
    .timeline-item {
        flex: 1;
        text-align: center;
        padding: 16px 12px;
        background: #F8FAFC;
        border-radius: 14px;
        border: 1px solid #F1F5F9;
        transition: all 0.3s ease;
        position: relative;
    }
    .timeline-item:hover {
        background: #EFF6FF;
        border-color: #2563EB40;
        transform: translateY(-3px);
        box-shadow: 0 4px 16px rgba(37,99,235,0.06);
    }
    .timeline-item .num {
        font-size: 1.4rem;
        font-weight: 800;
        background: linear-gradient(135deg, #2563EB, #7C3AED);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    .timeline-item .label {
        font-size: 0.8rem;
        font-weight: 600;
        color: #0F172A;
        margin-top: 4px;
    }
    .timeline-item .sub {
        font-size: 0.65rem;
        color: #94A3B8;
        margin-top: 2px;
    }
    .timeline-item .connector {
        position: absolute;
        top: 50%;
        right: -12px;
        width: 12px;
        height: 2px;
        background: #E2E8F0;
    }
    .timeline-item:last-child .connector {
        display: none;
    }
    
    /* ===== METRIC CARDS ===== */
    .metric-mini {
        display: flex;
        align-items: center;
        gap: 12px;
        padding: 10px 16px;
        background: #F8FAFC;
        border-radius: 12px;
        border: 1px solid #F1F5F9;
        transition: all 0.2s ease;
    }
    .metric-mini:hover {
        background: #EFF6FF;
        border-color: #2563EB40;
    }
    .metric-mini .num {
        font-size: 1.4rem;
        font-weight: 700;
        color: #0F172A;
        min-width: 50px;
    }
    .metric-mini .desc {
        font-size: 0.8rem;
        color: #64748B;
    }
    
    /* ===== GLOSSARY ===== */
    .glossary-item {
        display: flex;
        gap: 12px;
        padding: 10px 0;
        border-bottom: 1px solid #F8FAFC;
        align-items: flex-start;
    }
    .glossary-item:last-child {
        border-bottom: none;
    }
    .glossary-item .term {
        font-weight: 700;
        color: #0F172A;
        min-width: 100px;
        font-size: 0.85rem;
    }
    .glossary-item .def {
        color: #475569;
        font-size: 0.85rem;
        line-height: 1.5;
    }
    
    /* ===== DATA LINK ===== */
    .data-link {
        display: inline-flex;
        align-items: center;
        gap: 6px;
        color: #2563EB;
        font-weight: 600;
        text-decoration: none;
        transition: all 0.2s ease;
        padding: 4px 0;
        border-bottom: 2px solid transparent;
    }
    .data-link:hover {
        border-bottom-color: #2563EB;
        color: #1D4ED8;
    }
    .data-link .icon {
        font-size: 1rem;
    }
    
    /* ===== RESPONSIVE ===== */
    @media (max-width: 768px) {
        .info-grid {
            grid-template-columns: 1fr;
        }
        .timeline {
            flex-direction: column;
        }
        .timeline-item .connector {
            display: none;
        }
        .hero-card .hero-title {
            font-size: 1.3rem;
        }
        .page-header h1 {
            font-size: 1.6rem;
        }
    }
</style>
""", unsafe_allow_html=True)

# ============================================================
# HEADER - MODERN
# ============================================================
st.markdown("""
<div class="page-header fade-in">
    <h1>Tentang Proyek</h1>
    <p class="subtitle">Analisis Spasio-Temporal Deforestasi Sawit Industrial di Indonesia</p>
</div>
""", unsafe_allow_html=True)

# ============================================================
# HERO CARD
# ============================================================
st.markdown("""
<div class="hero-card fade-in">
    <div class="hero-title">
        🌳 <span>Ancaman Sistemik terhadap Hutan Tropis</span>
    </div>
    <div class="hero-desc">
        <b>Analisis Spasio-Temporal Deforestasi Sawit Industrial di Indonesia</b><br>
        Menggunakan K-Means Clustering dan SARIMA (2001–2024)
    </div>
    <div class="hero-badge">
        📊 Dashboard Interaktif · 514 Kabupaten · 24 Tahun Data
    </div>
</div>
""", unsafe_allow_html=True)

# ============================================================
# METODOLOGI TIMELINE - UPGRADED
# ============================================================
st.markdown("""
<div class="section-card fade-in">
    <h3>
        <span class="card-icon">🔬</span> Metodologi Penelitian
        <span class="badge">4 Tahap</span>
    </h3>
    <div class="timeline">
        <div class="timeline-item">
            <div class="num">01</div>
            <div class="label">Data Collection</div>
            <div class="sub">Trase Earth · 2001–2024</div>
            <div class="connector"></div>
        </div>
        <div class="timeline-item">
            <div class="num">02</div>
            <div class="label">Clustering</div>
            <div class="sub">K-Means · k=4</div>
            <div class="connector"></div>
        </div>
        <div class="timeline-item">
            <div class="num">03</div>
            <div class="label">Forecasting</div>
            <div class="sub">SARIMA · 2025–2030</div>
            <div class="connector"></div>
        </div>
        <div class="timeline-item">
            <div class="num">04</div>
            <div class="label">Visualization</div>
            <div class="sub">Streamlit Dashboard</div>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# ============================================================
# IDENTITAS + TECH STACK - SIDE BY SIDE
# ============================================================
col_id, col_stack = st.columns([1, 1])

with col_id:
    st.markdown("""
    <div class="section-card fade-in">
        <h3>
            <span class="card-icon">👩‍💻</span> Identitas
            <span class="badge">Mahasiswa</span>
        </h3>
        <div class="info-grid">
            <div class="info-row"><span class="label">Nama</span><span class="value">Indah Syahfitri</span></div>
            <div class="info-row"><span class="label">NIM</span><span class="value">2311532016</span></div>
            <div class="info-row"><span class="label">Email</span><span class="value">2311532016_indah@student.unand.ac.id</span></div>
            <div class="info-row"><span class="label">Mata Kuliah</span><span class="value">Visualisasi Data Spasio-Temporal</span></div>
            <div class="info-row"><span class="label">Institusi</span><span class="value">Universitas Andalas (UNAND)</span></div>
            <div class="info-row"><span class="label">Tahun</span><span class="value"><span class="highlight">2026</span></span></div>
        </div>
    </div>
    """, unsafe_allow_html=True)

with col_stack:
    st.markdown("""
    <div class="section-card fade-in">
        <h3>
            <span class="card-icon">🔧</span> Tech Stack
            <span class="badge">Open Source</span>
        </h3>
        <div class="tech-stack">
            <span class="tech-item"><span class="icon">🐍</span> Python</span>
            <span class="tech-item"><span class="icon">📊</span> Streamlit</span>
            <span class="tech-item"><span class="icon">🗺️</span> Folium</span>
            <span class="tech-item"><span class="icon">📈</span> Plotly</span>
            <span class="tech-item"><span class="icon">📦</span> Pandas</span>
            <span class="tech-item"><span class="icon">🧮</span> GeoPandas</span>
            <span class="tech-item"><span class="icon">🤖</span> Scikit-learn</span>
            <span class="tech-item"><span class="icon">📊</span> Statsmodels</span>
            <span class="tech-item"><span class="icon">📉</span> pmdarima</span>
        </div>
        <div style="margin-top:16px; padding-top:14px; border-top:1px solid #F1F5F9;">
            <div style="display:flex; gap:20px; flex-wrap:wrap;">
                <div class="metric-mini">
                    <span class="num">0.795</span>
                    <span class="desc">Silhouette Score<br><span style="font-size:0.65rem; color:#94A3B8;">K-Means Clustering</span></span>
                </div>
                <div class="metric-mini">
                    <span class="num">AIC</span>
                    <span class="desc">Auto-SARIMA<br><span style="font-size:0.65rem; color:#94A3B8;">Model Selection</span></span>
                </div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

# ============================================================
# 🔥 FIX: SUMBER DATA - DENGAN LINK TRASE EARTH
# ============================================================
st.markdown("""
<div class="section-card fade-in">
    <h3>
        <span class="card-icon">📦</span> Sumber Data
        <span class="badge">Open Data</span>
    </h3>
    <div style="display:grid; grid-template-columns:1fr 1fr; gap:6px 40px;">
        <div class="info-row"><span class="label">Dataset</span><span class="value">Spatial Metrics: Indonesia palm oil — palm oil deforestation, annual</span></div>
        <div class="info-row"><span class="label">Sumber</span><span class="value">
            <a class="data-link" href="https://trase.earth/open-data/datasets/spatial-metrics-indonesia-palm-oil-palm-oil-deforestation-annual" target="_blank">
                <span class="icon">🔗</span> Trase Earth Open Data
            </a>
        </span></div>
        <div class="info-row"><span class="label">Lisensi</span><span class="value">CC BY 4.0</span></div>
        <div class="info-row"><span class="label">Wilayah</span><span class="value">Indonesia (514 Kabupaten)</span></div>
        <div class="info-row"><span class="label">Periode</span><span class="value">2001–2024 (24 tahun)</span></div>
        <div class="info-row"><span class="label">Format</span><span class="value">CSV · GeoJSON</span></div>
    </div>
</div>
""", unsafe_allow_html=True)

# ============================================================
# GLOSARIUM / ISTILAH
# ============================================================
with st.expander("📖 Glosarium Istilah Teknis", expanded=False):
    st.markdown("""
    <div style="padding:8px 0;">
        <div class="glossary-item">
            <span class="term">🌲 Deforestasi</span>
            <span class="def">Hilangnya tutupan hutan secara permanen akibat aktivitas manusia, seperti pembukaan lahan untuk perkebunan sawit.</span>
        </div>
        <div class="glossary-item">
            <span class="term">📊 K-Means</span>
            <span class="def">Algoritma clustering yang mengelompokkan data berdasarkan kesamaan karakteristik. Dalam proyek ini, digunakan untuk mengelompokkan kabupaten berdasarkan pola deforestasi.</span>
        </div>
        <div class="glossary-item">
            <span class="term">📈 SARIMA</span>
            <span class="def">Model statistik untuk forecasting data deret waktu (time series) yang memiliki pola musiman. Singkatan dari Seasonal AutoRegressive Integrated Moving Average.</span>
        </div>
        <div class="glossary-item">
            <span class="term">📐 Silhouette Score</span>
            <span class="def">Metrik untuk mengevaluasi kualitas clustering. Nilai >0,7 menunjukkan struktur kluster yang baik.</span>
        </div>
        <div class="glossary-item">
            <span class="term">📊 RMSE & MAE</span>
            <span class="def">Metrik untuk mengukur akurasi model forecasting. Semakin kecil nilainya, semakin akurat model.</span>
        </div>
        <div class="glossary-item">
            <span class="term">🗺️ Choropleth</span>
            <span class="def">Peta tematik di mana area (kabupaten) diwarnai berdasarkan nilai data yang diwakilinya. Semakin gelap warna = semakin tinggi nilai.</span>
        </div>
        <div class="glossary-item">
            <span class="term">📜 Moratorium</span>
            <span class="def">Kebijakan penghentian sementara (moratorium) izin baru untuk pembukaan hutan alam primer dan lahan gambut yang diberlakukan pada 2011.</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

# ============================================================
# FOOTER / CREDIT
# ============================================================
st.markdown("""
<div class="fade-in" style="text-align:center; padding:20px 0 10px 0; border-top:1px solid #F1F5F9; margin-top:8px;">
    <div style="font-size:0.8rem; color:#94A3B8;">
        Dibuat dengan ❤️ oleh 
        <span style="color:#0F172A; font-weight:600;">Indah Syahfitri</span> 
        · NIM 2311532016 · UNAND 2026
        <br>
        <span style="font-size:0.7rem;">
            Visualisasi Data Spasio-Temporal · Lisensi CC BY 4.0
        </span>
    </div>
    <div style="display:flex; justify-content:center; gap:20px; margin-top:8px; font-size:0.7rem; color:#94A3B8;">
        <span>🐍 Python</span>
        <span>•</span>
        <span>📊 Streamlit</span>
        <span>•</span>
        <span>🗺️ Folium</span>
        <span>•</span>
        <span>📈 Plotly</span>
    </div>
</div>
""", unsafe_allow_html=True)