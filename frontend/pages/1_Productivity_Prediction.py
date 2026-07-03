from pathlib import Path

import pandas as pd
import streamlit as st
import folium

from streamlit_folium import st_folium

from services.api import api
from config import DATA_DIR, STYLE_PATH


# ==========================================================
# PAGE CONFIG
# ==========================================================

st.set_page_config(
    page_title="Crop Productivity Prediction",
    page_icon="🌾",
    layout="wide"
)

# ==========================================================
# BASE DIRECTORY
# ==========================================================

BASE_DIR = Path(__file__).resolve().parents[2]

DATA_DIR = BASE_DIR / "data" / "primary"

STYLE_PATH = BASE_DIR / "frontend" / "style.css"

# ==========================================================
# LOAD CSS
# ==========================================================

with open(STYLE_PATH, encoding="utf-8") as f:

    st.markdown(

        f"<style>{f.read()}</style>",

        unsafe_allow_html=True

    )


# ==========================================================
# LOAD LOCATION DATA
# ==========================================================

@st.cache_data(show_spinner=False)
def load_location():

    return pd.read_csv(

        DATA_DIR

        / "lat_long_kab_kota_clean.csv"

    )

location_df = load_location()


# ==========================================================
# PAGE HEADER
# ==========================================================

st.title("🌾 Crop Productivity Prediction")

st.caption(
    """
Prediksi produktivitas tanaman menggunakan model Machine Learning
berdasarkan lokasi, kondisi cuaca, dan karakteristik lahan.
"""
)

st.divider()


# ==========================================================
# INFORMATION CARD
# ==========================================================

info1, info2, info3 = st.columns(3)

with info1:

    st.info(
        """
📍 **Location**

Pilih kabupaten/kota untuk
mengisi koordinat secara otomatis.
"""
    )

with info2:

    st.info(
        """
🌦 **Weather**

Masukkan kondisi cuaca
sesuai lokasi lahan.
"""
    )

with info3:

    st.info(
        """
🤖 **AI Prediction**

Model XGBoost akan
mengestimasi produktivitas.
"""
    )


st.divider()


# ==========================================================
# LOCATION
# ==========================================================

st.subheader("📍 Informasi Lokasi")


left_col, right_col = st.columns(
    [2, 1]
)


with left_col:

    kabupaten = st.selectbox(

        "Kabupaten / Kota",

        sorted(
            location_df[
                "kabupaten_kota"
            ].unique()
        )

    )

    selected = location_df.loc[
        location_df["kabupaten_kota"]
        == kabupaten
    ].iloc[0]


    latitude = float(
        selected["latitude"]
    )

    longitude = float(
        selected["longitude"]
    )


with right_col:

    komoditas = st.selectbox(

        "Komoditas",

        [

            "Padi",

            "Jagung",

            "Singkong"

        ]

    )

# ==========================================================
# MAP
# ==========================================================

st.markdown("### 🗺 Lokasi Lahan")

map_col, info_col = st.columns([2.2, 1])

with map_col:

    farm_map = folium.Map(

        location=[
            latitude,
            longitude
        ],

        zoom_start=10,

        control_scale=True,

        tiles="OpenStreetMap"

    )

    folium.Marker(

        location=[
            latitude,
            longitude
        ],

        popup=f"""
        <b>{kabupaten}</b><br>
        Komoditas : {komoditas}
        """,

        tooltip=kabupaten,

        icon=folium.Icon(
            color="green",
            icon="leaf"
        )

    ).add_to(farm_map)

    map_data = st_folium(

        farm_map,

        width=None,

        height=430,

        returned_objects=[]

    )


with info_col:

    st.success(
        "📍 Lokasi berhasil dipilih"
    )

    st.metric(

        "Latitude",

        f"{latitude:.6f}"

    )

    st.metric(

        "Longitude",

        f"{longitude:.6f}"

    )

    st.metric(

        "Komoditas",

        komoditas

    )


st.divider()


# ==========================================================
# COORDINATE
# ==========================================================

st.subheader("🌍 Koordinat Lokasi")

coord1, coord2 = st.columns(2)

with coord1:

    latitude = st.number_input(

        "Latitude",

        value=float(latitude),

        format="%.6f"

    )

with coord2:

    longitude = st.number_input(

        "Longitude",

        value=float(longitude),

        format="%.6f"

    )


st.caption(
    "Koordinat otomatis mengikuti kabupaten yang dipilih, "
    "namun tetap dapat diubah secara manual."
)


st.divider()


# ==========================================================
# LAND INFORMATION
# ==========================================================

st.subheader("🌱 Informasi Lahan")

land1, land2 = st.columns(2)

with land1:

    luas_lahan = st.number_input(

        "Luas Lahan (Ha)",

        min_value=0.1,

        value=1.0,

        step=0.1

    )

with land2:

    st.metric(

        "Kabupaten",

        kabupaten

    )


st.divider()

# ==========================================================
# WEATHER SOURCE
# ==========================================================

st.subheader("🌦 Weather Source")

weather_mode = st.radio(

    "Pilih sumber data cuaca",

    [

        "Manual Input",

        "Automatic (Historical Weather)"

    ],

    horizontal=True

)

st.divider()


# ==========================================================
# WEATHER HELPER
# ==========================================================

weather = {

    "temperature": None,

    "temp_max": None,

    "temp_min": None,

    "rainfall": None,

    "humidity": None,

    "wind_speed": None,

    "solar_radiation": None

}


# ==========================================================
# MANUAL WEATHER
# ==========================================================

if weather_mode == "Manual Input":

    st.info(
        "Masukkan kondisi cuaca secara manual."
    )

    temp_col, rain_col, env_col = st.columns(3)

    with temp_col:

        st.markdown("#### 🌡 Temperature")

        weather["temperature"] = st.number_input(

            "Temperature (°C)",

            value=27.0,

            step=0.1

        )

        weather["temp_max"] = st.number_input(

            "Maximum Temperature (°C)",

            value=31.0,

            step=0.1

        )

        weather["temp_min"] = st.number_input(

            "Minimum Temperature (°C)",

            value=23.0,

            step=0.1

        )

    with rain_col:

        st.markdown("#### ☔ Rainfall")

        weather["rainfall"] = st.number_input(

            "Rainfall (mm)",

            value=250.0,

            step=1.0

        )

        weather["humidity"] = st.number_input(

            "Humidity (%)",

            value=80.0,

            step=1.0

        )

    with env_col:

        st.markdown("#### ☀ Environment")

        weather["wind_speed"] = st.number_input(

            "Wind Speed (m/s)",

            value=2.0,

            step=0.1

        )

        weather["solar_radiation"] = st.number_input(

            "Solar Radiation",

            value=18.0,

            step=0.1

        )

else:

    st.success(
        "Automatic Weather akan menggunakan "
        "data cuaca historis berdasarkan lokasi."
    )

st.divider()

# ==========================================================
# HISTORICAL WEATHER
# ==========================================================

@st.cache_data(show_spinner=False)
def load_weather():

    weather_df = pd.read_csv(

        DATA_DIR

        / "weather_yearly.csv"

    )

    weather_df["kabupaten"] = (

        weather_df["kabupaten"]

        .astype(str)

        .str.upper()

        .str.strip()

    )

    return weather_df


weather_df = load_weather()


# ==========================================================
# GET HISTORICAL WEATHER
# ==========================================================

def get_auto_weather(
    kabupaten,
):

    selected = (

        kabupaten

        .upper()

        .replace("KABUPATEN ", "")

        .replace("KOTA ", "")

        .strip()

    )

    data = weather_df.loc[

        weather_df["kabupaten"]

        .str.contains(

            selected,

            case=False,

            na=False

        )

    ]

    if data.empty:

        return None

    latest = (

        data

        .sort_values(

            "tahun",

            ascending=False

        )

        .iloc[0]

    )

    return {

        "temperature":

            float(latest["temperature"]),

        "temp_max":

            float(latest["temp_max"]),

        "temp_min":

            float(latest["temp_min"]),

        "rainfall":

            float(latest["rainfall"]),

        "humidity":

            float(latest["humidity"]),

        "wind_speed":

            float(latest["wind_speed"]),

        "solar_radiation":

            float(latest["solar_radiation"]),

        "tahun":

            int(latest["tahun"])

    }


# ==========================================================
# AUTOMATIC WEATHER
# ==========================================================

if weather_mode == "Automatic (Historical Weather)":

    auto_weather = get_auto_weather(
        kabupaten
    )

    if auto_weather:

        weather.update(auto_weather)

        st.success(
            f"✅ Historical Weather {weather['tahun']} loaded."
        )

    else:

        st.warning(
            "Historical weather tidak ditemukan."
        )

        st.stop()


# ==========================================================
# WEATHER SUMMARY
# ==========================================================

st.subheader("🌦 Weather Summary")

m1, m2, m3, m4 = st.columns(4)

with m1:

    st.metric(

        "Temperature",

        f"{weather['temperature']:.1f} °C"

    )

    st.metric(

        "Temp Max",

        f"{weather['temp_max']:.1f} °C"

    )

with m2:

    st.metric(

        "Temp Min",

        f"{weather['temp_min']:.1f} °C"

    )

    st.metric(

        "Rainfall",

        f"{weather['rainfall']:.1f} mm"

    )

with m3:

    st.metric(

        "Humidity",

        f"{weather['humidity']:.1f}%"

    )

    st.metric(

        "Wind Speed",

        f"{weather['wind_speed']:.2f} m/s"

    )

with m4:

    st.metric(

        "Solar Radiation",

        f"{weather['solar_radiation']:.2f}"

    )

    st.metric(

        "Location",

        kabupaten

    )

st.divider()

# ==========================================================
# PREDICTION BUTTON
# ==========================================================

predict_button = st.button(

    "🚀 Prediksi Produktivitas",

    type="primary",

    use_container_width=True

)

st.divider()

# ==========================================================
# HELPER
# ==========================================================

def build_payload():

    return {

        "kabupaten": kabupaten,

        "komoditas": komoditas,

        "luas_lahan": luas_lahan,

        "temperature": weather["temperature"],

        "temp_max": weather["temp_max"],

        "temp_min": weather["temp_min"],

        "rainfall": weather["rainfall"],

        "humidity": weather["humidity"],

        "wind_speed": weather["wind_speed"],

        "solar_radiation": weather["solar_radiation"]

    }


def validate_payload(payload):

    missing = []

    for key, value in payload.items():

        if value is None:

            missing.append(key)

    return missing


def generate_ai_recommendation(prediction):

    if prediction >= 70:

        return (
            "🌾 Potensi produktivitas sangat tinggi.\n\n"
            "Pertahankan pola budidaya saat ini, "
            "monitor kelembapan lahan dan lakukan "
            "pemupukan sesuai fase pertumbuhan."
        )

    elif prediction >= 55:

        return (
            "✅ Produktivitas diperkirakan baik.\n\n"
            "Pastikan irigasi tetap stabil dan "
            "monitor serangan hama selama fase vegetatif."
        )

    elif prediction >= 40:

        return (
            "⚠️ Produktivitas sedang.\n\n"
            "Perbaiki pengelolaan air dan "
            "pemupukan agar hasil panen meningkat."
        )

    return (
        "❗ Produktivitas diperkirakan rendah.\n\n"
        "Evaluasi kondisi lahan, kualitas benih "
        "dan strategi budidaya."
    )


# ==========================================================
# PREDICTION
# ==========================================================

if predict_button:

    payload = build_payload()

    missing = validate_payload(payload)

    if len(missing):

        st.error(

            "Input berikut belum lengkap:\n\n"

            + "\n".join(
                f"- {x}" for x in missing
            )

        )

        st.stop()

    progress = st.progress(0)

    status = st.empty()

    status.info(
        "Menyiapkan data..."
    )

    progress.progress(20)

    try:

        status.info(
            "Menghubungi Prediction API..."
        )

        progress.progress(45)

        result = api.predict(payload)

        progress.progress(75)

        # ==========================
        # ERROR HANDLING
        # ==========================

        if "detail" in result:

            st.error("Prediction API Error")

            st.json(result)

            st.stop()

        if "error" in result:

            st.error(result["error"])

            st.stop()

        if "predicted_productivity" not in result:

            st.error("Response backend tidak sesuai.")
            st.json(result)
            st.stop()

        prediction = float(
            result["predicted_productivity"]
        )

        estimasi_panen = float(
            result["estimated_yield_ton"]
        )

        confidence = None

        ai_recommendation = (

            generate_ai_recommendation(

                prediction

            )

        )

        progress.progress(100)

        status.success(

            "Prediksi berhasil."

        )

    except Exception as e:

        progress.empty()

        status.empty()

        st.error(

            "Prediction API gagal diakses."

        )

        st.exception(e)

        st.stop()

    # ======================================================
    # SAVE RESULT
    # ======================================================

    st.session_state["prediction"] = prediction

    st.session_state["confidence"] = confidence

    st.session_state["estimasi_panen"] = estimasi_panen

    st.session_state["recommendation"] = ai_recommendation

    st.session_state["payload"] = payload

    st.session_state["kabupaten"] = kabupaten

    st.session_state["komoditas"] = komoditas

    st.session_state["luas_lahan"] = luas_lahan

# ==========================================================
# RESULT DASHBOARD
# ==========================================================

if "prediction" in st.session_state:

    st.divider()

    st.header("📊 Hasil Prediksi")

    prediction = st.session_state["prediction"]

    confidence = st.session_state["confidence"]

    estimasi_panen = st.session_state["estimasi_panen"]

    recommendation = st.session_state["recommendation"]

    payload = st.session_state["payload"]

    tab1, tab2, tab3 = st.tabs(

        [

            "📈 Prediction",

            "💡 AI Insight",

            "📋 Input Summary"

        ]

    )

    # ======================================================
    # TAB 1
    # ======================================================

    with tab1:

        c1, c2, c3 = st.columns(3)

        with c1:

            st.metric(

                "🌾 Produktivitas",

                f"{prediction:.2f}",

                "Kuintal / Ha"

            )

        with c2:

            st.metric(

                "🚜 Estimasi Panen",

                f"{estimasi_panen:.2f}",

                "Ton"

            )

        with c3:

            if confidence is not None:
                st.metric(

                    "🎯 Confidence",

                    f"{confidence:.1f}%"

                )

            else:

                st.metric(

                    "🎯 Confidence",

                    "N/A"

                )

        st.progress(

            min(

                prediction / 100,

                1.0

            )

        )

        st.success(

            "Prediksi berhasil dibuat."

        )

    # ======================================================
    # TAB 2
    # ======================================================

    with tab2:

        st.markdown("### 🤖 AI Recommendation")

        st.info(

            recommendation

        )

        st.markdown("---")

        st.markdown("### 📍 Informasi Lokasi")

        st.write(

            f"**Kabupaten :** {kabupaten}"

        )

        st.write(

            f"**Komoditas :** {komoditas}"

        )

        st.write(

            f"**Luas Lahan :** {luas_lahan:.2f} Ha"

        )

    # ======================================================
    # TAB 3
    # ======================================================

    with tab3:

        summary = pd.DataFrame(

            {

                "Feature":

                payload.keys(),

                "Value":

                payload.values()

            }

        )

        st.dataframe(

            summary,

            use_container_width=True

        )

        export = pd.DataFrame(

            [

                {

                    "Kabupaten": kabupaten,

                    "Komoditas": komoditas,

                    "Prediction": prediction,

                    "Confidence": confidence,

                    "Estimasi Panen": estimasi_panen,

                    "Luas Lahan": luas_lahan

                }

            ]

        )

        st.download_button(

            "📥 Download CSV",

            export.to_csv(

                index=False

            ),

            file_name="prediction_result.csv",

            mime="text/csv",

            use_container_width=True

        )

st.divider()

st.caption(

    "Menanam AI • Productivity Prediction Module"

)