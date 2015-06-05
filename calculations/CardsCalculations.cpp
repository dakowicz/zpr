#include <string>
#include <vector>
#include <cstdlib>
#include <algorithm>
#include <cmath>
#include <boost/python.hpp>

class Card
{
    public:
        Card(std::string, std::string);
        Card();
        virtual ~Card();
        void setValues(std::string, std::string);
        std::string getFace();
        std::string getSuit();
        std::string getFace()const;
        std::string getSuit()const;
        bool operator==(const Card &);
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

std::string Card::getFace()
{
    return face;
}

std::string Card::getSuit()
{
    return suit;
}

std::string Card::getFace()const
{
    return face;
}

std::string Card::getSuit()const
{
    return suit;
}

bool Card::operator==(const Card &card)
{
    if(face != card.getFace())
        return false;
    if(suit != card.getSuit())
        return false;

    return true;
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
        if( cardsMatrix[i][12] && cardsMatrix[i][0] && cardsMatrix[i][1] && cardsMatrix[i][2] && cardsMatrix[i][3])
        {
            bestCardsValue[0] = -1;
            bestCardsValue[1] = 0;
            bestCardsValue[2] = 1;
            bestCardsValue[3] = 2;
            bestCardsValue[4] = 3;
            handRank = STRAIGHT_FLUSH;
            return true;
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
    if(faces[12] > 0 && faces[0] > 0 && faces[1] > 0 && faces[2] > 0 && faces[3] > 0)
    {
        bestCardsValue[0] = -1;
        bestCardsValue[1] = 0;
        bestCardsValue[2] = 1;
        bestCardsValue[3] = 2;
        bestCardsValue[4] = 3;
        handRank = STRAIGHT;
        return true;
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

void CreateMissingCards(std::vector<Card> &missingCards, std::vector<Card> &handCards, std::vector<Card> &tableCards)
{
    std::string faces[] = { "A", "K", "Q", "J", "10", "9", "8", "7", "6", "5", "4", "3", "2" };
    std::string suits[] = { "Hearts", "Diamonds", "Spades", "Clubs" };

    Card card;
    std::vector<Card>::iterator it;

    for(int i = 0; i < 4; ++i)
    {
        for(int j = 0; j < 13; ++j)
        {
            card.setValues(faces[j], suits[i]);
            missingCards.push_back(card);
        }
    }

    for(int i = 0; i < handCards.size(); ++i)
    {
        it = std::find(missingCards.begin(), missingCards.end(), handCards[i]);
        missingCards.erase(it);
    }

    for(int i = 0; i < tableCards.size(); ++i)
    {
        it = std::find(missingCards.begin(), missingCards.end(), tableCards[i]);
        missingCards.erase(it);
    }
}

boost::python::list CalculateProbability(boost::python::list handCards, boost::python::list tableCards, boost::python::object playersN, boost::python::object N)
{
    int iter = boost::python::extract<int>(N);

    int playersNumber = boost::python::extract<int>(playersN);
    if(playersNumber <= 1)
    {
        boost::python::list probability;
        probability.append(1);
        probability.append(0);
        probability.append(0);
        return probability;
    }

    int enemysNumber = playersNumber - 1;

    int handCardsSize = boost::python::extract<int>(handCards.attr("__len__")());
    int tableCardsSize = boost::python::extract<int>(tableCards.attr("__len__")());

    std::vector<Card> covered;
    std::vector<Card> exposed;

    std::vector<Card> cardsHand;
    std::vector<Card> cardsTable;

    std::vector<Card> cardsPlayer;
    std::vector<Card> cardsEnemy[enemysNumber];

    std::string cFace, cSuit;
    Card card;

    int winCounter = 0;
    int tieCounter = 0;
    int loseCounter = 0;

    std::srand(0);

    for(int i = 0; i < handCardsSize; ++i)
    {
        cFace = boost::python::extract<std::string>(handCards[i].attr("face"));
        cSuit = boost::python::extract<std::string>(handCards[i].attr("suit"));

        card.setValues(cFace, cSuit);
        cardsHand.push_back(card);
    }

    for(int i = 0; i < tableCardsSize; ++i)
    {
        cFace = boost::python::extract<std::string>(tableCards[i].attr("face"));
        cSuit = boost::python::extract<std::string>(tableCards[i].attr("suit"));

        card.setValues(cFace, cSuit);
        cardsTable.push_back(card);
    }

    CreateMissingCards(covered, cardsHand, cardsTable);

    int tableMissing;

    for(int i = 0; i < iter; ++i)
    {
        tableMissing = 5 - tableCardsSize;
        int index;

        for(int j = 0; j < tableCardsSize; ++j)
        {
            cardsPlayer.push_back(cardsTable[j]);
        
            for(int k = 0; k < enemysNumber; ++k)
                cardsEnemy[k].push_back(cardsTable[j]);
        }

        while(tableMissing != 0)
        {
            index = std::rand()%covered.size();

            exposed.push_back(covered[index]);
            cardsPlayer.push_back(covered[index]);

            for(int k = 0; k < enemysNumber; ++k)
                cardsEnemy[k].push_back(covered[index]);

            covered.erase(covered.begin() + index);
            --tableMissing;
        }

        for(int j = 0; j < handCardsSize; ++j)
        {
            cardsPlayer.push_back(cardsHand[j]);
            
            for(int k = 0; k < enemysNumber; ++k)
            {
                index = std::rand()%covered.size();

                exposed.push_back(covered[index]);
                cardsEnemy[k].push_back(covered[index]);

                covered.erase(covered.begin() + index);
            }
        }

        CardPackage cp1(cardsPlayer);
        CardPackage cp2[enemysNumber];
        for(int k = 0; k < enemysNumber; ++k)
            cp2[k].init(cardsEnemy[k]);

        cp1.calculateRank();
        for(int k = 0; k < enemysNumber; ++k)
            cp2[k].calculateRank();

        CardPackage *maxPointer = &cp2[0];
        for(int k = 1; k < enemysNumber; ++k)
        {
            if(cp2[k].getHandRank() > maxPointer->getHandRank())
                maxPointer = &cp2[k];
            else if(cp2[k].getHandRank() == maxPointer->getHandRank())
            {
                if(CompareHandsOfSameType(cp2[k], *maxPointer) == -1)
                    maxPointer = &cp2[k];
            }
        }


        if(cp1.getHandRank() > maxPointer->getHandRank())
            ++winCounter;
        else if(cp1.getHandRank() < maxPointer->getHandRank())
            ++loseCounter;
        else 
        {
            int wynik = CompareHandsOfSameType(cp1, *maxPointer);
            if(wynik == 1)
                ++loseCounter;
            else if(wynik == -1)
                ++winCounter;
            else
                ++tieCounter;
        }
        

        while(!exposed.empty())
        {
            covered.push_back(exposed.back());
            exposed.pop_back();
        }

        cardsPlayer.clear();
        for(int k = 0; k < enemysNumber; ++k)
            cardsEnemy[k].clear();
    }

    boost::python::list probability;
    probability.append((double)winCounter/(double)iter);
    probability.append((double)tieCounter/(double)iter);
    probability.append((double)loseCounter/(double)iter);

    return probability;
}


BOOST_PYTHON_MODULE(pokerCalculations)
{
    boost::python::def("compare_cards", CompareCards);
    boost::python::def("calculate_probability", CalculateProbability);
}