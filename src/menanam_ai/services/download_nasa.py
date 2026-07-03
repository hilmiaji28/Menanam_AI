# download_nasa.py

import pandas as pd
import requests
import time

# ==========================
# CONFIG
# ==========================

INPUT_FILE = "data/lat_long_kota_kab.csv"
OUTPUT_FILE = "data/raw/nasa_weather_daily.csv"

START_DATE = "20150101"
END_DATE = "20251231"

NASA_URL = "https://power.larc.nasa.gov/api/temporal/daily/point"

PARAMETERS = (
    "T2M,"
    "T2M_MAX,"
    "T2M_MIN,"
    "PRECTOTCORR,"
    "RH2M,"
    "WS2M,"
    "ALLSKY_SFC_SW_DWN"
)

# ==========================
# LOAD LOCATIONS
# ==========================

locations = pd.read_csv(INPUT_FILE)

print("\nColumns:")
print(locations.columns.tolist())

print("\nTotal Locations:")
print(len(locations))

# ==========================
# TEST MODE
# ==========================
# Untuk testing awal aktifkan:
#
# locations = locations.head(1)
#
# Setelah berhasil, comment lagi
# ==========================

all_records = []

# ==========================
# DOWNLOAD NASA DATA
# ==========================

for i, row in locations.iterrows():

    location_name = row["name"]
    latitude = row["lat"]
    longitude = row["long"]

    print(
        f"[{i+1}/{len(locations)}] "
        f"Downloading {location_name}"
    )

    params = {
        "parameters": PARAMETERS,
        "community": "AG",
        "latitude": latitude,
        "longitude": longitude,
        "start": START_DATE,
        "end": END_DATE,
        "format": "JSON"
    }

    try:

        response = requests.get(
            NASA_URL,
            params=params,
            timeout=60
        )

        if response.status_code != 200:

            print(
                f"Failed {location_name} "
                f"Status: {response.status_code}"
            )

            continue

        data = response.json()

        if "properties" not in data:

            print(
                f"Invalid response for "
                f"{location_name}"
            )

            continue

        weather = data["properties"]["parameter"]

        dates = weather["T2M"].keys()

        for date in dates:

            all_records.append({
                "kabupaten_kota": location_name,
                "latitude": latitude,
                "longitude": longitude,
                "date": date,

                "temperature":
                    weather["T2M"].get(date),

                "temp_max":
                    weather["T2M_MAX"].get(date),

                "temp_min":
                    weather["T2M_MIN"].get(date),

                "rainfall":
                    weather["PRECTOTCORR"].get(date),

                "humidity":
                    weather["RH2M"].get(date),

                "wind_speed":
                    weather["WS2M"].get(date),

                "solar_radiation":
                    weather["ALLSKY_SFC_SW_DWN"].get(date)
            })

        time.sleep(0.5)

    except Exception as e:

        print(
            f"Error {location_name}: {e}"
        )

# ==========================
# SAVE RESULT
# ==========================

weather_df = pd.DataFrame(all_records)

weather_df.to_csv(
    OUTPUT_FILE,
    index=False
)

print("\n======================")
print("DOWNLOAD COMPLETED")
print("======================")
print(f"Rows : {len(weather_df):,}")
print(f"File : {OUTPUT_FILE}")