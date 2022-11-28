import random
import time
import numpy as np
from math import sqrt
from random import choice
x0 = round(time.time() * 1000)


def random_choice():
    global x0
    a = 69069
    c = 5
    m = 2 ** 32
    X = (a * x0 + c) % m
    x0 = X
    Y = np.double(x0 / m)
    return Y

cups = [1000, 10, 2000, 1, 5000, 1, 2000, 10, 1000]
enter_pots = [1, 2, 3, 4, 5]
enter_pot = -1
# while enter_pot not in enter_pots:
#     try :
#         enter_pot = int(input("W którym kubku chcesz zaczać: 1,2,3,4,5"))
#         if enter_pot not in enter_pots:
#             print("Podałeś zły kubek, mozliwe kubki to: 1,2,3,4 lub 5!")
#     except: print("Podaj prawidłową wartość")

game_wall =[]
rows, cols=5,8
for i in range(rows):
    col = []
    for j in range(cols):
        col.append(0)
    game_wall.append(col)

################ ZAD 1
# print("ZAD 1")
# act_pot = enter_pot+3
# for i in range(rows-1):
#     site = random.choice([1,2])
#     if site == 1:
#         act_pot -=1

############### ZAD 2
print("ZAD 2")
mean_win = 0
for i in range(1000):
    act_pot = 6
    for i in range(rows - 1):
        site = random.choice([1, 2])
        if site == 1:
            act_pot -= 1
    mean_win += int(cups[act_pot])
print(mean_win/1000)

########### ZAD 3
print("ZAD 3")
value_for_pots = [0,0,0,0,0]
for i in enter_pots:
    mean_win = 0
    for j in range(1000):
        act_pot = i+3
        for k in range(rows - 1):
            site = random.choice([1, 2])
            if site == 1:
                act_pot -= 1
        mean_win += int(cups[act_pot])
    value_for_pots[i-1] = mean_win / 1000
print(value_for_pots)

################ ZAD 4
print("ZAD 4")
cups = [1000, 10, 2000, 1, 500, 1, 2000, 10, 1000]
value_for_pots = [0,0,0,0,0]
for i in enter_pots:
    mean_win = 0
    for j in range(1000):
        act_pot = i+3
        for k in range(rows - 1):
            site = random.choice([1, 2])
            if site == 1:
                act_pot -= 1
        mean_win += int(cups[act_pot])
    value_for_pots[i-1] = mean_win / 1000
print(value_for_pots)

#     .4.5.6.7.8.
#    .3.4.5.6.7.8.
#   .2.3.4.5.6.7.8.
#  .1.2.3.4.5.6.7.8.
# .0.1.2.3.4.5.6.7.8.
# |_|_|_|_|_|_|_|_|_|
