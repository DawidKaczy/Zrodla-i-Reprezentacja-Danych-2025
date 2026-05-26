# 🚴‍♂️ Predykcja Wypożyczeń Rowerów Miejskich (Chicago) - Data Pipeline & Machine Learning

## 📖 O projekcie
Niniejszy projekt stanowi kompletny potok przetwarzania danych (Data Pipeline) mający na celu przewidywanie dziennego zapotrzebowania na rowery miejskie w Chicago. Projekt demonstruje pełen cykl życia modelu analitycznego: od automatycznej akwizycji z wielu źródeł (Kaggle API, Web Scraping, Meteostat API), poprzez zaawansowane czyszczenie i inżynierię cech (Feature Engineering), aż po budowę i ewaluację modelu predykcyjnego opartego na algorytmie **XGBoost**.

Ze względu na optymalizację pamięciową i czasową I/O, w całym projekcie zrezygnowano z plików CSV na rzecz binarnego, zorientowanego kolumnowo formatu **Apache Parquet**.

## 🛠 Wykorzystane technologie
* **Język:** Python 3.x
* **Przetwarzanie danych:** Pandas, NumPy
* **Machine Learning:** Scikit-learn (StandardScaler, train_test_split, metryki), XGBoost (XGBRegressor)
* **Akwizycja danych:** Kagglehub, Requests, BeautifulSoup4 (Web Scraping), Meteostat (API)
* **Wizualizacja:** Matplotlib, Seaborn
* **Zarządzanie plikami:** moduły systemowe `os`, `shutil`, `glob`

---

## 📂 Struktura plików i przepływ danych (Pipeline)

Projekt podzielony jest na 7 sekwencyjnych etapów (skryptów `.py`), które należy uruchamiać w określonej kolejności:

* **`01.py` - Akwizycja logów rowerowych (Kaggle)**
  Pobiera surowe pliki transakcyjne z Kaggle, łączy je w jedną główną tabelę, wymusza poprawne typowanie kluczy i usuwa szum informacyjny. Wynik jest zapisywany jako zoptymalizowany plik Parquet.

* **`02.py` - Walidacja temporalna**
  Sprawdza integralność pierwszego wymiaru macierzy, dokonuje wektoryzowanej konwersji ciągów znaków na format `datetime64[ns]` oraz loguje zakres czasowy zebranych danych.

* **`03.py` - Kontekst behawioralny (Web Scraping)**
  Eksploruje tabelaryczne dane kalendarza z portalu *Office Holidays* dla zadanych lat. Pobiera dni ustawowo wolne od pracy w stanie Illinois w celu wzbogacenia modelu o zjawiska społeczne.

* **`04.py` - Akwizycja i modelowanie zmiennych pogodowych**
  Łączy się z API `meteostat` (stacja Chicago O'Hare). Oblicza uśrednioną temperaturę i obsługuje braki danych stosując heurystykę imputacji (Forward Fill dla temperatur, wypełnianie zerami dla opadów).

* **`05.py` - Integracja i Inżynieria Cech (Master Dataset)**
  Najważniejszy etap transformacji. Agreguje logi do dziennych wolumenów wypożyczeń (zmienna objaśniana $Y$). Wykonuje połączenia tabel (Inner/Left Joins). Przeprowadza One-Hot Encoding dla dni tygodnia (z redukcją pułapki zmiennych fikcyjnych) oraz standaryzację (*Z-Score Scaling*) dla cech pogodowych.

* **`06.py` - Trening i Ewaluacja Modelu XGBoost**
  Dzieli dane na zbiory treningowe i testowe (80/20). Inicjalizuje lasy gradientowe (`XGBRegressor`) i generuje predykcję. Oblicza metryki **MAE** (Mean Absolute Error) oraz **R²** (Współczynnik Determinacji) i generuje wykres 10 najważniejszych cech decyzyjnych (Feature Importances).

* **`07.py` - Opisowa analiza regresyjna**
  Generuje wykresy warstwowe za pomocą biblioteki `seaborn`, obrazujące linie trendu (regresję liniową OLS z przedziałem ufności) pomiędzy warunkami atmosferycznymi a natężeniem ruchu rowerowego.

