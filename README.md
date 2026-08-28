# Dinamica del partido (ht vs ft) — Taller de Programacion Cientifica

**Curso:** Programacion Cientifica — ITM, 4 semestre
**Evaluacion:** 1 (20 %)
**Equipo:** [completar nombres + correo]
**Dataset:** `openfootball/football.json` (dominio publico)

---

## 1. Definicion del problema

En el futbol, el resultado al medio tiempo (ht) y el resultado al tiempo
completo (ft) no siempre coinciden. Un equipo puede ir ganando al descanso y
empatar o perder al final, o viceversa. Este proyecto estudia **la dinamica del
partido**: como se relacionan los goles y el resultado del medio tiempo con los
del tiempo completo.

Pregunta central: **¿el medio tiempo predice el tiempo completo?** y, en
particular, **¿con que frecuencia hay remontadas?**

## 2. Objetivos

1. Construir un dataset limpio y reproducible a partir de los JSON de
   openfootball (carga, parseo, depuracion).
2. Analizar la relacion goles ht vs goles ft mediante un scatter con regresion
   lineal.
3. Cuantificar el porcentaje de remontadas (equipo perdia en ht y gano en ft)
   por equipo.
4. Construir una matriz de confusion del resultado ht -> ft como heatmap.

## 3. Alcance

**Entra:**
- Liga inicial: Premier League 2024-25 (`2024-25/en.1.json`).
- Variables: date, time, team1, team2, score.ht, score.ft, round.
- Analisis descriptivo + regresion lineal simple + matriz de confusion.

**No entra (fuera de alcance):**
- Modelos predictivos avanzados (Poisson bivariado, clasificadores).
- xG, posesion, tiros, tarjetas, alineaciones (no estan en el dataset).
- Comparacion entre ligas (punto 6 del archivo de ideas).
- Series temporales multi-año (punto 7).

## 4. Dataset

| Campo | Detalle |
|---|---|
| Nombre | openfootball/football.json |
| Fuente | https://github.com/openfootball/football.json |
| Licencia | Dominio publico |
| Formato | JSON, un archivo por temporada + liga |
| Cobertura | Premier League, Bundesliga, La Liga, Serie A, Ligue 1 y mas; 2010-11 a 2025-26 |
| Archivo inicial | `2024-25/en.1.json` — 380 partidos, 14 campos |

**Campos por partido:** `date`, `time`, `team1` (local), `team2` (visitante),
`score.ht` [g1, g2] (medio tiempo), `score.ft` [g1, g2] (tiempo completo),
`round` (jornada).

## 5. Variables de interes

- `ht_g1`, `ht_g2`: goles local/visitante al medio tiempo.
- `ft_g1`, `ft_g2`: goles local/visitante al tiempo completo.
- `res_ht`, `res_ft`: resultado (Local/Empate/Visitante) en cada momento.
- `remontada`: indicador de que el perdedor del ht gano el ft.

## 6. Limitaciones conocidas del dato

- `score.ht` es `null` en ~4-9 % de los partidos (medio tiempo no registrado).
  Esos partidos se conservan pero se excluyen del scatter ht vs ft y del
  analisis de remontadas.
- `score.ft` es `null` en partidos pospuestos/no jugados. Se eliminan porque no
  aportan resultado final.
- No hay metricas avanzadas (xG, posesion). Todos los analisis se basan en
  goles y resultados.

## 7. Estructura del proyecto

```
.
├── README.md
├── requirements.txt
├── ESTADO_TRABAJO.md          # estado del trabajo y handoff 50/50
├── data/
│   ├── raw/                   # dataset original (ver data/raw/README.md)
│   └── processed/             # salidas de parseo/depuracion
├── notebooks/
│   ├── 01_carga_parseo_depuracion.ipynb
│   └── 02_analisis_dinamica_ht_vs_ft.ipynb
└── src/
    ├── __init__.py
    ├── data_loader.py         # lectura JSON -> DataFrame
    └── data_clean.py          # parseo, depuracion, auditoria
```

## 8. Como ejecutar

```bash
pip install -r requirements.txt
jupyter notebook
```

Abrir `notebooks/01_carga_parseo_depuracion.ipynb` y ejecutar de arriba a abajo.

> **Ruta del dataset:** el codigo apunta a
> `C:\Users\1234\Documents\ITM\4 semestre\programacion_cientifica\football.json`.
> Si se clona en otra maquina, ajustar `DATA_DIR` en la primera celda del notebook.

## 9. Division del trabajo (50/50)

Ver `ESTADO_TRABAJO.md` para el detalle de lo hecho y lo pendiente.

| Parte | Responsable | Estado |
|---|---|---|
| Estructura del proyecto | [yo] | Hecho |
| requirements.txt, .gitignore | [yo] | Hecho |
| README inicial (problema/objetivos/alcance) | [yo] | Hecho |
| src/data_loader.py | [yo] | Hecho |
| src/data_clean.py | [yo] | Hecho |
| Notebook 01 (carga/parseo/depuracion) | [yo] | Hecho |
| Scatter ht vs ft | [yo] | Hecho |
| Regresion lineal sobre el scatter | [companero] | Pendiente |
| % remontadas por equipo | [companero] | Pendiente |
| Matriz de confusion ht -> ft (heatmap) | [companero] | Pendiente |
| README final + Git Flow | [companero] | Pendiente |
