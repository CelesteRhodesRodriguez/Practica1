#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Feb 23 13:37:32 2023

@author: alumno
"""

from multiprocessing import Process
from multiprocessing import BoundedSemaphore, Semaphore, Lock
from multiprocessing import current_process
from multiprocessing import Value, Array
from time import sleep
from random import random, randint


N = 20 #cantidad de números que producen los productores
K = 10 #capacidad de los buffer
NPROD = 5 #número de productores

def delay(factor = 3):
    sleep(random()/factor)


def add_data(storage, index, pid, data, mutex):
    mutex.acquire()
    try:
        storage[index.value] = data
        delay(6)
        index.value = index.value + 1
    finally:
        mutex.release()


def get_data(storage, index, mutex):
    mutex.acquire()
    try:
        data = storage[0]
        index.value = index.value - 1
        delay()
        for i in range(index.value):
            storage[i] = storage[i + 1]
        storage[index.value] = -1
    finally:
        mutex.release()
    return data


def producer(storage, index1, empty, non_empty, mutex):
    aux=0
    for v in range(N):
        num_aux=randint(aux,aux+10)
        print (f"producer {current_process().name} produciendo")
        delay(6)
        empty.acquire()
        add_data(storage, index1, int(current_process().name.split('_')[1]),
                 num_aux, mutex)
        aux=num_aux
        non_empty.release()
        print (f"producer {current_process().name} almacenado {v}")
        #print(storage[:],index1.value)
    print (f"producer {current_process().name} finalizando")
    delay(6)
    empty.acquire()
    add_data(storage, index1, int(current_process().name.split('_')[1]),
                 -1, mutex)
    non_empty.release()
    print (f"producer {current_process().name} finalizado")
    
    
def consumer(storage, index1, consumer_list, empty, non_empty, mutex):
    for i in range(NPROD):
        non_empty[i].acquire()
    for v in range(N*NPROD):
        l=[storage[k][0] for k in range(NPROD)]
        if l!=[-1 for k in range(NPROD)]:
            min_val = float('inf')
            for j in range(NPROD):
                if storage[j][0] < min_val and storage[j][0]>=0:
                    min_val = storage[j][0]
                    index=j
            non_empty[index].acquire()
            print (f"consumer desalmacenando")
            dato =get_data(storage[index], index1[index], mutex[index])
            empty[index].release()
            consumer_list.append(dato)
            print (f"consumer consumiendo {v}")
            #print(consumer_list)
            delay()

def main():
    storagelst = [Array('i', K) for i in range(NPROD)] #k es la capacidad del buffer y tenemos NPROD buffers, uno para cada productor
    index1 = [Value('i', 0) for i in range(NPROD)] #index1 para dentro de cada buffer indicar cual es el siguiente hueco vacío/cual es el ult elem
    consumer_list=[]
    for i in range(NPROD): 
        for k in range(K):
            storagelst[i][k] = -2
        print ("almacen inicial", storagelst[i][:], "indice", index1[i].value)

    """
    Es un problema en el que hay NPROD productores, necesitamos tener un semaforo por cada consumidor.
    Haremos una lista de semaforos por cada semaforo necesario
    """
  
    non_empty = [Semaphore(0) for i in range(NPROD)] #dice si está vacío.
    empty = [BoundedSemaphore(K) for i in range(NPROD)] #representa el numero de huecos en el buffer. -1 cuando añades(wait), +1 cuando quitas(signal), 0 completo(no te dejo pasar)
    mutex = [Lock() for i in range(NPROD)] #para add_data y get_data

    prodlst = [ Process(target=producer,
                        name=f'prod_{i}',
                        args=(storagelst[i], index1[i],  empty[i], non_empty[i], mutex[i]))
                for i in range(NPROD) ] #lista de procesos productores
  
    merge = Process(target=consumer, name=f'consumer', args=(storagelst, index1, consumer_list, empty, non_empty, mutex)) #proceso merge, para consumidor
    
    for p in prodlst + [merge]:
        p.start()

    for p in prodlst +[merge]:
        p.join()

if __name__ == '__main__':
    main()