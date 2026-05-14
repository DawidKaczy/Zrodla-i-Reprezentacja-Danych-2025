import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

print("Wczytywanie czytelnych danych (przed skalowaniem)...")
df_wykresy = pd.read_parquet("chicago_bikes_daily_master.parquet")

sns.set_theme(style="whitegrid")


plt.figure(figsize=(10, 6))
sns.regplot(
    data=df_wykresy,
    x='temperatura_c',
    y='liczba_wypozyczen',
    scatter_kws={'alpha': 0.5, 'color': '#ff7f0e'},
    line_kws={'color': 'red', 'linewidth': 2}
)

plt.title('Wpływ Temperatury na Wypożyczenia Rowerów (Chicago 2020-2022)', fontsize=14, pad=15)
plt.xlabel('Średnia Temperatura (°C)', fontsize=12)
plt.ylabel('Liczba Wypożyczeń Dziennie', fontsize=12)

plt.tight_layout()
plt.savefig('wykres_1_temperatura.png', dpi=300)
plt.show()



plt.figure(figsize=(10, 6))
sns.regplot(
    data=df_wykresy,
    x='opady_mm',
    y='liczba_wypozyczen',
    scatter_kws={'alpha': 0.5, 'color': '#1f77b4'},
    line_kws={'color': 'darkblue', 'linewidth': 2}
)

plt.title('Wpływ Opadów Deszczu na Wypożyczenia Rowerów (Chicago 2020-2022)', fontsize=14, pad=15)
plt.xlabel('Suma Opadów (mm)', fontsize=12)
plt.ylabel('Liczba Wypożyczeń Dziennie', fontsize=12)

plt.tight_layout()
plt.savefig('wykres_2_opady.png', dpi=300)
plt.show()

print("\nWykresy zostały zapisane jako 'wykres_1_temperatura.png' oraz 'wykres_2_opady.png'.")


