import calculations.pokerCalculations
import core.controller as controller
from deck import Deck


class Game:
    """
        class implements game logic
    """
    STARTING_SMALL_BLIND = 1
    STARTING_BIG_BLIND = 2
    STARTING_CHIPS = 1000

    def __init__(self, table):
        self.table = table
        self.deck = Deck()
        self.dealer = None
        self.tableCards = []
        self.smallBlind = self.STARTING_SMALL_BLIND
        self.bigBlind = self.STARTING_BIG_BLIND
        self.visited_players = 0
        self.round = 0

    def game_loop(self):
        self.start()
        while len(self.table.players) > 1:
            self.distribute_cards()
            self.set_blinds()
            self.table.notify_players()
            self.auction()
            self.flop()
            self.auction()
            self.turn()
            self.auction()
            self.river()
            self.auction()
            self.deal_win()
            self.prepare_next_round()
            self.table.notify_players()

    def start(self):
        self.dealer = self.table.players[0]
        print 'Game started'
        self.prepare_next_round()

    def distribute_cards(self):
        self.__distribute_players_one_card(self.dealer)
        self.__distribute_players_one_card(self.dealer)

    def set_blinds(self):
        dealer_index = self.table.players.index(self.dealer)
        players_number = len(self.table.players)
        if self.round % 5 == 0:
            self.smallBlind *= 2
            self.bigBlind *= 2
        if players_number == 2:
            self.table.players[dealer_index].add_to_pot(self.smallBlind)
            self.table.players[(dealer_index + 1) % players_number].add_to_pot(self.bigBlind)
        else:
            self.table.players[(dealer_index + 1) % players_number].add_to_pot(self.smallBlind)
            self.table.players[(dealer_index + 2) % players_number].add_to_pot(self.bigBlind)

    def auction(self):
        self.visited_players = 0
        while not self.auction_end():
            self.visited_players += 1
            player = self.__get_player_with_turn()
            if player.leaving:
                controller.pressed_fold(self, player)
                continue
            if player.fold:
                self.visited_players -= 1
                self.next_player_turn()
                continue
            if player.is_allin():
                self.next_player_turn()
                continue

            timeout = 1120.0
            input_ready = player.get_ready_input_socket(timeout)

            if len(input_ready) == 0:
                print player.name + ' waited too long'
                controller.pressed_leave(self, player)
                continue

            message = player.get_input()
            self.table.controller.serve_event(player, message['content'])

        self.set_turn_after_auction()

    def auction_end(self):
        if self.auction_participants() == 0:
            return True
        elif self.auction_participants() == 1:
            for player in self.table.players:
                if not player.fold and not player.is_allin() and player.contribution == self.max_contribution():
                    return True
                else:
                    return False

        if self.visited_players >= self.active_players():
            for player in self.table.players:
                if not player.fold and player.contribution != self.max_contribution():
                    return False
            return True
        else:
            return False

    def set_turn_after_auction(self):
        for player in self.table.players:
            player.turn = False
        self.dealer.turn = True
        self.next_player_turn()

    def auction_participants(self):
        auction_participants_number = 0
        for player in self.table.players:
            if not player.fold and not player.is_allin():
                auction_participants_number += 1
        return auction_participants_number

    def active_players(self):
        active_players_number = 0
        for player in self.table.players:
            if not player.fold:
                active_players_number += 1
        return active_players_number

    def flop(self):
        for i in range(3):
            self.tableCards.append(self.deck.get_card())
        self.table.notify_players()

    def turn(self):
        self.tableCards.append(self.deck.get_card())
        self.table.notify_players()

    def river(self):
        self.tableCards.append(self.deck.get_card())
        self.table.notify_players()

    def pot(self):
        pot = 0
        for player in self.table.players:
            pot += player.contribution
        return pot

    def deal_win(self):
        winners = self.find_winner()
        if len(winners) == 1:
            winners[0].chips += self.pot()
        else:
            winners_contribution = self.__count_winners_contribution(winners)
            for winner in winners:
                winner.chips += self.pot() * winner.contribution / winners_contribution
        self.__reset_contributions()

    def find_winner(self):
        players_and_theirs_cards = []
        for player in self.table.players:
            if not player.fold:
                player_cards = []
                player_cards.extend(player.get_cards())
                player_cards.extend(self.tableCards)
                players_and_theirs_cards.append((player, player_cards))

        if len(players_and_theirs_cards) == 0:
            raise Exception('No players compete')

        players_and_theirs_cards.sort(calculations.pokerCalculations.compare_cards, key=lambda pair: pair[1])
        winners = []
        for player_and_cards in players_and_theirs_cards:
            if calculations.pokerCalculations.compare_cards(players_and_theirs_cards[0][1], player_and_cards[1]) == 0:
                winners.append(player_and_cards[0])
            else:
                break

        for player in winners:
            print player.name
        return winners

    def prepare_next_round(self):
        self.round += 1
        self.__reset_fold()
        self.collect_cards()
        self.deck.shuffle()
        self.change_dealer()
        self.delete_leaving_players()
        self.delete_losers()
        self.set_player_turn()

    def collect_cards(self, player=None):
        if player:
            self.__return_cards(player)
        else:
            while len(self.tableCards) > 0:
                card = self.tableCards.pop()
                self.deck.collect_card(card)
            for player in self.table.players:
                self.__return_cards(player)

    def change_dealer(self):
        players_number = len(self.table.players)
        dealer_index = self.table.players.index(self.dealer)
        self.dealer = self.table.players[(dealer_index + 1) % players_number]
        self.set_player_turn()

    def delete_leaving_players(self):
        i = 0
        while i < len(self.table.players):
            player = self.table.players[i]
            i += 1
            if player.leaving:
                if player is self.dealer:
                    self.change_dealer()
                self.table.remove_player(player)
                i -= 1

    def delete_losers(self):
        i = 0
        while i < len(self.table.players):
            player = self.table.players[i]
            i += 1
            if player.chips == 0:
                if player is self.dealer:
                    self.change_dealer()
                self.table.remove_player(player)
                i -= 1

    def set_player_turn(self):
        players_number = len(self.table.players)
        dealer_index = self.table.players.index(self.dealer)
        for player in self.table.players:
            player.turn = False
        if players_number == 2:
            self.table.players[dealer_index].turn = True
        else:
            self.table.players[(dealer_index + 3) % players_number].turn = True

    def max_contribution(self):
        biggest_contribution = self.bigBlind
        for player in self.table.players:
            if player.contribution > biggest_contribution:
                biggest_contribution = player.contribution
        return biggest_contribution

    def next_player_turn(self):
        player_with_turn = self.__get_player_with_turn()
        player_with_turn.turn = False
        if self.auction_participants() == 0:
            return

        index = self.table.players.index(player_with_turn)
        next_player = self.table.players[(index + 1) % len(self.table.players)]
        next_player.turn = True
        if next_player.fold or next_player.is_allin():
            self.next_player_turn()

    def __get_player_with_turn(self):
        for player in self.table.players:
            if player.turn:
                return player
        raise Exception('None player has turn')

    def __reset_fold(self):
        for player in self.table.players:
            player.fold = False

    def __reset_contributions(self):
        for player in self.table.players:
            player.contribution = 0

    def __count_winners_contribution(self, winners):
        winners_contribution = 0
        for winner in winners:
            winners_contribution += winner.contribution
        return winners_contribution

    def __distribute_players_one_card(self, dealer):
        dealer_index = self.table.players.index(dealer)
        for player in self.table.players[dealer_index + 1: len(self.table.players)]:
            player.set_card(self.deck.get_card())
        for player in self.table.players[0: dealer_index + 1]:
            player.set_card(self.deck.get_card())

    def __return_cards(self, player):
        first_card, second_card = player.return_cards()
        if first_card is not None:
            self.deck.collect_card(first_card)
        if second_card is not None:
            self.deck.collect_card(second_card)