# pages/2_Clustering.py
import streamlit as st
import plotly.express as px
from streamlit_folium import st_folium
from utils.load_data import load_geojson, load_df_clustered, WARNA_KLUSTER, YEAR_COLS
from utils.map_utils import buat_peta_clustering
from utils.forecasting_utils import plot_trajektori

st.set_page_config(page_title="Clustering", page_icon="📊", layout="wide")

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
    
    /* ===== PAGE HEADER ===== */
    .page-header {
        text-align: center;
        padding: 16px 0 8px 0;
    }
    .page-header h1 {
        font-size: 2.2rem;
        font-weight: 800;
        background: linear-gradient(135deg, #6C5CE7 0%, #0984E3 100%);
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
    
    /* ===== CLUSTER CARD ===== */
    .cluster-card {
        background: #FFFFFF;
        border-radius: 14px;
        padding: 18px 16px;
        border: 1px solid #F1F5F9;
        text-align: center;
        transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
        cursor: default;
        position: relative;
        overflow: hidden;
    }
    .cluster-card::before {
        content: '';
        position: absolute;
        top: 0;
        left: 0;
        right: 0;
        height: 4px;
        background: linear-gradient(90deg, transparent, var(--card-color), transparent);
        opacity: 0;
        transition: opacity 0.3s ease;
    }
    .cluster-card:hover::before {
        opacity: 1;
    }
    .cluster-card:hover {
        border-color: var(--card-color, #2563EB);
        box-shadow: 0 8px 32px rgba(37,99,235,0.10);
        transform: translateY(-4px) scale(1.01);
    }
    .cluster-card .name {
        font-weight: 700;
        color: #0F172A;
        font-size: 1rem;
    }
    .cluster-card .count {
        font-size: 2rem;
        font-weight: 800;
        line-height: 1.2;
    }
    .cluster-card .pct {
        font-size: 0.8rem;
        color: #94A3B8;
        font-weight: 500;
    }
    .cluster-card .icon-big {
        font-size: 2.2rem;
        display: block;
        margin-bottom: 4px;
    }
    
    /* ===== INTERPRETATION CARD ===== */
    .interpretation-card {
        background: #FFFFFF;
        border-radius: 14px;
        padding: 18px 20px;
        border: 1px solid #E2E8F0;
        margin: 6px 0;
        transition: all 0.3s ease;
        height: 100%;
    }
    .interpretation-card:hover {
        border-color: var(--card-color, #2563EB);
        box-shadow: 0 4px 20px rgba(0,0,0,0.06);
        transform: translateY(-3px);
    }
    .interpretation-card .cluster-name {
        font-weight: 700;
        font-size: 1.1rem;
    }
    .interpretation-card .cluster-desc {
        color: #475569;
        font-size: 0.9rem;
        margin-top: 6px;
        line-height: 1.5;
    }
    .interpretation-card .cluster-tag {
        display: inline-block;
        padding: 3px 14px;
        border-radius: 20px;
        font-size: 0.7rem;
        font-weight: 700;
        margin-top: 8px;
        letter-spacing: 0.3px;
    }
    
    /* ===== INSIGHT BOX ===== */
    .insight-box {
        background: #F8FAFC;
        border-radius: 12px;
        padding: 16px 20px;
        border-left: 4px solid #2563EB;
        margin: 12px 0;
        transition: all 0.3s ease;
    }
    .insight-box:hover {
        background: #EFF6FF;
        border-left-color: #7C3AED;
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
        color: #2563EB;
        font-weight: 600;
    }
    
    /* ===== METRIC CARDS ===== */
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
    
    /* ===== LEGEND ===== */
    .legend-box {
        display: flex;
        align-items: center;
        gap: 10px;
        margin: 4px 0;
        padding: 4px 8px;
        border-radius: 8px;
        transition: background 0.2s ease;
    }
    .legend-box:hover {
        background: #F1F5F9;
    }
    .legend-color {
        width: 18px;
        height: 18px;
        border-radius: 6px;
        flex-shrink: 0;
        border: 1px solid rgba(0,0,0,0.06);
    }
    .legend-label {
        font-size: 0.85rem;
        color: #475569;
    }
    .legend-label b {
        color: #0F172A;
    }
    
    /* ===== TOOLTIP STYLING ===== */
    .stTooltipContent {
        border-radius: 12px !important;
        box-shadow: 0 8px 32px rgba(0,0,0,0.12) !important;
    }
    
    /* ===== SIDEBAR ===== */
    .sidebar-header {
        font-weight: 700;
        color: #0F172A;
        padding: 10px 0;
        border-bottom: 2px solid #6C5CE7;
        margin-bottom: 14px;
        font-size: 0.9rem;
        display: flex;
        align-items: center;
        gap: 8px;
    }
    
    /* ===== RESPONSIVE ===== */
    @media (max-width: 768px) {
        .page-header h1 {
            font-size: 1.5rem;
        }
        .cluster-card .count {
            font-size: 1.5rem;
        }
    }
</style>
""", unsafe_allow_html=True)

# ============================================================
# HEADER - DENGAN ANIMASI
# ============================================================
st.markdown("""
<div class="page-header fade-in">
    <h1>Trajectory-Based K-Means Clustering</h1>
    <p>Klasifikasi 514 kabupaten berdasarkan pola temporal deforestasi 2001–2024 (k=4)</p>
</div>
""", unsafe_allow_html=True)

# ============================================================
# EDUKASI: APA ITU CLUSTERING? (Expander dengan Animasi)
# ============================================================
with st.expander("🧠 Apa itu Clustering? (Klik untuk belajar)", expanded=False):
    st.markdown("""
    <div style="background: linear-gradient(135deg, #F0F4FF, #F5F0FF); border-radius: 14px; padding: 20px 24px; border: 1px solid #E0E7FF;">
        <div style="display: flex; gap: 16px; align-items: flex-start; flex-wrap: wrap;">
            <div style="flex: 2;">
                <div style="font-weight: 700; color: #0F172A; font-size: 1.1rem; margin-bottom: 6px;">
                    📊 Apa itu K-Means Clustering?
                </div>
                <div style="color: #475569; font-size: 0.95rem; line-height: 1.7;">
                    <b>Clustering</b> adalah teknik <b>machine learning unsupervised</b> yang mengelompokkan data 
                    berdasarkan kesamaan karakteristik. Dalam proyek ini, kita mengelompokkan 
                    <span style="color: #2563EB; font-weight: 600;">514 kabupaten</span> berdasarkan 
                    <span style="color: #2563EB; font-weight: 600;">pola deforestasi</span> dari waktu ke waktu.
                    <br><br>
                    <b>🔄 Cara Kerja K-Means:</b><br>
                    1. Tentukan jumlah kluster (k=4)<br>
                    2. Inisialisasi titik pusat (centroid) secara acak<br>
                    3. Kelompokkan setiap kabupaten ke centroid terdekat<br>
                    4. Perbarui centroid berdasarkan rata-rata kelompok<br>
                    5. Ulangi hingga stabil
                    <br><br>
                    <span style="background: #DBEAFE; padding: 2px 12px; border-radius: 12px; font-size: 0.85rem; color: #1E40AF;">
                        📌 Silhouette Score = 0.795 → Struktur kluster <b>BAIK</b>
                    </span>
                </div>
            </div>
            <div style="flex: 1; min-width: 120px; background: #FFFFFF; border-radius: 12px; padding: 16px; border: 1px solid #E2E8F0; text-align: center;">
                <div style="font-size: 2.5rem; margin-bottom: 4px;">🎯</div>
                <div style="font-weight: 700; color: #0F172A; font-size: 0.9rem;">4 Kluster</div>
                <div style="font-size: 0.75rem; color: #94A3B8;">Zero · Moderate<br>Declining · High</div>
                <div style="margin-top: 8px; background: #F1F5F9; border-radius: 8px; padding: 6px;">
                    <span style="font-size: 0.7rem; color: #475569;">Silhouette</span><br>
                    <span style="font-size: 1.1rem; font-weight: 700; color: #2563EB;">0.795</span>
                </div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

# ============================================================
# LOAD DATA
# ============================================================
with st.spinner("⏳ Loading clustering data..."):
    gdf = load_geojson()
    df = load_df_clustered()
    norm_cols = [f"norm_{y}" for y in YEAR_COLS]

# ============================================================
# SIDEBAR
# ============================================================
with st.sidebar:
    st.markdown("""
    <div class="sidebar-header">
        ⚙️ Filter Kluster
    </div>
    """, unsafe_allow_html=True)
    
    # Gunakan select all dengan checkbox style
    kluster_options = sorted(df["cluster_name"].unique().tolist())
    kluster_sel = st.multiselect(
        "Tampilkan Kluster",
        options=kluster_options,
        default=kluster_options,
        label_visibility="collapsed",
        placeholder="Pilih kluster yang ingin ditampilkan..."
    )
    
    st.markdown("---")
    st.markdown("""
    <div style="font-size:0.8rem; color:#64748B; line-height:1.8;">
        <b>💡 Tips Interaksi:</b><br>
        • Pilih kluster tertentu untuk fokus analisis<br>
        • Hover pada card untuk melihat efek animasi<br>
        • Scroll untuk menikmati efek fade-in<br>
        • Gunakan tab untuk view
    </div>
    """, unsafe_allow_html=True)
    
# ============================================================
# METRICS - DENGAN ANIMASI FADE-IN
# ============================================================
col_m1, col_m2, col_m3, col_m4 = st.columns(4)

metrics_data = [
    (f"{len(df)}", "🏙️ Total Kabupaten", "fade-in-delay-1"),
    (f"{(df['total_ha'] > 0).sum()}", "📍 Kabupaten Aktif", "fade-in-delay-2"),
    ("0.795", "📊 Silhouette Score", "fade-in-delay-3"),
    (df.loc[df['total_ha'].idxmax(), 'kabupaten'] if len(df) > 0 else "-", "🏆 Kabupaten Tertinggi", "fade-in-delay-4")
]

for col, (val, label, anim) in zip([col_m1, col_m2, col_m3, col_m4], metrics_data):
    with col:
        st.markdown(f"""
        <div class="metric-card {anim}">
            <div class="num">{val}</div>
            <div class="label">{label}</div>
        </div>
        """, unsafe_allow_html=True)

st.markdown("---")

# ============================================================
# CLUSTER SUMMARY CARDS - DENGAN ANIMASI
# ============================================================
st.markdown("""
<div class="fade-in" style="font-size:1rem; font-weight:700; color:#0F172A; margin-bottom:12px;">
    📊 Ringkasan Kluster
</div>
""", unsafe_allow_html=True)

cluster_summary = df.groupby("cluster_name").size().reset_index(name="count")
total_all = len(df)

# Emoji dan warna untuk setiap kluster
emoji_map = {"Zero": "🟢", "Moderate": "🟠", "Declining": "🔵", "High": "🔴"}

cols = st.columns(len(cluster_summary))
for idx, (col, row) in enumerate(zip(cols, cluster_summary.iterrows())):
    _, data = row
    name = data["cluster_name"]
    count = data["count"]
    pct = (count / total_all) * 100
    warna = WARNA_KLUSTER.get(name, "#636E72")
    emoji = emoji_map.get(name, "⬜")
    delay_class = f"fade-in-delay-{idx+1}"
    
    with col:
        st.markdown(f"""
        <div class="cluster-card {delay_class}" style="--card-color:{warna};">
            <span class="icon-big">{emoji}</span>
            <div class="name">{name}</div>
            <div class="count" style="color:{warna};">{count}</div>
            <div class="pct">{pct:.1f}% dari total</div>
        </div>
        """, unsafe_allow_html=True)

st.markdown("---")

# ============================================================
# INTERPRETASI KLUSTER - DENGAN ANIMASI
# ============================================================
st.markdown("""
<div class="fade-in" style="font-size:1rem; font-weight:700; color:#0F172A; margin-bottom:12px;">
    📖 Interpretasi Setiap Kluster
</div>
""", unsafe_allow_html=True)

# Data interpretasi kluster
cluster_interpretations = {
    "Zero": {
        "emoji": "🟢",
        "color": "#22C55E",
        "tag": "AMAN",
        "tag_color": "#ECFDF5",
        "tag_text": "#166534",
        "desc": "Kabupaten tanpa deforestasi signifikan (konsisten nol selama 2001–2024).",
        "detail": "✅ Menunjukkan keberhasilan kebijakan perlindungan hutan. Perlu dipertahankan status quo."
    },
    "Moderate": {
        "emoji": "🟠",
        "color": "#F59E0B",
        "tag": "AWAS",
        "tag_color": "#FFFBEB",
        "tag_text": "#92400E",
        "desc": "Deforestasi fluktuatif dengan intensitas sedang.",
        "detail": "⚠️ Membutuhkan pemantauan berkala. Berpotensi meningkat menjadi High jika tidak dikendalikan."
    },
    "Declining": {
        "emoji": "🔵",
        "color": "#3B82F6",
        "tag": "MEMBAIK",
        "tag_color": "#EFF6FF",
        "tag_text": "#1E40AF",
        "desc": "Tren deforestasi menurun signifikan.",
        "detail": "📉 Menunjukkan efektivitas kebijakan moratorium. Perkuat kebijakan yang ada."
    },
    "High": {
        "emoji": "🔴",
        "color": "#EF4444",
        "tag": "DARURAT",
        "tag_color": "#FEF2F2",
        "tag_text": "#991B1B",
        "desc": "Deforestasi konsisten tinggi sepanjang periode.",
        "detail": "🚨 Prioritas intervensi tertinggi. Memerlukan penegakan hukum dan kebijakan khusus."
    }
}

# Tampilkan interpretasi dalam grid
interp_cols = st.columns(4)
for idx, (col, (name, info)) in enumerate(zip(interp_cols, cluster_interpretations.items())):
    delay_class = f"fade-in-delay-{idx+1}"
    with col:
        st.markdown(f"""
        <div class="interpretation-card {delay_class}" style="--card-color:{info['color']}; border-left: 4px solid {info['color']};">
            <div class="cluster-name" style="color:{info['color']};">
                {info['emoji']} {name}
            </div>
            <div class="cluster-desc">{info['desc']}</div>
            <span class="cluster-tag" style="background:{info['tag_color']}; color:{info['tag_text']};">
                {info['tag']}
            </span>
            <div style="font-size:0.8rem; color:#64748B; margin-top:8px; line-height:1.5;">
                {info['detail']}
            </div>
        </div>
        """, unsafe_allow_html=True)

st.markdown("---")

# ============================================================
# TABS: Visual & Statistik
# ============================================================
tab1, tab2 = st.tabs(["📊 Visual Clustering", "📋 Statistik Kluster"])

with tab1:
    col_chart, col_traj = st.columns([1, 2])
    
    with col_chart:
        st.markdown("""
        <div class="fade-in" style="font-weight:700; color:#0F172A; margin-bottom:8px;">
            Distribusi Kluster
        </div>
        """, unsafe_allow_html=True)
        
        dist = df.groupby("cluster_name").size().reset_index(name="jumlah")
        color_map = {k: v for k, v in WARNA_KLUSTER.items() if k in dist['cluster_name'].values}
        
        fig_pie = px.pie(
            dist, values="jumlah", names="cluster_name",
            color="cluster_name", color_discrete_map=color_map,
            template="plotly_white"
        )
        fig_pie.update_traces(
            textposition="inside",
            textinfo="percent+label",
            hole=0.35,
            marker=dict(line=dict(color='white', width=2))
        )
        fig_pie.update_layout(
            showlegend=False,
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            height=350,
            margin=dict(l=20, r=20, t=20, b=20)
        )
        st.plotly_chart(fig_pie, use_container_width=True, key="pie_chart")
        
        # Keterangan pie chart
        st.markdown("""
        <div class="insight-box fade-in">
            <div class="title">💡 Apa ini?</div>
            <div class="desc">
                Diagram lingkaran menunjukkan persentase kabupaten di setiap kluster.
                <span class="highlight">71.8%</span> kabupaten masuk Kluster Zero 
                (tanpa deforestasi), sementara <span class="highlight">hanya 1.9%</span> 
                yang masuk Kluster High (deforestasi tinggi).
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    with col_traj:
        st.markdown("""
        <div class="fade-in" style="font-weight:700; color:#0F172A; margin-bottom:8px;">
            Rata-rata Trajektori per Kluster
        </div>
        """, unsafe_allow_html=True)
        
        fig_traj = plot_trajektori(df, norm_cols)
        fig_traj.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            height=350,
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=1.02,
                xanchor="right",
                x=1
            ),
            margin=dict(l=20, r=20, t=30, b=40)
        )
        st.plotly_chart(fig_traj, use_container_width=True, key="trajectory_chart")
        
        # Keterangan trajektori
        st.markdown("""
        <div class="insight-box fade-in">
            <div class="title">📈 Apa itu Trajektori?</div>
            <div class="desc">
                Grafik menunjukkan <span class="highlight">pola perubahan deforestasi</span> 
                rata-rata dari semua kabupaten dalam satu kluster dari 2001–2024.
                <br><br>
                • <b style="color:#EF4444;">🔴 High</b>: meningkat terus → prioritas intervensi<br>
                • <b style="color:#F59E0B;">🟠 Moderate</b>: fluktuatif → perlu pemantauan<br>
                • <b style="color:#3B82F6;">🔵 Declining</b>: menurun → kebijakan berhasil<br>
                • <b style="color:#22C55E;">🟢 Zero</b>: stabil nol → pertahankan
            </div>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Map
    st.markdown("""
    <div class="fade-in" style="font-size:1rem; font-weight:700; color:#0F172A; margin-bottom:12px;">
        🗺️ Peta Hasil Clustering
    </div>
    """, unsafe_allow_html=True)
    
    df_filter = df[df["cluster_name"].isin(kluster_sel)].copy()
    gdf_map = gdf.merge(
        df_filter[["kab_id_clean", "kabupaten", "provinsi", "cluster", "cluster_name", "total_ha"]],
        left_on="kabupaten_geocode", right_on="kab_id_clean", how="left"
    )
    gdf_map["cluster_name"] = gdf_map["cluster_name"].fillna("Zero")
    gdf_map["total_ha"] = gdf_map["total_ha"].fillna(0)
    
    m = buat_peta_clustering(gdf_map)
    st_folium(m, width=None, height=500, key="clustering_map")
    
    # Keterangan peta
    st.markdown("""
    <div class="insight-box fade-in">
        <div class="title">🗺️ Interpretasi Peta</div>
        <div class="desc">
            Peta menunjukkan sebaran spasial kluster di seluruh Indonesia.
            <br><br>
            <div class="legend-box">
                <div class="legend-color" style="background:#22C55E;"></div>
                <div class="legend-label"><b>Zero</b> — dominan di luar Sumatra & Kalimantan</div>
            </div>
            <div class="legend-box">
                <div class="legend-color" style="background:#F59E0B;"></div>
                <div class="legend-label"><b>Moderate</b> — tersebar di Sumatra & Kalimantan</div>
            </div>
            <div class="legend-box">
                <div class="legend-color" style="background:#3B82F6;"></div>
                <div class="legend-label"><b>Declining</b> — terkonsentrasi di beberapa area</div>
            </div>
            <div class="legend-box">
                <div class="legend-color" style="background:#EF4444;"></div>
                <div class="legend-label"><b>High</b> — titik panas deforestasi 🚨</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Distribusi per Pulau
    st.markdown("""
    <div class="fade-in" style="font-size:1rem; font-weight:700; color:#0F172A; margin-bottom:12px;">
        🏝️ Distribusi Kluster per Pulau
    </div>
    """, unsafe_allow_html=True)
    
    cross = df.groupby(["pulau", "cluster_name"]).size().reset_index(name="jumlah")
    color_map = {k: v for k, v in WARNA_KLUSTER.items() if k in cross['cluster_name'].unique()}
    
    fig_bar = px.bar(
        cross, x="pulau", y="jumlah", color="cluster_name",
        color_discrete_map=color_map,
        labels={"pulau": "Pulau", "jumlah": "Jumlah Kabupaten", "cluster_name": "Kluster"},
        template="plotly_white", barmode="stack"
    )
    fig_bar.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        height=350,
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        ),
        margin=dict(l=20, r=20, t=20, b=20)
    )
    fig_bar.update_traces(marker=dict(line=dict(width=0)))
    st.plotly_chart(fig_bar, use_container_width=True, key="island_chart")
    
    # Keterangan distribusi per pulau
    st.markdown("""
    <div class="insight-box fade-in">
        <div class="title">🏝️ Apa maknanya?</div>
        <div class="desc">
            Grafik batang menunjukkan <span class="highlight">sebaran kluster berdasarkan pulau</span>.
            <br><br>
            • <b>Sumatra</b>: dominasi Moderate & High — pusat perkebunan sawit<br>
            • <b>Kalimantan</b>: semua kluster terwakili — variasi aktivitas<br>
            • <b>Sulawesi & Timur</b>: dominasi Zero — minimal deforestasi<br>
            • <b>Jawa</b>: didominasi Zero — urbanisasi tinggi, minim hutan
        </div>
    </div>
    """, unsafe_allow_html=True)

with tab2:
    st.markdown("""
    <div class="fade-in" style="font-weight:700; color:#0F172A; margin-bottom:8px;">
        Statistik Deskriptif per Kluster
    </div>
    """, unsafe_allow_html=True)
    
    stats = df.groupby("cluster_name").agg({
        "total_ha": ["count", "mean", "std", "min", "max"]
    }).round(2)
    stats.columns = ["Jumlah", "Rata-rata", "Std Dev", "Min", "Max"]
    stats = stats.sort_values("Rata-rata", ascending=False)
    
    st.dataframe(
        stats,
        use_container_width=True,
        column_config={
            "Jumlah": st.column_config.NumberColumn("Jumlah", format="%d"),
            "Rata-rata": st.column_config.NumberColumn("Rata-rata (ha)", format="%.2f"),
            "Std Dev": st.column_config.NumberColumn("Std Dev", format="%.2f"),
            "Min": st.column_config.NumberColumn("Min (ha)", format="%.2f"),
            "Max": st.column_config.NumberColumn("Max (ha)", format="%.2f"),
        }
    )
    
    # Keterangan statistik
    st.markdown("""
    <div class="insight-box fade-in">
        <div class="title">📊 Cara Membaca Tabel</div>
        <div class="desc">
            Tabel menunjukkan <span class="highlight">statistik deskriptif</span> deforestasi per kluster.
            <br><br>
            • <b>Jumlah</b>: banyak kabupaten dalam kluster<br>
            • <b>Rata-rata</b>: rata-rata total deforestasi per kabupaten<br>
            • <b>Std Dev</b>: variasi antar kabupaten (semakin tinggi = semakin bervariasi)<br>
            • <b>Min/Max</b>: rentang nilai deforestasi terendah dan tertinggi
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    st.markdown("""
    <div class="fade-in" style="font-weight:700; color:#0F172A; margin-bottom:8px;">
        Detail Kabupaten per Kluster
    </div>
    """, unsafe_allow_html=True)
    
    kluster_tab = st.selectbox(
        "Pilih Kluster",
        sorted(df["cluster_name"].unique()),
        format_func=lambda x: f"🔵 {x}" if x != "Zero" else f"⚪ {x}",
        label_visibility="collapsed"
    )
    
    # Tampilkan deskripsi kluster yang dipilih
    if kluster_tab in cluster_interpretations:
        info = cluster_interpretations[kluster_tab]
        st.markdown(f"""
        <div style="background:#F8FAFC; border-radius:10px; padding:14px 18px; margin-bottom:14px; border-left:4px solid {info['color']};">
            <span style="font-weight:700; color:{info['color']};">{info['emoji']} {kluster_tab}</span>
            — {info['desc']}
            <span style="display:inline-block; padding:3px 12px; border-radius:20px; font-size:0.7rem; font-weight:700; background:{info['tag_color']}; color:{info['tag_text']}; margin-left:8px;">
                {info['tag']}
            </span>
        </div>
        """, unsafe_allow_html=True)
    
    df_tab = (df[df["cluster_name"] == kluster_tab]
              [["kabupaten", "provinsi", "cluster_name", "total_ha"]]
              .sort_values("total_ha", ascending=False)
              .reset_index(drop=True))
    df_tab.columns = ["Kabupaten", "Provinsi", "Kluster", "Total Deforestasi (ha)"]
    df_tab["Total Deforestasi (ha)"] = df_tab["Total Deforestasi (ha)"].round(2)
    
    st.dataframe(
        df_tab,
        use_container_width=True,
        height=400,
        column_config={
            "Kabupaten": st.column_config.TextColumn("Kabupaten", width="medium"),
            "Provinsi": st.column_config.TextColumn("Provinsi", width="medium"),
            "Kluster": st.column_config.TextColumn("Kluster", width="small"),
            "Total Deforestasi (ha)": st.column_config.NumberColumn(
                "Total Deforestasi (ha)",
                format="%.2f",
                width="small"
            )
        }
    )
    
    # Keterangan tabel detail
    st.markdown("""
    <div class="insight-box fade-in">
        <div class="title">📋 Cara Membaca Tabel Detail</div>
        <div class="desc">
            Tabel menunjukkan <span class="highlight">daftar kabupaten</span> dalam kluster yang dipilih,
            diurutkan dari deforestasi tertinggi ke terendah.
            <br><br>
            • Gunakan dropdown di atas untuk memilih kluster lain<br>
            • Kolom <b>Total Deforestasi (ha)</b> menunjukkan total selama 2001–2024<br>
            • Kabupaten dengan nilai tertinggi adalah <span class="highlight">prioritas intervensi</span> 🚨
        </div>
    </div>
    """, unsafe_allow_html=True)

# ============================================================
# FOOTER / KESIMPULAN AKHIR - DENGAN ANIMASI
# ============================================================
st.markdown("---")
st.markdown("""
<div class="fade-in" style="background: linear-gradient(135deg, #2563EB10, #7C3AED10); 
            border-radius: 16px; padding: 24px 28px; 
            border: 1px solid #2563EB20; margin-top: 16px;">
    <div style="font-weight:700; color:#0F172A; font-size:1.1rem; display:flex; align-items:center; gap:8px;">
        📌 Ringkasan Analisis Clustering
    </div>
    <div style="color:#475569; font-size:0.95rem; margin-top:10px; line-height:1.9;">
        <b>K-Means Clustering (k=4)</b> berhasil mengelompokkan 514 kabupaten 
        dengan <b>Silhouette Score = 0.795</b> (struktur kluster baik).
        <br><br>
        <b>🎯 Insight Utama:</b><br>
        <span style="display:inline-block; background:#ECFDF5; padding:4px 14px; border-radius:8px; margin:2px;">
            <span style="color:#22C55E; font-weight:700;">🟢 71.8%</span> Zero — <span style="color:#22C55E;">pertahankan</span>
        </span>
        <span style="display:inline-block; background:#FFFBEB; padding:4px 14px; border-radius:8px; margin:2px;">
            <span style="color:#F59E0B; font-weight:700;">🟠 22.2%</span> Moderate — <span style="color:#F59E0B;">monitor</span>
        </span>
        <span style="display:inline-block; background:#EFF6FF; padding:4px 14px; border-radius:8px; margin:2px;">
            <span style="color:#3B82F6; font-weight:700;">🔵 4.1%</span> Declining — <span style="color:#3B82F6;">perkuat</span>
        </span>
        <span style="display:inline-block; background:#FEF2F2; padding:4px 14px; border-radius:8px; margin:2px;">
            <span style="color:#EF4444; font-weight:700;">🔴 1.9%</span> High — <span style="color:#EF4444;">intervensi 🚨</span>
        </span>
    </div>
</div>
""", unsafe_allow_html=True)