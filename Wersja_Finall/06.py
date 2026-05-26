import pandas as pd
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, r2_score
from xgboost import XGBRegressor

input_path = r"C:\zrodla_i_reprezentacja_danych\Wersja_finalna\_05_FINAL_dane_znormalizowane.parquet"
df = pd.read_parquet(input_path)

X = df.drop(columns=['total_rides'])
y = df['total_rides']

# Podział na zbiór treningowy (80%) i testowy (20%)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Inicjalizacja i trening modelu XGBoost
model = XGBRegressor(n_estimators=100, learning_rate=0.1, max_depth=5, random_state=42, objective='reg:squarederror')
model.fit(X_train, y_train)

# Predykcja
predictions = model.predict(X_test)

# Wyniki
mae = mean_absolute_error(y_test, predictions)
r2 = r2_score(y_test, predictions)

print("-" * 30)
print("WYNIKI MODELU XGBOOST:")
print(f"Średni błąd (MAE): {mae:.2f}")
print(f"Współczynnik R2: {r2:.2f}")
print("-" * 30)

# Wizualizacja TOP 10 najważniejszych cech
feature_importances = pd.Series(model.feature_importances_, index=X.columns)
top_10 = feature_importances.sort_values(ascending=True).tail(10)

# Rysujemy wykres
plt.figure(figsize=(10, 6))

ax = top_10.plot(kind='barh', color='salmon', edgecolor='black')

ax.bar_label(ax.containers[0], fmt='%.3f', padding=3)

ax.set_xlim(right=top_10.max() * 1.15)

plt.title('TOP 10 najważniejszych cech (XGBoost)')
plt.xlabel('Ważność (Gain)')
plt.ylabel('Nazwa cechy')

plt.tight_layout()

plt.savefig("__wykres_waznosci_xgboost.png")
plt.show()
