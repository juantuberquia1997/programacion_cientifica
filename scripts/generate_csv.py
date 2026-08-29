from pathlib import Path
from src.data_loader import cargar_partidos
from src.data_clean import parsear_tipos, depurar, derivar_resultado

base = Path("data/raw/football.json")
# en el repo descargado, la carpeta raiz es 'data/raw/2024-25/en.1.json'
# detectamos automaticamente la ruta si existe
possible = Path("data/raw/2024-25/en.1.json")
if possible.exists():
    df = cargar_partidos(Path('data/raw') / '2024-25' / 'en.1.json', temporada='2024-25')
else:
    # fallback: intentar cargar como repo clonado en data/raw/football.json/...
    df = cargar_partidos(Path('data/raw') / '2024-25' / 'en.1.json', temporada='2024-25')

print(f"Filas crudas: {df.shape[0]}")

df = parsear_tipos(df)
df = depurar(df)
df = derivar_resultado(df)

out = Path('data/processed')
out.mkdir(parents=True, exist_ok=True)
out_file = out / 'premier_2024_25_limpio.csv'
df.to_csv(out_file, index=False)
print(f"CSV generado: {out_file} ({df.shape[0]} filas)")
