import pandas as pd
import glob
import os
import pyarrow

sciezka_do_plikow = r"C:\zrodla_i_reprezentacja_danych\pythonProject1\1\*tripdata.csv"
pliki = glob.glob(sciezka_do_plikow)

if not pliki:
    print("BŁĄD: Nie znaleziono żadnych plików! Sprawdź, czy ścieżka jest poprawna.")
    exit()

lista_df = []

print("Rozpoczynam wczytywanie plików...")
for plik in pliki:
    print(f"Wczytywanie: {plik}")
    df = pd.read_csv(plik)
    lista_df.append(df)

polaczone_dane = pd.concat(lista_df, ignore_index=True)

print("\nGotowe! Informacje o połączonym zbiorze:")
print(polaczone_dane.info())

# Wymuszenie konwersji problematycznych kolumn na typ tekstowy (string)
polaczone_dane['start_station_id'] = polaczone_dane['start_station_id'].astype(str)
polaczone_dane['end_station_id'] = polaczone_dane['end_station_id'].astype(str)

# Zapis do Parquet (format spełniający wymóg z wytycznych projektu)
nazwa_pliku_wyjsciowego = "divvy_tripdata_combined.parquet"
polaczone_dane.to_parquet(nazwa_pliku_wyjsciowego)

print(f"\nSukces! Cały zbiór został skompresowany i zapisany jako: {nazwa_pliku_wyjsciowego}")

