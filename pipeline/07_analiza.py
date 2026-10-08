import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

from paths import FIGURES, MASTER

df = pd.read_parquet(MASTER)
df["tavg"] = pd.to_numeric(df["tavg"])
df["prcp"] = pd.to_numeric(df["prcp"])
df["total_rides"] = pd.to_numeric(df["total_rides"])

plt.figure(figsize=(10, 6))
sns.regplot(
    data=df,
    x="tavg",
    y="total_rides",
    scatter_kws={"alpha": 0.4, "color": "orange"},
    line_kws={"color": "red"},
)
plt.title("Wpływ średniej temperatury na liczbę wypożyczeń")
plt.xlabel(r"Średnia temperatura ($^\circ C$)")
plt.ylabel("Całkowita liczba wypożyczeń")
plt.grid(True, linestyle="--", alpha=0.6)
temperature_path = FIGURES / "wplyw_temperatury.png"
plt.savefig(temperature_path)
print(f"Wykres temperatury zapisany: {temperature_path}")

plt.figure(figsize=(10, 6))
sns.regplot(
    data=df,
    x="prcp",
    y="total_rides",
    scatter_kws={"alpha": 0.4, "color": "blue"},
    line_kws={"color": "red"},
)
plt.title("Wpływ opadów na liczbę wypożyczeń")
plt.xlabel("Opady atmosferyczne (mm)")
plt.ylabel("Całkowita liczba wypożyczeń")
plt.grid(True, linestyle="--", alpha=0.6)
precipitation_path = FIGURES / "wplyw_opadow.png"
plt.savefig(precipitation_path)
print(f"Wykres opadów zapisany: {precipitation_path}")
