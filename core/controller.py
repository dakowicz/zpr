# functions serving players' action


def can_start_game(table):
    """
        checks if all conditions are met to start a game
    :param table: Table
    :return: boolean
    """
    if len(table.players) < table.PLAYERS_MINIMUM:
        return False
    for player in table.players:
        if not player.ready:
            return False
    return True


def pressed_start(table, player):
    """
        serves action start
    :param table: Table
    :param player: Player
    :return: nothing
    """
    if not can_start(table, player):
        pressed_leave(table, player)
        return

    player.ready = True
    table.notify_players()


def pressed_leave(table, player):
    """
        serves action leave
    :param table: Table
    :param player: Player
    :return: nothing
    """
    if not table.started:
        table.remove_player(player)
    else:
        player.leaving = True
        pressed_fold(table, player)
        # no need to send notification - already sent in pressed_fold
    print 'Player ' + player.name + ' has left'


def pressed_check(table, player):
    """
        serves action check
    :param table: Table
    :param player: Player
    :return: nothing
    """
    if not can_check(table, player):
        pressed_leave(table, player)
        return
    table.game.next_player_turn()
    table.notify_players()


def pressed_bet(table, player, value):
    """
        serves action get
    :param table: Table
    :param player: Player
    :param value: integer
    :return: nothing
    """
    if not can_bet(table, player, value):
        pressed_leave(table, player)
        return
    player.add_to_pot(value)
    table.game.next_player_turn()
    table.notify_players()


def pressed_call(table, player):
    """
        serves action call
    :param table: Table
    :param player: Player
    :return: nothing
    """
    if not can_call(table, player):
        pressed_leave(table, player)
        return
    player.add_to_pot(table.game.max_contribution() - player.contribution)
    table.game.next_player_turn()
    table.notify_players()


def pressed_raise(table, player, value):
    """
        serves action raise
    :param table: Table
    :param player: Player
    :param value: integer
    :return: nothing
    """
    if not can_raise(table, player, value):
        pressed_leave(table, player)
        return
    player.add_to_pot(table.game.max_contribution() - player.contribution + value)
    table.game.next_player_turn()
    table.notify_players()


def pressed_fold(table, player):
    """
        serves action fold
    :param table: Table
    :param player: Player
    :return: nothing
    """
    if not can_fold(table, player):
        return
    player.fold = True
    table.game.visited_players -= 1
    table.game.next_player_turn()
    table.notify_players()

#
# functions checking if action is available for player
#


def can_start(table, player):
    """
        checks if action start is available for given player
    :param table: Table
    :param player: Player
    :return: boolean
    """
    if table.started or player.ready:
        return False
    else:
        return True


def can_check(table, player):
    """
        checks if action check is available for given player
    :param table: Table
    :param player: Player
    :return: boolean
    """
    if not table.started or not player.turn or player.fold:
        return False
    elif table.game.max_contribution() != player.contribution:
        return False
    else:
        return True


def can_bet(table, player, value):
    """
        checks if action bet is available for given player
    :param table: Table
    :param player: Player
    :return: boolean
    """
    if not can_check(table, player) or player.chips < value:
        return False
    elif player.chips == value:
        return True
    elif value < table.game.bigBlind:
        return False
    else:
        return True


def can_call(table, player):
    """
        checks if action call is available for given player
    :param table: Table
    :param player: Player
    :return: boolean
    """
    if not table.started or not player.turn or player.fold:
        return False
    else:
        return True


def can_raise(table, player, value):
    """
        checks if action raise is available for given player
    :param table: Table
    :param player: Player
    :return: boolean
    """
    if not table.started or not player.turn or player.fold:
        return False
    elif table.game.max_contribution() - player.contribution + value > player.chips:
        return False
    elif table.game.max_contribution() - player.contribution + value == player.chips:
        return True
    elif value < table.game.bigBlind:
        return False
    else:
        return True


def can_fold(table, player):
    """
        checks if action fold is available for given player
    :param table: Table
    :param player: Player
    :return: boolean
    """
    if not table.started or not player.turn:
        return False
    else:
        return True


class Controller:
    def __init__(self, table):
        self.table = table
        self.event = {
            'start': pressed_start,
            'leave': pressed_leave,
            'check': pressed_check,
            'bet':   pressed_bet,
            'call':  pressed_call,
            'raise': pressed_raise,
            'fold':  pressed_fold,
        }

    def serve_event(self, player, data):
        try:
            if data.count(' ') == 1:
                action, argument = data.split(' ', 1)
                self.event[action](self.table, player, int(argument))
            else:
                self.event[data](self.table, player)
        except KeyError:
            print 'Improper input from player \'' + player.name + '\''
            pressed_leave(self.table, player)
        except ValueError:
            print 'Improper input argument from player \'' + player.name + '\''
            pressed_leave(self.table, player)
        except TypeError:
            print 'Improper number of arguments from player \'' + player.name + '\''
            pressed_leave(self.table, player)
