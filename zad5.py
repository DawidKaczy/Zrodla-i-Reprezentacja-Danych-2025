import pandas as pd
from sklearn.model_selection import train_test_split

print("Wczytywanie przygotowanych danych ML...")
df_ml = pd.read_parquet("chicago_bikes_ml_input.parquet")

# Oddzielenie cech (X - pogoda, daty) od naszego celu (y - liczba wypożyczeń)
X = df_ml.drop(columns=['liczba_wypozyczen'])
y = df_ml['liczba_wypozyczen']

# Podział (test_size=0.2 oznacza 20% na testy, random_state gwarantuje powtarzalność wyników)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

print(f"Szkolenie modelu na: {X_train.shape[0]} dniach.")
print(f"Testowanie modelu na: {X_test.shape[0]} dniach.")

import xgboost as xgb
from sklearn.metrics import mean_absolute_error, r2_score

# Inicjalizacja modelu
model_xgb = xgb.XGBRegressor(
    n_estimators=100,      # Liczba drzew decyzyjnych
    learning_rate=0.1,     # Szybkość uczenia
    max_depth=5,           # Maksymalna głębokość pojedynczego drzewa
    random_state=42
)

# TRENING (Uczenie maszyny)
model_xgb.fit(X_train, y_train)

# PROGNOZOWANIE (Egzamin na zbiorze testowym)
y_pred = model_xgb.predict(X_test)

# OCENA WYNIKÓW
mae = mean_absolute_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)

print("\n--- WYNIKI EGZAMINU MODELU ---")
print(f"Średni błąd modelu (MAE): pomyliliśmy się średnio o {mae:.0f} wypożyczeń dziennie.")
print(f"Skuteczność modelu (R^2): {r2:.2f}")


import matplotlib.pyplot as plt
import seaborn as sns

# Wyciągnięcie wag z wytrenowanego modelu
waznosc_cech = model_xgb.feature_importances_
nazwy_cech = X.columns

# Złączenie tego w ładną tabelkę (DataFrame) i posortowanie
df_waznosc = pd.DataFrame({'Cecha': nazwy_cech, 'Waznosc': waznosc_cech})
df_waznosc = df_waznosc.sort_values(by='Waznosc', ascending=False).head(10) # Bierzemy TOP 10

# Rysowanie wykresu
plt.figure(figsize=(10, 6))
sns.barplot(data=df_waznosc, x='Waznosc', y='Cecha', hue='Cecha', palette='viridis', legend=False)

plt.title("TOP 10 najważniejszych czynników wpływających na wypożyczenia (XGBoost)", fontsize=14)
plt.xlabel("Waga (wpływ na decyzję modelu)", fontsize=12)
plt.ylabel("Cecha (Feature)", fontsize=12)
plt.tight_layout()

# Zapisanie wykresu na dysk, żebyś mógł go wkleić do prezentacji lub sprawozdania
plt.savefig("feature_importance_xgboost.png")
plt.show()