from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA_RAW = ROOT / "data" / "raw"
DATA_PROCESSED = ROOT / "data" / "processed"
FIGURES = ROOT / "outputs" / "figures"

for directory in (DATA_RAW, DATA_PROCESSED, FIGURES):
    directory.mkdir(parents=True, exist_ok=True)

RIDES_MERGED = DATA_PROCESSED / "01_polaczone_dane_rowerowe.parquet"
RIDES_CLEAN = DATA_PROCESSED / "02_usuniete_dane_rowerowe.parquet"
HOLIDAYS = DATA_PROCESSED / "03_swieta_chicago.parquet"
WEATHER = DATA_PROCESSED / "04_pogoda_chicago.parquet"
MASTER = DATA_PROCESSED / "05_dane_znormalizowane.parquet"
