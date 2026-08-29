# data/raw — Dataset original

El dataset **no se duplica** en este repositorio. Se usa la copia local del repo
`openfootball/football.json`, que es de dominio publico.

## Ubicacion del dataset

```
C:\Users\1234\Documents\ITM\4 semestre\programacion_cientifica\football.json
```

## Estructura

Cada archivo es una temporada + liga, por ejemplo `2024-25/en.1.json`:

```json
{
  "name": "English Premier League 2024/25",
  "matches": [
    {
      "round": "Matchday 1",
      "date": "2024-08-16",
      "time": "20:00",
      "team1": "Manchester United FC",
      "team2": "Fulham FC",
      "score": { "ht": [0, 0], "ft": [1, 0] }
    }
  ]
}
```

## Campos

| Campo     | Tipo   | Significado                              |
|-----------|--------|------------------------------------------|
| `round`   | str    | Jornada (Matchday 1, Matchday 2, ...)    |
| `date`    | str    | Fecha ISO `YYYY-MM-DD`                   |
| `time`    | str    | Hora local `HH:MM`                       |
| `team1`   | str    | Equipo local                             |
| `team2`   | str    | Equipo visitante                         |
| `score.ht`| [int]  | Goles medio tiempo [local, visitante]    |
| `score.ft`| [int]  | Goles tiempo completo [local, visitante] |

## Notas de calidad (detectadas en la auditoria)

- `score.ht` puede ser `null` (medio tiempo no registrado) en ~4-9% de los partidos.
- `score.ft` puede ser `null` (partido pospuesto o no jugado).
- No incluye xG, posesion, tiros, tarjetas ni alineaciones.

## Fuente

- Repo: https://github.com/openfootball/football.json
- Licencia: dominio publico
