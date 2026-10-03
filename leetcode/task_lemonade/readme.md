![Accepted — Lemonade Change](screen/Captura_1.png)
![Accepted — Lemonade Change](screen/Captura_2.png)

url task leetcode : https://leetcode.com/problems/lemonade-change/

# Lemonade Change (Greedy)

Cada vaso cuesta 5; los clientes pagan con billetes de 5, 10 o 20 en orden. El cambio se da solo con los billetes ya recibidos. Decidir si se puede atender a todos.

**¿Que es greedy?** Elegir en cada paso la mejor opcion local sin deshacer decisiones: al recibir un 20 conviene dar `10 + 5` y no `5 + 5 + 5`, porque el billete de 5 es mas util (sirve para dar cambio de 10 y de 20) y hay que reservarlo. Si en algun momento no hay cambio exacto, la respuesta es `false`. El billete de 20 nunca se cuenta: no hay vuelto de 25.

**Complejidad:** O(n) tiempo (una pasada por los clientes) y O(1) espacio (dos contadores: `billFive` y `billTen`).