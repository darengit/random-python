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
            return hand
        else:
            raise ValueError('Not enough cards left in the deck')

        
                