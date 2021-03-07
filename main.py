import random

class Card:
    """ A representation of a playing card.
    
    Card is a node in a stack-based Deck.
    
    Attributes:
        rank (int): Card value, 0-12.
            0-8 corresponding to 2-10.
            9-12 corresponding to J, Q, K, A respectively.
        suit (int): Card category.
            0-3 corresponding to spades, clubs, diamonds, hearts respectively.
        next_card (Card): The next Card in the deck.
    
    """
    
    def __init__(self, rank, suit, next_card=None):
        self.rank = rank
        self.suit = suit
        self.next_card = next_card

    @property
    def rank_short_str(self):
        """ str: A short representation of the rank of the Card. """
        if self.rank <= 8:
            return str(self.rank + 2)
        return ['J', 'Q', 'K', 'A'][self.rank - 9]

    @property
    def suit_icon_str(self):
        """ str: A unicode icon representation of the suit of the Card. """
        return ['♠', '♣', '♦', '♥'][self.suit]

    def __str__(self):
        rank = self.rank_short_str
        suit = self.suit_icon_str
        return rank + suit

class Deck:
    """ A stack-based representation of a deck of playing cards.

    A stack is used because this project is meant for practice on stacks,
      among other things.

    Attributes:
        top_card (Card): The top card of the Deck, which is to be dealt first.
    
    """
    
    def __init__(self, top_card=None):
        self.top_card = top_card

    def push(self, card):
        card.next_card = self.top_card
        self.top_card = card

    def pop(self):
        card = self.top_card
        self.top_card = card.next_card
        return card

    @staticmethod
    def random():
        """ Return a standard Deck of 52 cards, suffled. """
        cards = []
        for rank in range(13):
            for suit in range(4):
                cards.append(Card(rank, suit))

        random.shuffle(cards)

        deck = Deck()
        for card in cards:
            deck.push(card)

        return deck

def prompt_choice():
    """ Prompt for a choice until a valid response is given. """
    print()
    print('What do you want to do?')

    choices = ['stay']

    for i, choice in enumerate(choices):
        print(f'{i + 1}. {choice}')

    while True:
        user_choice = input()
        
        try:
            user_choice = int(user_choice)
        except ValueError:
            print('Please input an integer.')
            continue

        if user_choice not in range(1, len(choices) + 1):
            print('Please input one of the provided choices.')
            continue
        
        break

    choice_str = choices[user_choice - 1]
    print(f'You chose to {choice_str}.')

    return choice_str

player_cards = []
dealer_cards = []

deck = Deck.random()
player_cards.append(deck.pop())
dealer_cards.append(deck.pop())
player_cards.append(deck.pop())
dealer_cards.append(deck.pop())

print('Your cards:', ', '.join(map(str, player_cards)))
print("Dealer's cards:", ', '.join(map(str, dealer_cards)))

prompt_choice()
