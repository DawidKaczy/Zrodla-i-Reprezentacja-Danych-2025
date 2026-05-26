import kagglehub
import os
import shutil

#---------------------------------------------------------------------------------------1
# 1. Definicja docelowej ścieżki projektu
target_dir = r"C:\zrodla_i_reprezentacja_danych\Wersja_finalna\dane_kaggle"

# 2. Pobieranie zbioru (pobierze do domyślnej pamięci podręcznej)
downloaded_path = kagglehub.dataset_download("gunnarn/chicago-bicycle-rent-usage")

# 3. Tworzenie folderu w projekcie, jeśli nie istnieje
if not os.path.exists(target_dir):
    os.makedirs(target_dir)
    print(f"Utworzono folder: {target_dir}")

# 4. Przenoszenie zawartości do Twojego projektu
for item in os.listdir(downloaded_path):
    s = os.path.join(downloaded_path, item)
    d = os.path.join(target_dir, item)

    if os.path.isdir(s):
        if os.path.exists(d):
            shutil.rmtree(d)
        shutil.copytree(s, d)
    else:
        shutil.copy2(s, d)

print(f"Pliki zostały zapisane w: {target_dir}")

#---------------------------------------------------------------------------------------2
import pandas as pd
import glob
import os

# 1. Ustawienie ścieżki do folderu z danymi
path = r"C:\zrodla_i_reprezentacja_danych\Wersja_finalna\dane_kaggle"

# 2. Pobranie listy wszystkich plików CSV
all_files = glob.glob(os.path.join(path, "*.csv"))
print(f"Znaleziono {len(all_files)} plików do połączenia.")

# 3. Wczytywanie plików i łączenie ich w jeden DataFrame
df_list = []
for filename in all_files:
    # Wymuszamy typ 'object' (string) podczas wczytywania,
    temp_df = pd.read_csv(filename, dtype={'start_station_id': str, 'end_station_id': str})
    df_list.append(temp_df)
    print(f"Wczytano: {os.path.basename(filename)} | Wierszy: {len(temp_df)}")

# Łączenie wszystkich tabel w jedną
full_df = pd.concat(df_list, axis=0, ignore_index=True)
print("-" * 30)
print(f"Sukces! Połączony zbiór ma {len(full_df)} wierszy.")

# NAPRAWA: Upewniamy się, że całe kolumny są traktowane jako tekst (string)
full_df['start_station_id'] = full_df['start_station_id'].astype(str)
full_df['end_station_id'] = full_df['end_station_id'].astype(str)

# 4. Definicja ścieżki i zapis do pliku Parquet
output_path = r"C:\zrodla_i_reprezentacja_danych\Wersja_finalna\_01_polaczone_dane_rowerowe.parquet"
full_df.to_parquet(output_path, index=False)

print(f"Plik został pomyślnie zapisany w: {output_path}")

#---------------------------------------------------------------------------------------3
columns_to_drop = [
    'ride_id', 'rideable_type', 'ended_at',
    'start_station_name', 'start_station_id',
    'end_station_name', 'end_station_id',
    'start_lat', 'start_lng', 'end_lat', 'end_lng', 'member_casual'
]

# Sprawdzamy, które z tych kolumn faktycznie są w tabeli (bezpieczeństwo)
existing_cols_to_drop = [col for col in columns_to_drop if col in full_df.columns]

# Usuwamy kolumny (inplace=True nadpisuje obecną tabelę w pamięci RAM)
full_df.drop(columns=existing_cols_to_drop, inplace=True)

print(f"Usunięto niepotrzebne kolumny. Zostały {len(full_df.columns)} kolumny.")
print(f"Zatrzymane kolumny: {list(full_df.columns)}")
print("-" * 30)

# 5. ZAPIS do nowego pliku
output_path = r"C:\zrodla_i_reprezentacja_danych\Wersja_finalna\_02_usuniete_dane_rowerowe.parquet"
full_df.to_parquet(output_path, index=False)

print("-" * 50)


