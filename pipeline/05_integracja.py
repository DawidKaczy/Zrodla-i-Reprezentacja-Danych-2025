import pandas as pd
from sklearn.preprocessing import StandardScaler

from paths import HOLIDAYS, MASTER, RIDES_CLEAN, WEATHER

df_rowery = pd.read_parquet(RIDES_CLEAN)
df_swieta = pd.read_parquet(HOLIDAYS)
df_pogoda = pd.read_parquet(WEATHER)

df_rowery["date"] = pd.to_datetime(df_rowery["started_at"]).dt.date
df_zagregowane = df_rowery.groupby("date").size().reset_index(name="total_rides")
df_zagregowane["day_of_week"] = pd.to_datetime(df_zagregowane["date"]).dt.day_name()

df_zagregowane["date"] = pd.to_datetime(df_zagregowane["date"])
df_swieta["date"] = pd.to_datetime(df_swieta["date"])
df_pogoda["date"] = pd.to_datetime(df_pogoda["date"])

master_df = pd.merge(df_zagregowane, df_pogoda, on="date", how="inner")
master_df = pd.merge(master_df, df_swieta, on="date", how="left")

master_df["is_holiday"] = master_df["is_holiday"].fillna(0).astype(int)
master_df.drop(columns=["holiday_name"], inplace=True)
master_df = pd.get_dummies(master_df, columns=["day_of_week"], drop_first=True)

scaler = StandardScaler()
kolumny_numeryczne = ["tavg", "tmin", "tmax", "prcp"]
master_df[kolumny_numeryczne] = scaler.fit_transform(master_df[kolumny_numeryczne])

master_df.drop(columns=["date"], inplace=True)
master_df.to_parquet(MASTER, index=False)
print(f"Zapisano zbiór modelowy ({len(master_df)} dni): {MASTER}")
