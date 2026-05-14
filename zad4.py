import pandas as pd

df_rowery = pd.read_parquet("divvy_tripdata_combined.parquet")
df_rowery['started_at'] = pd.to_datetime(df_rowery['started_at'])
df_rowery['data'] = df_rowery['started_at'].dt.date

# Agregacja
df_dzienne = df_rowery.groupby('data').size().reset_index(name='liczba_wypozyczen')
df_dzienne['data'] = pd.to_datetime(df_dzienne['data'])
poczatkowa_liczba = len(df_dzienne)

# Usunięcie braków i błędów
df_dzienne = df_dzienne.dropna()
df_dzienne = df_dzienne[df_dzienne['liczba_wypozyczen'] >= 0]

# Usuwanie Wartości Odstających (Outliers)
Q1 = df_dzienne['liczba_wypozyczen'].quantile(0.25)
Q3 = df_dzienne['liczba_wypozyczen'].quantile(0.75)
IQR = Q3 - Q1
dolna_granica = Q1 - 1.5 * IQR
gorna_granica = Q3 + 1.5 * IQR

df_dzienne_czyste = df_dzienne[(df_dzienne['liczba_wypozyczen'] >= dolna_granica) &
                               (df_dzienne['liczba_wypozyczen'] <= gorna_granica)].copy()

print(f"Rowery: Odfiltrowano {poczatkowa_liczba - len(df_dzienne_czyste)} błędnych lub odstających dni.")

print("--- 2. PRZYGOTOWANIE BAZY POGODOWEJ ---")
df_pogoda = pd.read_csv("pogoda_chicago_2020_2022.csv")
df_pogoda['data'] = pd.to_datetime(df_pogoda['data'])

# Czyszczenie braków w pogodzie
df_pogoda_czysta = df_pogoda.dropna().copy()
print(f"Pogoda: Gotowych dni do złączenia: {len(df_pogoda_czysta)}")


print("\n--- 3. ŁĄCZENIE CZYSTYCH BAZ (MERGE) ---")
# Teraz łączymy dwa w 100% czyste zbiory danych
df_master = pd.merge(df_dzienne_czyste, df_pogoda_czysta, on='data', how='inner')

print(f"Sukces! Czysty złączony zbiór liczy {len(df_master)} dni.")

from sklearn.preprocessing import StandardScaler

# --- 1. Inżynieria Cech ---
df_master['dzien_tygodnia'] = df_master['data'].dt.day_name()
df_master['miesiac'] = df_master['data'].dt.month_name()

# --- 2. One Hot Encoding ---
kolumny_do_kodowania = ['dzien_tygodnia', 'miesiac']
df_encoded = pd.get_dummies(df_master, columns=kolumny_do_kodowania, dtype=int)

# --- 3. Standaryzacja Danych ---
scaler = StandardScaler()
kolumny_numeryczne = ['temp_max_c', 'temp_min_c', 'temperatura_c', 'opady_mm']

# Skalowanie (nadpisujemy oryginalne kolumny)
df_encoded[kolumny_numeryczne] = scaler.fit_transform(df_encoded[kolumny_numeryczne])

# --- 4. Finalizacja ---
df_final = df_encoded.drop(columns=['data'])

print("Gotowe! Zbiór `df_final` jest idealnie przygotowany dla algorytmów ML.")
df_final.head()

# 1. Zapisujemy wersję czytelną (do analizy i wykresów)
df_final.to_parquet("chicago_bikes_daily_master.parquet")

# 2. Zapisujemy wersję dla modelu (po OHE i Skalowaniu)
# Tutaj lepiej użyć formatu .csv lub .parquet
df_final.to_parquet("chicago_bikes_ml_input.parquet")

print("Pomyślnie utworzono punkty kontrolne danych!")