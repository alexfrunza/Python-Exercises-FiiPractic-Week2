"""
    Implement a Poker Game using OOP principles:
        Use classes such as Card, Player, Deck etc. Up to you to
        decide the game complexity/features number
"""
import random


class InsufficientFunds(Exception):
    pass


class InvalidBet(Exception):
    pass


class InvalidOption(Exception):
    pass


# Playing Card class
class PlayingCard:
    def __init__(self, color, french, rank):
        self.color = color
        self.french = french
        self.rank = rank

    def __str__(self):
        return f"{self.rank} {self.color} {self.french}"


# Player class
class Player:
    def __init__(self, username, balance):
        self.username = username
        self.balance = balance
        self.hand = []
        self.status = "ready"
        self.spectate = False

    def __str__(self):
        return self.username

    def show_hand(self):
        for card in self.hand:
            print(card)

    def withdraw_money(self, amount):
        self.balance -= amount

    # Make a player ready
    def reset_status(self):
        self.status = 'ready'

    def check(self, game):
        if game.round_bet:
            raise InvalidOption
        self.status = "checked"

    def bet(self, game, amount=None):
        # Error handling
        if amount is None:
            raise InvalidOption

        amount = int(amount)
        if amount <= 0:
            raise InvalidBet
        elif self.balance < amount:
            raise InsufficientFunds

        game.take_money_from_a_player(self, amount)
        game.round_bet = amount
        game.player_who_betted = self

    def call(self, game):
        # Error handling
        if not game.round_bet:
            raise InvalidOption
        elif self.balance < game.round_bet:
            raise InsufficientFunds

        game.take_money_from_a_player(self, game.round_bet)

    def fold(self, game):
        self.spectate = True
        print(f"{self.username} it's out\n")


# Cards Deck class
class CardsDeck:
    def __init__(self):
        # Create a classic 52 cards pack
        cards_rank = ([i for i in range(2, 11)] + ["Ace", "Jack", "Queen", "King"]) * 4
        cards_color = ['Black', "Red"] * 26
        cards_french = ["Clubs", "Diamonds", "Spades", "Hearts"] * 13

        self._cards = [PlayingCard(color, french, rank) for rank, color, french in
                       zip(cards_rank, cards_color, cards_french)]

        # Shuffle the pack for every game to be different
        self.shuffle_cards()

    def __str__(self):
        return "A classic 52 cards pack"

    # Take a card from deck
    def draw_a_card(self):
        return self._cards.pop()

    def shuffle_cards(self):
        random.shuffle(self._cards)


class PokerTexasHoldem:
    def __init__(self, players, bet):
        self._status = 'on-going'
        self.prize = 0
        self._card_deck = CardsDeck()
        self.round = 1
        self.common_cards = []
        self.players = players
        self.round_bet = 0
        self.player_who_betted = None

        # Draw the common cards
        for _ in range(3):
            self.increment_common_cards()

        # Take initial bet from players and draw their 2 cards
        for player in self.players:
            self.take_money_from_a_player(player, bet)
            player.hand.append(self._card_deck.draw_a_card())
            player.hand.append(self._card_deck.draw_a_card())

    def __str__(self):
        return f"A Texas Hold'em Poker game with {', '.join([str(player) for player in self.players])}"

    def increment_common_cards(self):
        self.common_cards.append(self._card_deck.draw_a_card())

    def take_money_from_a_player(self, player, amount):
        player.withdraw_money(amount)
        self.prize += amount

    def reset_players_status(self):
        for player in self.players:
            player.reset_status()

    @property
    def active_players(self):
        return list(filter(lambda p: True if not p.spectate else False, self.players))

    @property
    def game_can_continue(self):
        return False not in map(lambda player: player.status == "checked" or player.spectate, self.players)

    @property
    def status(self):
        return self._status

    def end_game(self, winner=None):
        self._status = 'finished'

        if not winner:
            # Algorithm to see which hand are better
            winner = random.choice(self.active_players)

        winner.balance += self.prize
        print(f"{winner.username} won {self.prize} coins!")

        for player in self.players:
            print(f"{player.username}'s balance: {player.balance}")


# --------------------------------------------------------------------
# Tests


# Players
player1 = Player('player1', 1000)
player2 = Player('player2', 1000)
player3 = Player('player3', 1000)

players_list = [player1, player2, player3]
minimum_bet = 800

# Verify if players have at least minimum bet in their balance
accepted_players = [player for player in players_list if player.balance >= minimum_bet]

# Create a new poker game with players that have money
poker_game = PokerTexasHoldem(accepted_players, minimum_bet)


# Start game
while poker_game.status == 'on-going':

    print(f"Current game prize: {poker_game.prize}\n")

    # After first round the dealer draw a card and put it on table
    if poker_game.round > 2:
        poker_game.increment_common_cards()

    # After pre-flop show common cards
    if poker_game.round > 1:
        print("Common Cards: ")
        for common_card in poker_game.common_cards:
            print(common_card)
        print()

    # Verify if players made an action this round
    # Otherwise ask them to do something
    while not poker_game.game_can_continue:
        if poker_game.status == 'finished':
            break

        for player in poker_game.players:

            if len(poker_game.active_players) == 1:
                poker_game.end_game(poker_game.active_players[0])
                break

            if not player.spectate:
                print(f"{player.username}'s balance: {player.balance}")
                print(f'{player.username}\'s cards: ')
                player.show_hand()

                if poker_game.player_who_betted == player:
                    poker_game.round_bet = 0

                # Ask a player for an action until they made a valid one
                while True:
                    bid = None
                    instruction_args = [poker_game]

                    if poker_game.round_bet == 0:
                        player_instruction = input("Action (Check/Bet/Fold): ")
                        player_instruction = player_instruction.lower()
                        if player_instruction == 'bet':
                            bid = input("Amount: ")
                            instruction_args.append(bid)
                    else:
                        player_instruction = input("Action (Call/Fold): ")
                        player_instruction = player_instruction.lower()

                    try:
                        if bool({player_instruction} & {"check", "bet", "fold", "call"}):
                            getattr(player, player_instruction)(*instruction_args)
                            break
                        else:
                            raise AttributeError
                    except InvalidBet:
                        print("Your bet is invalid!")
                    except InsufficientFunds:
                        print("You have insufficient funds!")
                    except InvalidOption:
                        print("You can't do that option now!")
                    except ValueError:
                        print("Your bet must be an integer!")
                    except AttributeError:
                        print("Your action is invalid!")

                print()

    if len(poker_game.active_players) == 1 and poker_game.status == 'on-going':
        poker_game.end_game(poker_game.active_players[0])
    # After 4 rounds end game
    if poker_game.round == 4:
        poker_game.end_game()

    print(
        '\n'
        f'End of {poker_game.round} round\n'
        '#############################################\n'
    )

    # Make players ready for the next round
    poker_game.reset_players_status()
    # Increment round numbers
    poker_game.round += 1
