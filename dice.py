#!/usr/local/bin/python3

'''
6.
Write a program to simulate the playing of a simple dice game (played with one
standard 6-sided die). "Roll" the die to get a value from 1 to 6. This we will
call your point. Now keep rolling until you get the same value (your point)
again and see how many rolls it takes. Program it so you can play this game
repeatedly.
'''

from random import randrange, choice
from time import sleep

class Die:
    def __init__(self, nums, sides, choose, adds):
        self.n = choice(nums )
        self.s = choice(sides)
        self.a = choice(adds )

        self.k = choice(choose[self.n])
    
    def __repr__(self):
        if self.n == self.k and self.a:
            return "%dd%02d%+d  "  %(self.n, self.s, self.a)
        elif self.n == self.k:
            return "%dd%02d    "   %(self.n, self.s)
        elif self.a:
            return "%dd%02dk%d%+d" %(self.n, self.s, self.k, self.a)
        else:
            return "%dd%02dk%d  "  %(self.n, self.s, self.k)
    
    def roll(self):
        rolls = []
        for i in range(self.n):
            rolls.append(randrange(1, self.s + 1))
        rolls.sort(reverse=True)
        total = 0
        for i in rolls[:self.k]:
            total += i
        return total + self.a
    
    def chance(self, roll):
        got = 0
        options = []
        for i in range(self.s ** self.n):
            options.append([])
        for i in range(self.n):
            for j in range(self.s ** (self.n - i - 1)):
                for k in range(self.s):
                    for l in range(self.s ** i):
                        options[(j*self.s+k)*self.s**i+l].append(k+1)
        for i in options:
            i.sort(reverse=True)
            if sum(i[:self.k]) + self.a == roll:
                got += 1
        return got / len(options)

dice = [1,2,4,5], [4,6,8,12,20], {1:[1],2:[2],4:[1,3,4],5:[2,4,5]}, [-2,0,2,5,7]


for i in range(10):
    die = Die(*dice)
    roll = 0
    until = die.roll()
    print("\nRolling", die, end="")
    print(" until %2d" %until)
    print("Calculating probability...")
    p = die.chance(until)*100
    print("The probability of this roll is %.3f%%" %p)

    while roll != until:
        roll = die.roll()
        print("> %02d" %roll)
        sleep(0.3+p/16)
    sleep(0.3)
    print("> %02d" %roll)
    sleep(0.2)
