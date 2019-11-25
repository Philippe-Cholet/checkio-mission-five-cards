from itertools import combinations
from random import sample


class Card(str):
    RANKS = tuple('A 2 3 4 5 6 7 8 9 10 J Q K'.split())
    SUITS = tuple('♣♦♥♠')

    def __init__(self, card):
        rank, suit = card.split()
        self.rank, self.suit = self.RANKS.index(rank), self.SUITS.index(suit)

    def to(self, card):
        """ Distance to card from self.
            We have self.to(card) + card.to(self) == len(self.RANKS) == 13 """
        # assert self.suit == card.suit
        return (card.rank - self.rank) % len(self.RANKS)

    def __lt__(self, card):
        return (self.rank, self.suit) <= (card.rank, card.suit)

    @classmethod
    def random_hand(cls):
        if not hasattr(cls, 'DECK'):
            cls.DECK = [f'{r} {s}' for r in cls.RANKS for s in cls.SUITS]
        return sample(cls.DECK, 5)


def all_answers(*cards, n=1):
    cards = list(map(Card, cards))
    answers = {}
    all_pairs = [(A, B) for A, B in combinations(cards, 2) if A.suit == B.suit]
    for start, guess in all_pairs:
        bot_answer = cards.copy()
        bot_answer.remove(start)
        bot_answer.remove(guess)
        # Switch start and guess if needed.
        if start.to(guess) > 6:
            start, guess = guess, start
        delta = start.to(guess)  # <= 6 thanks to the switch.
        # We know starting point and delta.
        # Sort the three cards.
        bot_answer.sort()
        # Pop the one to put it first later.
        index_first = {1: 2, 2: 2, 3: 1, 4: 1, 5: 0, 6: 0}[delta]
        first = bot_answer.pop(index_first)
        # Reverse the other two when delta is even.
        if not delta % 2:  # or `if delta in (2, 4, 6):`.
            bot_answer.reverse()
        bot_answer.insert(0, first)
        # Insert the starting point.
        bot_answer.insert((n - 1) % 4, start)
        answers[tuple(bot_answer)] = guess
    return answers


if __name__ == '__main__':
    from tests import DATA

    assert Card('10 ♥').to(Card('A ♥')) == 4
    assert Card('A ♥').to(Card('10 ♥')) == 9

    deck = []
    for i, r in enumerate(Card.RANKS):
        for j, s in enumerate(Card.SUITS):
            card = Card(f'{r} {s}')
            assert (card.rank, card.suit) == (i, j), card
            deck.append(card)
    assert sorted(deck) == deck

    for cat, tests in DATA.items():
        if cat != 'Random':
            for n, cards, answers in tests:
                assert all_answers(*cards, n=n) == answers, (n, cards)
