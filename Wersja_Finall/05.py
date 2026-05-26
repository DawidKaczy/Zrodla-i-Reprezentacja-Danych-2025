import pandas as pd
from sklearn.preprocessing import StandardScaler

# 1. Wczytanie plików
df_rowery = pd.read_parquet(r"C:\zrodla_i_reprezentacja_danych\Wersja_finalna\_02_usuniete_dane_rowerowe.parquet")
df_swieta = pd.read_parquet(r"C:\zrodla_i_reprezentacja_danych\Wersja_finalna\_03_swieta_chicago.parquet")
df_pogoda = pd.read_parquet(r"C:\zrodla_i_reprezentacja_danych\Wersja_finalna\_04_pogoda_chicago.parquet")

# 2. Agregacja rowerów + wyciągnięcie dnia tygodnia
df_rowery['date'] = pd.to_datetime(df_rowery['started_at']).dt.date
df_zagregowane = df_rowery.groupby('date').size().reset_index(name='total_rides')
df_zagregowane['day_of_week'] = pd.to_datetime(df_zagregowane['date']).dt.day_name()

# 3. Ujednolicenie formatów dat
df_zagregowane['date'] = pd.to_datetime(df_zagregowane['date'])
df_swieta['date'] = pd.to_datetime(df_swieta['date'])
df_pogoda['date'] = pd.to_datetime(df_pogoda['date'])

# 4. Łączenie
master_df = pd.merge(df_zagregowane, df_pogoda, on='date', how='inner')
master_df = pd.merge(master_df, df_swieta, on='date', how='left')

# 5. Czyszczenie świąt
master_df['is_holiday'] = master_df['is_holiday'].fillna(0).astype(int)
master_df.drop(columns=['holiday_name'], inplace=True)

# 6. One Hot Encoding (dni tygodnia)
master_df = pd.get_dummies(master_df, columns=['day_of_week'], drop_first=True)

# 7. Standaryzacja
scaler = StandardScaler()
kolumny_numeryczne = ['tavg', 'tmin', 'tmax', 'prcp']
master_df[kolumny_numeryczne] = scaler.fit_transform(master_df[kolumny_numeryczne])

# 8. Zapis finalny
master_df.drop(columns=['date'], inplace=True) # Model nie czyta dat
master_df.to_parquet(r"C:\zrodla_i_reprezentacja_danych\Wersja_finalna\_05_FINAL_dane_znormalizowane.parquet", index=False)
