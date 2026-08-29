"""
data_clean.py — Parseo y depuracion del dataset de partidos.

Etapas del flujo: PARSEAR (tipo) -> DEPURAR (calidad).
No se imputa aqui; los faltantes se documentan y se deciden en el notebook.

Reglas de dominio aplicadas:
  - goles >= 0 (no pueden ser negativos)
  - ft_g1 >= ht_g1 y ft_g2 >= ht_g2 (el tiempo completo no puede tener
    menos goles que el medio tiempo)
  - date valida y parseada a datetime
  - team1 != team2 (un equipo no juega contra si mismo)
"""

from __future__ import annotations

import pandas as pd


def parsear_tipos(df: pd.DataFrame) -> pd.DataFrame:
    """
    Interpreta los valores crudos como tipos con semantica.

    - date -> datetime (formato ISO YYYY-MM-DD)
    - goles -> Int64 nullable (admite NaN reales del JSON)
    - time -> string normalizada
    - equipos -> string sin espacios laterales
    """
    df = df.copy()

    # Fechas: el dataset trae ISO, pero dejamos dayfirst=False explicito.
    df["date"] = pd.to_datetime(df["date"], errors="coerce", format="%Y-%m-%d")

    # Goles: a entero nullable. errors='coerce' vuelve NaN lo ilegible.
    for col in ["ht_g1", "ht_g2", "ft_g1", "ft_g2"]:
        df[col] = pd.to_numeric(df[col], errors="coerce").astype("Int64")

    # Texto: strip para evitar duplicados por espacios.
    for col in ["team1", "team2", "round", "league_name", "time"]:
        if col in df.columns:
            df[col] = df[col].astype("string").str.strip()

    return df


def auditoria(df: pd.DataFrame) -> pd.DataFrame:
    """
    Auditoria minima obligatoria del prototipo.

    Devuelve un DataFrame con: dtype, n_faltantes, pct_faltantes, n_unicos.
    Imprime ademas el conteo de duplicados.
    """
    reporte = pd.DataFrame({
        "dtype": df.dtypes.astype(str),
        "n_faltantes": df.isna().sum(),
        "pct_faltantes": (df.isna().mean() * 100).round(2),
        "n_unicos": df.nunique(dropna=False),
    })
    print("=== Auditoria por columna ===")
    print(reporte)
    print(f"\nFilas duplicadas (exactas): {df.duplicated().sum()}")
    return reporte


def marcar_inconsistencias(df: pd.DataFrame) -> pd.DataFrame:
    """
    Marca filas que rompen reglas de dominio. No las borra: las senala.

    Columnas booleanas anadidas:
      - imp_goles_neg: algun gol < 0
      - imp_ft_menor_ht: ft < ht en algun equipo
      - imp_mismo_equipo: team1 == team2
      - imp_fecha_invalida: date NaT (no se pudo parsear)
      - sin_ft: ft_g1 o ft_g2 faltante (partido sin resultado)
      - sin_ht: ht_g1 o ht_g2 faltante (medio tiempo no registrado)
    """
    df = df.copy()

    df["imp_goles_neg"] = (
        (df[["ht_g1", "ht_g2", "ft_g1", "ft_g2"]] < 0).any(axis=1)
    )
    # ft >= ht solo se puede evaluar donde ambos existen
    ambos = df["ht_g1"].notna() & df["ft_g1"].notna()
    df["imp_ft_menor_ht"] = False
    df.loc[ambos, "imp_ft_menor_ht"] = (
        (df.loc[ambos, "ft_g1"] < df.loc[ambos, "ht_g1"])
        | (df.loc[ambos, "ft_g2"] < df.loc[ambos, "ht_g2"])
    )
    df["imp_mismo_equipo"] = df["team1"].eq(df["team2"]) & df["team1"].notna()
    df["imp_fecha_invalida"] = df["date"].isna()
    df["sin_ft"] = df["ft_g1"].isna() | df["ft_g2"].isna()
    df["sin_ht"] = df["ht_g1"].isna() | df["ht_g2"].isna()

    return df


def depurar(df: pd.DataFrame, eliminar_sin_ft: bool = True) -> pd.DataFrame:
    """
    Aplica las decisiones de depuracion justificadas.

    Decisiones (documentadas en el README):
      1. Eliminar filas con ft faltante: un partido sin resultado final no
         aporta al analisis ht vs ft. Es informacion no recuperable.
      2. Conservar filas con ht faltante pero ft presente: el medio tiempo
         falta, pero el resultado final si sirve para otros analisis. Se
         excluyen del scatter ht vs ft pero no se borran del dataset.
      3. Eliminar filas con inconsistencias imposibles (goles negativos,
         ft < ht, mismo equipo): son errores de captura.
      4. Eliminar duplicados exactos.
    """
    df = marcar_inconsistencias(df)

    imposible = (
        df["imp_goles_neg"]
        | df["imp_ft_menor_ht"]
        | df["imp_mismo_equipo"]
    )
    n_imposible = imposible.sum()
    if n_imposible:
        print(f"[depurar] {n_imposible} fila(s) con inconsistencias imposibles -> eliminadas")

    df = df.loc[~imposible].copy()

    if eliminar_sin_ft:
        n_sin_ft = df["sin_ft"].sum()
        if n_sin_ft:
            print(f"[depurar] {n_sin_ft} fila(s) sin resultado final (ft) -> eliminadas")
        df = df.loc[~df["sin_ft"]].copy()

    # Duplicados exactos
    n_dup = df.duplicated().sum()
    if n_dup:
        print(f"[depurar] {n_dup} fila(s) duplicada(s) exacta(s) -> eliminadas")
    df = df.drop_duplicates(keep="first").copy()

    return df.reset_index(drop=True)


def derivar_resultado(df: pd.DataFrame) -> pd.DataFrame:
    """
    Anade columnas derivadas utiles para el analisis del punto 5:
      - ht_total, ft_total: goles totales del partido
      - res_ht: resultado al medio tiempo ('L' local, 'E' empate, 'V' visitante)
      - res_ft: resultado al tiempo completo
      - remontada: el perdedor del ht gano el ft (solo donde ht existe)
    """
    df = df.copy()
    df["ht_total"] = df["ht_g1"] + df["ht_g2"]
    df["ft_total"] = df["ft_g1"] + df["ft_g2"]

    def _res(g1, g2):
        if pd.isna(g1) or pd.isna(g2):
            return pd.NA
        if g1 > g2:
            return "L"
        if g1 < g2:
            return "V"
        return "E"

    df["res_ht"] = df.apply(lambda r: _res(r["ht_g1"], r["ht_g2"]), axis=1)
    df["res_ft"] = df.apply(lambda r: _res(r["ft_g1"], r["ft_g2"]), axis=1)

    # Remontada: iba perdiendo en ht y gano en ft
    df["remontada"] = (
        ((df["res_ht"] == "V") & (df["res_ft"] == "L"))  # perdia local, gano local
        | ((df["res_ht"] == "L") & (df["res_ft"] == "V"))  # perdia visita, gano visita
    ).astype("boolean")  # nullable bool: admite pd.NA donde no hay ht
    # Donde no hay ht, no se puede evaluar remontada
    df.loc[df["res_ht"].isna(), "remontada"] = pd.NA

    return df


if __name__ == "__main__":
    from pathlib import Path
    from data_loader import cargar_partidos

    base = Path(r"C:\Users\1234\Documents\ITM\4 semestre\programacion_cientifica\football.json")
    df = cargar_partidos(base / "2024-25" / "en.1.json")
    df = parsear_tipos(df)
    print("\n--- Antes de depurar ---")
    print(df.shape)
    auditoria(df)
    df_limpio = depurar(df)
    df_limpio = derivar_resultado(df_limpio)
    print("\n--- Despues de depurar ---")
    print(df_limpio.shape)
    print(df_limpio[["team1", "team2", "ht_g1", "ht_g2", "ft_g1", "ft_g2",
                     "res_ht", "res_ft", "remontada"]].head(5))
