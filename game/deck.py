import random
from card import Card


class Deck:
    DECK_SIZE = 52

    def __init__(self):
        self.deck = []
        for suit in Card.SUIT:
            for face in Card.FACE:
                self.deck.append(Card(face, suit))

    def shuffle(self):
        """
            shuffles deck, if all cards are not in the deck, raises exception
        :return: nothing
        """
        if len(self.deck) != self.DECK_SIZE:
            raise Exception('All cards have not been returned. ' + str(len(self.deck)) + ' cards in the deck.\n')
        else:
            random.shuffle(self.deck)

    def collect_card(self, card):
        """
            adds given card to deck, raises exception if given card is already in the deck
        :raise: raise exception if card is already in the deck
        :param card: card which will be inserted into deck
        :return: nothing
        """
        if card not in self.deck:
            self.deck.append(card)
        else:
            raise Exception('Card is already in the deck.\n')

    def get_card(self, position=0):
        """
            remove and return card on given position
        :param position:
        :return: removed card
        """
        card = self.deck[position]
        self.deck.pop(position)
        return card
