"""
###################################################
Created on Fri Aug 23 05:17:40 2013 #
@PyPokerSimulations #
@author: Russell J. Adams #
@email: russell.adams2014@gmail.com #
###################################################


"""

import cProfile

def handtype(card1,card2,flop1=(-12,"a"),flop2=(-22,"b"),
             flop3=(-32,"z"),turn=(-42,"d"),river=(-52,"e")):
    '''Returns the hand type of the given hand. Royal Flush, Straight
       Flush, Four of a Kind, Fullhouse, Flush, Straight, Three of a
       Kind, Two Pair, Pair, High Card.'''
    # Putting each card (Value, Suit) into a list.
    temp = [card1,card2,flop1,flop2,flop3,turn,river]
    # Adds, each card(by value) to the cards dictionary. If the 
    # card is already in the dictionary, it instead appends the suit
    # to the existing key value of the dictionary.
    best_hand = []
    cards = {}
    for card in temp:
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
            return "Royal Flush",10,best_hand
        else:
            hand_type = "Straight"
    # Straight Flush
    # Iterates over each key in cards dictionary. And checks to 
    # see if each key value from +1 to +4 exists after that key.
    # Then checks to see if their suits all match
    for key,value in cards.iteritems():
        if (key+1 in cards) & (key+2 in cards) & (key+3 in cards) & (key+4 in cards):
            if (cards[key]==cards[key+1]) & (cards[key]==cards[key+2]) & (cards[key]==cards[key+3]) & (cards[key]==cards[key+4]):
                return "Straight Flush",9,best_hand
            else:
                hand_type = "Straight"               
    # Four of a kind
    # Iterates over each key in the cards dictionary.
    # Then checks to see if the key value's length is 4.
    # i.e  dict = {7:'s','c','h','d'}
    # len(dict[7]) = 4
    best_hand = []
    tmp = []
    cardsCopy = cards.copy()
    for key,value in cards.iteritems():
        if len(value) == 4:
            if key == 1:
                best_hand.append(14)
                del cardsCopy[1]
            else:
                best_hand.append(key)
                del cardsCopy[key]
            for key,value in cardsCopy.iteritems():
                tmp.append(key)
            best_hand.append(max(tmp))
            
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
        if len(value) == 3:
            if key == 1:
                for i in value:
                    best_hand.append((14,i))
            for i in value:
                best_hand.append((key,i))
            del x[key]
            for key2,value2 in x.iteritems():
                if len(value2) >= 2:
                    if key2 == 1:
                        for i in value2:
                            best_hand.append((14,i))
                    for j in value2:
                        best_hand.append((key2,value2))
                    return "Fullhouse",7,best_hand               
    # Flush
    # Iterates over each key value in the cards dictionary.
    # Keeps track of the suits and returns Flush if it finds 5 or more.
    '''Need to create a best_hand return for flushes'''
    clubs = 0
    spades = 0
    diamonds = 0
    hearts = 0
    for key in cards:
        if cards[key] == ['c']:
            clubs+=1
        if cards[key] == ['s']:
            spades+=1
        if cards[key] == ['d']:
            diamonds+=1
        if cards[key] == ['h']:
            hearts+=1
    if (clubs >= 5): 
        for key in cards:
            if cards[key] == 'c':
                best_hand.append(key)
        return "Flush",6, best_hand.sort()
    if (spades >= 5):
        for key in cards:
            if cards[key] == 's':
                best_hand.append(key)
        return "Flush",6, best_hand.sort()
    if (diamonds >= 5): 
        for key in cards:
            if cards[key] == 'd':
                best_hand.append(key)
        return "Flush",6, best_hand.sort()
    if (hearts >= 5):
        for key in cards:
            if cards[key] == 'h':
                best_hand.append(key)
        return "Flush",6, best_hand.sort()
    # Three of a kind
    # Iterates over each key value in the cards dictionary.
    # If the length of any value is 3, it returns Three of a Kind.
    best_hand = []
    tmp = []    
    cardsCopy = cards.copy()
    for key,value in cards.iteritems():
        if len(value) == 3:
            if key == 1:
                best_hand.append(14)
            else:
                best_hand.append(key)
            del cardsCopy[key]
            for key2,value2 in cardsCopy.iteritems():
                tmp.append(key2)
            tmp.sort()
            best_hand.append(tmp[-1])
            best_hand.append(tmp[-2])
            return "Three of a Kind",5,best_hand
           
    # Two Pair
    best_hand = []
    tmp = []
    cardsCopy = cards.copy()
    for key, value in cardsCopy.iteritems():
        if len(value) == 2:
            if key == 1:
                best_hand.append(15)
            else:
                best_hand.append(key)
        else:
            if key == 1:
                best_hand.append(14)
            else:
                tmp.append(key)
    if len(best_hand) == 3:
        best_hand.sort()
        del best_hand[0]
        best_hand.append(tmp[0])
        return "Two Pair",3,best_hand
    if len(best_hand) == 2:
        best_hand.sort()
        best_hand.append(tmp[2])
        return "Two Pair",3,best_hand
    # Pair
    best_hand = []
    tmp = []
    cardsCopy = cards.copy()
    for key,value in cards.iteritems():
        if len(value) == 2:
            best_hand.append(key)
            del cardsCopy[key]
            for key in cardsCopy.iterkeys():
                tmp.append(key)
    if len(best_hand) == 1:
        best_hand.append(tmp[4])
        best_hand.append(tmp[3])
        best_hand.append(tmp[2])
        return "One Pair",2,best_hand

    # High Card
    best_hand = []
    if hand_type:
        for key in cards.iterkeys():
            if (key+1 in cards) and (key+2 in cards) and (key+3 in cards) and (key+4 in cards):
                best_hand.append(key)
                best_hand.append(key+1)
                best_hand.append(key+2)
                best_hand.append(key+3)
                best_hand.append(key+4)
                return hand_type,5,best_hand
        if (10 in cards) and (11 in cards) and (12 in cards) and (13 in cards) and (1 in cards):
            best_hand.append(10)
            best_hand.append(11)
            best_hand.append(12)
            best_hand.append(13)
            best_hand.append(14)
            return hand_type,5,best_hand
    else:
        for key in cards.iterkeys():
            best_hand.append(key)
        return "High Card",1, best_hand

def evaluate(card1,card2,card3,card4,board):
    '''Evaluate one hand vs another.'''       
    # Create flops for the hands and put them in a list
    # The first hand is (c1,s1),(c2,s2) = (card one,suit one),(card two, suit two)  
    test1 = [card1,card2]
    test2 = [card3,card4]
    for x in board:
        test1.append(x)
        test2.append(x)
    Hand1 = handtype(test1[0],test1[1],test1[2],test1[3],test1[4],test1[5],test1[6])
    Hand2 = handtype(test2[0],test2[1],test2[2],test2[3],test2[4],test2[5],test2[6])
    # First Check to see if we can get off easy. i.e Fullhouse vs One Pair
    if (Hand1[1] > Hand2[1]):
        return 1
    if (Hand1[1] < Hand2[1]):
        return 2
    # We didn't get off easy, now to compare similar hands.
    # Starting with One Pair vs One Pair. The most common I'd assume.
    if (Hand1[0] == "High Card"):
        if (Hand1[2][0] == 1) and (Hand2[2][0] == 1):
            del(Hand1[2][0])
            del(Hand2[2][0])
        if Hand1[2] > Hand2[2]:
            return 1
        if Hand1[2] < Hand2[2]:
            return 2
        else:
            print("high card")
            print Hand1[2], '-->',Hand2[2]
            print test1, '-->',test2
            return 0
    if (Hand1[0] == "One Pair"):
        if (Hand1[2][0] == 1) and (Hand2[2][0] == 1):
            del(Hand1[2][0])
            del(Hand1[2][0])
            if (Hand1[2][0] > Hand2[2][0]):
                return 1
            if (Hand1[2][0] < Hand2[2][0]):
                return 2
            else:
                return 0
        if (Hand1[2][0] == 1):
            return 1
        if (Hand2[2][0] == 1):
            return 2
        if Hand1[2] > Hand2[2]:
            return 1
        if Hand1[2] < Hand2[2]:
            return 2
        else:
            return 0
    # Now checking two pair combinations to see which is better.
    elif (Hand1[0] == "Two Pair"):
        if (Hand1[2] > Hand2[2]):
            return 1
        if (Hand1[2] < Hand2[2]):
            return 2
        else:
            return 0
                    
    # Now checking Three of a Kind combinations to see which is better.
    elif (Hand1[0] == "Three of a Kind"):
        if (Hand1[2] > Hand2[2]):
            return 1
        if (Hand1[2] < Hand2[2]):
            return 2
        else:
            return 0
    
    # Need to do one for Flushes
    elif (Hand1[0] == "Flush"):
        # This is working already.
        # I'm not sure how.
        pass
    
    # Need to do one for Straights
    elif (Hand1[0] == "Straight"):
        if (Hand1[2][4] > Hand2[2][4]):
            return 1
        if (Hand1[2][4] < Hand2[2][4]):
            return 2
        else:
            return 0
    
    # Now checking Fullhouses
    elif (Hand1[0] == "Fullhouse"):
        if (Hand1[2][2][0] == 1) and (Hand2[2][2] == 1):
            if (Hand1[2][3] > Hand2[2][3]):
                return 1
            if (Hand1[2][3] < Hand2[2][3]):
                return 2
            else:
                return 0
        if (Hand1[2][2] == 1):
            return 1
        if (Hand2[2][2] == 1):
            return 2
        if (Hand1[2] > Hand2[2]):
            return 1
        if (Hand1[2] < Hand2[2]):
            return 2
        else:
            return 0
    # Now checking Four of a Kinds
    elif (Hand1[0] == "Four of a Kind"):
        if (Hand1[2][0] == Hand2[2][0]):
            if (Hand1[2][1] > Hand2[2][1]):
                return 1
            if (Hand1[2][1] < Hand2[2][1]):
                return 2
        if (Hand1[2][0] > Hand2[2][0]):
            return 1
        if (Hand1[2][0] < Hand2[2][0]):
            return 2
        else:
            return 0
        

    else:
        return 0
