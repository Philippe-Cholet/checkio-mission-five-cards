from tests import TESTS


def result_in_answers(data, test):
    # Compare list and tuple doesn't raise an error: be sure all are tuples.
    user_result = tuple(data['code_result'])
    answers = map(tuple, test['answer'])
    return user_result in answers, None


if __name__ != '__main__':
    from checkio import api
    from checkio.signals import ON_CONNECT
    from checkio.referees.code import CheckiORefereeCode

    api.add_listener(
        ON_CONNECT,
        CheckiORefereeCode(
            tests=TESTS,
            check_result=result_in_answers,
        ).on_ready,
    )

else:
    try:
        from my_solution import bot, magician
    except ImportError:
        print('You can check all tests locally, '
              'if your script is named "my_solution.py".')
    else:
        all_tests = ((cat, test_nb, test) for cat, tests in TESTS.items()
                     for test_nb, test in enumerate(tests, 1))
        nb_success = 0
        for cat, test_nb, test in all_tests:
            test_code = test['show']['python-3']
            data = dict(code_result=eval(test_code))
            success = result_in_answers(data, test)[0]
            if not success:
                print(f'You failed the {cat.lower()} test #{test_nb}.',
                      test_code, sep='\n    ')
                break
            nb_success += 1
        else:
            print('Well done!',
                  f'You successfully passed all the {nb_success} tests.')
