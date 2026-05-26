#---------------------------------------------------------------------------------------4
import pandas as pd

# 1. Ścieżka do pliku z usuniętymi kolumnami
input_path = r"C:\zrodla_i_reprezentacja_danych\Wersja_finalna\_02_usuniete_dane_rowerowe.parquet"

# 2. Wczytanie danych
df = pd.read_parquet(input_path)

# 3. Konwersja na format datetime (żeby operacje na datach były precyzyjne)
df['started_at'] = pd.to_datetime(df['started_at'])

# 4. Wyznaczenie pierwszego i ostatniego dnia
pierwszy_przejazd = df['started_at'].min()
ostatni_przejazd = df['started_at'].max()

# 5. Sprawdzenie liczby wierszy
liczba_wierszy = len(df)

# 5. Wyświetlenie wyników
print(f"Pierwszy zarejestrowany przejazd: {pierwszy_przejazd}")
print(f"Ostatni zarejestrowany przejazd:  {ostatni_przejazd}")
print(f"Całkowita liczba przejazdów (wierszy): {liczba_wierszy:,}".replace(',', ' '))