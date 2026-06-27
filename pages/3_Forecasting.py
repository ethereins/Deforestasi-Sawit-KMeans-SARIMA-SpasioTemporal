# pages/3_Forecasting.py
import streamlit as st
import pandas as pd
import plotly.express as px

from utils.load_data import (
    load_df_clustered,
    load_forecast,
    load_evaluasi,
    WARNA_KLUSTER,
    YEAR_COLS
)

from utils.forecasting_utils import plot_forecast

st.set_page_config(page_title="Forecasting", page_icon="📈", layout="wide")

# ============================================================
# CSS - MODERN DENGAN ANIMASI FADE-IN
# ============================================================
st.markdown("""
<style>
    /* ===== ANIMASI FADE-IN ===== */
    @keyframes fadeInUp {
        from {
            opacity: 0;
            transform: translateY(30px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    @keyframes fadeInScale {
        from {
            opacity: 0;
            transform: scale(0.95);
        }
        to {
            opacity: 1;
            transform: scale(1);
        }
    }
    
    @keyframes slideInLeft {
        from {
            opacity: 0;
            transform: translateX(-30px);
        }
        to {
            opacity: 1;
            transform: translateX(0);
        }
    }
    
    @keyframes slideInRight {
        from {
            opacity: 0;
            transform: translateX(30px);
        }
        to {
            opacity: 1;
            transform: translateX(0);
        }
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
    .fade-in-delay-5 {
        animation: fadeInUp 0.7s ease 0.5s forwards;
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
    
    /* ===== PAGE HEADER ===== */
    .page-header {
        text-align: center;
        padding: 16px 0 8px 0;
    }
    .page-header h1 {
        font-size: 2.2rem;
        font-weight: 800;
        background: linear-gradient(135deg, #E17055 0%, #D63031 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin: 0;
        letter-spacing: -0.5px;
    }
    .page-header p {
        color: #64748B;
        font-size: 1rem;
        margin-top: 4px;
    }
    
    /* ===== EVALUATION CARD ===== */
    .eval-card {
        background: #FFFFFF;
        border-radius: 14px;
        padding: 16px 20px;
        border: 1px solid #F1F5F9;
        text-align: center;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        cursor: default;
        height: 100%;
        position: relative;
        overflow: hidden;
    }
    .eval-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 4px;
        background: var(--card-color);
        opacity: 0;
        transition: opacity 0.3s ease;
    }
    .eval-card:hover::before {
        opacity: 1;
    }
    .eval-card:hover {
        border-color: var(--card-color, #2563EB);
        box-shadow: 0 8px 32px rgba(37,99,235,0.10);
        transform: translateY(-4px) scale(1.01);
    }
    .eval-card .name {
        font-weight: 700;
        color: #0F172A;
        font-size: 0.95rem;
    }
    .eval-card .value {
        font-size: 1.6rem;
        font-weight: 800;
        line-height: 1.3;
    }
    .eval-card .sub {
        font-size: 0.75rem;
        color: #94A3B8;
        font-weight: 500;
        margin-top: 2px;
    }
    .eval-card .icon-big {
        font-size: 1.8rem;
        display: block;
        margin-bottom: 2px;
    }
    
    /* ===== INSIGHT BOX ===== */
    .insight-box {
        background: #F8FAFC;
        border-radius: 12px;
        padding: 16px 20px;
        border-left: 4px solid #E17055;
        margin: 12px 0;
        transition: all 0.3s ease;
    }
    .insight-box:hover {
        background: #FEF2F2;
        border-left-color: #D63031;
    }
    .insight-box .title {
        font-weight: 600;
        color: #0F172A;
        font-size: 0.9rem;
        display: flex;
        align-items: center;
        gap: 8px;
    }
    .insight-box .desc {
        color: #475569;
        font-size: 0.9rem;
        margin-top: 6px;
        line-height: 1.7;
    }
    .insight-box .highlight {
        color: #E17055;
        font-weight: 600;
    }
    
    /* ===== EDU BOX ===== */
    .edu-box {
        background: #F0FDF4;
        border-radius: 14px;
        padding: 18px 22px;
        border-left: 4px solid #22C55E;
        margin: 12px 0;
        transition: all 0.3s ease;
    }
    .edu-box:hover {
        background: #ECFDF5;
        box-shadow: 0 4px 16px rgba(34,197,94,0.10);
    }
    .edu-box .title {
        font-weight: 700;
        color: #166534;
        font-size: 1rem;
        display: flex;
        align-items: center;
        gap: 8px;
    }
    .edu-box .desc {
        color: #1E293B;
        font-size: 0.95rem;
        margin-top: 6px;
        line-height: 1.8;
    }
    .edu-box .highlight {
        color: #22C55E;
        font-weight: 600;
    }
    .edu-box .term {
        display: inline-block;
        background: #DCFCE7;
        padding: 3px 14px;
        border-radius: 20px;
        font-size: 0.8rem;
        font-weight: 600;
        color: #166534;
    }
    
    /* ===== METRIC CARD ===== */
    .metric-card {
        background: #FFFFFF;
        border-radius: 14px;
        padding: 14px 18px;
        border: 1px solid #F1F5F9;
        text-align: center;
        transition: all 0.3s ease;
    }
    .metric-card:hover {
        border-color: #E1705540;
        box-shadow: 0 4px 20px rgba(225,112,85,0.08);
        transform: translateY(-2px);
    }
    .metric-card .num {
        font-size: 1.6rem;
        font-weight: 800;
        color: #0F172A;
    }
    .metric-card .label {
        font-size: 0.7rem;
        color: #94A3B8;
        font-weight: 500;
        margin-top: 2px;
    }
    
    /* ===== SIDEBAR ===== */
    .sidebar-header {
        font-weight: 700;
        color: #0F172A;
        padding: 10px 0;
        border-bottom: 2px solid #E17055;
        margin-bottom: 14px;
        font-size: 0.9rem;
        display: flex;
        align-items: center;
        gap: 8px;
    }
    
    /* ===== CI EXPLANATION ===== */
    .ci-visual {
        background: #FFFFFF;
        border-radius: 12px;
        padding: 16px;
        border: 1px solid #E2E8F0;
        margin: 8px 0;
        text-align: center;
    }
    .ci-visual .bar {
        height: 20px;
        border-radius: 8px;
        background: linear-gradient(90deg, #E17055, #F59E0B, #E17055);
        margin: 8px 0;
        position: relative;
    }
    .ci-visual .bar .line {
        position: absolute;
        top: -4px;
        height: 28px;
        width: 3px;
        background: #0F172A;
        border-radius: 2px;
    }
    .ci-visual .labels {
        display: flex;
        justify-content: space-between;
        font-size: 0.7rem;
        color: #94A3B8;
    }
    
    /* ===== RESPONSIVE ===== */
    @media (max-width: 768px) {
        .page-header h1 {
            font-size: 1.5rem;
        }
        .eval-card .value {
            font-size: 1.2rem;
        }
    }
</style>
""", unsafe_allow_html=True)

# ============================================================
# HEADER - DENGAN ANIMASI
# ============================================================
st.markdown("""
<div class="page-header fade-in">
    <h1>Forecasting SARIMA per Kluster</h1>
    <p>Proyeksi laju deforestasi sawit industrial per kluster hingga 2030</p>
</div>
""", unsafe_allow_html=True)

# ============================================================
# EDUKASI: APA ITU FORECASTING?
# ============================================================
with st.expander("🔮 Apa itu Forecasting? (Klik untuk belajar)", expanded=False):
    st.markdown("""
    <div style="background: linear-gradient(135deg, #F0FDF4, #ECFDF5); border-radius: 14px; padding: 20px 24px; border: 1px solid #DCFCE7;">
        <div style="display: flex; gap: 16px; align-items: flex-start; flex-wrap: wrap;">
            <div style="flex: 2;">
                <div style="font-weight: 700; color: #0F172A; font-size: 1.1rem; margin-bottom: 6px;">
                    📈 Forecasting = Memprediksi Masa Depan
                </div>
                <div style="color: #475569; font-size: 0.95rem; line-height: 1.8;">
                    <b>Forecasting</b> atau <b>peramalan</b> adalah teknik untuk memprediksi nilai di masa depan 
                    berdasarkan pola data historis.
                    <br><br>
                    Di sini, kami menggunakan model <span style="color: #22C55E; font-weight: 600;">SARIMA</span> 
                    (Seasonal AutoRegressive Integrated Moving Average) — sebuah metode statistik yang 
                    sangat baik untuk data <span style="color: #22C55E; font-weight: 600;">time series</span> 
                    (data deret waktu) seperti deforestasi tahunan.
                    <br><br>
                    <span style="background: #DCFCE7; padding: 3px 14px; border-radius: 20px; font-size: 0.85rem; color: #166534; font-weight: 600;">
                        📌 Intinya: Pola 2001–2024 → Prediksi 2025–2030
                    </span>
                </div>
            </div>
            <div style="flex: 1; min-width: 120px; background: #FFFFFF; border-radius: 12px; padding: 16px; border: 1px solid #E2E8F0; text-align: center;">
                <div style="font-size: 2.5rem; margin-bottom: 4px;">⏳</div>
                <div style="font-weight: 700; color: #0F172A; font-size: 0.9rem;">24 Tahun Data</div>
                <div style="font-size: 0.75rem; color: #94A3B8;">2001 → 2024</div>
                <div style="margin-top: 8px; background: #F1F5F9; border-radius: 8px; padding: 6px;">
                    <span style="font-size: 0.7rem; color: #475569;">Proyeksi</span><br>
                    <span style="font-size: 1.1rem; font-weight: 700; color: #E17055;">2025 → 2030</span>
                </div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

# ============================================================
# LOAD DATA
# ============================================================
with st.spinner("⏳ Loading forecasting data..."):
    df_clust = load_df_clustered()
    df_forecast = load_forecast()
    df_eval = load_evaluasi()

# ============================================================
# DATA PREP (tidak diubah)
# ============================================================
df_clust.columns = df_clust.columns.map(str)
YEAR_COLS = [str(y) for y in YEAR_COLS]
available_years = [col for col in YEAR_COLS if col in df_clust.columns]

cluster_hist = {}
for c in sorted(df_clust["cluster"].unique()):
    nama = df_clust[df_clust["cluster"] == c]["cluster_name"].iloc[0]
    total = df_clust[df_clust["cluster"] == c][available_years].sum(axis=0)
    total.index = available_years
    cluster_hist[c] = {"nama": nama, "series": total}

# ============================================================
# SIDEBAR - DENGAN EDUKASI CI
# ============================================================
with st.sidebar:
    st.markdown("""
    <div class="sidebar-header">
        ⚙️ Filter Forecast
    </div>
    """, unsafe_allow_html=True)
    
    kluster_list = [d["nama"] for d in cluster_hist.values() if d["nama"] != "Zero"]
    kluster_sel = st.multiselect(
        "Tampilkan Kluster",
        options=kluster_list,
        default=kluster_list,
        label_visibility="collapsed"
    )
    
    show_ci = st.checkbox(
        "📊 Tampilkan Confidence Interval (±10%)",
        value=True,
        label_visibility="visible"
    )
    
    # EDUKASI: Visualisasi CI di Sidebar
    st.markdown("---")
    st.markdown("""
    <div style="font-size:0.8rem; color:#64748B; line-height:1.8;">
        <b>💡 Apa itu Confidence Interval?</b><br>
        Interval kepercayaan menunjukkan <b>rentang ketidakpastian</b> prediksi.
    </div>
    """, unsafe_allow_html=True)
    
    # Visualisasi CI sederhana
    if show_ci:
        st.markdown("""
        <div class="ci-visual">
            <div style="font-size:0.75rem; color:#64748B; font-weight:500;">Prediksi: 10.000 ha</div>
            <div class="bar" style="position:relative;">
                <div style="position:absolute; left:50%; top:-4px; height:28px; width:3px; background:#0F172A; border-radius:2px;"></div>
                <div style="position:absolute; left:40%; top:6px; height:8px; width:20%; background:#E17055; border-radius:4px;"></div>
            </div>
            <div class="labels">
                <span>9.000 ha</span>
                <span style="font-weight:600; color:#0F172A;">±10%</span>
                <span>11.000 ha</span>
            </div>
            <div style="font-size:0.6rem; color:#94A3B8; margin-top:4px;">
                Nilai sebenarnya diperkirakan antara 9.000–11.000 ha
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    st.markdown("""
    <div style="font-size:0.7rem; color:#94A3B8; text-align:center;">
        <b>📈 SARIMA Forecasting</b><br>
        Auto-ARIMA · AIC Criterion
    </div>
    """, unsafe_allow_html=True)

# ============================================================
# METRICS - DENGAN ANIMASI
# ============================================================
st.markdown("""
<div class="fade-in" style="font-size:1rem; font-weight:700; color:#0F172A; margin-bottom:12px;">
    📊 Evaluasi Model SARIMA
</div>
""", unsafe_allow_html=True)

# EDUKASI: Apa itu RMSE dan MAE?
with st.expander("📊 Apa itu RMSE dan MAE? (Klik untuk belajar)", expanded=False):
    st.markdown("""
    <div class="edu-box">
        <div class="title">📊 RMSE & MAE = Cara Mengukur Akurasi Prediksi</div>
        <div class="desc">
            <b>RMSE</b> (Root Mean Square Error) dan <b>MAE</b> (Mean Absolute Error) 
            adalah metrik untuk mengukur <span class="highlight">seberapa akurat</span> 
            model dalam memprediksi.
            <br><br>
            • <b>MAE</b>: Rata-rata selisih antara prediksi dan nilai aktual.<br>
            • <b>RMSE</b>: Mirip MAE, tetapi lebih sensitif terhadap error besar.
            <br><br>
            <span class="term">📌 Semakin kecil nilai RMSE/MAE = semakin akurat model!</span>
            <br><br>
            Contoh: MAE = 826 ha berarti rata-rata prediksi meleset sekitar 826 hektar.
        </div>
    </div>
    """, unsafe_allow_html=True)

df_eval_aktif = df_eval[df_eval["cluster_name"] != "Zero"].reset_index(drop=True)

# Deteksi nama kolom
if "rmse_ha" in df_eval.columns:
    rmse_col = "rmse_ha"
    mae_col = "mae_ha"
elif "RMSE (ha)" in df_eval.columns:
    rmse_col = "RMSE (ha)"
    mae_col = "MAE (ha)"
elif "RMSE" in df_eval.columns:
    rmse_col = "RMSE"
    mae_col = "MAE"
else:
    rmse_col = df_eval.columns[df_eval.columns.str.contains("rmse|RMSE", case=False)].tolist()
    mae_col = df_eval.columns[df_eval.columns.str.contains("mae|MAE", case=False)].tolist()
    rmse_col = rmse_col[0] if rmse_col else "rmse_ha"
    mae_col = mae_col[0] if mae_col else "mae_ha"

# Tampilkan evaluasi cards dengan animasi
eval_cols = st.columns(len(df_eval_aktif))
for idx, (col, row) in enumerate(zip(eval_cols, df_eval_aktif.iterrows())):
    _, row_data = row
    with col:
        warna = WARNA_KLUSTER.get(row_data["cluster_name"], "#636E72")
        rmse_val = row_data[rmse_col]
        mae_val = row_data[mae_col]
        delay_class = f"fade-in-delay-{idx+1}"
        
        st.markdown(f"""
        <div class="eval-card {delay_class}" style="--card-color:{warna};">
            <span class="icon-big">{['🟢','🟠','🔵','🔴'][idx]}</span>
            <div class="name" style="color:{warna};">{row_data['cluster_name']}</div>
            <div class="value" style="color:{warna};">{rmse_val:,.0f}</div>
            <div class="sub">RMSE · MAE: {mae_val:,.0f} ha</div>
        </div>
        """, unsafe_allow_html=True)

st.markdown("---")

# ============================================================
# MAIN CHART - DENGAN ANIMASI
# ============================================================
st.markdown("""
<div class="fade-in" style="font-size:1rem; font-weight:700; color:#0F172A; margin-bottom:12px;">
    🔮 Proyeksi Deforestasi 2025–2030
</div>
""", unsafe_allow_html=True)

# Chart
fig = plot_forecast(cluster_hist, df_forecast, kluster_sel, show_ci)
fig.update_layout(
    plot_bgcolor='rgba(0,0,0,0)',
    paper_bgcolor='rgba(0,0,0,0)',
    legend=dict(
        orientation="h",
        yanchor="bottom",
        y=1.02,
        xanchor="right",
        x=1
    ),
    hovermode='x unified',
    height=450,
    margin=dict(l=40, r=40, t=40, b=40),
    font=dict(color="#475569")
)
st.plotly_chart(fig, use_container_width=True, key="forecast_chart")

# EDUKASI: Cara membaca grafik forecast
st.markdown("""
<div class="edu-box fade-in">
    <div class="title">📈 Cara Membaca Grafik Forecasting</div>
    <div class="desc">
        Grafik ini menampilkan <span class="highlight">dua jenis data</span>:
        <br><br>
        <b>1. Garis penuh (Historis)</b> — Data deforestasi aktual dari 2001–2024<br>
        <b>2. Garis putus-putus (Forecast)</b> — Prediksi deforestasi untuk 2025–2030
        <br><br>
        <span class="term">📌 Perhatikan:</span> Jika garis putus-putus <span class="highlight">naik</span>, 
        berarti deforestasi diperkirakan meningkat. Jika <span class="highlight">turun</span>, 
        berarti deforestasi diperkirakan menurun.
        <br><br>
        <span style="color:#94A3B8; font-size:0.85rem;">
            Area berbayang di sekitar garis prediksi adalah Confidence Interval (±10%).
        </span>
    </div>
</div>
""", unsafe_allow_html=True)

# ============================================================
# INSIGHT PANEL + TABLE - DENGAN ANIMASI
# ============================================================
col_insight, col_table = st.columns([1, 2])

with col_insight:
    st.markdown("""
    <div class="insight-box fade-in">
        <div style="font-weight:700; color:#0F172A; margin-bottom:8px;">📌 Interpretasi</div>
    """, unsafe_allow_html=True)
    
    if len(kluster_sel) > 0:
        latest = df_forecast[df_forecast["cluster_name"].isin(kluster_sel)]
        latest_2030 = latest[latest["year"] == 2030]
        if len(latest_2030) > 0:
            max_cluster = latest_2030.loc[latest_2030["forecast_ha"].idxmax(), "cluster_name"]
            max_val = latest_2030["forecast_ha"].max()
            warna = WARNA_KLUSTER.get(max_cluster, "#E17055")
            st.markdown(f"""
            <div style="padding:10px 0; border-bottom:1px solid #F1F5F9;">
                <div style="font-size:0.75rem; color:#94A3B8; font-weight:600;">🏆 Tertinggi 2030</div>
                <div style="font-size:1.3rem; font-weight:800; color:{warna};">{max_cluster}</div>
                <div style="font-size:0.95rem; color:#64748B;">{max_val:,.0f} ha</div>
            </div>
            """, unsafe_allow_html=True)
    
    st.markdown("""
    <div style="padding:10px 0; border-bottom:1px solid #F1F5F9;">
        <div style="font-size:0.75rem; color:#94A3B8; font-weight:600;">🧠 Model</div>
        <div style="font-size:0.95rem; color:#0F172A; font-weight:600;">Auto-SARIMA</div>
        <div style="font-size:0.8rem; color:#94A3B8;">AIC Criterion</div>
    </div>
    <div style="padding:10px 0; border-bottom:1px solid #F1F5F9;">
        <div style="font-size:0.75rem; color:#94A3B8; font-weight:600;">📚 Training</div>
        <div style="font-size:0.95rem; color:#0F172A; font-weight:600;">2001–2019</div>
        <div style="font-size:0.8rem; color:#94A3B8;">19 tahun data</div>
    </div>
    <div style="padding:10px 0;">
        <div style="font-size:0.75rem; color:#94A3B8; font-weight:600;">🧪 Test</div>
        <div style="font-size:0.95rem; color:#0F172A; font-weight:600;">2020–2024</div>
        <div style="font-size:0.8rem; color:#94A3B8;">5 tahun validasi</div>
    </div>
    </div>
    """, unsafe_allow_html=True)

with col_table:
    st.markdown("""
    <div class="fade-in" style="font-weight:700; color:#0F172A; margin-bottom:8px;">
        📋 Tabel Proyeksi
    </div>
    """, unsafe_allow_html=True)
    
    df_pivot = df_forecast.pivot_table(
        index="year",
        columns="cluster_name",
        values="forecast_ha"
    ).reset_index()
    df_pivot.columns.name = None
    df_pivot = df_pivot.rename(columns={"year": "Tahun"})
    df_pivot["Tahun"] = df_pivot["Tahun"].astype(int)
    for col in df_pivot.columns[1:]:
        df_pivot[col] = df_pivot[col].round(2)
    
    st.dataframe(
        df_pivot,
        use_container_width=True,
        height=280,
        column_config={
            "Tahun": st.column_config.NumberColumn("Tahun", format="%d"),
            **{col: st.column_config.NumberColumn(
                col, 
                format="%.2f ha",
                help=f"Proyeksi deforestasi untuk kluster {col}"
               ) for col in df_pivot.columns[1:]}
        }
    )

st.markdown("---")

# ============================================================
# INTERPRETASI TABEL + EDUKASI - DENGAN ANIMASI
# ============================================================
with st.expander("📖 Interpretasi Hasil & Metodologi", expanded=False):
    st.markdown("""
    ### 📊 Ringkasan Hasil Forecasting
    
    | Kluster | Distribusi | Tren Historis | Proyeksi 2030 | Implikasi Kebijakan |
    |---|---|---|---|---|
    | 🟢 Zero | 369 kab (71.8%) | Konsisten nol | Tetap rendah | Pertahankan status quo |
    | 🟠 Moderate | 114 kab (22.2%) | Fluktuasi sedang | Perlu pemantauan | Pemantauan berkala |
    | 🔵 Declining | 21 kab (4.1%) | Tren menurun | Stabil rendah | Moratorium berhasil |
    | 🔴 High | 10 kab (1.9%) | Konsisten tinggi | Berpotensi naik | Prioritas intervensi |
    """)
    
    st.info(
        "**📘 Catatan Metodologi:** Model SARIMA dipilih secara otomatis menggunakan "
        "kriteria AIC terkecil (Auto-ARIMA). Training set: 2001–2019, "
        "Test set: 2020–2024. Confidence interval: ±10% dari nilai prediksi."
    )
    
    # EDUKASI tambahan - Glosarium
    st.markdown("""
    <div class="edu-box">
        <div class="title">📚 Glosarium Istilah</div>
        <div class="desc">
            <b>SARIMA</b> — Seasonal AutoRegressive Integrated Moving Average: 
            Model statistik untuk data deret waktu dengan pola musiman.<br><br>
            <b>Auto-ARIMA</b> — Proses otomatis mencari parameter terbaik untuk model SARIMA.<br><br>
            <b>AIC</b> (Akaike Information Criterion) — Kriteria untuk memilih model terbaik 
            (semakin kecil AIC = semakin baik model).<br><br>
            <b>Training Set</b> — Data yang digunakan untuk "belajar" pola (2001–2019).<br>
            <b>Test Set</b> — Data yang digunakan untuk menguji akurasi model (2020–2024).<br><br>
            <b>Confidence Interval (CI)</b> — Rentang nilai yang menunjukkan tingkat ketidakpastian prediksi.
        </div>
    </div>
    """, unsafe_allow_html=True)

# ============================================================
# FOOTER / KESIMPULAN AKHIR - DENGAN ANIMASI
# ============================================================
st.markdown("---")
st.markdown("""
<div class="fade-in" style="background: linear-gradient(135deg, #E1705510, #D6303110); 
            border-radius: 16px; padding: 24px 28px; 
            border: 1px solid #E1705520; margin-top: 16px;">
    <div style="font-weight:700; color:#0F172A; font-size:1.1rem; display:flex; align-items:center; gap:8px;">
        📌 Ringkasan Hasil Forecasting
    </div>
    <div style="color:#475569; font-size:0.95rem; margin-top:10px; line-height:1.9;">
        <b>Model SARIMA</b> berhasil memproyeksikan deforestasi per kluster hingga 2030 
        dengan akurasi terbaik pada <b>Kluster Declining</b> (MAE = 826 ha).
        <br><br>
        <b>🎯 Proyeksi 2025–2030:</b><br>
        <span style="display:inline-block; background:#FEF2F2; padding:4px 14px; border-radius:8px; margin:2px;">
            <span style="color:#EF4444; font-weight:700;">🔴 High</span> — 84.289 ha total
        </span>
        <span style="display:inline-block; background:#FFFBEB; padding:4px 14px; border-radius:8px; margin:2px;">
            <span style="color:#F59E0B; font-weight:700;">🟠 Moderate</span> — 66.752 ha total
        </span>
        <span style="display:inline-block; background:#EFF6FF; padding:4px 14px; border-radius:8px; margin:2px;">
            <span style="color:#3B82F6; font-weight:700;">🔵 Declining</span> — 42.967 ha total
        </span>
        <span style="display:inline-block; background:#ECFDF5; padding:4px 14px; border-radius:8px; margin:2px;">
            <span style="color:#22C55E; font-weight:700;">🟢 Zero</span> — 0 ha total ✅
        </span>
        <br><br>
        <span style="font-size:0.85rem; color:#94A3B8;">
            💡 Insight: Kluster High dan Moderate tetap menjadi penyumbang deforestasi utama 
            dan memerlukan intervensi kebijakan yang berkelanjutan.
        </span>
    </div>
</div>
""", unsafe_allow_html=True)