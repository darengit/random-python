#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Mar 11 12:06:38 2017

@author: goodwin
"""

import random

suit_map = {'clubs': 'c', 'diamonds': 'd', 'hearts': 'h', 'spades': 's'}
number_map = {10:'T', 11:'J', 12:'Q', 13:'K', 14:'A'}
for i in range(2, 10):
    number_map[i] = str(i)
handtype_map = {'highcard':1,
                'pair':2,
                'twopair':3,
                'threeofakind':4,
                'straight':5,
                'flush':6,
                'fullhouse':7,
                'fourofakind':8,
                'straightflush':9}
    

class Card(object):
    def __init__(self, number, suit):
        self.number = number
        self.suit = suit
    
    def get_number(self):
        return self.number
    
    def get_suit(self):
        return self.suit
    
    def __repr__(self):
        return number_map[self.number] + suit_map[self.suit]

    def __lt__(self, other):
        return self.number < other.number
    
    def __eq__(self, other):
        return self.number == other.number

class Deck(object):
    def __init__(self):
        self.deck = []
        for num in range(2, 15):
            for suit in ['clubs', 'diamonds', 'hearts', 'spades']:
                self.deck.append(Card(num, suit))

    def shuffle(self):
        random.shuffle(self.deck)
    
    def deal_hand(self):
        if len(self.deck) >= 5:
            hand = []
            for i in range(5):
                hand.append(self.deck.pop())
            return Hand(hand)
        else:
            raise ValueError('Not enough cards left in the deck')
    
    def deal_top_card(self):
        return self.deck.pop()

class Hand(object):
    def __init__(self, list_of_5_cards):
        self.hand = list_of_5_cards
        self.handtype = self.getHandType()
    
    def getHandType(self):
        htype = 'highcard'
        numbers = self.get_num_counts()
        maxfreq = max(numbers.values())
        minfreq = min(numbers.values())
        if maxfreq == 2:
            if len(numbers) == 3:
                htype = 'twopair'
            else:
                htype = 'pair'
        if maxfreq == 3:
            if minfreq == 2:
                htype = 'fullhouse'
            else:
                htype = 'threeofakind'
        if maxfreq == 4:
            htype = 'fourofakind'
        smallest = min(numbers.keys())
        largest = max(numbers.keys())
        sorted_cards = sorted(numbers.keys(), reverse=True)
        isStraight = False
        isFlush = True
        if maxfreq == 1:
            if largest-smallest == 4 or (largest == 14 and sorted_cards[1] == 5):
                isStraight = True
        suit = self.hand[0].get_suit()
        for card in self.hand[1:]:
            if card.get_suit() != suit:
               isFlush = False
               break
        if isStraight:
            htype = 'straight'
        if isFlush:
            htype = 'flush'
        if isStraight and isFlush:
            htype = 'straightflush'    
        return htype

    def discard_and_draw(self, lst, deck):
        assert len(lst) <= 5
        for num in lst:
            assert 0 <= num < 5
        for num in lst:
            del self.hand[num]
            self.hand.insert(num, deck.deal_top_card())
        
    def get_hand(self):
        return self.hand
        
    def __repr__(self):
        return str(self.hand)
    
    #return list of card ranks in sorted order        
    def sort_by_number(self):
        return list(sorted(map(lambda card: card.get_number(), self.hand), reverse=True))
    
    def get_num_counts(self):
        numbers = {}
        for card in self.hand:
            if card.get_number() not in numbers:
                numbers[card.get_number()] = 1
            else:
                numbers[card.get_number()] += 1
        return numbers
        
    def __lt__(self, other):
        myhand = handtype_map[self.getHandType()]
        theirhand = handtype_map[other.getHandType()]
        if myhand == theirhand:
            numbers = self.get_num_counts()
            othernumbers = other.get_num_counts()
            #handle case of A2345
            if myhand in [5,9]:
                if max(numbers) == 14 and min(numbers) == 2:
                    numbers[1] = 1
                    del numbers[14]
                if max(othernumbers) == 14 and min(othernumbers) == 2:
                    othernumbers[1] = 1
                    del othernumbers[14]
            return (sorted(numbers, key=lambda k: (numbers[k], k), reverse=True) <
                    sorted(othernumbers, key=lambda k: (othernumbers[k], k), reverse=True))
        else:
            return myhand < theirhand

    def __eq__(self, other):
        myhand = handtype_map[self.getHandType()]
        theirhand = handtype_map[other.getHandType()]
        if myhand == theirhand:
            numbers = self.get_num_counts()
            othernumbers = other.get_num_counts()
            return (sorted(numbers, key=lambda k: (numbers[k], k), reverse=True) ==
                    sorted(othernumbers, key=lambda k: (othernumbers[k], k), reverse=True))
        else:
            return False
            
            
print('Welcome to 5-Card Draw Poker!')
str_players = input('Please input number of players (1-5): ')
while str_players not in ['1', '2', '3', '4', '5']:
    str_players = input('Invalid number entered.  Please enter a number between 1 and 5: ')
num_players = int(str_players)
players_hands = []
deck = Deck()
deck.shuffle()
for i in range(num_players):
    players_hands.append(deck.deal_hand())
    print('\nPlayer ' + str(i+1) + ', this is your hand: ' + str(players_hands[i]))
    for num, card in enumerate(players_hands[i].get_hand()):
        print(num, card)
    print('\nPlayer ' + str(i+1) + ', please choose the cards you would like to discard.')
    print('You may choose to discard none or all of your cards.')
    print('Enter them using the indices to the left of the cards printed above.')
    print('When choosing multiple cards, please just separate the indices with a space.')
    print('Example: 0 2 4  This will discard cards 0, 2, and 4 from your hand and draw 3 new cards.')
    while True:
        idx_string = input('Please enter the indices of the card(s) you choose to discard.  If none, just press enter: ')
        if idx_string == '':
            idx_int_lst = []
            break
        idx_str_lst = idx_string.split()
        if len(idx_str_lst) > 5 or len(idx_str_lst) != len(set(idx_str_lst)):
            print('Invalid input.  Please try again.')
            continue
        try:
            idx_int_lst = [int(idx) for idx in idx_str_lst]
            if all([0 <= j < 5 for j in idx_int_lst]):
                break
            else:
                print('Invalid input.  Please try again.')
        except:
            print('Invalid input.  Please try again.')
    players_hands[i].discard_and_draw(idx_int_lst, deck)
    print('\nPlayer ' + str(i+1) + ', this is your new hand: ' + str(players_hands[i]) + '\n')

winning_hand = max(players_hands)
winners = []
for i, v in enumerate(players_hands):
    if v == winning_hand:
        winners.append((i, v))
if len(winners) == 1:
    print('Player ' + str(winners[0][0]+1) + ' wins with a ' + winners[0][1].getHandType() + '!')
#in the event of a tie
else:
    winners_num = [str(winner[0]+1) for winner in winners]
    print('Players ' + ', '.join(winners_num) + ' win with a ' + winners[0][1].getHandType() + '!')


c1 = Card(4, 'spades')
c2 = Card(4, 'hearts')
c3 = Card(4, 'spades')
c4 = Card(4, 'diamonds')
c5 = Card(14, 'hearts')
hand1 = Hand([c1,c2,c3,c4,c5])
d1 = Card(4, 'hearts')
d2 = Card(4, 'hearts')
d3 = Card(4, 'hearts')
d4 = Card(14, 'spades')
d5 = Card(4, 'hearts')
hand2 = Hand([d1,d2,d3,d4,d5])
e1 = Card(3, 'clubs')
e2 = Card(6, 'clubs')
e3 = Card(5, 'clubs')
e4 = Card(7, 'clubs')
e5 = Card(4, 'hearts')
hand3 = Hand([e1,e2,e3,e4,e5])

'''
players_hands = [hand1, hand2, hand3]
winning_hand = max(players_hands)
winners = []
for i, v in enumerate(players_hands):
    if v == winning_hand:
        winners.append((i, v))
if len(winners) == 1:
    print('Player ' + str(winners[0][0]+1) + ' wins with a ' + winners[0][1].getHandType() + '!')
#in the event of a tie
else:
    winners_num = [str(winner[0]+1) for winner in winners]
    print('Players ' + ', '.join(winners_num) + ' win with a ' + winners[0][1].getHandType() + '!')
'''
