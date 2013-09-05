# -*- coding: utf-8 -*-
"""
###################################################
Created on Fri Aug 23 05:17:40 2013               #
@PyPokerSimulations                               #
@author: Russell J. Adams                         #
@email: russell.adams2014@gmail.com               #
###################################################


"""
#import cProfile

import random
from math import factorial,pi
from itertools import combinations
from handeval import evaluate

def combin(n,k):
    '''Combination function. For example, if you wanted to know how many
       possible 5 card hand combinations from a deck of 52. You can call
       Combin(52,5)'''
    return factorial(n)/(factorial(k)*(factorial(n-k)))
    
def createdeck():
    '''Create a list of all 52 cards in a single deck'''
    deck = []    
    values = [2,3,4,5,6,7,8,9,10,11,12,13,14]
    suits = ['s','c','h','d']        
    for value in values:
        for suit in suits:
            deck.append((value,suit))
    return deck
    
def createboards(card1,card2,card3=None,card4=None,flop1=(None,None),flop2=(None,None),flop3=(None,None)):
    '''Returns all possible 5 card boards for 2-4 hole cards. You can also
       specify a flop, and instead create all possible turn/river cards.'''
    deck = createdeck()
    # Remove the four specified cards from the deck.
    deck.remove(card1)
    deck.remove(card2)
    if card3:
        deck.remove(card3)
        deck.remove(card4)
    # Check to see if a flop was specified. If so, remove those 3 from the deck.
    if flop1 != (None,None):
        deck.remove(flop1)
        deck.remove(flop2)
        deck.remove(flop3)
        c = list(combinations(deck,2))
        return c
        boards = {}
        for j in range(len(c)):
            boards[j] = c[j]
        return boards
    # Using itertools.combinations we create all 5 card combinations from
    # the remaining cards in the deck. Then place each of those
    # combinations into a dictionary for quick lookup.        
    c = list(combinations(deck,3))
    boards = {}
    for j in range(len(c)):
        boards[j] =c[j]
    return boards
        
def randomrange(card1,card2,flop=None):
    '''Creates a random range for an opponent'''
    deck = createdeck()
    deck.remove(card1)
    deck.remove(card2)
    if flop != None:
        deck.remove(flop[0])
        deck.remove(flop[1])
        deck.remove(flop[2])
    c = list(combinations(deck,2))
    hands = {}
    for i in range(len(c)):
        hands[i] = c[i]
    return hands

def equity(card1,card2,card3,card4,simulations=1000000):
    '''Equates the equity of one specified hand,
       versus another specified hand. Monte Carlo style.'''
    one = 0.0
    two = 0.0
    tie = 0.0
    # create a dictionary of flops to use randomly
    # This seems effecient, but I've pondered about using instead
    # random.choice(deck) for each of the remaining 5 cards
    # I think, though, that dictionary lookup may prove to be faster
    flops = createboards(card1,card2,card3,card4)
    # How many times you want to run the hand versus the other hand
    # Default value is 30000    
    for i in range(simulations):
        # choose a flop to use, randomly
        flop = random.choice(flops)
        # evaluate the two hands against eachother                   
        x = evaluate(card1,card2,card3,card4,flop)
        if x == 1:
            one+=1.0
        elif x == 2:
            two+=1.0
        else:
            tie+=1.0
    total = one+two+tie
    print total
    print("One is winning ",float(one/total))
    print("Two is winning ",float(two/total))
    print("And they are tying ",float(tie/total))
    
def equityVsrandom(card1,card2,flop=None,simulations=10000):
    '''Equates the equity of one specified hand, versus another 
       Random Hand.'''
    ranrange = randomrange(card1,card2)
    one = 0.0
    two = 0.0
    tie = 0.0
    if flop == None:
        flops = createboards(card1,card2)
        for i in range(simulations):
            flop = random.choice(flops)
            card3,card4 = random.choice(ranrange)
            x = evaluate(card1,card2,card3,card4,flop)
            if x == 1:
                one+=1.0
            elif x == 2:
                two+=1.0
            else:
                tie+=1.0
    else:
        flops = createboards(card1,card2,card3=None,card4=None,flop1=flop[0],
                             flop2=flop[1],flop3=flop[2])
        for i in range(simulations):
            card3,card4 = random.choice(ranrange)
            x = random.choice(flops)
            x = evaluate(card1,card2,card3,card4,random.choice(flops)+flop)
            if x == 1:
                one+=1.0
            elif x == 2:
                two+=1.0
            else:
                tie+=1.0
                
    total = one+two+tie
    results = (one/total*100),(two/total*100),(tie/total*100)
    return results
