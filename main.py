import math
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
    def rank_long_str(self):
        """ str: A long representation of the rank of the Card. """

        return [
            'two', 'three', 'four', 'five', 'six', 'seven', 'eight',
            'nine', 'ten', 'jack', 'queen', 'king', 'ace'
        ][self.rank]

    @property
    def suit_icon_str(self):
        """ str: A unicode icon representation of the suit of the Card. """

        return ['♠', '♣', '♦', '♥'][self.suit]

    @property
    def is_face_card(self):
        """ bool: Whether Card is one that depicts a person. """

        return self.rank > 8

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

class Chip:
    """ A representation of a casino chip (token).

    Attributes:
        value (int): Chip denomination; the value of a single chip.
        type (str): Unique representation of chip's type, like color.

    """

    def __init__(self, value, chip_type):
        self.value = value
        self.type = chip_type

class BasePlayer:
    """ A representation of a person who can participate in the game. """

    def __init__(self):
        self.hand = []
        self.chips = []

    def remove_chips(self, amount):
        """ Remove chips from player's stack.

        Remove chips in decreasing value until total value of `amount`
          chips have been removed.

        """

        new_stack = []
        remaining_amount = amount

        self.chips.sort(key=lambda chip: chip.value, reverse=True)
        for chip in self.chips[:]:
            if chip.value <= remaining_amount:
                new_stack.append(chip)
                self.chips.remove(chip)
                remaining_amount -= chip.value

        return new_stack

    def print_chips(self):
        """ Print amount of every chip type in stack, and total value. """

        chip_types = []
        chip_amount_by_type = {}
        for chip in self.chips:
            if chip_amount_by_type.get((chip.value, chip.type)) is None:
                chip_amount_by_type[(chip.value, chip.type)] = 0
                chip_types.append((chip.value, chip.type))
            chip_amount_by_type[(chip.value, chip.type)] += 1
        chip_types.sort(key=lambda tup: tup[0])

        total_value = 0

        for chip_value, chip_type in chip_types:
            chip_amount = chip_amount_by_type[(chip_value, chip_type)]
            print(f'{chip_amount} {chip_type} (${chip_value}) chips')

            total_value += chip_amount * chip_value

        print(f'Total chip value: ${total_value}')

    @property
    def hand_value(self):
        """ Calculate the total value of cards in a hand (list). """

        total_card_value = 0

        for card in self.hand:
            if card.is_face_card:
                if card.rank_long_str == 'ace':
                    # If card is an ace, it is valued as 1
                    #   if valuing it as 11 would lead to a bust.
                    if total_card_value + 11 > 21:
                        total_card_value += 1
                    else:
                        total_card_value += 11
                else:
                    total_card_value += 10
            else:
                # A numeric card is valued according to its numeric value.
                total_card_value += card.rank + 2

        return total_card_value

class Dealer(BasePlayer):
    """ A representation of a card dealer. """

    def deal(self, deck, player, player_name):
        """ Deal a single Card from `deck` to `player`s hand. """

        card = deck.pop()
        player.hand.append(card)
        print(f'Dealer deals {player_name} {card}')

    def deal_initial(self, deck, player):
        """ Deal to player and dealer 2 cards each, for game start. """

        self.deal(deck, player, 'you')
        self.deal(deck, self, 'himself')
        self.deal(deck, player, 'you')
        self.deal(deck, self, 'himself')

class Player(BasePlayer):
    """ A representation of a blackjack player. """

def prompt_choice(choices):
    """ Prompt for a choice until a valid response is given. """

    print()
    print('What do you want to do?')

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

player = Player()
dealer = Dealer()

for chip_num, chip_value, chip_type in [
        (0, 1, 'blue'),
        (20, 5, 'red'),
        (8, 25, 'green'),
        (2, 100, 'black'),
        (0, 500, 'purple'),
        (0, 1000, 'orange')
    ]:
    for _ in range(chip_num):
        chip = Chip(chip_value, chip_type)
        player.chips.append(chip)

for chip_num, chip_value, chip_type in [
        (100, 1, 'blue'),
        (20, 5, 'red'),
        (12, 25, 'green'),
        (5, 100, 'black'),
        (2, 500, 'purple'),
        (1, 1000, 'orange')
    ]:
    for _ in range(chip_num):
        chip = Chip(chip_value, chip_type)
        dealer.chips.append(chip)

def game():
    """ Play a single blackjack session. """

    first_move = True

    player.hand = []
    dealer.hand = []

    print('Dealer shuffles a deck of cards.')
    deck = Deck.random()

    print()
    print('Your chips:')
    player.print_chips()

    print()
    print("Dealer's chips:")
    dealer.print_chips()

    print()
    print('Place a bet.')
    choice = prompt_choice(
        ['bet minimum ($5)', 'bet maximum ($500)']
    )
    if choice == 'bet minimum ($5)':
        player_bet = 5
    elif choice == 'bet maximum ($500)':
        player_bet = 500

    player_bet_chips = player.remove_chips(player_bet)

    print()
    dealer.deal_initial(deck, player)

    while True:
        print()
        print('Your hand:', ', '.join(map(str, player.hand)))
        print("Dealer's hand:", ', '.join(map(str, dealer.hand)))

        if first_move and player.hand_value == 21:
            print()
            print('You got blackjack! You win.')

            win_amount = math.ceil(player_bet * 3 / 2)
            win_chips = dealer.remove_chips(win_amount)
            player.chips += player_bet_chips + win_chips
            print(f'You win ${win_amount + player_bet}.')
            break

        choice = prompt_choice(['stay', 'hit'])
        print()
        if choice == 'stay':
            dealer_hand_value = dealer.hand_value
            player_hand_value = player.hand_value

            if dealer_hand_value == player_hand_value:
                print(
                    "It's a push. Both the dealer and you "
                    f'have the same hand value of {player_hand_value}.'
                )

                player.chips += player_bet_chips
                print(f'You get your ${player_bet} back.')
            elif player_hand_value > dealer_hand_value:
                print(
                    'You win! Your hand value is '
                    f"{player_hand_value} vs dealer's {dealer_hand_value}."
                )

                win_chips = dealer.remove_chips(player_bet)
                player.chips += player_bet_chips + win_chips
                print(f'You win ${player_bet * 2}.')
            else:
                print(
                    'You lose. Your hand value is '
                    f"{player_hand_value} vs dealer's {dealer_hand_value}."
                )
                print(f'You lose ${player_bet}.')
            break
        elif choice == 'hit':
            dealer.deal(deck, player, 'you')

            hand_value = player.hand_value
            if hand_value > 21:
                print()
                print(f'You have busted with hand value of {hand_value}.')
                break

        first_move = False

game()

while True:
    choice = prompt_choice(['play again', 'quit'])
    if choice == 'play again':
        print()
        game()
    elif choice == 'quit':
        break
