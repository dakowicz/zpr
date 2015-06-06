import time
import calculations.pokerCalculations
import core.controller as controller
from deck import Deck


class Game:
    """
        class implements game logic.
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
        """
            game main loop, ends if only one player left
        :return: nothing
        """
        self.start()
        while len(self.table.players) > 1:
            self.distribute_cards()
            self.calculate_probability()
            self.set_blinds()
            self.table.notify_players()
            self.auction()
            self.flop()
            self.auction()
            self.turn()
            self.auction()
            self.river()
            self.auction()
            self.showdown()
            self.deal_win()
            self.prepare_next_round()
            self.table.notify_players()

    def start(self):
        """
            does all things necessary before game
        :return: nothing
        """
        self.dealer = self.table.players[0]
        print 'Game started'
        self.prepare_next_round()

    def distribute_cards(self):
        """
            distributes two cards to all players
        :return: nothing
        """
        self.__distribute_players_one_card()
        self.__distribute_players_one_card()

    def set_blinds(self):
        """
            increases blinds if necessary and sets players' contributions if are on blinds
        :return: nothing
        """
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
        """
            auction loop - listen for players input and drop them out if they exceeded timeout
        :return: nothing
        """
        self.visited_players = 0
        while not self.is_auction_finished():
            self.visited_players += 1
            player = self.__get_player_with_turn()

            input_ready = player.get_ready_input_socket(self.table.TIMEOUT)

            if len(input_ready) == 0:
                print 'Player ' + player.name + ' removed - waited too long.'
                controller.pressed_leave(self.table, player)
            else:
                try:
                    message = player.get_input()
                    self.table.controller.serve_event(player, message['content'])
                except Exception as msg:
                    print msg
                    controller.pressed_leave(self.table, player)

        self.set_turn_after_auction()

    def is_auction_finished(self):
        """
            checks if auction should be finished
        :return: boolean
        """
        if self.not_folded_and_not_allin_players() == 0:
            return True
        elif self.not_folded_and_not_allin_players() == 1:
            for player in self.table.players:
                if not player.fold and not player.is_allin():
                    if player.contribution == self.max_contribution():
                        return True
                    else:
                        return False

        if self.visited_players >= self.not_folded_players():
            for player in self.table.players:
                if not player.fold and player.contribution != self.max_contribution():
                    return False
            return True
        else:
            return False

    def set_turn_after_auction(self):
        """
            set turn to player after dealer
        :return: nothing
        """
        self.__reset_turn()
        self.dealer.turn = True
        self.next_player_turn()

    def not_folded_and_not_allin_players(self):
        """
            returns number of players who has not folded and are not all in
        :return: integer
        """
        result = 0
        for player in self.table.players:
            if not player.fold and not player.is_allin():
                result += 1
        return result

    def not_folded_players(self):
        """
            returns number of players who has not folded
        :return: integer
        """
        result = 0
        for player in self.table.players:
            if not player.fold:
                result += 1
        return result

    def flop(self):
        """
            sets first three table cards
        :return: nothing
        """
        for i in range(3):
            self.tableCards.append(self.deck.get_card())
        self.calculate_probability()
        self.table.notify_players()

    def turn(self):
        """
            sets fourth table card
        :return: nothing
        """
        self.tableCards.append(self.deck.get_card())
        self.calculate_probability()
        self.table.notify_players()

    def river(self):
        """
            sets fifth table card
        :return: nothing
        """
        self.tableCards.append(self.deck.get_card())
        self.calculate_probability()
        self.table.notify_players()

    def showdown(self):
        """
            sends players message about opponent players
        :return: nothing
        """
        for player in self.table.players:
            if not player.fold:
                player.visible = True
        self.__reset_turn()
        self.table.notify_players()
        time.sleep(4)
        for player in self.table.players:
            player.visible = False

    def pot(self):
        """
            returns sum of all players contribution
        :return: integer
        """
        pot = 0
        for player in self.table.players:
            pot += player.contribution
        return pot

    def deal_win(self):
        """
            finds winners in a round and sets theirs win
        :return: nothing
        """
        winners = self.find_winner()
        if len(winners) == 1:
            winners[0].chips += self.pot()
        else:
            winners_contribution = self.__count_winners_contribution(winners)
            for winner in winners:
                winner.chips += self.pot() * winner.contribution / winners_contribution
        self.__reset_contributions()

    def find_winner(self):
        """
            finds winners in a round, uses C++ function to compare cards
        :return: list of Players
        """
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

        return winners

    def calculate_probability(self):
        for player in self.table.players:
            if player.fold:
                player.win_probability = 0.0
                player.draw_probability = 0.0
                player.loss_probability = 100.0
            else:
                probability = calculations.pokerCalculations.calculate_probability(player.get_cards(), self.tableCards, self.not_folded_players(), 10000)
                player.win_probability = probability[0] * 100
                player.draw_probability = probability[1] * 100
                player.loss_probability = probability[2] * 100

    def prepare_next_round(self):
        """
            does all necessary things before next round
        :return: nothing
        """
        self.round += 1
        self.__reset_fold()
        self.collect_cards()
        self.deck.shuffle()
        self.change_dealer()
        self.delete_leaving_players()
        self.delete_losers()
        self.set_player_turn()

    def collect_cards(self, player=None):
        """
            collects cards from player or table and players and add them to the deck
        :param player: Player (default = None)
        :return: nothing
        """
        if player:
            self.__return_cards(player)
        else:
            while len(self.tableCards) > 0:
                card = self.tableCards.pop()
                self.deck.collect_card(card)
            for player in self.table.players:
                self.__return_cards(player)

    def change_dealer(self):
        """
            set next player as a dealer
        :return: nothing
        """
        players_number = len(self.table.players)
        dealer_index = self.table.players.index(self.dealer)
        self.dealer = self.table.players[(dealer_index + 1) % players_number]
        self.set_player_turn()

    def delete_leaving_players(self):
        """
            removes all players, who decided to leave, from table
        :return: nothing
        """
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
        """
            removes all players, who have lost, from table
        :return: nothing
        """
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
        """
            sets player turn from which round will start
        :return: nothing
        """
        players_number = len(self.table.players)
        dealer_index = self.table.players.index(self.dealer)
        self.__reset_turn()
        if players_number == 2:
            self.table.players[dealer_index].turn = True
        else:
            self.table.players[(dealer_index + 3) % players_number].turn = True

    def max_contribution(self):
        """
            returns the biggest player contribution
        :return: integer
        """
        biggest_contribution = 0
        for player in self.table.players:
            if player.contribution > biggest_contribution:
                biggest_contribution = player.contribution
        return biggest_contribution

    def next_player_turn(self):
        """
            sets next player turn
        :return: nothing
        """
        player_with_turn = self.__get_player_with_turn()
        player_with_turn.turn = False
        if self.not_folded_and_not_allin_players() == 0:
            return

        index = self.table.players.index(player_with_turn)
        next_player = self.table.players[(index + 1) % len(self.table.players)]
        next_player.turn = True
        if next_player.fold or next_player.is_allin():
            self.next_player_turn()

    def __get_player_with_turn(self):
        """
            returns player with turn, raises exception if such does not exist
        :raise: Exception
        :return: Player
        """
        for player in self.table.players:
            if player.turn:
                return player
        raise Exception('None player has turn')

    def __reset_turn(self):
        """
            sets turn as False to all players
        :return: nothing
        """
        for player in self.table.players:
            player.turn = False

    def __reset_fold(self):
        """
            sets fold as False to all players
        :return: nothing
        """
        for player in self.table.players:
            player.fold = False

    def __reset_contributions(self):
        """
            sets contribution as 0 to all players
        :return: nothing
        """
        for player in self.table.players:
            player.contribution = 0

    def __count_winners_contribution(self, winners):
        """
            returns sum of given players contributions
        :param winners: list of Players
        :return: integer
        """
        winners_contribution = 0
        for winner in winners:
            winners_contribution += winner.contribution
        return winners_contribution

    def __distribute_players_one_card(self):
        """
            distribute all players one card
        :return: nothing
        """
        dealer_index = self.table.players.index(self.dealer)
        for player in self.table.players[dealer_index + 1: len(self.table.players)]:
            player.set_card(self.deck.get_card())
        for player in self.table.players[0: dealer_index + 1]:
            player.set_card(self.deck.get_card())

    def __return_cards(self, player):
        """
            collects cards from given player and add them to the deck
        :return: nothing
        """
        first_card, second_card = player.return_cards()
        if first_card is not None:
            self.deck.collect_card(first_card)
        if second_card is not None:
            self.deck.collect_card(second_card)