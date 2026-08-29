import urllib.request
from pathlib import Path

url = "https://raw.githubusercontent.com/openfootball/football.json/master/2024-25/en.1.json"
out = Path("data/raw/2024-25/en.1.json")
out.parent.mkdir(parents=True, exist_ok=True)
print(f"Descargando {url} -> {out}")
urllib.request.urlretrieve(url, out)
print("Descargado.")
