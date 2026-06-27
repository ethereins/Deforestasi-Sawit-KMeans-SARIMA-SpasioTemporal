import pandas as pd
import geopandas as gpd
import streamlit as st

WARNA_KLUSTER = {
    "Zero"     : "#2ecc71",
    "Moderate" : "#f39c12",
    "Declining": "#3498db",
    "High"     : "#e74c3c"
}

PULAU_MAP = {
    "ACEH":"Sumatera","SUMATERA UTARA":"Sumatera","SUMATERA BARAT":"Sumatera",
    "RIAU":"Sumatera","KEPULAUAN RIAU":"Sumatera","JAMBI":"Sumatera",
    "SUMATERA SELATAN":"Sumatera","BENGKULU":"Sumatera","LAMPUNG":"Sumatera",
    "BANGKA BELITUNG":"Sumatera","KALIMANTAN BARAT":"Kalimantan",
    "KALIMANTAN TENGAH":"Kalimantan","KALIMANTAN SELATAN":"Kalimantan",
    "KALIMANTAN TIMUR":"Kalimantan","KALIMANTAN UTARA":"Kalimantan",
    "PAPUA":"Papua","PAPUA BARAT":"Papua","PAPUA SELATAN":"Papua",
    "PAPUA TENGAH":"Papua","PAPUA PEGUNUNGAN":"Papua","PAPUA BARAT DAYA":"Papua",
    "SULAWESI UTARA":"Sulawesi","SULAWESI TENGAH":"Sulawesi",
    "SULAWESI SELATAN":"Sulawesi","SULAWESI TENGGARA":"Sulawesi",
    "GORONTALO":"Sulawesi","SULAWESI BARAT":"Sulawesi",
    "MALUKU":"Maluku & Lainnya","MALUKU UTARA":"Maluku & Lainnya",
}

YEAR_COLS = list(range(2001, 2025))

@st.cache_data
def load_geojson():
    gdf = gpd.read_file("data/raw/deforestasi_kabupaten.geojson")
    gdf["kabupaten_geocode"] = gdf["kabupaten_geocode"].astype(str)
    return gdf

@st.cache_data
def load_df_long():
    df = pd.read_csv("data/processed/df_long.csv")
    df["kab_id_clean"] = df["kab_id"].str.replace("ID-", "")
    return df

@st.cache_data
def load_df_clustered():
    df = pd.read_csv("data/processed/df_clustered.csv")
    df["kab_id_clean"] = df["kab_id"].str.replace("ID-", "")
    df["pulau"] = df["provinsi"].map(PULAU_MAP).fillna("Jawa & Lainnya")
    return df

@st.cache_data
def load_forecast():
    return pd.read_csv("data/processed/forecast_2025_2030.csv")

@st.cache_data
def load_evaluasi():
    return pd.read_csv("data/processed/evaluasi_sarima.csv")
