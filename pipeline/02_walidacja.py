import pandas as pd

from paths import RIDES_CLEAN

df = pd.read_parquet(RIDES_CLEAN)
df["started_at"] = pd.to_datetime(df["started_at"])

pierwszy_przejazd = df["started_at"].min()
ostatni_przejazd = df["started_at"].max()
liczba_wierszy = len(df)

print(f"Pierwszy zarejestrowany przejazd: {pierwszy_przejazd}")
print(f"Ostatni zarejestrowany przejazd:  {ostatni_przejazd}")
print(f"Całkowita liczba przejazdów (wierszy): {liczba_wierszy:,}".replace(",", " "))
