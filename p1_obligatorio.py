"""
Prática 1: Programación concurrente (parte obligatoria). De: Celeste Rhodes Rodríguez.\
"""
from multiprocessing import Process
from multiprocessing import BoundedSemaphore, Semaphore, Lock
from multiprocessing import current_process
from multiprocessing import Value, Array
from time import sleep
from random import random, randint


N = 20 #cantidad de n\'fameros que producen los productores
NPROD = 5 #n\'famero de productores

def delay(factor = 3):
    sleep(random()/factor)


def producer( index1, non_empty):
    aux=0
    for v in range(N):
        num_aux=randint(aux,aux+10)
        print (f"producer {current_process().name} produciendo")
        delay(6)
        index1.value=num_aux
        aux=num_aux
        non_empty.release()
        print (f"producer {current_process().name} almacenado {v}")
        #print(index1.value)
    print (f"producer {current_process().name} finalizando")
    delay(6)
    index1.value=-1
    non_empty.release()
    print (f"producer {current_process().name} finalizado")
    
    
def consumer(index1, consumer_list, non_empty):
    for i in range(NPROD):
        non_empty[i].acquire() #espera a que todos hayan producido
    for v in range(N*NPROD):
        l=[index1[k] for k in range(NPROD)]
        if l!=[-1 for k in range(NPROD)]:
            min_val = float('inf')
            for j in range(NPROD):
                if index1[j] < min_val and index1[j]>=0:
                    min_val = index1[j]
                    index=j
            print (f"consumer desalmacenando")
            dato =index1[index]
            consumer_list.append(dato)
        non_empty[index].acquire()
        print (f"consumer consumiendo {v}")
            #print(consumer_list)
        delay()

def main():
    index1 = [Value('i', 0) for i in range(NPROD)] #cada index1 se corresponde con el objeto compartido entre un productor y el consumidor
    consumer_list=[]
    for i in range(NPROD):
        index1[i].value = -2

    """
    Es un problema en el que hay NPROD productores, necesitamos tener un semaforo por cada consumidor.
    Haremos una lista de semaforos por cada semaforo necesario
    """
  
    non_empty = [BoundedSemaphore(0) for i in range(NPROD)] 

    prodlst = [ Process(target=producer,
                        name=f'prod_{i}',
                        args=(index1[i], non_empty[i]))
                for i in range(NPROD) ] #lista de procesos productores
  
    merge = Process(target=consumer, name=f'consumer', args=(index1, consumer_list, non_empty)) #proceso merge, para consumidor
    
    for p in prodlst + [merge]:
        p.start()

    for p in prodlst +[merge]:
        p.join()

if __name__ == '__main__':
    main()