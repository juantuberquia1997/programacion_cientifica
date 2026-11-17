# Taller de grafos — Problema 4.8 · La calle cerrada

En esta carpeta está la entrega del taller de grafos del periodo 2026-2. Es un solo archivo, `index.html`, que se abre con doble clic: no hay que instalar nada ni tener internet.

## url video exposicion:
https://www.veed.io/view/8d8b4759-b350-4af7-8f9e-d2f814a254bc?source=Dashboard&panel=share

## Qué cuenta el archivo

Es la exposición de un problema propio sobre un barrio imaginario de 10 esquinas unidas por 11 calles. Todas las calles cuestan 1. La pregunta del problema es:

> ¿Cuántas calles hay que recorrer de la Casa a la Estación con la red completa, y qué pasa cuando se cierra la calle del Puente a la Estación?

La respuesta se encuentra con BFS (el algoritmo que avanza por olas con una cola) corrido dos veces:

- **Con la red completa:** 4 calles — Casa → Iglesia → Cafetería → Puente → Estación.
- **Con la calle Puente–Estación cerrada:** 5 calles — Casa → Iglesia → Cafetería → Biblioteca → Plaza → Estación.

El mínimo subió porque todas las rutas de 4 calles pasaban por la calle que se cerró.

## Cómo se navega

- **Flechas ← →** (o los botones de abajo): cambiar de diapositiva.
- En los dos laboratorios: **N** y **P** avanzan o retroceden el algoritmo paso a paso, y la **barra espaciadora** lo reproduce.
- También sirven los botones de la barra inferior: reiniciar, anterior, siguiente, reproducir y ver el cierre.

## Para grabar el video (4 a 6 minutos)

El video se graba mostrando este archivo en el navegador y explicando en voz alta, en este orden:

1. Nombre, número del problema (4.8) y la pregunta en una oración.
2. El grafo: las 10 esquinas y su lista de vecinos.
3. El primer laboratorio avanzando, señalando la cola y los números de calles.
4. El cierre de la calle Puente–Estación.
5. El segundo laboratorio avanzando y la nueva respuesta.
6. El antes y el después: las dos rutas y por qué son distintas.

