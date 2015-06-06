#!/usr/bin/python
import os.path
import sys
sys.path.append(os.path.pardir)
import pokerCalculations
    from game.card import Card


H2 = Card("2", "Hearts")
D2 = Card("2", "Diamonds")
C2 = Card("2", "Clubs")
S2 = Card("2", "Spades")

H3 = Card("3", "Hearts")
D3 = Card("3", "Diamonds")
C3 = Card("3", "Clubs")
S3 = Card("3", "Spades")

H4 = Card("4", "Hearts")
D4 = Card("4", "Diamonds")
C4 = Card("4", "Clubs")
S4 = Card("4", "Spades")

H5 = Card("5", "Hearts")
D5 = Card("5", "Diamonds")
C5 = Card("5", "Clubs")
S5 = Card("5", "Spades")

H6 = Card("6", "Hearts")
D6 = Card("6", "Diamonds")
C6 = Card("6", "Clubs")
S6 = Card("6", "Spades")

H7 = Card("7", "Hearts")
D7 = Card("7", "Diamonds")
C7 = Card("7", "Clubs")
S7 = Card("7", "Spades")

H8 = Card("8", "Hearts")
D8 = Card("8", "Diamonds")
C8 = Card("8", "Clubs")
S8 = Card("8", "Spades")

H9 = Card("9", "Hearts")
D9 = Card("9", "Diamonds")
C9 = Card("9", "Clubs")
S9 = Card("9", "Spades")

H10 = Card("10", "Hearts")
D10 = Card("10", "Diamonds")
C10 = Card("10", "Clubs")
S10 = Card("10", "Spades")

HJ = Card("J", "Hearts")
DJ = Card("J", "Diamonds")
CJ = Card("J", "Clubs")
SJ = Card("J", "Spades")

HQ = Card("Q", "Hearts")
DQ = Card("Q", "Diamonds")
CQ = Card("Q", "Clubs")
SQ = Card("Q", "Spades")

HK = Card("K", "Hearts")
DK = Card("K", "Diamonds")
CK = Card("K", "Clubs")
SK = Card("K", "Spades")

HA = Card("A", "Hearts")
DA = Card("A", "Diamonds")
CA = Card("A", "Clubs")
SA = Card("A", "Spades")

errors = 0
corrects = 0

""" pair of K """
pair1 = [HA,SK,D10,DK,H2,H4,S5]
""" pair of 10 """
pair2 = [S5,D10,H10,SJ,CQ,S7,H3]
""" pair of 3 """
pair3 = [S5,C7,H3,S3,H2,CQ,DK]
""" pair of J """
pair4 = [CK,DJ,S6,SJ,H3,S5,H10]
""" pair of K """
pair5 = [SK,S9,D6,S4,HK,D3,D7]
""" two pairs: K, 10 """
two_p1 = [SK,HK,H10,C10,S7,D3,S2]
""" two pairs: D, 3 """
two_p2 = [SQ,HQ,H3,C10,S7,D3,S2]
""" two pairs: 5, 7 """
two_p3 = [S5,H5,H7,C10,S7,D3,S2]
""" two pairs: D, 8 """
two_p4 = [SQ,HQ,H10,C8,S8,D3,S2]
""" two pairs: D, 8 """
two_p5 = [SK,H8,H10,CQ,S7,DQ,S8]
""" two pairs: 5, 7 """
two_p6 = [S5,H5,H7,C10,S7,D3,S3]
""" high card: A """
high_card1 = [SA,DJ,H6,S3,C6,C8,H2]
""" high card: 9 """
high_card2 = [S9,D2,H6,S3,C4,C8,H7]
""" hifh card: Q """
high_card3 = [CQ,S4,H5,CJ,S7,C2,H6]
""" three of a kind: A """
three1 = [CA,SA,HK,C5,S8,DA,H9]
""" three of a kind: K """
three2 = [CK,SK,HK,C5,S8,H2,H9]
""" three of a kind: 3 """
three3 = [C3,SK,H3,C5,S3,H2,H9]
""" three of a kind: 3 """
three4 = [C3,SK,H3,C5,S3,H2,HQ]
""" straight: A,K,Q,J,10 """
str1 = [SA,HJ,C6,H7,S10,DQ,DK]
""" straight: 4,5,6,7,8 """
str2 = [S4,H5,C6,H7,S8,DQ,DK]
""" straight: 6,7,8,9,10 """
str3 = [S9,H10,C6,H7,S8,DQ,DK]
""" flush: Hearts with hifh K """
flush1 = [H3,H6,H8,H9,D4,HK,C5]
""" flush: Diamonds with high J """
flush2 = [D7,D4,D2,DJ,D9,C7,C2]
""" flush: Diamonds with high A """
flush3 = [D4,D7,DA,D9,D3,C4,H4]
""" full House: JJJ,44 """
fullh1 = [SJ,CJ,HJ,H4,C4,S2,S8]
""" full House: 333,KK """
fullh2 = [S3,C3,H3,H4,CK,SK,S8]
""" full House: 333,55 """
fullh3 = [S3,C3,H3,H4,C5,S2,S5]
""" four of a kind: 5 """
four1 = [S5,C5,D5,H5,C5,C3,H2]
""" four of a kind: 7 """
four2 = [S7,C7,D7,H7,C5,C3,H2]
""" four of a kind: 7 """
four3 = [S7,C7,D7,H7,CK,C3,H2]
""" straight flush: 5,6,7,8,9 """
strfl1 = [S5,S6,S7,S8,S9,HQ,H2]
""" straight flush: 8,9,10,J,Q """
strfl2 = [S8,S9,S10,SJ,SQ,HQ,H2]
""" royal straight flush """
royal1 = [HA,HK,HQ,HJ,H10,C4,C7]





if pokerCalculations.compare_cards(pair3, pair1) != 1:
print "error in comparison: 1"
errors = errors + 1
if pokerCalculations.compare_cards(pair4, pair5) != 1:
print "error in comparison: 2"
errors = errors + 1
if pokerCalculations.compare_cards(pair2, pair4) != 1:
print "error in comparison: 3"
errors = errors + 1
if pokerCalculations.compare_cards(pair5, pair1) != 1:
print "error in comparison: 4"
errors = errors + 1
if pokerCalculations.compare_cards(two_p3, two_p2) != 1:
print "error in comparison: 5"
errors = errors + 1
if pokerCalculations.compare_cards(two_p5, two_p2) != -1:
print "error in comparison: 6"
errors = errors + 1
if pokerCalculations.compare_cards(two_p4, two_p5) != 1:
print "error in comparison: 7"
errors = errors + 1
if pokerCalculations.compare_cards(two_p1, two_p4) != -1:
print "error in comparison: 8"
errors = errors + 1
if pokerCalculations.compare_cards(pair4, royal1) != 1:
print "error in comparison: 9"
errors = errors + 1
if pokerCalculations.compare_cards(two_p6, str2) != 1:
print "error in comparison: 10"
errors = errors + 1
if pokerCalculations.compare_cards(three2, four3) != 1:
print "error in comparison: 11"
errors = errors + 1
if pokerCalculations.compare_cards(two_p4, royal1) != 1:
print "error in comparison: 12"
errors = errors + 1
if pokerCalculations.compare_cards(three2, fullh3) != 1:
print "error in comparison: 13"
errors = errors + 1
if pokerCalculations.compare_cards(high_card2, two_p1) != 1:
print "error in comparison: 14"
errors = errors + 1
if pokerCalculations.compare_cards(strfl2, royal1) != 1:
print "error in comparison: 15"
errors = errors + 1
if pokerCalculations.compare_cards(flush3, four2) != 1:
print "error in comparison: 16"
errors = errors + 1
if pokerCalculations.compare_cards(two_p2, flush2) != 1:
print "error in comparison: 17"
errors = errors + 1
if pokerCalculations.compare_cards(three2, fullh3) != 1:
print "error in comparison: 18"
errors = errors + 1
if pokerCalculations.compare_cards(strfl2, strfl1) != -1:
print "error in comparison: 19"
errors = errors + 1
if pokerCalculations.compare_cards(four1, four2) != 1:
print "error in comparison: 20"
errors = errors + 1
if pokerCalculations.compare_cards(four2, four3) != 1:
print "error in comparison: 21"
errors = errors + 1
if pokerCalculations.compare_cards(fullh1, fullh2) != -1:
print "error in comparison: 22"
errors = errors + 1
if pokerCalculations.compare_cards(fullh2, fullh3) != -1:
print "error in comparison: 23"
errors = errors + 1
if pokerCalculations.compare_cards(flush2, flush3) != 1:
print "error in comparison: 24"
errors = errors + 1
if pokerCalculations.compare_cards(str1, str2) != -1:
print "error in comparison: 25"
errors = errors + 1
if pokerCalculations.compare_cards(str2, str3) != 1:
print "error in comparison: 26"
errors = errors + 1
if pokerCalculations.compare_cards(three3, three1) != 1:
print "error in comparison: 27"
errors = errors + 1
if pokerCalculations.compare_cards(three3, three4) != 1:
print "error in comparison: 28"
errors = errors + 1
if pokerCalculations.compare_cards(three3, three2) != 1:
print "error in comparison: 29"
errors = errors + 1
if pokerCalculations.compare_cards(three3, high_card2) != -1:
print "error in comparison: 30"
errors = errors + 1

corrects = 30 - errors;
print "Correct:"
print corrects
print "Error:"
print errors



