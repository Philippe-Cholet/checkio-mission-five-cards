from all_answers import Card, all_answers
from random import choice


def random_data(n):
    hand = Card.random_hand()
    return [n, tuple(hand), all_answers(*hand, n=n)]


DATA = {
    'Basic': [
        # Example
        [1, ('A ♥', '3 ♦', 'K ♠', 'Q ♣', 'J ♦'),
         {('J ♦', 'A ♥', 'Q ♣', 'K ♠'): '3 ♦'}],

        # Cards from "Nain Jaune" / "Yellow Dwarf"
        [2, ('10 ♦', 'J ♣', 'Q ♠', 'K ♥', '7 ♦'),
         {('Q ♠', '7 ♦', 'J ♣', 'K ♥'): '10 ♦'}],

        # 3♠, 1♦, 1♣
        [3, ('K ♦', 'K ♠', '2 ♣', '8 ♠', '10 ♠'),
         {('2 ♣', '10 ♠', '8 ♠', 'K ♦'): 'K ♠',
          ('8 ♠', '2 ♣', '10 ♠', 'K ♦'): 'K ♠',
          ('K ♠', 'K ♦', '8 ♠', '2 ♣'): '10 ♠'}],
        ],

    'Extra': [
        # 5♥
        [4, ('10 ♥', 'J ♥', 'Q ♥', 'K ♥', 'A ♥'),
         {('K ♥', 'A ♥', 'Q ♥', '10 ♥'): 'J ♥',
          ('K ♥', 'J ♥', 'A ♥', '10 ♥'): 'Q ♥',
          ('J ♥', 'A ♥', 'Q ♥', '10 ♥'): 'K ♥',
          ('Q ♥', 'K ♥', 'J ♥', '10 ♥'): 'A ♥',
          ('K ♥', 'A ♥', '10 ♥', 'J ♥'): 'Q ♥',
          ('Q ♥', '10 ♥', 'A ♥', 'J ♥'): 'K ♥',
          ('Q ♥', '10 ♥', 'K ♥', 'J ♥'): 'A ♥',
          ('J ♥', 'A ♥', '10 ♥', 'Q ♥'): 'K ♥',
          ('K ♥', 'J ♥', '10 ♥', 'Q ♥'): 'A ♥',
          ('Q ♥', '10 ♥', 'J ♥', 'K ♥'): 'A ♥'}],

        # 3♥, 2♦
        [5, ('2 ♦', '9 ♥', 'K ♦', '4 ♥', '2 ♥'),
         {('K ♦', '9 ♥', '4 ♥', '2 ♥'): '2 ♦',
          ('4 ♥', '2 ♦', '2 ♥', 'K ♦'): '9 ♥',
          ('9 ♥', '2 ♦', 'K ♦', '4 ♥'): '2 ♥',
          ('2 ♥', 'K ♦', '9 ♥', '2 ♦'): '4 ♥'}],

        # 4♣, 1♠
        [6, ('K ♣', 'A ♣', '6 ♠', '4 ♣', '9 ♣'),
         {('9 ♣', 'K ♣', '4 ♣', '6 ♠'): 'A ♣',
          ('6 ♠', 'K ♣', '9 ♣', 'A ♣'): '4 ♣',
          ('4 ♣', '9 ♣', '6 ♠', 'A ♣'): 'K ♣',
          ('9 ♣', 'A ♣', '6 ♠', 'K ♣'): '4 ♣',
          ('4 ♣', '9 ♣', '6 ♠', 'K ♣'): 'A ♣',
          ('A ♣', '4 ♣', '6 ♠', 'K ♣'): '9 ♣'}],

        # 3♣, 1♦, 1♠
        [7, ('2 ♣', '10 ♣', 'Q ♦', '4 ♣', 'Q ♠'),
         {('4 ♣', 'Q ♦', '10 ♣', 'Q ♠'): '2 ♣',
          ('Q ♠', 'Q ♦', '2 ♣', '10 ♣'): '4 ♣',
          ('2 ♣', 'Q ♠', '4 ♣', 'Q ♦'): '10 ♣'}],

        # 2♥, 2♦, 1♣
        [8, ('K ♣', '5 ♥', '4 ♥', '10 ♦', 'J ♦'),
         {('K ♣', '10 ♦', 'J ♦', '4 ♥'): '5 ♥',
          ('K ♣', '4 ♥', '5 ♥', '10 ♦'): 'J ♦'}],
        ],

    'Random': [random_data(n) for n in range(1, 31, 3)],
    }


from_user = '''
try:
    {0} = USER_GLOBAL['{0}']
except KeyError:
    raise NotImplementedError("Where is '{0}'?")
'''

functions_to_import = ('bot', 'magician')
init_code = ''.join(map(from_user.format, functions_to_import))

run_test = '''
RET['code_result'] = {}
'''


def prepare_test(code, answers):
    return {'test_code': {'python-3': init_code + run_test.format(code)},
            'show': {'python-3': code},
            'answer': answers}


def test_code(function, cards, n):
    args = list(map(repr, cards))
    if n != 1:
        args.append(f'n={n}')
    args = ', '.join(args)
    return f"{function}({args})"


def bot_test(n, cards, answers, **_):
    code = test_code('bot', cards, n)
    return prepare_test(code, list(answers))


def magician_test(n, _, answers, random=False):
    L = sorted(answers.items())
    cards, answer = (choice(L) if random else
                     L[len(L) // 2])  # or whatever fixed index
    code = test_code('magician', cards, n)
    return prepare_test(code, [answer])


test_makers = bot_test, magician_test

TESTS = {cat: ([choice(test_makers)(*test, random=True) for test in tests]
               if cat == 'Random' else
               [maker(*test) for test in tests for maker in test_makers])
         for cat, tests in DATA.items()}


if __name__ == '__main__':
    # from pprint import pprint
    # pprint(TESTS, width=200)

    for tests in TESTS.values():
        for test in tests:
            print(
                # test['test_code']['python-3'],
                test['show']['python-3'],
                )
