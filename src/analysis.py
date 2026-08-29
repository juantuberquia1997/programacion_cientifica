"""Analisis post-procesado: regresion, remontadas por equipo y matriz de confusion.

Uso:
    python -m src.analysis

Requiere que exista `data/processed/premier_2024_25_limpio.csv`.
Si no existe, el script imprime instrucciones para regenerarlo (notebook 01).
"""
from __future__ import annotations
import os
from pathlib import Path
import sys
import textwrap

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import statsmodels.api as sm


ROOT = Path(__file__).resolve().parents[1]
PROCESSED = ROOT / "data" / "processed"
CSV_PATH = PROCESSED / "premier_2024_25_limpio.csv"


def load_clean_df(path: Path = CSV_PATH) -> pd.DataFrame:
    if not path.exists():
        raise FileNotFoundError(
            f"CSV limpio no encontrado: {path}\nEjecuta notebooks/01_carga_parseo_depuracion.ipynb para generarlo."
        )
    return pd.read_csv(path)


def regression_ht_ft(df: pd.DataFrame) -> sm.regression.linear_model.RegressionResults:
    df2 = df.dropna(subset=["ht_total", "ft_total"]).copy()
    X = sm.add_constant(df2["ht_total"])
    modelo = sm.OLS(df2["ft_total"], X).fit()
    # guardar figura
    plt.figure(figsize=(8, 6))
    sns.scatterplot(x="ht_total", y="ft_total", data=df2, alpha=0.6)
    xs = np.linspace(df2["ht_total"].min(), df2["ht_total"].max(), 100)
    ys = modelo.params["const"] + modelo.params["ht_total"] * xs
    plt.plot(xs, ys, color="red", label=f"reg: y={modelo.params['ht_total']:.3f}x+{modelo.params['const']:.3f}")
    plt.xlabel("Goles HT (total)")
    plt.ylabel("Goles FT (total)")
    plt.title("Scatter HT vs FT con recta de regresión")
    plt.legend()
    PROCESSED.mkdir(parents=True, exist_ok=True)
    out_fig = PROCESSED / "regression_ht_vs_ft.png"
    plt.tight_layout()
    plt.savefig(out_fig, dpi=150)
    plt.close()
    # guardar resumen
    out_txt = PROCESSED / "regression_summary.txt"
    out_txt.write_text(modelo.summary().as_text())
    return modelo


def remontadas_por_equipo(df: pd.DataFrame) -> pd.DataFrame:
    # Filtrar partidos con ht y ft
    df2 = df.dropna(subset=["res_ht", "res_ft"]).copy()
    # Definir ganador FT y quien perdia en HT
    # res_ht/res_ft codifican 'L' local, 'E' empate, 'V' visitante
    def ganador_ft(row):
        if row["res_ft"] == "L":
            return row["team1"]
        if row["res_ft"] == "V":
            return row["team2"]
        return None

    def perdedor_ht(row):
        if row["res_ht"] == "L":
            return row["team2"]
        if row["res_ht"] == "V":
            return row["team1"]
        return None

    df2["ganador_ft"] = df2.apply(ganador_ft, axis=1)
    df2["perdedor_ht"] = df2.apply(perdedor_ht, axis=1)
    # remontada a favor de X: ganador_ft == X and perdedor_ht == X
    remontadas_records = []
    for _, r in df2.iterrows():
        if pd.isna(r["ganador_ft"]) or pd.isna(r["perdedor_ht"]):
            continue
        if r["ganador_ft"] == r["perdedor_ht"]:
            remontadas_records.append({"team": r["ganador_ft"], "match_id": _})

    rem_df = pd.DataFrame(remontadas_records)
    # partidos con ht por equipo (a favor o en contra) -> contaremos por apariciones
    # Para % a favor usamos: remontadas_a_favor / partidos_con_ht
    equipos = pd.unique(df2[["team1", "team2"]].values.ravel())
    stats = []
    for team in equipos:
        partidos_con_ht = df2[(df2["team1"] == team) | (df2["team2"] == team)].shape[0]
        rem_a_favor = rem_df[rem_df["team"] == team].shape[0]
        pct = (rem_a_favor / partidos_con_ht * 100) if partidos_con_ht > 0 else 0.0
        stats.append({"team": team, "partidos_con_ht": partidos_con_ht, "remontadas_a_favor": rem_a_favor, "pct_remontadas": pct})

    stats_df = pd.DataFrame(stats).sort_values("pct_remontadas", ascending=False)
    # graficar top 15
    plt.figure(figsize=(10, 8))
    top = stats_df.head(15).sort_values("pct_remontadas")
    sns.barplot(x="pct_remontadas", y="team", data=top, palette="viridis")
    plt.xlabel("% Remontadas a favor")
    plt.ylabel("")
    plt.title("Top 15 equipos: % de remontadas a favor (con HT registrado)")
    plt.tight_layout()
    plt.savefig(PROCESSED / "remontadas_por_equipo.png", dpi=150)
    plt.close()
    stats_df.to_csv(PROCESSED / "remontadas_por_equipo.csv", index=False)
    return stats_df


def matriz_confusion(df: pd.DataFrame) -> pd.DataFrame:
    df2 = df.dropna(subset=["res_ht", "res_ft"]).copy()
    tabla = pd.crosstab(df2["res_ht"], df2["res_ft"], normalize="index")
    plt.figure(figsize=(6, 5))
    sns.heatmap(tabla, annot=True, fmt=".2f", cmap="Blues")
    plt.xlabel("Resultado FT")
    plt.ylabel("Resultado HT")
    plt.title("Matriz de confusión: res_ht -> res_ft (por fila)")
    plt.tight_layout()
    plt.savefig(PROCESSED / "matriz_confusion_ht_ft.png", dpi=150)
    plt.close()
    tabla.to_csv(PROCESSED / "matriz_confusion_ht_ft.csv")
    return tabla


def main():
    try:
        df = load_clean_df()
    except FileNotFoundError as e:
        print(str(e))
        print(textwrap.dedent(
            """
            Sugerencia:
              - Abrir `notebooks/01_carga_parseo_depuracion.ipynb` y ejecutar para generar
                `data/processed/premier_2024_25_limpio.csv`.
              - Alternativamente, exportar el CSV manualmente a `data/processed/`.
            """
        ))
        sys.exit(1)

    print("Ejecutando regresión HT -> FT ...")
    modelo = regression_ht_ft(df)
    print(modelo.summary())
    print("Calculando remontadas por equipo ...")
    stats_df = remontadas_por_equipo(df)
    print(stats_df.head(10).to_string(index=False))
    print("Generando matriz de confusión HT -> FT ...")
    tabla = matriz_confusion(df)
    print(tabla)


if __name__ == "__main__":
    main()
