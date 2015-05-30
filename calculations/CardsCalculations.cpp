#include <iostream>
#include <string>
#include <vector>
#include <boost/python.hpp>

class Card
{
    public:
        Card(std::string, std::string);
        Card();
        virtual ~Card();
        void setValues(std::string, std::string);
        void print();
        std::string getFace();
        std::string getSuit();
    private:
        std::string face;
        std::string suit;
};

Card::Card(std::string cFace, std::string cSuit): face(cFace), suit(cSuit)
{

}

Card::Card()
{
    suit = "-";
    face = "-";
}

void Card::setValues(std::string cFace, std::string cSuit)
{
    suit = cSuit;
    face = cFace;
}

void Card::print()
{
    std::cout<<"Face: "<<face<<"\nSuit: "<<suit<<std::endl;
}

std::string Card::getFace()
{
    return face;
}

std::string Card::getSuit()
{
    return suit;
}

Card::~Card()
{

}

class CardPackage
{
    public:
        CardPackage();
        CardPackage(std::vector<Card>);
        virtual ~CardPackage();
        void init(std::vector<Card>);
        void calculateRank();
        int getHandRank();
        int getBestCardValue(int);
        enum HandRank
        {
            NO_TYPE, HIGH_CARD, ONE_PAIR, TWO_PAIRS, THREE_OF_A_KIND, STRAIGHT, FLUSH, FULL_HOUSE, FOUR_OF_A_KIND,
            STRAIGHT_FLUSH, ROYAL_STRAIGHT_FLUSH,
        };
    private:
        int bestCardsValue[5];
        bool cardsMatrix[4][13];
        int faces[13];
        int suits[4];
        HandRank handRank;
        bool isRoyalStraightFlush();
        bool isStraightFlush();
        bool isFourOfAKind();
        bool isFullHouse();
        bool isFlush();
        bool isStraight();
        bool isThreeOfAKind();
        bool isTwoPairs();
        bool isOnePair();
        bool isHighCard();
};

CardPackage::CardPackage()
{
    for(int i = 0; i < 4; ++i)
        for(unsigned j = 0; j < 13; ++j)
            cardsMatrix[i][j] = false;

    for(int i = 0; i < 4; ++i)
        suits[i] = 0;

    for(int i = 0; i < 13; ++i)
        faces[i] = 0;

    for(int i = 0; i < 5; ++i)
        bestCardsValue[i] = -1;

    handRank = NO_TYPE;
}

CardPackage::CardPackage(std::vector<Card> cards)
{
    for(int i = 0; i < 4; ++i)
        for(unsigned j = 0; j < 13; ++j)
            cardsMatrix[i][j] = false;

    for(int i = 0; i < 4; ++i)
        suits[i] = 0;

    for(int i = 0; i < 13; ++i)
        faces[i] = 0;

    for(int i = 0; i < 5; ++i)
        bestCardsValue[i] = -1;

    for(int i = 0; i < 7; ++i)
    {
        unsigned f,s;

        if( cards[i].getFace() == "A" )
            f = 12;
        else if( cards[i].getFace() == "K" )
            f = 11;
        else if( cards[i].getFace() == "Q" )
            f = 10;
        else if( cards[i].getFace() == "J" )
            f = 9;
        else if( cards[i].getFace() == "10" )
            f = 8;
        else if( cards[i].getFace() == "9" )
            f = 7;
        else if( cards[i].getFace() == "8" )
            f = 6;
        else if( cards[i].getFace() == "7" )
            f = 5;
        else if( cards[i].getFace() == "6" )
            f = 4;
        else if( cards[i].getFace() == "5" )
            f = 3;
        else if( cards[i].getFace() == "4" )
            f = 2;
        else if( cards[i].getFace() == "3" )
            f = 1;
        else
            f = 0;


        if( cards[i].getSuit() == "Hearts" )
            s = 3;
        else if( cards[i].getSuit() == "Diamonds" )
            s = 2;
        else if( cards[i].getSuit() == "Clubs" )
            s = 1;
        else
            s = 0;

        faces[f] = faces[f] + 1;
        suits[s] = suits[s] + 1;
        cardsMatrix[s][f] = true;
        handRank = NO_TYPE;
    }
}

void CardPackage::init(std::vector<Card> cards)
{
    for(int i = 0; i < 7; ++i)
    {
        unsigned f,s;

        if( cards[i].getFace() == "A" )
            f = 12;
        else if( cards[i].getFace() == "K" )
            f = 11;
        else if( cards[i].getFace() == "Q" )
            f = 10;
        else if( cards[i].getFace() == "J" )
            f = 9;
        else if( cards[i].getFace() == "10" )
            f = 8;
        else if( cards[i].getFace() == "9" )
            f = 7;
        else if( cards[i].getFace() == "8" )
            f = 6;
        else if( cards[i].getFace() == "7" )
            f = 5;
        else if( cards[i].getFace() == "6" )
            f = 4;
        else if( cards[i].getFace() == "5" )
            f = 3;
        else if( cards[i].getFace() == "4" )
            f = 2;
        else if( cards[i].getFace() == "3" )
            f = 1;
        else
            f = 0;


        if( cards[i].getSuit() == "Hearts" )
            s = 3;
        else if( cards[i].getSuit() == "Diamonds" )
            s = 2;
        else if( cards[i].getSuit() == "Clubs" )
            s = 1;
        else
            s = 0;

        faces[f] = faces[f] + 1;
        suits[s] = suits[s] + 1;
        cardsMatrix[s][f] = true;
    }
}

CardPackage::~CardPackage()
{

}

bool CardPackage::isRoyalStraightFlush()
{
    for(int i = 0; i < 4; ++i)
    {
        if( cardsMatrix[i][12] && cardsMatrix[i][11] && cardsMatrix[i][10] && cardsMatrix[i][9] && cardsMatrix[i][8] )
        {
            bestCardsValue[0] = 12;
            bestCardsValue[1] = 11;
            bestCardsValue[2] = 10;
            bestCardsValue[3] = 9;
            bestCardsValue[4] = 8;
            handRank = ROYAL_STRAIGHT_FLUSH;
            return true;
        }
    }
    return false;
}

bool CardPackage::isStraightFlush()
{
    for(int i = 0; i < 4; ++i)
    {
        if(suits[i] < 5)
            continue;

        unsigned counter = 0;

        for(int j = 12; j >= 0; --j)
        {
            if( cardsMatrix[i][j] )
            {
                if(++counter == 5)
                {
                    bestCardsValue[0] = j+4;
                    bestCardsValue[1] = j+3;
                    bestCardsValue[2] = j+2;
                    bestCardsValue[3] = j+1;
                    bestCardsValue[4] = j;
                    handRank = STRAIGHT_FLUSH;
                    return true;
                }
            }
            else
                counter = 0;
        }
    }
    return false;
}

bool CardPackage::isFourOfAKind()
{
    for(int i = 12; i >= 0; --i)
    {
        if( faces[i] == 4 )
        {
            bestCardsValue[0] = bestCardsValue[1] = bestCardsValue[2] = bestCardsValue[3] = i;
            faces[i] = 0;
            for(int k = 12; k >= 0; --k)
            {
                if(faces[k] > 0)
                {
                    bestCardsValue[4] = k;
                    break;
                }
            }
            handRank = FOUR_OF_A_KIND;
            return true;
        }
    }
    return false;
}

bool CardPackage::isFullHouse()
{
    bool isThree = false;
    bool isTwo = false;

    for(int i = 12; i >= 0; --i)
    {
        if( !isThree && faces[i] == 3)
        {
            isThree = true;
            bestCardsValue[0] = bestCardsValue[1] = bestCardsValue[2] = i;
        }
        else if( !isTwo && faces[i] == 2)
        {
            isTwo = true;
            bestCardsValue[3] = bestCardsValue[4] = i;
        }

        if(isThree && isTwo)
        {
            handRank = FULL_HOUSE;
            return true;
        }
    }
    return false;
}

bool CardPackage::isFlush()
{
    for(int i = 0; i < 4; ++i)
    {
        if(suits[i] >= 5)
        {
            int counter = 0;
            for(int j = 12; j >= 0; --j)
            {
                if( cardsMatrix[i][j] )
                {
                    bestCardsValue[counter++] = j;
                    if(counter == 5)
                        break;
                }
            }
            handRank = FLUSH;
            return true;
        }
    }
    return false;
}

bool CardPackage::isStraight()
{
    int counter = 0;
    for(int i = 12; i >= 0; --i)
    {
        if(faces[i] > 0)
        {
            if( ++counter == 5 )
            {
                bestCardsValue[0] = i+4;
                bestCardsValue[1] = i+3;
                bestCardsValue[2] = i+2;
                bestCardsValue[3] = i+1;
                bestCardsValue[4] = i;
                handRank = STRAIGHT;
                return true;
            }
        }
        else
            counter = 0;
    }
    return false;
}

bool CardPackage::isThreeOfAKind()
{
    for(int i = 12; i >= 0; --i)
    {
        if(faces[i] == 3)
        {
            bestCardsValue[0] = bestCardsValue[1] = bestCardsValue[2] = i;
            faces[i] = 0;
            int counter = 3;
            for(int j = 12; j >= 0; --j)
            {
                if(faces[j] > 0)
                {
                    for(int k = 0; k < faces[j]; ++k)
                    {
                        bestCardsValue[counter++] = j;
                        if(counter == 5)
                        {
                            handRank = THREE_OF_A_KIND;
                            return true;
                        }
                    }
                }
            }
        }
    }
    return false;
}

bool CardPackage::isTwoPairs()
{
    bool firstPair = false;
    bool secondPair = false;

    for(int i = 12; i >= 0; --i)
    {
        if(!firstPair && faces[i] == 2)
        {
            firstPair = true;
            bestCardsValue[0] = bestCardsValue[1] = i;
        }
        else if(!secondPair && faces[i] == 2)
        {
            secondPair = true;
            bestCardsValue[2] = bestCardsValue[3] = i;
        }

        if(firstPair && secondPair)
        {
            faces[bestCardsValue[0]] = 0;
            faces[bestCardsValue[2]] = 0;
            for(int j = 12; j >= 0; --j)
            {
                if(faces[j] > 0)
                {
                    bestCardsValue[4] = j;
                    break;
                }
            }
            handRank = TWO_PAIRS;
            return true;
        }
    }
    return false;
}

bool CardPackage::isOnePair()
{
    for(int i = 12; i >= 0; --i)
    {
        if(faces[i] == 2)
        {
            bestCardsValue[0] = bestCardsValue[1] = i;
            int counter = 2;
            faces[i] = 0;
            for(int j = 12; j >= 0; --j)
            {
                if(faces[j] > 0)
                {
                    for(int k = 0; k < faces[j]; ++k)
                    {
                        bestCardsValue[counter++] = j;
                        if(counter == 5)
                        {
                            handRank = ONE_PAIR;
                            return true;
                        }
                    }
                }
            }
        }
    }
    return false;
}

bool CardPackage::isHighCard()
{
    int counter = 0;
    for(int i = 12; i >= 0; --i)
    {
        if(faces[i] > 0 )
        {
            for(int j = 0; j < faces[i]; ++j)
            {
                bestCardsValue[counter++] = i;
                if(counter == 5)
                {
                    handRank = HIGH_CARD;
                    return true;
                }
            }
        }
    }
    return false;
}

void CardPackage::calculateRank()
{
    if(isRoyalStraightFlush()) return;
    if(isStraightFlush()) return;
    if(isFourOfAKind()) return;
    if(isFullHouse()) return;
    if(isFlush()) return;
    if(isStraight()) return;
    if(isThreeOfAKind()) return;
    if(isTwoPairs()) return;
    if(isOnePair()) return;
    if(isHighCard()) return;
}

int CardPackage::getHandRank()
{
    return handRank;
}

int CardPackage::getBestCardValue(int index)
{
    return bestCardsValue[index];
}

int CompareHandsOfSameType(CardPackage &cp1, CardPackage &cp2)
{
    for( int i = 0; i < 5; ++i)
    {
        if( cp1.getBestCardValue(i) > cp2.getBestCardValue(i) )
            return -1;
        else if( cp1.getBestCardValue(i) < cp2.getBestCardValue(i) )
            return 1;
    }
    return 0;
}

boost::python::object CompareCards(boost::python::list set1, boost::python::list set2)
{
    int set1len = boost::python::extract<int>(set1.attr("__len__")());
    int set2len = boost::python::extract<int>(set2.attr("__len__")());

    std::vector<Card> v1, v2;
    std::string cFace, cSuit;
    Card card;
    CardPackage cp1, cp2;
    int result;

    for(int i = 0; i < set1len; ++i)
    {
        cFace = boost::python::extract<std::string>(set1[i].attr("face"));
        cSuit = boost::python::extract<std::string>(set1[i].attr("suit"));

        card.setValues(cFace, cSuit);
        v1.push_back(card);
    }

    for(int i = 0; i < set2len; ++i)
    {
        cFace = boost::python::extract<std::string>(set2[i].attr("face"));
        cSuit = boost::python::extract<std::string>(set2[i].attr("suit"));

        card.setValues(cFace, cSuit);
        v2.push_back(card);
    }

    cp1.init(v1);
    cp2.init(v2);

    cp1.calculateRank();
    cp2.calculateRank();

    if( cp1.getHandRank() > cp2.getHandRank() )
        result = -1;
    else if( cp1.getHandRank() < cp2.getHandRank() )
        result =  1;
    else
        result = CompareHandsOfSameType( cp1, cp2 );

    boost::python::object pyObject(result);
    return pyObject;
}


BOOST_PYTHON_MODULE(pokerCalculations)
{
    boost::python::def("compare_cards", CompareCards);
}
