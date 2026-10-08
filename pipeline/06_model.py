import matplotlib.pyplot as plt
import pandas as pd
from sklearn.metrics import mean_absolute_error, r2_score
from sklearn.model_selection import train_test_split
from xgboost import XGBRegressor

from paths import FIGURES, MASTER

df = pd.read_parquet(MASTER)
X = df.drop(columns=["total_rides"])
y = df["total_rides"]

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

model = XGBRegressor(
    n_estimators=100,
    learning_rate=0.1,
    max_depth=5,
    random_state=42,
    objective="reg:squarederror",
)
model.fit(X_train, y_train)
predictions = model.predict(X_test)

mae = mean_absolute_error(y_test, predictions)
r2 = r2_score(y_test, predictions)

print("-" * 30)
print("WYNIKI MODELU XGBOOST:")
print(f"Średni błąd (MAE): {mae:.2f}")
print(f"Współczynnik R2: {r2:.2f}")
print("-" * 30)

feature_importances = pd.Series(model.feature_importances_, index=X.columns)
top_10 = feature_importances.sort_values(ascending=True).tail(10)

plt.figure(figsize=(10, 6))
ax = top_10.plot(kind="barh", color="salmon", edgecolor="black")
ax.bar_label(ax.containers[0], fmt="%.3f", padding=3)
ax.set_xlim(right=top_10.max() * 1.15)
plt.title("TOP 10 najważniejszych cech (XGBoost)")
plt.xlabel("Ważność (Gain)")
plt.ylabel("Nazwa cechy")
plt.tight_layout()

figure_path = FIGURES / "waznosc_cech_xgboost.png"
plt.savefig(figure_path)
print(f"Wykres zapisany: {figure_path}")
plt.show()
