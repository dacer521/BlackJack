import random


class Card:
    RANKS = (1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13)
    SUITS = ("Diamonds", "Hearts", "Spades", "Clubs")

    def __init__(self, rank, suit):
        self.rank = rank
        self.suit = suit.capitalize()

    def __str__(self):
        if self.rank == 1:
            return f"Ace of {self.suit}"
        elif self.rank == 11:
            return f"Jack of {self.suit}"
        elif self.rank == 12:
            return f"Queen of {self.suit}"
        elif self.rank == 13:
            return f"King of {self.suit}"
        else:
            return f"{self.rank} of {self.suit}"


class Deck:

    def __init__(self):
        self.cards = [Card(rank, suit) for suit in Card.SUITS for rank in Card.RANKS]
        self.shuffle()

    def shuffle(self):
        random.shuffle(self.cards)

    def deal(self):
        if self.cards:
            return self.cards.pop()
        else:
            return None  # Shouldn't happen in a single round of BlackJack

    def calcValue(self, hand):
        total = 0
        aces = 0

        for card in hand:
            if card.rank == 1:
                aces += 1
                total += 11
            elif card.rank in [11, 12, 13]:
                total += 10
            else:
                total += card.rank

        while total > 21 and aces:
            total -= 10
            aces -= 1

        return total


class BlackJack:

    def __init__(self, player):
        self.player = player
        self.deck = Deck()
        self.hand = [self.deck.deal(), self.deck.deal()]
        self.bust = False
        self.done = False

    def hit(self):
        dealt_card = self.deck.deal()
        self.hand.append(dealt_card)
        if self.player:
            print(f'You got dealt a {dealt_card}')
        if self.deck.calcValue(self.hand) > 21:
            self.bust = True
        return self.deck.calcValue(self.hand)

    def stand(self):
        self.done = True

    def eval(self, com, bet):
        player_val = self.deck.calcValue(self.hand)
        com_val = com.deck.calcValue(com.hand)

        print(f'Player total : {player_val}, House total : {com_val}')

        if self.bust and com.bust:
            return 'tie', 0
        elif self.bust and not com.bust:
            return 'com win', -bet
        elif com.bust and not self.bust:
            return 'player win', bet
        elif player_val > com_val:
            return 'player win', bet
        elif player_val < com_val:
            return 'com win', -bet
        else:
            return 'tie', 0


def game(player, com, bet):
    while True:
        print(f'Your total is {player.deck.calcValue(player.hand)}')
        action = input('Would you like to hit or stand? ').lower()
        if action == 'hit':
            player.hit()
            if player.bust:
                print("Player busts!")
                return 'com win', -bet
        if action == 'stand':
            player.stand()
            break

    while com.deck.calcValue(com.hand) <= 16 and not com.bust:
        com.hit()
        if com.bust:
            print("Computer busts!")
            return 'player win', bet

    return player.eval(com, bet)


def prtUI():
    print("Welcome to BlackJack")
    player_money = 1000
    print(f'You have ${player_money}')

    while player_money > 0:
        try:
            bet = int(input("How much would you like to bet? "))
            if bet <= 0 or bet > player_money:
                print("Invalid bet amount. Please bet within your limits.")
                continue

            player = BlackJack(True)
            com = BlackJack(False)

            print(f"Player's hand: {[str(card) for card in player.hand]}")
            print(f"Computer's visible hand: {com.hand[0]}")

            if player.deck.calcValue(player.hand) == 21:
                print("Player has Blackjack!")
                result, change = player.eval(com, bet)
            elif com.deck.calcValue(com.hand) == 21:
                print("Computer has Blackjack!")
                result, change = player.eval(com, bet)
            else:
                result, change = game(player, com, bet)

            print(result)
            player_money += change
            print(
                f"Player's money: ${player_money if player_money > 0 else 0}")
            if player_money <= 0:
                print("You're out of money! Game over.")
                break

            play_again = input("Do you want to walk away? (yes/no): ").lower()
            if play_again == 'yes':
                break

        except ValueError:
            print('Invalid input, please try again')


prtUI()
