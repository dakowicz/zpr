class Card:
    SUIT = ('Hearts', 'Diamonds', 'Clubs', 'Spades')
    FACE = ('2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K', 'A')

    def __init__(self, face, suit):
        self.face = face
        self.suit = suit

    def __str__(self):
        if self.face is None and self.suit is None:
            return None
        else:
            return self.face + ' ' + self.suit