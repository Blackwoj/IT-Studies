import numpy as np
import random

n = 1000 # ilosc produktów
B = 300 # rozmiar precaka
values = []
for i in range(n): values.append(random.normalvariate(3,0.16))
print(values)


