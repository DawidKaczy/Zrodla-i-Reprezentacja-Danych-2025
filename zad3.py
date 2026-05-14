import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

import pandas as pd

print("Wczytywanie danych pogodowych...")
df_pogoda = pd.read_csv("open-meteo-41.86N87.65W179m.csv")

# 1. Zmiana nazwy kolumny i konwersja na format daty zrozumiały dla Pythona
df_pogoda = df_pogoda.rename(columns={'time': 'data'})
df_pogoda['data'] = pd.to_datetime(df_pogoda['data'])

# 2. Definiujemy nasz zakres czasowy (maska filtrująca)
data_poczatkowa = pd.to_datetime('2020-04-26')
data_koncowa = pd.to_datetime('2022-07-29')

maska = (df_pogoda['data'] >= data_poczatkowa) & (df_pogoda['data'] <= data_koncowa)

# Wycinamy tylko te wiersze, które mieszczą się w naszych widełkach
df_pogoda_przefiltrowana = df_pogoda.loc[maska].copy()

# 3. Ujednolicenie formatu daty (samo RRRR-MM-DD), żeby za chwilę połączyć to z rowerami
df_pogoda_przefiltrowana['data'] = df_pogoda_przefiltrowana['data'].dt.date

# 4. Zmiana nazw kolumn na prostsze (bez spacji i znaków specjalnych)
df_pogoda_przefiltrowana = df_pogoda_przefiltrowana.rename(columns={
    'temperature_2m_max (°C)': 'temp_max_c',
    'temperature_2m_min (°C)': 'temp_min_c',
    'rain_sum (mm)': 'opady_mm'
})

# Wyliczamy też średnią (na wszelki wypadek) i zaokrąglamy
df_pogoda_przefiltrowana['temperatura_c'] = ((df_pogoda_przefiltrowana['temp_max_c'] + df_pogoda_przefiltrowana['temp_min_c']) / 2).round(2)

# 5. Zostawiamy wszystko to, czego potrzebuje model ML (dodane temp_max i temp_min)
df_pogoda_czysta = df_pogoda_przefiltrowana[['data', 'temp_max_c', 'temp_min_c', 'temperatura_c', 'opady_mm']].copy()

print(f"Początek: {df_pogoda_czysta['data'].min()}")
print(f"Koniec: {df_pogoda_czysta['data'].max()}")
print(f"Liczba dni: {len(df_pogoda_czysta)}")

# Podgląd
df_pogoda_czysta.head()

# Zapis do pliku
nazwa_pliku_pogodowego = "pogoda_chicago_2020_2022.csv"
df_pogoda_czysta.to_csv(nazwa_pliku_pogodowego, index=False)
print(f"\nDane zapisane w pliku: {nazwa_pliku_pogodowego}")
