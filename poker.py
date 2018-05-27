import sys
import string
import random
import os

class p_card:
    #Value 2 represents a 2, value 14 represents an ace.
    value = 0
    #alias is the character that represents the card's strength
    alias = ""
    suit = ""
    #sel indicates whether player has selected card (for discarding).
    sel = 0

def main():

    if len(sys.argv) > 1:
        print("Usage: poker.py")

    p_factor = 1
    chips = 0

    main_menu(p_factor,chips)

def set_paytable(p_factor):

    paytable ={
        "Royal Flush":800*p_factor,
        "Straight Flush":50*p_factor,
        "Four of a Kind":25*p_factor,
        "Full House":9*p_factor,
        "Flush":6*p_factor,
        "Straight":4*p_factor,
        "Three of a Kind":3*p_factor,
        "Two Pair":2*p_factor,
        "Jacks or Better":1*p_factor
    }

    return paytable


def main_menu(p_factor,chips):

    error = ""

    #Print menu and wait for input
    while True:

##        print("\n"*100)
        os.system("cls")

        paytable = set_paytable(p_factor)
		
        print(
"""Chips: {}
Payout multiplier: {}

Enter one of the following:
    add_chips
    paytable
    play
    quit
""".format(chips,p_factor)
             )
        if error:
            print(error)

        inp = input()
        inp = inp.lower()

        #Add chips
        if inp == "add_chips":

            error = ""

            while True:

                os.system('cls')
                
                print("Current chip stack: {}".format(chips))
                print("Enter BACK to return to menu\n")
                if error:
                    print(error)

                inp = input("Chips to insert: ")
                inp = inp.replace(",","")
                inp = inp.lower()

                if inp == "back":
                    break

                try:
                    inp = int(inp)
                    if (inp <= 0 or inp > 100000):
                        error = "Input must be between 0 and 100,000"
                    elif chips + inp > 100000:
                        error = "Cannot add chips beyond 100,000"
                    else:
                        chips += inp
                        break
                except:
                    error = "Input must be positive integer"

        #Show paytable and allow modification
        if inp == "paytable":

            error = ""

            while True:

                paytable = set_paytable(p_factor)

                print("\n"*100)

                for key,value in paytable.items():
                    if key == "Flush":
                        print(key+"\t\t"+"= "+str(value))
                    else:
                        print(key+"\t"+"= "+str(value))

                print("")
                print("Payout multiplier: {}".format(p_factor))
                print("")
                print("Enter BACK to return to menu")
                if error:
                    print(error)

                inp = input("New payout multiplier:")
                inp = inp.lower()
                if inp == "back":
                    break
                try:
                    inp = float(inp)
                    if inp < 0:
                        error = "Multiplier must be positive"
                    elif inp >10:
                        error = "Maximum multiplier value is 10.0"
                    else:
                        p_factor = inp
                except:
                    error = "Enter positive number or BACK"

        if inp == "play":
            if chips == 0:
                error = "Add chips to play"
            else:
                chips = play(chips,paytable)

        if inp == "quit":
            break

def play(chips,paytable):

    while True:
        deck = list(range(52))

        bet  = betting(chips)
        chips -= bet
        hand = round1(deck)
        discarding(hand)
        hand = round2(hand,deck)
        strength,winnings = payout(hand,paytable,bet)
        chips += winnings

        print(strength)
        print("You won {} chips     Current chip stack: {}\n".format(winnings,chips))
        print("Enter MENU to return to menu")
        print("Enter anything else to continue playing")
        inp = input().lower()

        if inp == "menu":
            break
        if chips == 0:
            break

    return chips

#Prompts player for bet amount
def betting(chips):

    bet = 0
    while bet <= 0 or bet > chips:
        print("Chip stack: {}".format(chips))
        inp = input("Bet amount: ")
        try:
            inp = int(inp)
            bet = inp
        except:
            pass
    return bet

#Draws initial hand from deck
def round1(deck):

    hand = []
    for i in range(5):
        card = draw(deck)
        hand.append(card)

    return hand

#Draws random card from deck, adds it to hand, and deletes it from deck.
def draw(deck):
    card = p_card()
    d_len = len(deck)
    c_num = random.randrange(d_len)
    val = deck[c_num]
    del deck[c_num]

    card.value = (val % 13) + 2
    r_val = card.value

    if r_val > 9:
        if r_val == 10:
            card.alias = "T"
        if r_val == 11:
            card.alias = "J"
        if r_val == 12:
            card.alias = "Q"
        if r_val == 13:
            card.alias = "K"
        if r_val == 14:
            card.alias = "A"
    else:
        card.alias = str(r_val)

    suit = int(val / 13)
    if suit == 0:
        card.suit = "c"
    if suit == 1:
        card.suit = "d"
    if suit == 2:
        card.suit = "h"
    if suit == 3:
        card.suit = "s"

    return card

#Clears terminal and prints game-state.
def visual(hand):

    #Labels player will use to reference cards in hand.
    lab = [' 1 ',' 2 ',' 3 ',' 4 ',' 5 ']

    #Add brackets to labels to indicate selection.
    i = 0
    for card in hand:
        if card.sel == True:
            lab[i] = "[{}]".format(i+1)
        i += 1

    #Printing of game-state
    os.system('cls')
	
    print("""
 ---  ---  ---  ---  ---
| {0.alias} || {1.alias} || {2.alias} || {3.alias} || {4.alias} |
| {0.suit} || {1.suit} || {2.suit} || {3.suit} || {4.suit} |
 ---  ---  ---  ---  ---
 {5}  {6}  {7}  {8}  {9}"""
            .format(hand[0], hand[1], hand[2], hand[3], hand[4], lab[0], lab[1], lab[2], lab[3], lab[4])
         )

#Prompts player to discard cards
def discarding(hand):

    while True:

        visual(hand)
        print("Enter cards to select/deselect (1,2,3,4,5) or CONFIRM (c) discarding")
        inp = input()
        inp = inp.lower()
        if inp == "confirm" or inp == "c":
            break

        inp = inp.replace(",","")
        selection = []
        try:
            for char in inp:
                selection.append(int(char))
            for n in selection:
                if hand[n-1].sel == 0:
                    hand[n-1].sel = 1
                else:
                    hand[n-1].sel = 0
        except:
            pass

def round2(hand,deck):

    i = 0
    for card in hand:
        if hand[i].sel == 1:
            hand[i] = draw(deck)
        i += 1

    visual(hand)
    return hand

def payout(hand,paytable,bet):

    #Check for flush
    flush = True
    for card in hand:
        if card.suit != hand[0].suit:
            flush = False
            break

    #Check for straight
    straight = True

    #Check for unique values
    i = 0
    for card in hand:
        for j in range(i):
            if card.value == hand[i-(j+1)].value:
                straight = False
        i += 1

    #Check if all cards in range
    if straight == True:

        for i in range(5):
            for card in hand:
                if card.value <= hand[i].value - 5 or card.value >= hand[i].value + 5:
                    if card.value == 14:
                        if 1 <= hand[i].value - 5:
                            straight = False
                            break
                    else:
                        straight = False
                        break

            if hand[i].value == 14 and straight == False:
                straight = True
                for card in hand:
                    if card.value >= 6 and card.value != 14:
                        straight = False
                        break

            if straight == False:
                break

    #Check for straight flush
    if straight == True and flush == True:
        #Check for royal flush
        ace,king = False, False
        for card in hand:
            if card.value == 13:
                king = True
            if card.value == 14:
                ace = True
        if ace == True and king == True:
            return "Royal Flush",paytable["Royal Flush"]*bet
        return "Straight Flush",paytable["Straight Flush"]*bet

    #Count repeated values
    counts = [0] * 5
    for card in hand:
        for i in range(5):
            if card.value == hand[i].value:
                counts[i] += 1

    #Check for four-of-a-kind
    if 4 in counts:
        return "Four of a Kind",paytable["Four of a Kind"]*bet

    #Check for fullhouse
    if 3 in counts and 2 in counts:
        return "Full House",paytable["Full House"]*bet

    if flush == True:
        return "Flush",paytable["Flush"]*bet

    if straight == True:
        return "Straight",paytable["Straight"]*bet

    #Check for three-of-a-kind
    if 3 in counts:
        return "Three of a Kind",paytable["Three of a Kind"]*bet

    #Check for two-pair
    if counts.count(2) == 4:
        return "Two Pair",paytable["Two Pair"]*bet

    #Check for jacks or better
    i = 0
    for i in range(5):
        c = 0
        if hand[i].value >= 11:
            for card in hand:
                if card.value == hand[i].value:
                    c += 1
            if c == 2:
                return "Jacks or Better",paytable["Jacks or Better"]*bet

    return "",0

if __name__ == "__main__":
    main()
