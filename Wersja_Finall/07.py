import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

input_path = r"C:\zrodla_i_reprezentacja_danych\Wersja_finalna\_05_FINAL_dane_znormalizowane.parquet"
df = pd.read_parquet(input_path)

df['tavg'] = pd.to_numeric(df['tavg'])
df['prcp'] = pd.to_numeric(df['prcp'])
df['total_rides'] = pd.to_numeric(df['total_rides'])

# 2. Wykres wpływu średniej temperatury (tavg)
plt.figure(figsize=(10, 6))
sns.regplot(data=df, x='tavg', y='total_rides',
            scatter_kws={'alpha':0.4, 'color':'orange'},
            line_kws={'color':'red'})
plt.title('Wpływ średniej temperatury na liczbę wypożyczeń')
plt.xlabel(r'Średnia temperatura ($^\circ C$)')
plt.ylabel('Całkowita liczba wypożyczeń')
plt.grid(True, linestyle='--', alpha=0.6)
plt.savefig("__wykres_wplyw_temperatury.png")
print("Wykres temperatury zapisany jako: wykres_wplyw_temperatury.png")

# 3. Wykres wpływu opadów (prcp)
plt.figure(figsize=(10, 6))
sns.regplot(data=df, x='prcp', y='total_rides',
            scatter_kws={'alpha':0.4, 'color':'blue'},
            line_kws={'color':'red'})
plt.title('Wpływ opadów na liczbę wypożyczeń')
plt.xlabel('Opady atmosferyczne (mm)')
plt.ylabel('Całkowita liczba wypożyczeń')
plt.grid(True, linestyle='--', alpha=0.6)
plt.savefig("__wykres_wplyw_opadow.png")
print("Wykres opadów zapisany jako: wykres_wplyw_opadow.png")