from turtle import width
from numpy import arange
from players import *
from game import *
import matplotlib.pyplot as plt


def calc_accuracy(p1, p2, times):

    s1 = 0
    s2 = 0
    
    for i in range(0, times):
        g = Game(p1, p2)
        if g.play() == p1:
            s1 += 1
        else:
            s2 += 1

    return (s1, s2)

def print_accuracy(p1, p2, times):
    
    s1, s2 = calc_accuracy(p1, p2, times)
    print(f'RESULTS: Player 1 of type {type(p1).__name__}: {s1} ({s1/times}%), Player 2 of type {type(p2).__name__}: {s2} ({s2/times}%)')

def graph_accuracy(p1, p2, period, quantity):
    bins = []
    data1 = []
    data2 = []
    for i in range(0, quantity):
        s1, s2 = calc_accuracy(p1, p2, period)
        data1 += [s1]
        data2 += [s2]
        bins += [f'{period*i} - {period*(i+1)}']

    x = arange(quantity)
    width = 0.4

    plt.bar(x-width/2, data1, width)
    plt.bar(x+width/2, data2, width) 

    plt.legend([f"Player 1: {type(p1).__name__}", f"Player 2: {type(p2).__name__}"])
    plt.xticks(x, bins, fontsize=4)

    plt.xlabel("Periods")
    plt.ylabel("Amount of Wins")

    plt.show()  
    

    

