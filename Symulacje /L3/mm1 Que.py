import numpy as np
import math
import time
import matplotlib.pyplot as plt
import random
x0 = round(time.time() * 1000)

def random_uni():
    global x0
    a = 69069
    c = 5
    m = 2 ** 32
    X = (a * x0 + c) % m
    x0 = X
    Y = np.double(x0 / m)
    return Y

def expr(_lambda):
    return -math.log(random_uni())/_lambda

n =100000
service = []
for i in range(n): service.append(expr(0.125)) # srednio 8 min to Beta a do expr dajemy lambde
arrival = []
arrival.append(0)
for i in range(1,n): arrival.append(arrival[i-1] + expr(0.1))
#
# print(f"czas obsługi{service}")
# print(f"czas przyjscia{arrival }")
enter_service_time,leave_service_time=[],[]
for i in range(n):
    enter_service_time.append(i)
    leave_service_time.append(i)

leave_service_time[0]=service[0]
for i in range(1,n):
    if leave_service_time[i-1]<arrival[i]:enter_service_time[i]=arrival[i]
    else: enter_service_time[i] = leave_service_time[i-1]
    leave_service_time[i] = enter_service_time[i]+service[i]
waiting_time = 0
for i in range(n):
    waiting_time+= enter_service_time[i]-arrival[i]
mean_waitning_time = waiting_time/n
for i in range(n):
    print(f"kilen:{i+1}")
    print(f"Czas przyjscia: {arrival[i]}")
    print(f"Czasy wejscia: {enter_service_time[i]}")
    print(f"Czasy wyjścia: {leave_service_time[i]}")
    print(f"Czasy czas oczekiwania: {enter_service_time[i]-arrival[i]}")


round_service_time = []
round_arrival_time =[]
for i in range(n):
    round_service_time.append(round(service[i],1))
for i in range(1,n):
    round_arrival_time.append(round(arrival[i]-arrival[i-1],1))

bins_count = 500
plt.hist(round_service_time, bins=bins_count)
plt.title("Histogram serwisu")
plt.xlabel("Czas serwisu")
plt.ylabel("Ilośc rekordów")
plt.show()

bins_count = 200
plt.hist(round_arrival_time, bins=bins_count)
plt.title("Histogram przychodznia nowych klientów ")
plt.xlabel("Różnice w przyjściach")
plt.ylabel("Ilośc rekordów")
plt.show()

print(f"\nŚrednia czas oczekiwania: {mean_waitning_time}")
