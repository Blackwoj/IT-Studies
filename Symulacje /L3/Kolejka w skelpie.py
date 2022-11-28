import time
import numpy as np
import queue

def random_choice():
    global x0
    a = 69069
    c = 5
    m = 2 ** 32
    X = (a * x0 + c) % m
    x0 = X
    Y = np.double(x0 / m)
    return Y


def poisson(freq = 1 ):
def expon(freq = 1 ):

que = queue.Queue()
service_time = 0
on_service = 0
que.put(1)
working_time=0
serviced_clients=0
open_time= 100
while open_time>0:
    open_time-=1
    Minute = 60
    working_time += 1
    new_client = np.random.poisson(0.1,1) #if new client came
    if new_client>0:
        while new_client>0:
            que.put(1)
            new_client-=1
    print(f"Actual que lenght:{que.qsize()}")
    print(f"Actual working time in minutes:{working_time}")
    print(f"Clients served:{serviced_clients}")
    print(f"Remaining service time:{service_time/60} ")
    while Minute >0:
        if not que.empty() and on_service == 0:
            service_time = int(np.random.exponential(8,1)*60)
            que.get()
            on_service=1
        if(service_time>0):
            service_time-=1
        Minute -=1
        if service_time == 0:
            on_service = 0
            serviced_clients +=1
    # time.sleep((2))