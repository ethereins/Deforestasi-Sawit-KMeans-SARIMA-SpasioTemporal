import folium
import json
from utils.load_data import WARNA_KLUSTER


def buat_peta_choropleth(gdf_map, judul, colorscale="YlOrRd"):
    m = folium.Map(location=[-2.5, 118], zoom_start=5, tiles="CartoDB positron")

    folium.Choropleth(
        geo_data     = json.loads(gdf_map.to_json()),
        data         = gdf_map,
        columns      = ["kabupaten_geocode", "deforestasi_ha"],
        key_on       = "feature.properties.kabupaten_geocode",
        fill_color   = colorscale,
        fill_opacity = 0.78,
        line_opacity = 0.15,
        legend_name  = judul,
        nan_fill_color = "#e8e8e8",
        highlight    = True
    ).add_to(m)

    folium.GeoJson(
        json.loads(gdf_map.to_json()),
        style_function     = lambda x: {"fillOpacity": 0, "weight": 0.3, "color": "white"},
        highlight_function = lambda x: {"fillOpacity": 0.2, "weight": 2, "color": "#333"},
        tooltip = folium.GeoJsonTooltip(
            fields   = ["kabupaten_name", "province_name", "deforestasi_ha"],
            aliases  = ["📍 Kabupaten", "🏛️ Provinsi", "🌳 Deforestasi (ha)"],
            localize = True, sticky = True,
            style = ("background-color:white;color:#333;font-family:Arial;"
                     "font-size:13px;padding:8px;border-radius:6px;border:1px solid #ccc;")
        )
    ).add_to(m)

    title_html = f"""
    <div style="position:fixed;top:12px;left:50%;transform:translateX(-50%);
         z-index:9999;background:white;padding:8px 16px;border-radius:8px;
         border:1px solid #ddd;font-family:Arial;font-size:13px;
         box-shadow:2px 2px 6px rgba(0,0,0,0.1);">
    <b>🌳 {judul}</b>
    </div>
    """
    m.get_root().html.add_child(folium.Element(title_html))
    return m


def buat_peta_clustering(gdf_map):
    m = folium.Map(location=[-2.5, 118], zoom_start=5, tiles="CartoDB positron")

    def style_function(feature):
        nama = feature["properties"].get("cluster_name", "Zero")
        return {
            "fillColor"  : WARNA_KLUSTER.get(nama, "#cccccc"),
            "fillOpacity": 0.75,
            "color"      : "white",
            "weight"     : 0.5
        }

    folium.GeoJson(
        json.loads(gdf_map.to_json()),
        style_function     = style_function,
        highlight_function = lambda x: {"fillOpacity": 0.95, "weight": 2, "color": "#333"},
        tooltip = folium.GeoJsonTooltip(
            fields   = ["kabupaten_name", "province_name", "cluster_name", "total_ha"],
            aliases  = ["📍 Kabupaten", "🏛️ Provinsi", "📌 Kluster", "🌳 Total (ha)"],
            localize = True, sticky = True,
            style = ("background-color:white;color:#333;font-family:Arial;"
                     "font-size:13px;padding:8px;border-radius:6px;border:1px solid #ccc;")
        )
    ).add_to(m)

    legend_html = "".join([
        '<div style="position:fixed;bottom:30px;left:30px;z-index:9999;',
        'background:white;padding:12px;border-radius:8px;',
        'border:1px solid #ddd;font-family:Arial;font-size:13px;',
        'box-shadow:2px 2px 6px rgba(0,0,0,0.1);">',
        "<b>Kluster Deforestasi Sawit</b><br>"
    ] + [
        f'<i style="background:{v};width:12px;height:12px;'
        f'display:inline-block;margin-right:6px;border-radius:2px;"></i>{k}<br>'
        for k, v in WARNA_KLUSTER.items()
    ] + ["</div>"])
    m.get_root().html.add_child(folium.Element(legend_html))
    return m
