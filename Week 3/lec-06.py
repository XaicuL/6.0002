import random

class FairRoulette():
    def __init__(self):
        self.pockets = []

        for i in range(1,37):
            self.pockets.append(i)

        self.ball = None
        self.pocketOdds = len(self.pockets) - 1

    def spin(self):
        self.ball = random.choice(self.pockets)

    def betPocket(self, pocket, amt):
        if str(pocket) == str(self.ball):
            return amt*self.pocketOdds
        else:
            return -amt

    def __str__(self):
        return 'Fair Roulette'

    def playRoulette(game, numspins, pocket, bet):
        totPocket = 0

        for i in range(numspins):
            game.spin()
            totPocket += game.betPocket(pocket, bet)

        if toPrint:
            print(f"{numspins} spins of {game}")
            print(f"Expected return betting {pocket} = {str(100*totPocket/numspins)} ")

        return (totPocket/numspins)

game = FairRoulette()

for numSpins in (100, 1000000):
    for i in range(3):
        playRoulette(game, numSpins, 2,1 , True)

import random
import numpy as np
import matplotlib.pyplot as plt
import scipy.integrate

def roll_die():
    return random.choice([1,2,3,4,5,6])

def roll_n(n):
    result = ''
    for i in range(n):
        result = result + str(roll_die())

    print(result)

# roll_n(10)

def flip(num_flips):
    heads = 0
    for i in range(num_flips):
        if random.choice(('H', 'T')) == 'H':
            heads += 1

    return heads/num_flips

def flip_sim(num_flips_per_trial, num_trials):
    frac_heads = []
    for i in range(num_trials):
        frac_heads.append(flip(num_flips_per_trial))

    mean = sum(frac_heads)/len(frac_heads)
    return mean

flip_sim(10,1)
print(f"Mean = {flip_sim(10,1)}")

import random

# # Figure 17-3 from page 350
def regress_to_mean(num_flips, num_trials):
    #Get fraction of heads for each trial of num_flips
    frac_heads = []
    for t in range(num_trials):
        frac_heads.append(flip(num_flips))
    #Find trials with extreme results and for each the next trial
    extremes, next_trials = [], []
    for i in range(len(frac_heads) - 1):
        if frac_heads[i] < 0.33 or frac_heads[i] > 0.66:
            extremes.append(frac_heads[i])
            next_trials.append(frac_heads[i+1])
    #Plot results
    plt.plot(range(len(extremes)), extremes, 'ko',
               label = 'Extreme')
    plt.plot(range(len(next_trials)), next_trials, 'k^',
               label = 'Next Trial')
    plt.axhline(0.5)
    plt.ylim(0, 1)
    plt.xlim(-1, len(extremes) + 1)
    plt.xlabel('Extreme Example and Next Trial')
    plt.ylabel('Fraction Heads')
    plt.title('Regression to the Mean')
    plt.legend(loc = 'best')

random.seed(0)
regress_to_mean(15, 50)

# # Figure 17-5 from page 352
def flip_plot(min_exp, max_exp):
    """Assumes min_exp and max_exp positive ints; min_exp < max_exp
       Plots results of 2**min_exp to 2**max_exp coin flips"""
    ratios, diffs, x_axis = [], [], []
    for exp in range(min_exp, max_exp + 1):
        x_axis.append(2**exp)
    for num_flips in x_axis:
        num_heads = 0
        for n in range(num_flips):
            if random.choice(('H', 'T')) == 'H':
                num_heads += 1
        num_tails = num_flips - num_heads
        try:
            ratios.append(num_heads/num_tails)
            diffs.append(abs(num_heads - num_tails))
        except ZeroDivisionError:
            continue
    plt.title('Difference Between Heads and Tails')
    plt.xlabel('Number of Flips')
    plt.ylabel('Abs(#Heads - #Tails)')
    plt.xticks(rotation = 'vertical')
    plt.plot(x_axis, diffs, 'k')
    plt.figure()
    plt.title('Heads/Tails Ratios')
    plt.xlabel('Number of Flips')
    plt.ylabel('#Heads/#Tails')
    plt.xticks(rotation = 'vertical')
    plt.plot(x_axis, ratios, 'k')

# random.seed(0)
# flip_plot(4, 20)
























