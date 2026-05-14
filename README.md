# 🚲 Chicago Divvy Bikes: Przewidywanie Popytu (Machine Learning)

## 📌 O projekcie
Projekt ten to kompletny rurociąg danych (Data Pipeline) oraz model uczenia maszynowego (Machine Learning) stworzony w celu przewidywania dziennej liczby wypożyczeń rowerów miejskich w Chicago. Algorytm analizuje warunki pogodowe (temperaturę, opady) oraz specyfikę dnia (np. weekend), aby oszacować zapotrzebowanie na rowery.

W ramach projektu przetworzono **ponad 12 milionów** pojedynczych rekordów przejazdów z lat 2020-2022, łącząc je z historycznymi danymi meteorologicznymi.

## 🛠 Technologie i Biblioteki
* **Język:** Python 3
* **Przetwarzanie danych:** `pandas`, `pyarrow` (format Parquet)
* **Wizualizacja:** `matplotlib`, `seaborn`
* **Machine Learning:** `scikit-learn` (StandardScaler, podział danych), `xgboost` (XGBRegressor)

## 📊 Źródła Danych
Z uwagi na rozmiar (wiele gigabajtów), surowe dane nie znajdują się w tym repozytorium. Aby odtworzyć projekt, należy pobrać:
1. **Dane rowerowe:** Historyczne przejazdy systemu Divvy (dostępne np. na Kaggle lub oficjalnej stronie miasta Chicago).
2. **Dane pogodowe:** Pobierane z darmowego archiwum API **Open-Meteo** (temperatura, opady deszczu).

## 🚀 Architektura Rozwiązania (Rurociąg Danych)
1. **Agregacja:** Zmniejszenie 12 milionów wierszy do formatu dziennego.
2. **Czyszczenie (Preprocessing):** Usunięcie wartości odstających (outlierów), obsługa braków danych.
3. **Inżynieria Cech (Feature Engineering):** Wydobycie dni tygodnia i miesięcy za pomocą One-Hot Encodingu.
4. **Skalowanie:** Standaryzacja zmiennych pogodowych za pomocą `StandardScaler`.
5. **Modelowanie:** Wytrenowanie algorytmu **XGBoost Regressor** na 80% danych i testowanie na 20%.

## 📈 Wyniki Modelu
Nasz model osiągnął bardzo zadowalające wyniki, udowadniając, że pogoda jest głównym czynnikiem determinującym ruch rowerowy w mieście:
* **R² (Współczynnik determinacji):** `0.72` (Model wyjaśnia 69% zmienności w danych)
* **MAE (Średni błąd bezwzględny):** `~3485` (Przy maksymalnym dziennym ruchu wynoszącym ponad 25 000 rowerów).

**Najważniejsze cechy (Feature Importance):**
Badanie wykazało, że kluczowy wpływ na liczbę wypożyczeń mają:
1. Temperatura (im cieplej, tym więcej wypożyczeń).
2. Opady deszczu (nawet mały deszcz drastycznie obniża popyt).
3. Dni weekendowe (np. Sobota).

## 👨‍💻 Autor
* Projekt zaliczeniowy / Portfolio Data Science - 2026
