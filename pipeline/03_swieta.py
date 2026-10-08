from datetime import datetime

import pandas as pd
import requests
from bs4 import BeautifulSoup

from paths import HOLIDAYS

lata = [2020, 2021, 2022]
swieta_lista = []

naglowki = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    )
}

for rok in lata:
    url = f"https://www.officeholidays.com/countries/usa/illinois/{rok}"
    response = requests.get(url, headers=naglowki, timeout=30)

    if response.status_code != 200:
        print(f"Błąd! Serwer odrzucił połączenie dla roku {rok}. Kod: {response.status_code}")
        continue

    soup = BeautifulSoup(response.content, "html.parser")
    tabela = soup.find("table", class_="country-table")
    if not tabela:
        print(f"Brak tabeli świąt dla roku {rok}.")
        continue

    for wiersz in tabela.find("tbody").find_all("tr"):
        czas_tag = wiersz.find("time")
        komorki = wiersz.find_all("td")

        if czas_tag and czas_tag.has_attr("datetime") and len(komorki) >= 3:
            data_obj = datetime.strptime(czas_tag["datetime"], "%Y-%m-%d").date()
            swieta_lista.append(
                {
                    "date": data_obj,
                    "holiday_name": komorki[2].text.strip(),
                    "is_holiday": 1,
                }
            )

df_swieta = pd.DataFrame(swieta_lista)
df_swieta = df_swieta.drop_duplicates(subset=["date"])
df_swieta["date"] = pd.to_datetime(df_swieta["date"])
df_swieta.to_parquet(HOLIDAYS, index=False)
print(f"Zapisano {len(df_swieta)} dni świątecznych: {HOLIDAYS}")
