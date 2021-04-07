from collections import defaultdict

def solve_root(f : callable, error : float) -> callable:
    if error <= 0:
        raise AssertionError('error should not be negative')

    def inner_func(negf, posf):
        inner_func.iterations = 0
        if f(negf) >= 0:
            raise AssertionError('f(negf) should not be positive')
        if f(posf) <= 0:
            raise AssertionError('f(posf) should not be negative')

        while True:
            inner_func.iterations += 1
            mid = (negf + posf) / 2
            if f(mid) < 0:
                negf = mid
            elif f(mid) > 0:
                posf = mid
            if abs(posf - negf) <= error:
                return mid
    return inner_func


def by_diversity(db : {int:{str:int}}) -> [(int,int)]:
    result = [(item[0], len(item[1])) for item in db.items()]
    return sorted(result, key=lambda x: x[1], reverse=True)


def by_size(db : {int:{str:int}}) -> [int]:
    result = sorted([(item[0], sum(item[1].values())) for item in db.items()], key=lambda x: x[1], reverse=True)
    return [x[0] for x in result]


def by_party(db : {int:{str:int}}) -> [str]:
    # result = list(set([x for item in db.items() for x in item[1].keys()]))
    pairs = [(party, p[1]) for party in list(set([x for item in db.items() for x in item[1].keys()])) for single_dict in db.values() for p in single_dict.items() if p[0] == party]

    # parties = ['d', 'l', 'r', 'i']
    # some_list = [(party, list(map(lambda y: y[1], filter(lambda x: x[0] == party, pairs)))) for party in list(set([x for item in db.items() for x in item[1].keys()]))]
    # some_list = [(i[0], sum(i[1])) for i in [(party, list(map(lambda y: y[1], filter(lambda x: x[0] == party, pairs)))) for party in list(set([x for item in db.items() for x in item[1].keys()]))]]

    # some_dict = {pairs[p][0]: (pairs[p - 1][1] + pairs[p][1]) if pairs[p][0] == pairs[p - 1][0] else (pairs[p][1]) for p in range(1, len(pairs))}
    # print(some_dict)
    # print(some_list)
    # print(pairs)
    # for pair in pairs:
    #     some_dict[pair[0]] += pair[1]
    # result = [item for item in some_dict.items()]
    # result = sorted([item for item in some_dict.items()], key=lambda x: x[1], reverse=True)
    # result = [x[0] for x in sorted([item for item in some_dict.items()], key=lambda x: x[1], reverse=True)]

    return [x[0] for x in sorted([item for item in [(i[0], sum(i[1])) for i in \
           [(party, list(map(lambda y: y[1], filter(lambda x: x[0] == party, pairs)))) \
           for party in list(set([x for item in db.items() for x in item[1].keys()]))]]],
                                 key=lambda x: x[1], reverse=True)]


def registration_by_state(db : {int:{str:int}}, state_zips : {str:{int}}) -> {str:{str:int}}:
    pass


if __name__ == '__main__':
    # This code is useful for debugging your functions, especially
    #   when they raise exceptions: better than using driver.driver().
    # Feel free to add more tests (including tests showing in the bsc.txt file)
    # Use the driver.driver() code only after you have removed any bugs
    #   uncovered by these test cases.

    import math


    print('\nTesting solve_root')
    def f(x):
        return 3*x**4 + 3*x**3 - 1
    rooter = solve_root(f, .0001)
    r = rooter(0,1)
    print(f'root 1 is approximately {r} where f({r}) = {f(r)} using {rooter.iterations} iterations')
    r = rooter(-1,-2)
    print(f'root 2 is approximately {r} where f({r}) = {f(r)} using {rooter.iterations} iterations')

    def f(x):
        return 23*math.sqrt(x) - (10*math.log2(x)**2+1000)
    rooter = solve_root(f, .001)
    r = rooter(10000,20000)
    print(f'root is approximately {r} where f({r}) = {f(r)} using {rooter.iterations} iterations')


    print('\nTesting by_diversity')
    db1 = {1: {'d': 15, 'i': 15,          'r': 15},
           2: {'d': 12,                   'r':  8},
           3: {'d': 10, 'i': 30, 'l': 20, 'r': 22},
           4: {'d': 30, 'l': 20,          'r': 30},
           5: {'i': 15, 'l': 15,          'r': 15}}
    print(by_diversity(db1))
    db2 = {1000: {'d': 50, 'i': 27,          'r': 18, 'x': 46},
           2000: {'d': 32,                   'r': 58},
           3000: {'d': 20, 'i': 30, 'l': 20, 'r': 22},
           4000: {'d': 40, 'i': 20, 'l': 40, 'r': 39, 'x': 46},
           5000: {'d': 20, 'i': 30, 'l': 20,          'x': 15},
           6000: {         'i': 30,                   'x': 46},
           7000: {                  'l': 20                  },
           8000: {         'i': 15, 'l': 15, 'r': 15}}
    print(by_diversity(db2))


    print('\nTesting by_size')
    db1 = {1: {'d': 15, 'i': 15,          'r': 15},
           2: {'d': 12,                   'r':  8},
           3: {'d': 10, 'i': 30, 'l': 20, 'r': 22},
           4: {'d': 30, 'l': 20,          'r': 30},
           5: {'i': 15, 'l': 15,          'r': 15}}
    print(by_size(db1))
    db2 = {1000: {'d': 50, 'i': 27,          'r': 18, 'x': 46},
           2000: {'d': 32,                   'r': 58},
           3000: {'d': 20, 'i': 30, 'l': 20, 'r': 22},
           4000: {'d': 40, 'i': 20, 'l': 40, 'r': 39, 'x': 46},
           5000: {'d': 20, 'i': 30, 'l': 20,          'x': 15},
           6000: {         'i': 30,                   'x': 46},
           7000: {                  'l': 20,                 },
           8000: {         'i': 15, 'l': 15, 'r': 15}}
    print(by_size(db2))


    print('\nTesting by_party')
    db1 = {1: {'d': 15, 'i': 15,          'r': 15},
           2: {'d': 12,                   'r':  8},
           3: {'d': 10, 'i': 30, 'l': 20, 'r': 22},
           4: {'d': 30, 'l': 20,          'r': 30},
           5: {'i': 15, 'l': 15,          'r': 15}}
    print(by_party(db1))
    db2 = {1000: {'d': 50, 'i': 27,          'r': 18, 'x': 46},
           2000: {'d': 32,                   'r': 58},
           3000: {'d': 20, 'i': 30, 'l': 20, 'r': 22},
           4000: {'d': 40, 'i': 20, 'l': 40, 'r': 39, 'x': 46},
           5000: {'d': 20, 'i': 30, 'l': 20,          'x': 15},
           6000: {         'i': 30,                   'x': 46},
           7000: {                  'l': 20,                 },
           8000: {         'i': 15, 'l': 15, 'r': 15}}
    print(by_party(db2))


    print('\nTesting registration_by_state')
    db1 = {1: {'d': 15, 'i': 15, 'r': 15}, 2: {'d': 12, 'r':  8}, 3: {'d': 10, 'i': 30, 'l': 20, 'r': 22}, 4: {'d': 30, 'l': 20, 'r': 30}, 5: {'i': 15, 'l': 15, 'r': 15}}
    print(registration_by_state(db1,{'CA': {1,3}, 'WA': {2,4,5}}))
    db2 = {1000: {'d': 50, 'i': 27,          'r': 18, 'x': 46},
           2000: {'d': 32,                   'r': 58},
           3000: {'d': 20, 'i': 30, 'l': 20, 'r': 22},
           4000: {'d': 40, 'i': 20, 'l': 40, 'r': 39, 'x': 46},
           5000: {'d': 20, 'i': 30, 'l': 20,          'x': 15},
           6000: {         'i': 30,                   'x': 46},
           7000: {                  'l': 20,                 },
           8000: {         'i': 15, 'l': 15, 'r': 15}}
    print(registration_by_state(db2,{'CA' : {1000,3000,7000}, 'WA': {2000,4000,5000,8000}, 'OR' : {6000}, 'NV' : {}}))



    print('\ndriver testing with batch_self_check:')
    import driver
    driver.default_file_name = "bscq1S21.txt"
#     driver.default_show_traceback = True
#     driver.default_show_exception = True
#     driver.default_show_exception_message = True
    driver.driver()

