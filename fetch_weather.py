#!/usr/bin/env python3
import json
import urllib.request
from datetime import datetime, timezone

# =========================
# Darna University Campus
# =========================
PLACE_NAME = "جامعة درنة – ليبيا"
LAT = 32.7670
LON = 22.6367
TZ = "Africa/Tripoli"

URL = (
    "https://api.open-meteo.com/v1/forecast"
    f"?latitude={LAT}&longitude={LON}"
    "&current=temperature_2m,relative_humidity_2m,apparent_temperature,wind_speed_10m,weather_code"
    "&hourly=temperature_2m"
    "&daily=temperature_2m_max,temperature_2m_min,weather_code,precipitation_probability_max"
    f"&timezone={TZ}"
)

def main():
    req = urllib.request.Request(URL, headers={"User-Agent": "darna-campus-weather"})
    with urllib.request.urlopen(req) as r:
        data = json.loads(r.read())

    daily_out = []
    for i in range(7):
        daily_out.append({
            "date": data["daily"]["time"][i],
            "tmax_c": data["daily"]["temperature_2m_max"][i],
            "tmin_c": data["daily"]["temperature_2m_min"][i],
            "weather_code": data["daily"]["weather_code"][i],
            "precip_prob_pct": data["daily"]["precipitation_probability_max"][i],
        })

    hourly_out = []
    for i in range(24):
        hourly_out.append({
            "time": data["hourly"]["time"][i],
            "temp_c": data["hourly"]["temperature_2m"][i],
        })

    out = {
        "meta": {
            "place_name": PLACE_NAME,
            "lat": LAT,
            "lon": LON,
            "timezone": TZ,
            "source": "open-meteo",
            "generated_utc": datetime.now(timezone.utc).isoformat()
        },
        "current": {
            "temperature_c": data["current"]["temperature_2m"],
            "feels_like_c": data["current"]["apparent_temperature"],
            "humidity_pct": data["current"]["relative_humidity_2m"],
            "wind_speed_kmh": data["current"]["wind_speed_10m"],
            "weather_code": data["current"]["weather_code"]
        },
        "daily": daily_out,
        "hourly": {
            "next24": hourly_out
        }
    }

    with open("weather.json", "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=2)

if __name__ == "__main__":
    main()
