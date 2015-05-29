class Hand:
    def __init__(self):
        self.firstCard = None
        self.secondCard = None

    def return_cards(self):
        """
            removes and returns both cards from hand
        :return: Card, Card
        """
        first_card = self.firstCard
        second_card = self.secondCard
        self.firstCard = None
        self.secondCard = None
        return first_card, second_card

    def set_card(self, card):
        """
            adds card to hand, raises exception if hand already contains two cards
        :raise: Exception
        :param card: Card
        :return: nothing
        """
        if self.firstCard is None:
            self.firstCard = card
        elif self.secondCard is None:
            self.secondCard = card
        else:
            raise Exception('Already two cards on a hand')