import json
import game
import hand
import select
import time
from core.server import Server


class Player:
    def __init__(self, name, (socket, address)):
        self.name = name
        self.socket = socket
        self.address = address
        self.chips = game.Game.STARTING_CHIPS
        self.hand = hand.Hand()
        self.contribution = 0
        self.win_probability = 0.0
        self.draw_probability = 0.0
        self.loss_probability = 0.0
        self.visible = False
        self.fold = False
        self.ready = False
        self.leaving = False
        self.turn = False
        self.arrival_time = time.time()

    def get_input(self):
        """
            reads data from socket
        :return: string
        """
        return json.loads(self.recv_data(self.socket))

    def get_ready_input_socket(self, timeout):
        """
            wait until players socket received data or timeout was exceeded
        :param timeout: float
        :return: list of sockets
        """
        waiting_time = 0.0
        input_ready = []
        while waiting_time < timeout:
            input_ready, output_ready, except_ready = select.select([self.socket], [], [], 2.0)
            waiting_time += 2.0
            if len(input_ready) != 0:
                break
        return input_ready

    def send(self, message):
        """
            send data to client
        :param message: primary type (dictionary)
        :return: nothing
        """
        self.socket.send(json.dumps(message))

    def add_to_pot(self, value):
        """
            adds players chips to pot
        :param value: integer
        :return: nothing
        """
        try:
            self.__add_contribution(value)
        except Exception:
            self.__add_contribution(self.chips)

    def is_allin(self):
        """
            checks if player added all his chips to pot
        :return: boolean
        """
        if self.chips == 0 and self.contribution > 0:
            return True
        else:
            return False

    def return_cards(self):
        """
            removes and returns player hand
        :return: Card, Card
        """
        return self.hand.return_cards()

    def set_card(self, card):
        """
            adds card to player hand
        :param card: Card
        :return: nothing
        """
        self.hand.set_card(card)

    def get_cards(self):
        """
            returns players hand (two cards)
        :return: list of Cards
        """
        return [self.hand.firstCard, self.hand.secondCard]

    def info(self):
        """
            returns string containing information about player
        :return: string
        """
        information = self.name + ' '
        if not self.visible:
            information += 'None None'
        else:
            information += str(self.hand.firstCard) + ' ' + str(self.hand.secondCard)
        return information + ' ' + str(self.ready) + ' ' + str(self.turn) + ' ' + str(self.fold) + ' ' + str(self.chips) + ' ' + str(self.contribution)

    def __add_contribution(self, contribution):
        """
            sets players contribution or raises exception if player has not enough chips
        :raise: Exception
        :param contribution: integer
        :return: nothing
        """
        if self.chips >= contribution:
            self.contribution += contribution
            self.chips -= contribution
        else:
            raise Exception('Player ' + self.name + ' do not have enough chips')


        """
                method decodes receive data from HTML WebSocket client
            :return: nothing
            """
    def recv_data (self,client):
        # as a simple server, we expect to receive:
        #    - all data at one go and one frame
        #    - one frame at a time
        #    - text protocol
        #    - no ping pong messages
        data = bytearray(client.recv(Server.package_size))

        print data

        if(len(data) < 6):
            raise Exception("Error reading data")
        # FIN bit must be set to indicate end of frame

        assert(0x1 == (0xFF & data[0]) >> 7)
        # data must be a text frame
        # 0x8 (close connection) is handled with assertion failure
        assert(0x1 == (0xF & data[0]))

        # assert that data is masked
        assert(0x1 == (0xFF & data[1]) >> 7)
        datalen = (0x7F & data[1])

        str_data = ''
        if(datalen > 0):
            mask_key = data[2:6]
            masked_data = data[6:(6+datalen)]
            unmasked_data = [masked_data[i] ^ mask_key[i%4] for i in range(len(masked_data))]
            str_data = str(bytearray(unmasked_data))
        print str_data
        return str_data