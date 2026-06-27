# app.py - Modern Dashboard Landing dengan Animasi
import streamlit as st
import pandas as pd
from utils.load_data import load_df_long, load_df_clustered

# ============================================================
# PAGE CONFIG
# ============================================================
st.set_page_config(
    page_title="Deforestasi Dashboard",
    page_icon="🌿",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# ============================================================
# GLOBAL CSS DENGAN ANIMASI
# ============================================================
st.markdown("""
<style>
    /* ===== ANIMASI ===== */
    @keyframes fadeInUp {
        from { opacity: 0; transform: translateY(30px); }
        to { opacity: 1; transform: translateY(0); }
    }
    
    @keyframes fadeInScale {
        from { opacity: 0; transform: scale(0.95); }
        to { opacity: 1; transform: scale(1); }
    }
    
    @keyframes slideInLeft {
        from { opacity: 0; transform: translateX(-30px); }
        to { opacity: 1; transform: translateX(0); }
    }
    
    @keyframes slideInRight {
        from { opacity: 0; transform: translateX(30px); }
        to { opacity: 1; transform: translateX(0); }
    }
    
    @keyframes pulse {
        0%, 100% { transform: scale(1); }
        50% { transform: scale(1.02); }
    }
    
    .fade-in {
        animation: fadeInUp 0.7s ease forwards;
    }
    .fade-in-delay-1 {
        animation: fadeInUp 0.7s ease 0.1s forwards;
        opacity: 0;
    }
    .fade-in-delay-2 {
        animation: fadeInUp 0.7s ease 0.2s forwards;
        opacity: 0;
    }
    .fade-in-delay-3 {
        animation: fadeInUp 0.7s ease 0.3s forwards;
        opacity: 0;
    }
    .fade-in-delay-4 {
        animation: fadeInUp 0.7s ease 0.4s forwards;
        opacity: 0;
    }
    .fade-scale {
        animation: fadeInScale 0.8s ease forwards;
    }
    .slide-left {
        animation: slideInLeft 0.7s ease forwards;
    }
    .slide-right {
        animation: slideInRight 0.7s ease forwards;
    }
    .pulse {
        animation: pulse 2s ease-in-out infinite;
    }
    
    /* ===== RESET & BASE ===== */
    .main {
        background: #F8FAFC;
    }
    .stApp {
        background: #F8FAFC;
    }
    
    /* ===== TYPOGRAPHY ===== */
    .hero-title {
        font-size: 3.2rem;
        font-weight: 800;
        color: #0F172A;
        letter-spacing: -1px;
        line-height: 1.2;
    }
    .hero-title span {
        background: linear-gradient(135deg, #2563EB, #7C3AED);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    .hero-subtitle {
        font-size: 1.1rem;
        color: #64748B;
        margin-top: 8px;
        line-height: 1.6;
        max-width: 600px;
    }
    
    /* ===== CARDS ===== */
    .card {
        background: #FFFFFF;
        border-radius: 16px;
        padding: 24px 20px;
        box-shadow: 0 1px 3px rgba(0,0,0,0.04), 0 4px 16px rgba(0,0,0,0.04);
        border: 1px solid #F1F5F9;
        transition: all 0.25s ease;
        height: 100%;
    }
    .card:hover {
        transform: translateY(-4px);
        box-shadow: 0 8px 32px rgba(37,99,235,0.10);
        border-color: #2563EB30;
    }
    .card-icon {
        font-size: 1.8rem;
        margin-bottom: 12px;
        display: block;
    }
    .card-title {
        font-size: 1rem;
        font-weight: 600;
        color: #0F172A;
        margin-bottom: 4px;
    }
    .card-desc {
        font-size: 0.9rem;
        color: #64748B;
        line-height: 1.5;
        margin-bottom: 12px;
    }
    .card-badge {
        display: inline-block;
        padding: 2px 12px;
        border-radius: 20px;
        font-size: 0.7rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.3px;
        color: #2563EB;
        background: #EFF6FF;
    }
    
    /* ===== KPI METRIC ===== */
    .kpi-card {
        background: #FFFFFF;
        border-radius: 14px;
        padding: 18px 20px;
        border: 1px solid #F1F5F9;
        box-shadow: 0 1px 3px rgba(0,0,0,0.03);
        transition: all 0.3s ease;
    }
    .kpi-card:hover {
        border-color: #2563EB40;
        box-shadow: 0 4px 16px rgba(37,99,235,0.06);
        transform: translateY(-3px);
    }
    .kpi-value {
        font-size: 2.2rem;
        font-weight: 700;
        color: #0F172A;
        line-height: 1.2;
    }
    .kpi-label {
        font-size: 0.8rem;
        color: #64748B;
        font-weight: 500;
        text-transform: uppercase;
        letter-spacing: 0.3px;
    }
    .kpi-trend {
        font-size: 0.75rem;
        font-weight: 600;
        padding: 2px 10px;
        border-radius: 20px;
        display: inline-block;
        margin-top: 4px;
    }
    .kpi-trend.up { color: #22C55E; background: #ECFDF5; }
    .kpi-trend.down { color: #EF4444; background: #FEF2F2; }
    .kpi-trend.neutral { color: #F59E0B; background: #FFFBEB; }
    
    /* ===== NAV CARD ===== */
    .nav-card {
        background: #FFFFFF;
        border-radius: 14px;
        padding: 20px;
        text-align: center;
        border: 1px solid #F1F5F9;
        cursor: pointer;
        transition: all 0.3s ease;
        text-decoration: none;
        display: block;
        height: 100%;
    }
    .nav-card:hover {
        transform: translateY(-6px) scale(1.02);
        border-color: #2563EB;
        box-shadow: 0 12px 40px rgba(37,99,235,0.12);
    }
    .nav-card .icon {
        font-size: 2.8rem;
        display: block;
        margin-bottom: 8px;
        transition: transform 0.3s ease;
    }
    .nav-card:hover .icon {
        transform: scale(1.1) rotate(-5deg);
    }
    .nav-card .label {
        font-weight: 600;
        color: #0F172A;
        font-size: 1rem;
    }
    .nav-card .desc {
        font-size: 0.8rem;
        color: #94A3B8;
        margin-top: 4px;
    }
    
    /* ===== DIVIDER ===== */
    .section-divider {
        height: 1px;
        background: linear-gradient(90deg, transparent, #E2E8F0, transparent);
        margin: 32px 0;
    }
    
    /* ===== SECTION LABEL ===== */
    .section-label {
        font-size: 0.75rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 1px;
        color: #94A3B8;
        margin-bottom: 4px;
    }
    .section-heading {
        font-size: 1.6rem;
        font-weight: 700;
        color: #0F172A;
        margin-bottom: 20px;
    }
    
    /* ===== INSIGHT BOX ===== */
    .insight-box {
        background: linear-gradient(135deg, #2563EB10, #7C3AED10);
        border-radius: 16px;
        padding: 20px 24px;
        border: 1px solid #2563EB20;
        transition: all 0.3s ease;
    }
    .insight-box:hover {
        border-color: #2563EB40;
        box-shadow: 0 4px 20px rgba(37,99,235,0.06);
    }
    
    /* ===== RESPONSIVE ===== */
    @media (max-width: 768px) {
        .hero-title {
            font-size: 2rem;
        }
        .kpi-value {
            font-size: 1.6rem;
        }
        .section-heading {
            font-size: 1.2rem;
        }
    }
</style>
""", unsafe_allow_html=True)

# ============================================================
# LOAD DATA (tanpa mengubah logic)
# ============================================================
with st.spinner("⏳ Memuat data..."):
    df_long = load_df_long()
    df_clust = load_df_clustered()

# Hitung KPI
total_kab = len(df_clust)
total_deforestasi = df_long["deforestasi_ha"].sum()
cluster_dominan = df_clust["cluster_name"].value_counts().idxmax()
trend_terakhir = df_long.groupby("year")["deforestasi_ha"].sum().tail(3).values
trend_label = "Meningkat" if trend_terakhir[-1] > trend_terakhir[0] else "Menurun"

# ============================================================
# HERO SECTION - DENGAN ANIMASI
# ============================================================
col_hero_left, col_hero_right = st.columns([2, 1])

with col_hero_left:
    st.markdown("""
    <div class="fade-in" style="padding: 24px 0;">
        <div class="hero-title">
            🌿 <span>Ancaman Sistemik</span><br>Hutan Tropis
        </div>
        <div class="hero-subtitle">
            Analisis Spasio-Temporal Deforestasi Sawit Industrial di Indonesia<br>
            <span style="color: #94A3B8; font-size: 0.9rem;">2001–2024 · K-Means Clustering · SARIMA Forecasting</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

with col_hero_right:
    st.markdown(f"""
    <div class="fade-in-delay-1" style="background: linear-gradient(135deg, #2563EB10, #7C3AED10); 
                border-radius: 16px; padding: 24px; border: 1px solid #2563EB20;
                margin-top: 12px; transition: all 0.3s ease;">
        <div style="font-size: 0.8rem; color: #64748B; font-weight: 600; 
                    text-transform: uppercase; letter-spacing: 0.5px;">
            📌 Insight Cepat
        </div>
        <div style="font-size: 1.1rem; font-weight: 700; color: #0F172A; margin-top: 4px;">
            {total_deforestasi:,.0f} ha deforestasi
        </div>
        <div style="font-size: 0.9rem; color: #64748B;">
            dari {total_kab:,} kabupaten · Kluster dominan: <b>{cluster_dominan}</b>
        </div>
        <div style="margin-top: 8px;">
            <span class="kpi-trend {"up" if trend_label == "Meningkat" else "down"}">
                {"📈" if trend_label == "Meningkat" else "📉"} {trend_label}
            </span>
        </div>
    </div>
    """, unsafe_allow_html=True)

st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)

# ============================================================
# KPI CARDS - DENGAN ANIMASI
# ============================================================
st.markdown('<div class="section-label fade-in">📊 Key Metrics</div>', unsafe_allow_html=True)

k1, k2, k3, k4 = st.columns(4)

with k1:
    st.markdown(f"""
    <div class="kpi-card fade-in-delay-1">
        <div class="kpi-value">{total_kab:,}</div>
        <div class="kpi-label">🏙️ Total Kabupaten</div>
    </div>
    """, unsafe_allow_html=True)

with k2:
    st.markdown(f"""
    <div class="kpi-card fade-in-delay-2">
        <div class="kpi-value">{total_deforestasi:,.0f}</div>
        <div class="kpi-label">🌲 Total Deforestasi (ha)</div>
    </div>
    """, unsafe_allow_html=True)

with k3:
    st.markdown(f"""
    <div class="kpi-card fade-in-delay-3">
        <div class="kpi-value">{cluster_dominan}</div>
        <div class="kpi-label">📊 Kluster Dominan</div>
    </div>
    """, unsafe_allow_html=True)

with k4:
    st.markdown(f"""
    <div class="kpi-card fade-in-delay-4">
        <div class="kpi-value">2024</div>
        <div class="kpi-label">📅 Tahun Terakhir</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)

# ============================================================
# NAVIGATION CARDS - DENGAN ANIMASI
# ============================================================
st.markdown('<div class="section-label fade-in">🧭 Navigasi Dashboard</div>', unsafe_allow_html=True)
st.markdown('<div class="section-heading fade-in">Jelajahi Analisis</div>', unsafe_allow_html=True)

nav1, nav2, nav3, nav4 = st.columns(4)

with nav1:
    st.markdown("""
    <a href="/Peta_Deforestasi" target="_self" style="text-decoration: none;">
        <div class="nav-card fade-in-delay-1">
            <span class="icon">🗺️</span>
            <div class="label">Peta Deforestasi</div>
            <div class="desc">Choropleth interaktif per kabupaten</div>
            <span class="card-badge" style="margin-top: 8px;">View Map</span>
        </div>
    </a>
    """, unsafe_allow_html=True)

with nav2:
    st.markdown("""
    <a href="/Clustering" target="_self" style="text-decoration: none;">
        <div class="nav-card fade-in-delay-2">
            <span class="icon">📊</span>
            <div class="label">Clustering</div>
            <div class="desc">K-Means trajectory-based k=4</div>
            <span class="card-badge" style="margin-top: 8px;">Explore</span>
        </div>
    </a>
    """, unsafe_allow_html=True)

with nav3:
    st.markdown("""
    <a href="/Forecasting" target="_self" style="text-decoration: none;">
        <div class="nav-card fade-in-delay-3">
            <span class="icon">📈</span>
            <div class="label">Forecasting</div>
            <div class="desc">Proyeksi SARIMA hingga 2030</div>
            <span class="card-badge" style="margin-top: 8px;">Predict</span>
        </div>
    </a>
    """, unsafe_allow_html=True)

with nav4:
    st.markdown("""
    <a href="/Tentang" target="_self" style="text-decoration: none;">
        <div class="nav-card fade-in-delay-4">
            <span class="icon">ℹ️</span>
            <div class="label">Tentang Proyek</div>
            <div class="desc">Metodologi & teknologi yang digunakan</div>
            <span class="card-badge" style="margin-top: 8px;">Learn More</span>
        </div>
    </a>
    """, unsafe_allow_html=True)

st.markdown('<div class="section-divider"></div>', unsafe_allow_html=True)

# ============================================================
# QUICK INSIGHTS - DENGAN ANIMASI
# ============================================================
with st.expander("📋 Ringkasan Metodologi", expanded=False):
    st.markdown("""
    <div style="display:grid; grid-template-columns:1fr 1fr; gap:20px; padding:8px 0;">
        <div style="background:#F8FAFC; border-radius:12px; padding:16px 20px; border-left:4px solid #2563EB;">
            <div style="font-weight:700; color:#0F172A; font-size:0.95rem;">🔬 K-Means Clustering (k=4)</div>
            <ul style="color:#475569; font-size:0.9rem; line-height:1.8; padding-left:20px;">
                <li>514 kabupaten dikelompokkan berdasarkan pola temporal</li>
                <li>Silhouette Score: <b style="color:#2563EB;">0.795</b></li>
                <li>4 kluster: Zero · Moderate · Declining · High</li>
            </ul>
        </div>
        <div style="background:#F8FAFC; border-radius:12px; padding:16px 20px; border-left:4px solid #E17055;">
            <div style="font-weight:700; color:#0F172A; font-size:0.95rem;">📈 SARIMA Forecasting</div>
            <ul style="color:#475569; font-size:0.9rem; line-height:1.8; padding-left:20px;">
                <li>Auto-ARIMA per kluster (AIC criterion)</li>
                <li>Training: 2001–2019 | Test: 2020–2024</li>
                <li>Proyeksi: <b style="color:#E17055;">2025–2030</b></li>
            </ul>
        </div>
    </div>
    """, unsafe_allow_html=True)

# ============================================================
# FOOTER - DENGAN ANIMASI
# ============================================================
st.markdown("""
<div class="fade-in" style="text-align:center; padding:20px 0 10px 0; border-top:1px solid #F1F5F9; margin-top:16px;">
    <div style="font-size:0.8rem; color:#94A3B8;">
        Dibuat dengan ❤️ oleh 
        <span style="color:#0F172A; font-weight:600;">Indah Syahfitri</span> 
        · NIM 2311532016 · UNAND 2026
    </div>
</div>
""", unsafe_allow_html=True)