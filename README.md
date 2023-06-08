# Practica1: merge concurrente

1. Motivación

El objetivo es implementar un merge concurrente que tome números producidos por varios procesos y los almacene de forma creciente en una única lista. Nos aseguraremos de que se cumplan las condiciones de exclusión mutua y que los números sean introducidos en orden creciente.

2. Descripción

El problema consiste en tener NPROD procesos productores que generan números no negativos de forma creciente. Cada proceso almacena el valor producido en una variable compartida con el consumidor, utilizando semáforos para controlar el acceso. Un valor de -1 indica que el proceso ha terminado de producir y un valor de -2 indica que el almacén está vacío.

El proceso merge actúa como consumidor y debe esperar a que los productores tengan listo un elemento e introducir el menor de ellos en una lista o array compartido. El proceso merge maneja todos los semáforos para garantizar la exclusión mutua y el ordenamiento creciente de los números.

Además, se incluye una modificación en la que se tiene un buffer de tamaño fijo para que los productores almacenen valores antes de ser consumidos por el merge.

3. Modo de uso

Se requiere el módulo multiprocessing de Python para ejecutar el programa.

Es posible ajustar los valores de las constantes N, K y NPROD para probar diferentes configuraciones del problema. Estos valores controlan el número de elementos producidos, la capacidad del buffer y el número de productores respectivamente.

Al ejecutar el programa, se generará la salida que muestra el proceso de producción y consumo de números por parte de los productores y el merge. Se pueden revisar los resultados y verificar que los números son almacenados de forma creciente en la lista compartida.
