# pages/1_Peta_Deforestasi.py
import streamlit as st
import pandas as pd
import plotly.express as px
from streamlit_folium import st_folium
from utils.load_data import load_geojson, load_df_long, YEAR_COLS
from utils.map_utils import buat_peta_choropleth
import time

st.set_page_config(page_title="Peta Deforestasi", page_icon="🗺️", layout="wide")

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
    
    .fade-scale {
        animation: fadeInScale 0.8s ease forwards;
    }
    
    .slide-left {
        animation: slideInLeft 0.7s ease forwards;
    }
    
    .slide-right {
        animation: slideInRight 0.7s ease forwards;
    }
    
    /* ===== PAGE HEADER ===== */
    .page-header {
        text-align: center;
        padding: 16px 0 8px 0;
    }
    .page-header h1 {
        font-size: 2.2rem;
        font-weight: 800;
        background: linear-gradient(135deg, #0F172A 0%, #2563EB 50%, #00B894 100%);
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
    
    /* ===== MAP CARD ===== */
    .map-card {
        background: #FFFFFF;
        border-radius: 16px;
        padding: 16px 16px 8px 16px;
        border: 1px solid #F1F5F9;
        box-shadow: 0 1px 3px rgba(0,0,0,0.04);
        transition: all 0.3s ease;
    }
    .map-card:hover {
        border-color: #2563EB40;
        box-shadow: 0 8px 32px rgba(37,99,235,0.08);
    }
    .map-card .map-title {
        font-weight: 700;
        color: #0F172A;
        font-size: 0.95rem;
        margin-bottom: 8px;
        display: flex;
        align-items: center;
        gap: 8px;
    }
    .map-card .map-title .badge {
        font-size: 0.65rem;
        font-weight: 600;
        background: #DBEAFE;
        color: #1E40AF;
        padding: 2px 12px;
        border-radius: 12px;
    }
    
    /* ===== INSIGHT PANEL ===== */
    .insight-panel {
        background: #F8FAFC;
        border-radius: 14px;
        padding: 18px 20px;
        border: 1px solid #F1F5F9;
        transition: all 0.3s ease;
        height: 100%;
    }
    .insight-panel:hover {
        background: #EFF6FF;
        border-color: #2563EB40;
    }
    .insight-panel .label {
        font-size: 0.7rem;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        color: #94A3B8;
    }
    .insight-panel .value {
        font-size: 1.5rem;
        font-weight: 800;
        color: #0F172A;
    }
    .insight-panel .sub {
        font-size: 0.85rem;
        color: #64748B;
    }
    .insight-panel .highlight-box {
        background: #FFFFFF;
        border-radius: 8px;
        padding: 8px 12px;
        margin-top: 8px;
        border: 1px solid #E2E8F0;
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
        border-color: #2563EB40;
        box-shadow: 0 4px 20px rgba(37,99,235,0.08);
        transform: translateY(-2px);
    }
    .metric-card .num {
        font-size: 1.5rem;
        font-weight: 800;
        color: #0F172A;
    }
    .metric-card .label {
        font-size: 0.7rem;
        color: #94A3B8;
        font-weight: 500;
        margin-top: 2px;
    }
    
    /* ===== EDU BOX ===== */
    .edu-box {
        background: #EFF6FF;
        border-radius: 14px;
        padding: 18px 22px;
        border-left: 4px solid #2563EB;
        margin: 12px 0;
        transition: all 0.3s ease;
    }
    .edu-box:hover {
        background: #DBEAFE;
        box-shadow: 0 4px 16px rgba(37,99,235,0.08);
    }
    .edu-box .title {
        font-weight: 700;
        color: #1E40AF;
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
        color: #2563EB;
        font-weight: 600;
    }
    .edu-box .term {
        display: inline-block;
        background: #DBEAFE;
        padding: 3px 14px;
        border-radius: 20px;
        font-size: 0.8rem;
        font-weight: 600;
        color: #1E40AF;
    }
    
    /* ===== SIDEBAR ===== */
    .sidebar-header {
        font-weight: 700;
        color: #0F172A;
        padding: 10px 0;
        border-bottom: 2px solid #2563EB;
        margin-bottom: 14px;
        font-size: 0.9rem;
        display: flex;
        align-items: center;
        gap: 8px;
    }
    
    /* ===== COLOR SCALE PREVIEW ===== */
    .color-preview {
        display: flex;
        border-radius: 8px;
        overflow: hidden;
        margin: 6px 0;
        height: 24px;
    }
    .color-preview .c {
        flex: 1;
        height: 100%;
    }
    .color-preview-label {
        display: flex;
        justify-content: space-between;
        font-size: 0.6rem;
        color: #94A3B8;
        margin-top: 2px;
    }
    
    /* ===== RESPONSIVE ===== */
    @media (max-width: 768px) {
        .page-header h1 {
            font-size: 1.5rem;
        }
        .metric-card .num {
            font-size: 1.2rem;
        }
        .insight-panel .value {
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
    <h1>Peta Deforestasi</h1>
    <p>Visualisasi choropleth interaktif per kabupaten/kota di Indonesia</p>
</div>
""", unsafe_allow_html=True)

# ============================================================
# EDUKASI: APA ITU DEFORESTASI?
# ============================================================
with st.expander("🌳 Apa itu Deforestasi? (Klik untuk belajar)", expanded=False):
    st.markdown("""
    <div style="background: linear-gradient(135deg, #EFF6FF, #F0FDF4); border-radius: 14px; padding: 20px 24px; border: 1px solid #DBEAFE;">
        <div style="display: flex; gap: 16px; align-items: flex-start; flex-wrap: wrap;">
            <div style="flex: 2;">
                <div style="font-weight: 700; color: #0F172A; font-size: 1.1rem; margin-bottom: 6px;">
                    🌲 Deforestasi = Penghilangan Hutan Secara Permanen
                </div>
                <div style="color: #475569; font-size: 0.95rem; line-height: 1.8;">
                    <b>Deforestasi</b> adalah hilangnya tutupan hutan secara permanen yang disebabkan oleh aktivitas manusia, 
                    seperti pembukaan lahan untuk <span style="color: #2563EB; font-weight: 600;">perkebunan kelapa sawit</span>, pertanian, atau pertambangan.
                    <br><br>
                    Dalam konteks peta ini, yang diukur adalah <span style="color: #2563EB; font-weight: 600;">deforestasi akibat ekspansi sawit industrial</span> 
                    — yaitu pembukaan hutan untuk perkebunan kelapa sawit skala besar.
                    <br><br>
                    <span style="background: #DBEAFE; padding: 3px 14px; border-radius: 20px; font-size: 0.85rem; color: #1E40AF; font-weight: 600;">
                        📌 Satuan: Hektar (ha) — 1 ha ≈ luas lapangan sepak bola
                    </span>
                </div>
            </div>
            <div style="flex: 1; min-width: 100px; background: #FFFFFF; border-radius: 12px; padding: 16px; border: 1px solid #E2E8F0; text-align: center;">
                <div style="font-size: 2.5rem; margin-bottom: 4px;">🌿</div>
                <div style="font-weight: 700; color: #0F172A; font-size: 0.9rem;">Hutan Tropis</div>
                <div style="font-size: 0.75rem; color: #94A3B8;">Indonesia</div>
                <div style="margin-top: 8px; background: #F1F5F9; border-radius: 8px; padding: 6px;">
                    <span style="font-size: 0.7rem; color: #475569;">Periode Data</span><br>
                    <span style="font-size: 1rem; font-weight: 700; color: #2563EB;">2001 → 2024</span>
                </div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

# ============================================================
# LOAD DATA
# ============================================================
with st.spinner("⏳ Loading peta..."):
    gdf = load_geojson()
    df_long = load_df_long()

# ============================================================
# SIDEBAR - MODERN DENGAN EDUKASI COLORSCALE
# ============================================================
with st.sidebar:
    st.markdown("""
    <div class="sidebar-header">
        ⚙️ Filter Peta
    </div>
    """, unsafe_allow_html=True)
    
    mode = st.radio(
        "Mode Tampilan",
        ["📅 Tahun Tunggal", "📊 Rata-rata Rentang", "📊 Total Rentang"],
        label_visibility="collapsed"
    )
    
    mode_map = {
        "📅 Tahun Tunggal": "Tahun Tunggal",
        "📊 Rata-rata Rentang": "Rata-rata Rentang",
        "📊 Total Rentang": "Total Rentang"
    }
    mode_clean = mode_map[mode]
    
    if mode_clean == "Tahun Tunggal":
        tahun_tunggal = st.slider(
            "Tahun", 2001, 2024, 2015,
            format="%d",
            label_visibility="collapsed"
        )
    else:
        col_a, col_b = st.columns(2)
        tahun_awal = col_a.selectbox("Dari", YEAR_COLS, index=0, label_visibility="collapsed")
        tahun_akhir = col_b.selectbox("Hingga", YEAR_COLS, index=len(YEAR_COLS)-1, label_visibility="collapsed")
    
    colorscale = st.selectbox(
        "🎨 Skema Warna",
        ["YlOrRd", "RdPu", "OrRd", "YlGn", "Blues"],
        index=0,
        label_visibility="collapsed"
    )
    
    # EDUKASI: Apa itu Skema Warna?
    with st.expander("🎨 Apa itu Skema Warna?", expanded=False):
        st.markdown("""
        <div style="font-size:0.85rem; color:#475569; line-height:1.7;">
            <b>Skema warna</b> menentukan bagaimana nilai deforestasi 
            direpresentasikan di peta.
            <br><br>
            <b>📌 Semakin gelap = semakin tinggi deforestasi</b>
            <br><br>
            <div style="background:#F8FAFC; border-radius:8px; padding:10px;">
                <div style="font-weight:600; font-size:0.75rem; color:#0F172A;">YlOrRd (Rekomendasi)</div>
                <div class="color-preview">
                    <div class="c" style="background:#FFFFB2;"></div>
                    <div class="c" style="background:#FECC5C;"></div>
                    <div class="c" style="background:#FD8D3C;"></div>
                    <div class="c" style="background:#F03B20;"></div>
                    <div class="c" style="background:#BD0026;"></div>
                </div>
                <div class="color-preview-label">
                    <span>Rendah</span>
                    <span>Sedang</span>
                    <span>Tinggi</span>
                </div>
                <div style="font-size:0.7rem; color:#94A3B8; margin-top:4px;">
                    ✅ Paling intuitif: kuning → merah = bahaya
                </div>
            </div>
            <br>
            <div style="background:#F8FAFC; border-radius:8px; padding:10px;">
                <div style="font-weight:600; font-size:0.75rem; color:#0F172A;">YlGn (Hindari)</div>
                <div class="color-preview">
                    <div class="c" style="background:#FFFFCC;"></div>
                    <div class="c" style="background:#C2E699;"></div>
                    <div class="c" style="background:#78C679;"></div>
                    <div class="c" style="background:#31A354;"></div>
                    <div class="c" style="background:#006837;"></div>
                </div>
                <div style="font-size:0.7rem; color:#94A3B8; margin-top:4px;">
                    ⚠️ Hijau = hutan, bisa membingungkan
                </div>
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    st.markdown("""
    <div style="font-size:0.8rem; color:#64748B; line-height:1.8;">
        <b>💡 Tips:</b><br>
        • Pilih <b>Tahun Tunggal</b> untuk melihat deforestasi di tahun tertentu<br>
        • Pilih <b>Rata-rata Rentang</b> untuk melihat tren rata-rata<br>
        • Pilih <b>Total Rentang</b> untuk melihat akumulasi deforestasi
    </div>
    """, unsafe_allow_html=True)

# ============================================================
# PROSES DATA
# ============================================================
if mode_clean == "Tahun Tunggal":
    df_agg = (df_long[df_long["year"] == tahun_tunggal]
              .groupby("kab_id_clean")["deforestasi_ha"].sum().reset_index())
    judul = f"Deforestasi Sawit Industrial (ha) — {tahun_tunggal}"
elif mode_clean == "Rata-rata Rentang":
    df_agg = (df_long[df_long["year"].between(tahun_awal, tahun_akhir)]
              .groupby("kab_id_clean")["deforestasi_ha"].mean().reset_index())
    judul = f"Rata-rata Deforestasi (ha) — {tahun_awal}–{tahun_akhir}"
else:
    df_agg = (df_long[df_long["year"].between(tahun_awal, tahun_akhir)]
              .groupby("kab_id_clean")["deforestasi_ha"].sum().reset_index())
    judul = f"Total Deforestasi (ha) — {tahun_awal}–{tahun_akhir}"

gdf_map = gdf.merge(df_agg, left_on="kabupaten_geocode", right_on="kab_id_clean", how="left")
gdf_map["deforestasi_ha"] = gdf_map["deforestasi_ha"].fillna(0)

# ============================================================
# METRICS - DENGAN ANIMASI
# ============================================================
total = gdf_map["deforestasi_ha"].sum()
maks = gdf_map["deforestasi_ha"].max()
aktif = (gdf_map["deforestasi_ha"] > 0).sum()
idx_maks = gdf_map["deforestasi_ha"].idxmax()
kab_maks = gdf_map.loc[idx_maks, "kabupaten_name"] if idx_maks < len(gdf_map) else "-"

col_metrics = st.columns(4)
metrics_data = [
    (f"{total:,.0f}", "🌲 Total Deforestasi (ha)", "fade-in-delay-1"),
    (f"{maks:,.0f}", "📈 Nilai Tertinggi (ha)", "fade-in-delay-2"),
    (kab_maks, "🏆 Kabupaten Tertinggi", "fade-in-delay-3"),
    (f"{aktif}", "📍 Kabupaten Aktif", "fade-in-delay-4")
]

for col, (val, label, anim) in zip(col_metrics, metrics_data):
    with col:
        st.markdown(f"""
        <div class="metric-card {anim}">
            <div class="num">{val}</div>
            <div class="label">{label}</div>
        </div>
        """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ============================================================
# MAP + INSIGHT - DENGAN ANIMASI
# ============================================================
col_map, col_insight = st.columns([3, 1])

with col_map:
    st.markdown(f"""
    <div class="map-card fade-in">
        <div class="map-title">
            {judul}
            <span class="badge">🗺️ Interaktif</span>
        </div>
    """, unsafe_allow_html=True)
    
    m = buat_peta_choropleth(gdf_map, judul, colorscale)
    st_folium(m, width=None, height=520, key="deforestasi_map")
    
    st.markdown("</div>", unsafe_allow_html=True)

with col_insight:
    st.markdown(f"""
    <div class="insight-panel fade-in">
        <div class="label">📌 Insight</div>
        <div style="margin-top: 12px;">
            <div class="value">{total:,.0f}</div>
            <div class="sub">Total deforestasi</div>
        </div>
        <div style="margin-top: 12px; padding-top: 12px; border-top: 1px solid #E2E8F0;">
            <div class="value">{maks:,.0f}</div>
            <div class="sub">Nilai tertinggi di {kab_maks}</div>
        </div>
        <div style="margin-top: 12px; padding-top: 12px; border-top: 1px solid #E2E8F0;">
            <div class="value">{aktif}</div>
            <div class="sub">Kabupaten aktif</div>
        </div>
        <div class="highlight-box" style="margin-top:12px; background:#EFF6FF; border-color:#2563EB40;">
            <div style="font-size:0.7rem; color:#94A3B8;">🎨 Skema Warna</div>
            <div style="font-size:0.8rem; color:#0F172A; font-weight:600;">{colorscale}</div>
            <div style="font-size:0.7rem; color:#64748B;">{mode_clean}</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")

# ============================================================
# EDUKASI: APA ITU PETA CHOROPLETH?
# ============================================================
with st.expander("🗺️ Apa itu Peta Choropleth? (Klik untuk belajar)", expanded=False):
    st.markdown("""
    <div class="edu-box">
        <div class="title">🗺️ Peta Choropleth = Peta dengan Warna Berdasarkan Nilai</div>
        <div class="desc">
            <b>Choropleth</b> adalah jenis peta tematik di mana area (dalam hal ini kabupaten) 
            diwarnai berdasarkan nilai data yang diwakilinya.
            <br><br>
            <b>Di peta ini:</b><br>
            • <span style="color:#FFFFB2;">■ Kuning terang</span> = deforestasi rendah<br>
            • <span style="color:#F03B20;">■ Merah</span> = deforestasi sedang<br>
            • <span style="color:#BD0026;">■ Merah tua</span> = deforestasi tinggi<br>
            • <span style="color:#FFFFFF;">■ Putih</span> = tidak ada data / nol deforestasi
            <br><br>
            <span class="term">📌 Semakin gelap warnanya, semakin tinggi deforestasi!</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

# ============================================================
# TREN CHART + EDUKASI
# ============================================================
st.markdown("""
<div class="fade-in" style="font-size: 1.1rem; font-weight: 700; color: #0F172A; margin-bottom: 4px;">
    📈 Tren Deforestasi Nasional
</div>
<div style="font-size: 0.85rem; color: #94A3B8; margin-bottom: 16px;">2001–2024</div>
""", unsafe_allow_html=True)

tren = df_long.groupby("year")["deforestasi_ha"].sum().reset_index()
fig = px.line(
    tren, x="year", y="deforestasi_ha",
    markers=True, template="plotly_white",
    labels={"year": "Tahun", "deforestasi_ha": "Total Deforestasi (ha)"}
)
fig.update_traces(
    line=dict(color='#2563EB', width=3),
    marker=dict(size=8, color='#2563EB', line=dict(width=2, color='white'))
)
fig.add_vline(
    x=2011, line_dash="dash", line_color="#EF4444",
    annotation_text="Moratorium 2011", annotation_position="top"
)
fig.update_layout(
    plot_bgcolor='rgba(0,0,0,0)',
    paper_bgcolor='rgba(0,0,0,0)',
    hovermode='x unified',
    height=350,
    margin=dict(l=40, r=40, t=40, b=40)
)
st.plotly_chart(fig, use_container_width=True, key="trend_chart")

# EDUKASI: Apa itu Moratorium?
st.markdown("""
<div class="edu-box fade-in">
    <div class="title">📜 Apa itu Moratorium 2011?</div>
    <div class="desc">
        <b>Moratorium</b> adalah kebijakan penghentian sementara (moratorium) izin baru untuk 
        pembukaan hutan alam dan lahan gambut yang dikeluarkan oleh Pemerintah Indonesia pada tahun 2011.
        <br><br>
        <span class="highlight">Tujuannya:</span> Mengurangi laju deforestasi dan emisi gas rumah kaca 
        dengan menghentikan sementara pemberian izin baru untuk perkebunan sawit di hutan primer dan lahan gambut.
        <br><br>
        <span class="term">✅ Efeknya:</span> Terlihat pada grafik di atas — setelah tahun 2011, 
        tren deforestasi cenderung menurun, meskipun masih terjadi fluktuasi.
    </div>
</div>
""", unsafe_allow_html=True)

st.markdown("---")

# ============================================================
# TOP 10 PER DEKADE + EDUKASI
# ============================================================
st.markdown("""
<div class="fade-in" style="font-size: 1.1rem; font-weight: 700; color: #0F172A; margin-bottom: 4px;">
    🏆 Top 10 Kabupaten per Dekade
</div>
<div style="font-size: 0.85rem; color: #94A3B8; margin-bottom: 16px;">
    Kabupaten dengan deforestasi tertinggi di setiap periode
</div>
""", unsafe_allow_html=True)

import plotly.graph_objects as go
from plotly.subplots import make_subplots

dekade = {
    "2001–2008": list(range(2001, 2009)),
    "2009–2016": list(range(2009, 2017)),
    "2017–2024": list(range(2017, 2025))
}

fig2 = make_subplots(rows=1, cols=3, subplot_titles=list(dekade.keys()))
colors = ['#2563EB', '#7C3AED', '#EF4444']

for i, (label, years) in enumerate(dekade.items(), start=1):
    top10 = (
        df_long[df_long["year"].isin(years)]
        .groupby("kabupaten")["deforestasi_ha"].sum()
        .sort_values(ascending=False).head(10).reset_index()
    )
    fig2.add_trace(
        go.Bar(
            x=top10["deforestasi_ha"],
            y=top10["kabupaten"],
            orientation="h",
            showlegend=False,
            marker_color=colors[i-1],
            marker=dict(cornerradius=4)
        ),
        row=1, col=i
    )
fig2.update_layout(
    height=400,
    template="plotly_white",
    plot_bgcolor='rgba(0,0,0,0)',
    paper_bgcolor='rgba(0,0,0,0)',
    margin=dict(l=20, r=20, t=40, b=20)
)
fig2.update_yaxes(autorange="reversed")
st.plotly_chart(fig2, use_container_width=True, key="top10_chart")

# EDUKASI: Interpretasi Top 10
st.markdown("""
<div class="edu-box fade-in">
    <div class="title">🏆 Cara Membaca Grafik Top 10</div>
    <div class="desc">
        Grafik ini menunjukkan <span class="highlight">10 kabupaten dengan deforestasi tertinggi</span> 
        di setiap periode (2001–2008, 2009–2016, 2017–2024).
        <br><br>
        <b>Yang perlu diperhatikan:</b><br>
        • Semakin panjang batang = semakin besar deforestasi<br>
        • Perhatikan perubahan nama kabupaten antar periode — apakah sama atau berganti?<br>
        • Kabupaten yang muncul terus-menerus adalah <span class="highlight">prioritas intervensi</span>
        <br><br>
        <span class="term">💡 Contoh:</span> Jika suatu kabupaten muncul di ketiga periode, 
        berarti deforestasi terjadi secara konsisten dan memerlukan tindakan segera.
    </div>
</div>
""", unsafe_allow_html=True)

# ============================================================
# FOOTER / RINGKASAN - DENGAN ANIMASI
# ============================================================
st.markdown("---")
st.markdown("""
<div class="fade-in" style="background: linear-gradient(135deg, #2563EB10, #00B89410); 
            border-radius: 16px; padding: 24px 28px; 
            border: 1px solid #2563EB20; margin-top: 16px;">
    <div style="font-weight:700; color:#0F172A; font-size:1.1rem; display:flex; align-items:center; gap:8px;">
        📌 Ringkasan Peta Deforestasi
    </div>
    <div style="color:#475569; font-size:0.95rem; margin-top:10px; line-height:1.9;">
        Peta ini menampilkan <b>sebaran spasial deforestasi sawit industrial</b> di Indonesia 
        dari tahun 2001 hingga 2024.
        <br><br>
        <b>🎯 Insight Utama:</b><br>
        • Total deforestasi: <span style="font-weight:700; color:#EF4444;">{total:,.0f} ha</span><br>
        • Kabupaten tertinggi: <span style="font-weight:700; color:#2563EB;">{kab_maks}</span> dengan {maks:,.0f} ha<br>
        • <span style="font-weight:700; color:#22C55E;">{aktif}</span> kabupaten aktif dari 514 total
        <br><br>
        <span style="font-size:0.85rem; color:#94A3B8;">
            💡 Gunakan filter di sidebar untuk mengeksplorasi data lebih lanjut.
        </span>
    </div>
</div>
""".format(total=total, kab_maks=kab_maks, maks=maks, aktif=aktif), unsafe_allow_html=True)