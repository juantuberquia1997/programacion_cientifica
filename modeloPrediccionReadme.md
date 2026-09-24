# Modelo de prediccion: medio tiempo -> resultado final

`notebooks/04_modelo_prediccion.ipynb`

## Problema y variables

Dado el marcador al medio tiempo, predecir el resultado final.

| Rol | Variable |
| --- | --- |
| X (predictoras) | `ht_g1`, `ht_g2` — goles local/visitante al descanso |
| y (objetivo) | `res_ft` — resultado final: L (local) / E (empate) / V (visitante) |

## Modelo

Regresion logistica multinomial (scikit-learn): sencillo, interpretable y
devuelve probabilidades por clase. Split train/test 75/25 estratificado,
`random_state=42`. 364 partidos con ht registrado.

## Resultados (test, 91 partidos)

| Modelo | Accuracy |
| --- | --- |
| Regresion logistica | **0.648** |
| Baseline "resultado no cambia" | 0.571 |
| Baseline clase mayoritaria | 0.429 |

- P(local gana | 1-0 al ht) = 0.62 (empirica exacta: 0.62); con 2-0 sube a 0.82.
- Ganar el primer tiempo es senal fuerte pero no determinante (~1 de cada 3
  lideres no gana).
- El modelo nunca predice empates: clase dificil en futbol.


## Ejecucion

```bash
jupyter lab
```

Abrir el notebook 04 y ejecutar todas las celdas. Genera
`data/processed/matriz_confusion_modelo.png`,
`data/processed/probabilidades_marcador_ht.png` y
`data/processed/probabilidades_escenarios_ht.csv`.
