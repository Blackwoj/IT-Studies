import random
import time
import numpy as np
import matplotlib.pyplot as plt
from math import sqrt
from scipy import stats

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

def rps():  # 1 - rock; 2 - paper; 3 - scissors
    player_1 = int(np.ceil(random_choice() * 3))
    player_2 = int(np.ceil(random_choice() * 3))
    if player_1 == 1:
        if player_2 == 1:
            return "Draw"
        elif player_2 == 2:
            return "Lose"
        else:
            return "Win"
    if player_1 == 2:
        if player_2 == 2:
            return "Draw"
        elif player_2 == 3:
            return "Lose"
        else:
            return "Win"
    if player_1 == 3:
        if player_2 == 3:
            return "Draw"
        elif player_2 == 1:
            return "Lose"
        else:
            return "Win"


def dice_game():
    player_1_1 = int(np.ceil(random_choice() * 6))
    player_1_2 = int(np.ceil(random_choice() * 6))
    player_2_1 = int(np.ceil(random_choice() * 6))
    player_2_2 = int(np.ceil(random_choice() * 6))
    result = player_1_1+ player_1_2 - player_2_1 - player_2_2
    return player_1_1+player_1_2,result
    # if result > 0:
    #     return "Win", result
    # elif result == 0:
    #     return "Draw", result
    # else:
    #     return "Lose", result


archery_target = {
    10: [0, 80],
    9: [80, 160],
    8: [160, 240],
    7: [240, 320],
    6: [320, 400],
    5: [400, 480],
    4: [480, 560],
    3: [560, 640],
    2: [640, 720],
    1: [720, 800],
    0: [800, 1300]
}


def archer_fight(n):  # odległości od 1 do 10 pkt co 8 cm
    player_1_points = 0
    global player_1_score_his
    player_2_points = 0
    global player_2_score_his
    shot_point = 0
    for i in range(n):
        player_1 = round(random_choice() * 1000, 2)
        shot_point = round(random_choice()*360, 2)
        player_2_x = round(random_choice() * 900, 2)
        player_2_y = round(random_choice() * 900, 2)
        player_2 = sqrt(player_2_x ** 2 + player_2_y ** 2)
        global archery_target
        for key in archery_target:
            if archery_target[key][0] <= player_1 < archery_target[key][1]:
                player_1_points += key
                # player_1_score_his.append(key)
            if archery_target[key][0] <= player_2 < archery_target[key][1]:
                player_2_points += key
                # player_2_score_his.append(key)
    return player_1_points - player_2_points


############# RPS ##################
score_p1 = []
for i in range(100):
    score_p1.append(rps())
order = {"Win":0, "Draw":1, "Lose":2}
score_p1.sort(key=lambda val:order[val])
data_to_his = np.asarray(score_p1)
plt.hist(data_to_his, bins=3)
plt.title("Wyniki 1 gracza gry KPN")
plt.xlabel("Wyniki")
plt.ylabel("Ilości rekordów")
plt.show()
unique = ['Win', 'Lose', 'Draw']
counted_score_p1 = {}
for i in unique:
    no = 0
    for j in score_p1:
        if i == j:
            no+=1
    counted_score_p1[i]=no
values_to_test = list(counted_score_p1.values())
print(stats.chisquare(values_to_test))
# H0 Jeden Gracz odnosi znaczne zwycięztwo
# Alpha 0,05
################ dice_game #####################
results_dice_roll = []
differences_dice_roll = []
for i in range(30):
    result = dice_game()
    results_dice_roll.append(result[0])
    differences_dice_roll.append(result[1])

plt.hist(results_dice_roll,bins=12, color="m", range=(1,12))
plt.title("Wynik 30 rzutów koścmi")
plt.xlabel("Wyniki")
plt.ylabel("Ilość rekordów")
plt.show()
differences_dice_roll.sort()
plt.hist(differences_dice_roll, bins=11, range=(-5,5), color="g")
plt.title("Różnice w wyniku rzutu kości")
plt.xlabel("Wartości")
plt.ylabel("Ilość Rekordów")
plt.show()

###################### Archery Fight ####################
A_fight_results = []
for i in range(20):
    if archer_fight(10)<0:
        A_fight_results.append("Player 2")
    elif archer_fight(10) > 0:
        A_fight_results.append("Player 1")
    else:
        A_fight_results.append("Draw")
order_archery = {"Player 1":0, "Draw":1, "Player 2":2}
A_fight_results.sort(key=lambda val:order_archery[val])
plt.hist(A_fight_results,bins = 3, color="y")
plt.title("Wyniki Walki Łuczników")
plt.xlabel("Wynik")
plt.ylabel("Ilość Rekordów")
plt.show()
