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
from math import factorial
from itertools import combinations

def combin(n,k):
    '''Combination function. For example, if you wanted to know how many
       possible 5 card hand combinations from a deck of 52. You can call
       Combin(52,5)'''
    return factorial(n)/(factorial(k)*(factorial(n-k)))
    
def createdeck():
    '''Create a list of all 52 cards in a single deck'''
    deck = []    
    values = [1,2,3,4,5,6,7,8,9,10,11,12,13]
    suits = ['s','c','h','d']        
    for value in values:
        for suit in suits:
            deck.append((value,suit))
    return deck

def handtype(card1,card2,flop1=(-12,"a"),flop2=(-22,"b"),
             flop3=(-32,"z"),turn=(-42,"d"),river=(-52,"e")):
    '''Returns the hand type of the given hand. Royal Flush, Straight
       Flush, Four of a Kind, Fullhouse, Flush, Straight, Three of a
       Kind, Two Pair, Pair, High Card.'''
    # Putting each card (Value, Suit) into a list.
    x = [card1,card2,flop1,flop2,flop3,turn,river]
    # Adds, each card(by value) to the cards dictionary. If the 
    # card is already in the dictionary, it instead appends the suit
    # to the existing key value of the dictionary.
    best_hand = []
    cards = {}
    for card in x:
        if card[0] > 0:
            if card[0] in cards:
                cards[card[0]].append(card[1])
            else:
                cards[card[0]] = [card[1]]
    # Royal Flush
    # Checks if 10,J,Q,K,A are in the cards dictionary.
    # Then checks to see if their suits all match.
    hand_type = None
    if (1 in cards) & (10 in cards) & (11 in cards)& (12 in cards) & (13 in cards):
        if (cards[1]==cards[10]) & (cards[1]==cards[11]) & (cards[1]==cards[12]) & (cards[1]==cards[13]):
            return "Royal Flush",10
        else:
            hand_type = "Straight"
    # Straight Flush
    # Iterates over each key in cards dictionary. And checks to 
    # see if each key value from +1 to +4 exists after that key.
    # Then checks to see if their suits all match
    for key in cards:
        if (key+1 in cards) & (key+2 in cards) & (key+3 in cards) & (key+4 in cards):
            if (cards[key]==cards[key+1]) & (cards[key]==cards[key+2]) & (cards[key]==cards[key+3]) & (cards[key]==cards[key+4]):
                return "Straight Flush",9
            else:
                hand_type = "Straight"               
    # Four of a kind
    # Iterates over each key in the cards dictionary.
    # Then checks to see if the key value's length is 4.
    # i.e  dict = {7:'s','c','h','d'}
    # len(dict[7]) = 4
    for key,value in cards.iteritems():
        if len(cards[key]) == 4:
            for i in value:
                best_hand.append((key,i))
            return "Four of a Kind",8,best_hand
    # Fullhouse
    # Iterates over each key in the cards dictionary.
    # Checks to see if any of the key value's lengths is 3.
    # If it is, it deletes that key from the dictionary copy.
    # Then iterates over the copied dictionary again to see if another
    # key value is greater than or equal to 2.
    best_hand = []    
    x = cards.copy()
    for key,value in cards.iteritems():
        if len(cards[key]) == 3:
            for i in value:
                best_hand.append((key,i))
            del x[key]
            for key2,value2 in x.iteritems():
                if len(x[key2]) >= 2:
                    for j in value2:
                        best_hand.append((key2,j))
                    return "Fullhouse",7,sorted(best_hand, key=lambda p: p[0])               
    # Flush
    # Iterates over each key value in the cards dictionary.
    # Keeps track of the suits and returns Flush if it finds 5 or more.
    '''Need to create a best_hand return for flushes'''
    best_hand = []
    spades = 0
    clubs = 0
    hearts = 0
    diamonds = 0
    for key in cards:
        if 's' in cards[key]:
            spades += 1
        elif 'c' in cards[key]:
            clubs += 1
        elif 'h' in cards[key]:
            hearts += 1
        elif 'd' in cards[key]:
            diamonds += 1
    if (spades>=5) or (clubs>=5) or (hearts>=5) or (diamonds>=5):
        return "Flush",6
    # Three of a kind
    # Iterates over each key value in the cards dictionary.
    # If the length of any value is 3, it returns Three of a Kind.
    for key,value in cards.iteritems():
        if len(cards[key]) == 3:
            for i in value:
                best_hand.append((key,i))
            return "Three of a Kind",4,best_hand           
    # Two Pair
    best_hand = []
    cardsCopy = cards.copy()
    for key,value in cards.iteritems():
        if len(cards[key]) == 2:
            for j in value:
                best_hand.append((key,j))
            del cardsCopy[key]
            for key2,value2 in cardsCopy.iteritems():
                if len(cardsCopy[key2]) == 2:
                    for i in value2:
                        best_hand.append((key2,i))
                    return "Two Pair",3, sorted(best_hand, key=lambda p: p[0])
    # Pair
    best_hand = []
    for key,value in cards.iteritems():
        if len(cards[key]) == 2:
            for i in value:
                best_hand.append((key,i))
            return "One Pair",2,best_hand
    # High Card
    if hand_type:
        return hand_type,5
    else:
        for key in cards:
            best_hand.append(key)
        return "High Card",1, best_hand
         
def createboards(card1,card2,card3,card4,flop1=(None,None),flop2=(None,None),flop3=(None,None)):
    '''Returns all possible 5 card boards for 2-4 hole cards. You can also
       specify a flop, and instead create all possible turn/river cards.'''
    deck = createdeck()
    x = list(deck)
    # Remove the four specified cards from the deck.
    x.remove(card1)
    x.remove(card2)
    x.remove(card3)
    x.remove(card4)
    # Check to see if a flop was specified. If so, remove those 3 from the deck.
    if flop1 != (None,None):
        x.remove(flop1)
        x.remove(flop2)
        x.remove(flop3)
        c = list(combinations(x,2))
        boards = {}
        for j in range(len(c)):
            boards[j] = c[j]
            return boards
    # Using itertools.combinations we create all 5 card combinations from
    # the remaining cards in the deck. Then place each of those
    # combinations into a dictionary for quick lookup.        
    c = list(combinations(x,5))
    boards = {}
    for j in range(len(c)):
        boards[j] =c[j]
    return boards

def evaluate(card1,card2,card3,card4,flop):
    '''Evaluate one hand vs another.'''       
    # Create flops for the hands and put them in a list
    # The first hand is (c1,s1),(c2,s2) = (card one,suit one),(card two, suit two)
    test1 = [card1,card2]
    test2 = [card3,card4]
    for x in flop:
        test1.append(x)
        test2.append(x)
    Hand1 = handtype(test1[0],test1[1],test1[2],test1[3],test1[4],test1[5],test1[6])
    Hand2 = handtype(test2[0],test2[1],test2[2],test2[3],test2[4],test2[5],test2[6])
    # First Check to see if we can get off easy. i.e Fullhouse vs One Pair
    if (Hand1[1] > Hand2[1]):
        return 1
    elif (Hand2[1] > Hand1[1]):
        return 2
    # We didn't get off easy, now to compare similar hands.
    else:
        # Starting with One Pair vs One Pair. The most common I'd assume.
        if (Hand1[0] == "One Pair"):
            if (Hand1[2][0][0] == 1):
                if (Hand2[2][0][0] == 1):
                    return 0
                else:
                    return 1
            elif (Hand2[2][0][0] == 1):
                return 2
            elif (Hand1[2][0][0] > Hand2[2][0][0]):
                return 1
            elif (Hand2[2][0][0] > Hand1[2][0][0]):
                return 2
            else:
                # This could be done better!
                return 0
        # Now checking two pair combinations to see which is better.
        elif (Hand1[0] == "Two Pair"):
            if (Hand1[2][0][0] == 1):
                if (Hand2[2][0][0] == 1):
                    if (Hand1[2][2][0] > Hand2[2][2][0]):
                        return 1
                    elif (Hand2[2][2][0] > Hand1[2][2][0]):
                        return 2
                    # This could be done better!
                    elif (Hand2[2][2][0] == Hand1[2][2][0]):
                        return 0
                    else:
                        return 1
                else:
                    return 1
            elif (Hand2[2][0][0] == 1):
                return 2
            elif (Hand1[2][3][0] > Hand2[2][3][0]):
                return 1
            elif (Hand2[2][3][0] > Hand1[2][3][0]):
                return 2
            else:
                # This could be done better!
                return 0
                    
        # Now checking Three of a Kind combinations to see which is better.
        elif (Hand1[0] == "Three of a Kind"):
            if (Hand1[2][0][0] == 1):
                if (Hand2[2][0][0] == 1):
                    return 0
                else:
                    return 1
            elif (Hand2[2][0][0] == 1):
                return 2
            elif (Hand1[2][0][0] > Hand2[2][0][0]):
                return 1
            elif (Hand2[2][0][0] > Hand1[2][0][0]):
                return 2
            else:
                # This could be done better!
                return 0
        
        # Need to do one for Flushes
        
        # Need to do one for Straights
        
        # Now checking Fullhouses
        elif (Hand1[0] == "Fullhouse"):
            if (Hand1[2][0][0] == 1):
                if (Hand2[2][0][0] == 1):
                    if (Hand1[2][2][0] == 1) and (Hand2[2][2][0] != 1):
                        return 1
                    elif (Hand2[2][2][0] == 1) and (Hand1[2][2][0] != 1):
                        return 2
                    elif (Hand1[2][4][0] > (Hand2[2][4][0])):
                        return 1
                    else:
                        return 2
                else:
                    return 1
            elif (Hand2[2][0][0] == 1):
                return 2
            elif (Hand1[2][4][0] > Hand2[2][4][0]):
                return 1
            else:
                return 2
        # Now checking Four of a Kinds
        elif (Hand1[0] == "Four of a Kind"):
            if (Hand1[2][0][0] == 1):
                return 1
            elif (Hand2[2][0][0] == 1):
                return 2
            elif (Hand1[2][0][0] > Hand2[2][0][0]):
                return 1
            else:
                return 2   
        # Need to do one for Straight Flushes
        
def randomrange(card1,card2):
    '''Creates a random range for an opponent'''
    deck = createdeck()
    deck.remove(card1)
    deck.remove(card2)
    c = list(combinations(deck,2))
    hands = {}
    for i in range(len(c)):
        hands[i] = c[i]
    return hands

def equity(card1,card2,card3,card4,simulations=30000):
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
    
def equityVsrandom(card1,card2,simulations=30000):
    '''Equates the equity of one specified hand, versus another 
       Random Hand.'''
    ranrange = randomrange(card1,card2)
    card3,card4 = random.choice(ranrange)
    one = 0.0
    two = 0.0
    tie = 0.0
    flops = createboards(card1,card2,card3,card4)
    for i in range(simulations):
        flop = random.choice(flops)
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
