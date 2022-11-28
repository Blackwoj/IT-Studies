import numpy as np
import math

def go():
    s = int(input("szczaly"))
    xk = float(input("xk(koniec calkowania)= "))
    xp = float(input("xp(poczatek calkowania)= "))
    xp, xk = sorted([xp, xk])
    print(mc(s, xk, xp))


def f(x):
    return math.exp(((-x**2)/2))

def mc(s, xk, xp):
    traf = 0
    dx = np.abs(xk - xp)
    for i in range(s):
        x = xp + np.random.random() * (abs(xp - xk))
        traf += f(x)
    wynik = dx * traf / s
    return wynik

go()
