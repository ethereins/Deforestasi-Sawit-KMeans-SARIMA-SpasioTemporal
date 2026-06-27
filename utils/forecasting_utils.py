# utils/forecasting_utils.py
import plotly.graph_objects as go
from utils.load_data import WARNA_KLUSTER, YEAR_COLS


# ============================================================
# FUNGSI BANTU: Konversi hex ke rgba
# ============================================================
def hex_to_rgba(hex_color, alpha=0.13):
    """
    Konversi warna hex ke format rgba yang valid untuk Plotly
    
    Parameters:
    -----------
    hex_color : str
        Warna dalam format hex (e.g. '#e74c3c', '#ccc')
    alpha : float
        Nilai opacity antara 0-1
    
    Returns:
    --------
    str : Warna dalam format rgba (e.g. 'rgba(231, 76, 60, 0.13)')
    """
    hex_color = hex_color.lstrip('#')
    
    # Handle 3-digit hex (e.g. #ccc → #cccccc)
    if len(hex_color) == 3:
        hex_color = ''.join([c*2 for c in hex_color])
    
    # Handle 8-digit hex (e.g. #e74c3c22) - buang bagian alpha
    if len(hex_color) == 8:
        hex_color = hex_color[:6]
    
    r = int(hex_color[0:2], 16)
    g = int(hex_color[2:4], 16)
    b = int(hex_color[4:6], 16)
    
    return f'rgba({r}, {g}, {b}, {alpha})'


# ============================================================
# PLOT TRAJEKTORI
# ============================================================
def plot_trajektori(df_clustered, norm_cols):
    fig = go.Figure()
    
    for c in sorted(df_clustered["cluster"].unique()):
        nama = df_clustered[df_clustered["cluster"] == c]["cluster_name"].iloc[0]
        subset = df_clustered[df_clustered["cluster"] == c][norm_cols].values
        mean_t = subset.mean(axis=0)
        
        color = WARNA_KLUSTER.get(nama, "#636E72")
        
        fig.add_trace(go.Scatter(
            x=YEAR_COLS,
            y=mean_t,
            mode="lines+markers",
            name=f"{nama} (n={len(subset)})",
            line=dict(color=color, width=2.5),
            marker=dict(size=6, color=color)
        ))
    
    fig.add_vline(
        x=2011,
        line_dash="dash",
        line_color="gray",
        annotation_text="Moratorium 2011"
    )
    
    fig.update_layout(
        xaxis_title="Tahun",
        yaxis_title="Deforestasi (normalized 0–1)",
        template="plotly_white",
        height=350,
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)'
    )
    
    return fig


# ============================================================
# PLOT FORECAST
# ============================================================
def plot_forecast(cluster_hist, df_forecast, kluster_sel, show_ci=True):
    """
    Membuat plot forecasting per kluster
    
    Parameters:
    -----------
    cluster_hist : dict
        Dictionary berisi data historis per kluster
    df_forecast : pd.DataFrame
        DataFrame berisi hasil forecast
    kluster_sel : list
        Daftar kluster yang akan ditampilkan
    show_ci : bool
        Tampilkan confidence interval atau tidak
    """
    future_years = list(range(2025, 2031))
    fig = go.Figure()

    for c, data in cluster_hist.items():
        nama = data["nama"]
        
        if nama not in kluster_sel:
            continue
        
        # 🔥 Ambil warna
        color = WARNA_KLUSTER.get(nama, "#636E72")
        
        # Data historis
        hist_vals = data["series"].values
        
        # Data forecast
        df_f = df_forecast[df_forecast["cluster_name"] == nama]
        
        if len(df_f) > 0:
            future_vals = df_f["forecast_ha"].values
        else:
            future_vals = []

        # ===== TRACE HISTORIS =====
        fig.add_trace(go.Scatter(
            x=YEAR_COLS,
            y=hist_vals,
            mode="lines+markers",
            name=f"{nama} (Historis)",
            line=dict(color=color, width=2.5),
            marker=dict(size=6, color=color)
        ))

        # ===== TRACE FORECAST =====
        if len(future_vals) > 0:
            fig.add_trace(go.Scatter(
                x=future_years,
                y=future_vals,
                mode="lines+markers",
                name=f"{nama} (Forecast)",
                line=dict(color=color, dash="dash", width=2.5),
                marker=dict(size=8, color=color, symbol="diamond")
            ))

            # ===== CONFIDENCE INTERVAL =====
            if show_ci:
                ci_upper = future_vals * 1.1
                ci_lower = future_vals * 0.9
                
                # 🔥 FIX: Gunakan hex_to_rgba, BUKAN color + "22"
                fill_color = hex_to_rgba(color, 0.13)
                
                fig.add_trace(go.Scatter(
                    x=list(future_years) + list(future_years[::-1]),
                    y=list(ci_upper) + list(ci_lower[::-1]),
                    fill="toself",
                    fillcolor=fill_color,  # ✅ Valid: 'rgba(231, 76, 60, 0.13)'
                    line=dict(color="rgba(0,0,0,0)"),
                    showlegend=False,
                    hoverinfo="skip"
                ))

    # ===== GARIS VERTIKAL =====
    fig.add_vline(
        x=2024,
        line_dash="dot",
        line_color="gray",
        annotation_text="← Historis | Proyeksi →",
        annotation_position="top"
    )
    
    fig.add_vline(
        x=2011,
        line_dash="dash",
        line_color="lightgray",
        annotation_text="Moratorium 2011",
        annotation_position="bottom"
    )

    # ===== LAYOUT =====
    fig.update_layout(
        xaxis_title="Tahun",
        yaxis_title="Total Deforestasi (ha)",
        template="plotly_white",
        height=500,
        hovermode="x unified",
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1
        ),
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)'
    )
    
    return fig