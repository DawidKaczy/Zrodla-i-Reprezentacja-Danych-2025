from datetime import datetime

import pandas as pd
from meteostat import daily

from paths import WEATHER

start_date = datetime(2020, 4, 1)
end_date = datetime(2022, 7, 31)
chicago_station = "72530"

data = daily(chicago_station, start_date, end_date)
weather_df = data.fetch()

if weather_df is None or weather_df.empty:
    print("BŁĄD: API nie zwróciło danych! Sprawdź połączenie sieciowe.")
else:
    weather_df = weather_df.reset_index()
    weather_df = weather_df[["time", "tmin", "tmax", "prcp"]]
    weather_df["tavg"] = ((weather_df["tmin"] + weather_df["tmax"]) / 2).round(2)
    weather_df.rename(columns={"time": "date"}, inplace=True)
    weather_df["date"] = pd.to_datetime(weather_df["date"]).dt.date

    weather_df["prcp"] = weather_df["prcp"].fillna(0)
    weather_df["tmin"] = weather_df["tmin"].ffill()
    weather_df["tmax"] = weather_df["tmax"].ffill()
    weather_df["tavg"] = weather_df["tavg"].fillna(
        ((weather_df["tmin"] + weather_df["tmax"]) / 2).round(2)
    )

    weather_df.to_parquet(WEATHER, index=False)
    print(f"Zapisano pogodę: {WEATHER}")
