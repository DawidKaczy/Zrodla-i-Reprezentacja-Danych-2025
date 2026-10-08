import glob
import os
import shutil

import kagglehub
import pandas as pd

from paths import DATA_RAW, RIDES_CLEAN, RIDES_MERGED

downloaded_path = kagglehub.dataset_download("gunnarn/chicago-bicycle-rent-usage")

for item in os.listdir(downloaded_path):
    source = os.path.join(downloaded_path, item)
    destination = DATA_RAW / item

    if os.path.isdir(source):
        if destination.exists():
            shutil.rmtree(destination)
        shutil.copytree(source, destination)
    else:
        shutil.copy2(source, destination)

print(f"Pliki zostały zapisane w: {DATA_RAW}")

all_files = glob.glob(str(DATA_RAW / "*.csv"))
print(f"Znaleziono {len(all_files)} plików do połączenia.")

df_list = []
for filename in all_files:
    temp_df = pd.read_csv(filename, dtype={"start_station_id": str, "end_station_id": str})
    df_list.append(temp_df)
    print(f"Wczytano: {os.path.basename(filename)} | Wierszy: {len(temp_df)}")

full_df = pd.concat(df_list, axis=0, ignore_index=True)
print("-" * 30)
print(f"Sukces! Połączony zbiór ma {len(full_df)} wierszy.")

full_df["start_station_id"] = full_df["start_station_id"].astype(str)
full_df["end_station_id"] = full_df["end_station_id"].astype(str)

full_df.to_parquet(RIDES_MERGED, index=False)
print(f"Plik został pomyślnie zapisany w: {RIDES_MERGED}")

columns_to_drop = [
    "ride_id",
    "rideable_type",
    "ended_at",
    "start_station_name",
    "start_station_id",
    "end_station_name",
    "end_station_id",
    "start_lat",
    "start_lng",
    "end_lat",
    "end_lng",
    "member_casual",
]
existing_cols_to_drop = [col for col in columns_to_drop if col in full_df.columns]
full_df.drop(columns=existing_cols_to_drop, inplace=True)

print(f"Usunięto niepotrzebne kolumny. Zostały {len(full_df.columns)} kolumny.")
print(f"Zatrzymane kolumny: {list(full_df.columns)}")
print("-" * 30)

full_df.to_parquet(RIDES_CLEAN, index=False)
print(f"Zapisano oczyszczony zbiór: {RIDES_CLEAN}")
