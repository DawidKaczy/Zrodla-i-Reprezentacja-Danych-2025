# ---------------------------------------------------------------------------------------5
import requests
from bs4 import BeautifulSoup
import pandas as pd
from datetime import datetime

lata = [2020, 2021, 2022]
swieta_lista = []

naglowki = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
}

for rok in lata:
    url = f"https://www.officeholidays.com/countries/usa/illinois/{rok}"

    response = requests.get(url, headers=naglowki)

    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')

        tabela = soup.find('table', class_='country-table')

        if tabela:
            wiersze = tabela.find('tbody').find_all('tr')

            for wiersz in wiersze:
                czas_tag = wiersz.find('time')

                komorki = wiersz.find_all('td')

                if czas_tag and czas_tag.has_attr('datetime') and len(komorki) >= 3:
                    data_str = czas_tag['datetime']

                    nazwa_swieta = komorki[2].text.strip()

                    data_obj = datetime.strptime(data_str, "%Y-%m-%d").date()

                    swieta_lista.append({
                        'date': data_obj,
                        'holiday_name': nazwa_swieta,
                        'is_holiday': 1
                    })
    else:
        print(f"Błąd! Serwer odrzucił połączenie dla roku {rok}. Kod: {response.status_code}")

df_swieta = pd.DataFrame(swieta_lista)

df_swieta = df_swieta.drop_duplicates(subset=['date'])

df_swieta['date'] = pd.to_datetime(df_swieta['date'])

output_path = r"C:\zrodla_i_reprezentacja_danych\Wersja_finalna\_03_swieta_chicago.parquet"
df_swieta.to_parquet(output_path, index=False)
