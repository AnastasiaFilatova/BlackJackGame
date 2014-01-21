# Black Jack Game
# Made by Anastasia Filatova
# anastasia.n.filatova@gmail.com

# This was a project done for Coursera Class
# Introduction to Interactive Programming in Python
# from Rice University.

import simplegui
import random

CARD_SIZE = (73, 98)
CARD_CENTER = (36.5, 49)
card_images = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/cards.jfitz.png")

CARD_BACK_SIZE = (71, 96)
CARD_BACK_CENTER = (35.5, 48)
card_back = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/card_back.png")    

in_play = False # shows if the round is still in play
outcome = '' # keeps game messages
score = 0

# init globals for cards
SUITS = ('C', 'S', 'H', 'D')
RANKS = ('A', '2', '3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K')
VALUES = {'A':1, '2':2, '3':3, '4':4, '5':5, '6':6, '7':7, '8':8, '9':9, 'T':10, 'J':10, 'Q':10, 'K':10}
    
class Card:
    def __init__(self, suit, rank):
        '''Inits Card object'''
        if (suit in SUITS) and (rank in RANKS):
            self.suit = suit
            self.rank = rank
        else:
            self.suit = None
            self.rank = None
            print "Invalid card: ", suit, rank

    def __str__(self):
        '''Returns the string of object's attributes'''
        return self.suit + self.rank

    def get_suit(self):
        '''Returns the suit attribute''' 
        return self.suit

    def get_rank(self):
        '''Returns the rank attribute''' 
        return self.rank

    def draw(self, canvas, pos):
        '''Draws object on the canvas'''
        card_loc = (CARD_CENTER[0] + CARD_SIZE[0] * RANKS.index(self.rank), 
                    CARD_CENTER[1] + CARD_SIZE[1] * SUITS.index(self.suit))
        canvas.draw_image(card_images, card_loc, CARD_SIZE,
                         [pos[0] + CARD_CENTER[0], pos[1] + CARD_CENTER[1]],
                         CARD_SIZE)
          
# define hand class
class Hand:
    def __init__(self):
        '''Creates Hand object'''
        self.hand_cards = []
        
    def __str__(self):
        '''Returns a string representation of a hand'''
        return " ".join(str(card) for card in self.hand_cards)

    def add_card(self, card):
        '''Adds a card object to a hand'''
        self.hand_cards.append(card)  
    
    def get_value(self):
        '''Counts aces as 1, if the hand has an ace, then adds 10 to hand value if it doesn't bust'''    
        value, aces = 0, 0
        for card in self.hand_cards:
            if card.get_rank() == 'A':
                aces += 1
        value = sum([VALUES[card.get_rank()] for card in self.hand_cards])
        if aces == 0:
            return value
        else:
            if value + 10 <= 21:
                return value + 10
            else:
                return value
    def busted(self):
        '''Check busted player or not'''
        if self.get_value() > 21:
            return True
        else:
            return False
   
    def draw(self, canvas, pos):
        '''Draws a hand on the canvas'''
        global in_play
        i = 0
        if len(self.hand_cards) <= 5:
            for card in self.hand_cards:
                card.draw(canvas, [pos[0] + i * CARD_SIZE[0], pos[1]])
                i += 1
                  
    def draw_card_back(self, canvas, pos): 
        canvas.draw_image(card_back, CARD_BACK_CENTER, CARD_BACK_SIZE,
                         [pos[0] + CARD_BACK_CENTER[0],
                         pos[1] + CARD_BACK_CENTER[1]],
                         CARD_BACK_SIZE)  
class Deck:
    def __init__(self):
        '''Creates a Deck object'''
        self.deck_list = [Card(suit, rank) for suit in SUITS for rank in RANKS]               

    def shuffle(self):
        '''Shuffles the deck''' 
        random.shuffle(self.deck_list)

    def deal_card(self):
        '''Deals a card object from the deck'''
        return self.deck_list.pop() 
    
    def __str__(self):
        '''Returns a string representing the deck'''
        return " ".join(str(card) for card in self.deck_list)

def deal():
    '''Creates event handler for "Deal" button. 
    You lose round when press the button in the middle of the round.'''
    
    global outcome, in_play, deck, player_hand, diler_hand, score
    deck, player_hand, diler_hand = Deck(), Hand(), Hand()
    
    outcome = "Hit or Stand?"
    if not in_play:
        deck.shuffle()
    else:
        outcome = "You have lost this round!"
        score -= 1
    
    for i in range(2):
        player_hand.add_card(deck.deal_card())
        diler_hand.add_card(deck.deal_card())
    in_play = True
    #print "Deck:", deck
    #print "Player", player_hand, "Value", player_hand.get_value()
    #print "Diler", diler_hand, "Value", diler_hand.get_value()

def hit():
    '''Creates event handler for "Hit" button. If the hand is in play, hit the player.
    If busted, assign a message to outcome, update in_play and score.'''
    
    global outcome, in_play, score
    if not player_hand.busted() and in_play:
        player_hand.add_card(deck.deal_card())
        #print "\nPlayer", player_hand, "Value", player_hand.get_value()
        if player_hand.busted():
            outcome = "You are busted! New Deal?"
            in_play = False
            score -= 1

def stand():
    '''Creates event handler for "Stand" button. If hand is in play, 
    repeatedly hit dealer until his hand = 17 or more. Assign a message
    to outcome, update in_play and score'''
    
    global outcome, in_play, score
   
    if not player_hand.busted() and in_play:
        while diler_hand.get_value() < 17:
            diler_hand.add_card(deck.deal_card())
            #print "\nDiler", diler_hand, "Value", diler_hand.get_value()
        if diler_hand.busted():
            outcome = "Diler is busted! New Deal?"
            score += 1
        else:
            if player_hand.get_value() <= diler_hand.get_value():
                outcome = "Diler won! New Deal?"
                score -= 1
            else:
                outcome = "You won! New Deal?"
                score += 1
        in_play = False
        
def draw(canvas):
    '''Draws text and diler and player hands on the canvas'''
    global in_play
    canvas.draw_text("Blackjack", (230, 50), 35, 'Black')
    canvas.draw_text("Diler", (50, 130), 25, 'Black')
    canvas.draw_text("You", (50, 330), 25, 'Black')
    canvas.draw_text("Score = " + str(score), (250, 300), 25, 'Black')
    canvas.draw_text(str(outcome), (250, 130), 25, 'Black')
    player_hand.draw(canvas, [50, 350])
    diler_hand.draw(canvas, [50, 150])
    if in_play:
        diler_hand.draw_card_back(canvas, [50, 150])

# initialization frame
frame = simplegui.create_frame("Blackjack", 600, 600)
frame.set_canvas_background("Green")

#create buttons and canvas callback
frame.add_button("Deal", deal, 200)
frame.add_button("Hit",  hit, 200)
frame.add_button("Stand", stand, 200)
frame.add_label("Made by Anastasia Filatova")
frame.set_draw_handler(draw)

# get things rolling
deal()
frame.start()
