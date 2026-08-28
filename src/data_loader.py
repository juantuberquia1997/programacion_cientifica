"""
data_loader.py — Lectura del dataset football.json (openfootball).

Etapa del flujo: LEER (I/O).
Responsabilidad: llevar el JSON crudo a un DataFrame plano, sin inventar valores.
No parsea tipos ni depura; eso va en data_clean.py.
"""

from __future__ import annotations

import json
import re
from pathlib import Path

import pandas as pd

# Mapeo de codigo de pais/liga -> nombre legible.
# Se infiere del nombre del archivo (ej. "en.1" -> Inglaterra 1ra division).
CODIGOS_LIGA = {
    "en": "Inglaterra",
    "es": "Espana",
    "de": "Alemania",
    "it": "Italia",
    "fr": "Francia",
    "pt": "Portugal",
    "nl": "Paises Bajos",
    "at": "Austria",
    "br": "Brasil",
    "jp": "Japon",
    "cn": "China",
    "tr": "Turquia",
    "sco": "Escocia",
    "mx": "Mexico",
    "be": "Belgica",
    "gr": "Grecia",
    "uefa": "UEFA",
}


def _extraer_codigo_liga(nombre_archivo: str) -> str:
    """Devuelve el codigo de liga desde un nombre como 'en.1.json' -> 'en'."""
    base = Path(nombre_archivo).stem  # 'en.1'
    partes = base.split(".")
    return partes[0] if partes else "desconocido"


def _extraer_division(nombre_archivo: str) -> int | None:
    """Devuelve la division desde 'en.1.json' -> 1, 'en.2.json' -> 2."""
    base = Path(nombre_archivo).stem
    partes = base.split(".")
    if len(partes) > 1 and partes[1].isdigit():
        return int(partes[1])
    return None


def cargar_partidos(ruta_json: str | Path, temporada: str | None = None) -> pd.DataFrame:
    """
    Carga un archivo JSON de football.json y devuelve un DataFrame plano.

    Parametros
    ----------
    ruta_json : str | Path
        Ruta al archivo, ej. '.../2024-25/en.1.json'.
    temporada : str | None
        Etiqueta de temporada (ej. '2024-25'). Si es None se intenta inferir
        del directorio padre del archivo.

    Returns
    -------
    pd.DataFrame con columnas:
        date, time, team1, team2, ht_g1, ht_g2, ft_g1, ft_g2, round,
        league_name, league_code, division, season, source_file

    Notas
    -----
    - ht_g1/ht_g2 y ft_g1/ft_g2 quedan como float cuando el JSON trae null
      (medio tiempo no registrado o partido pospuesto). No se imputan aqui;
      se documentan como faltantes reales y se tratan en data_clean.py.
    """
    ruta = Path(ruta_json)
    with open(ruta, encoding="utf-8") as f:
        data = json.load(f)

    matches = data.get("matches", [])
    league_name = data.get("name", "")
    nombre_archivo = ruta.name
    league_code = _extraer_codigo_liga(nombre_archivo)
    division = _extraer_division(nombre_archivo)

    if temporada is None:
        # El directorio padre suele ser la temporada: '2024-25'
        temporada = ruta.parent.name

    filas = []
    for m in matches:
        score = m.get("score") or {}
        ht = score.get("ht")  # [g1, g2] o None
        ft = score.get("ft")  # [g1, g2] o None
        filas.append({
            "date": m.get("date"),
            "time": m.get("time"),
            "team1": m.get("team1"),
            "team2": m.get("team2"),
            "round": m.get("round"),
            "ht_g1": ht[0] if ht is not None else None,
            "ht_g2": ht[1] if ht is not None else None,
            "ft_g1": ft[0] if ft is not None else None,
            "ft_g2": ft[1] if ft is not None else None,
            "league_name": league_name,
            "league_code": league_code,
            "division": division,
            "season": temporada,
            "source_file": nombre_archivo,
        })

    df = pd.DataFrame(filas)
    return df


def cargar_multiples(
    base_dir: str | Path,
    temporadas: list[str],
    ligas: list[str],
) -> pd.DataFrame:
    """
    Carga y concatena varias temporadas/ligas en un solo DataFrame.

    Parametros
    ----------
    base_dir : str | Path
        Directorio raiz del repo football.json.
    temporadas : list[str]
        Ej. ['2024-25', '2023-24'].
    ligas : list[str]
        Codigos de archivo sin extension, ej. ['en.1', 'es.1'].

    Returns
    -------
    pd.DataFrame concatenado con columna 'source_file' para trazabilidad.
    """
    base = Path(base_dir)
    frames = []
    for temp in temporadas:
        for liga in ligas:
            ruta = base / temp / f"{liga}.json"
            if not ruta.exists():
                print(f"[aviso] no existe: {ruta}")
                continue
            frames.append(cargar_partidos(ruta, temporada=temp))
    if not frames:
        return pd.DataFrame()
    return pd.concat(frames, ignore_index=True)


if __name__ == "__main__":
    # Smoke test rapido
    import sys
    base = r"C:\Users\1234\Documents\ITM\4 semestre\programacion_cientifica\football.json"
    df = cargar_partidos(Path(base) / "2024-25" / "en.1.json")
    print(df.shape)
    print(df.dtypes)
    print(df.head(3))
