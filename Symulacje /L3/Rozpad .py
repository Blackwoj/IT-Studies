import math
import generators
import matplotlib.pyplot as plt
import numpy as np
import time

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

def rozpad(half_life: int | float) -> list[int]:
    _lambda = math.log(2) / half_life  # ln
    data: list[int] = []
    for i in range(10000):
        t = y = x = 0
        while not y < x:
            t = random_choice()* 51000
            x = _lambda * math.exp(-_lambda * t)
            y = random_choice()*_lambda
        data.append(t)
    return data


if __name__ == '__main__':
    hl = 5730
    dist = rozpad(hl)
    dist_normalized = [s * math.log(2) / hl for s in dist]
    bins_count = 100
    scaled_data = np.histogram(dist, bins=bins_count, density=True)
    counts, bins = scaled_data[1], (scaled_data[0] * hl / math.log(2))
    plt.bar(counts[:-1], bins, 51000 / bins_count)
    plt.ylabel('p-stwo')
    plt.xlabel('czas')
    plt.show()
    closest = min(zip(counts[:-1], bins), key=lambda x: abs(x[1] - 0.65))
    print(f'kot będzie żywy z p-stwem 0.65 po {closest[0]} latach')