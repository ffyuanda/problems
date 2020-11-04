def calculate(cases):

    houses, budget = [int(i) for i in input().split(' ')]
    prices = [int(j) for j in input().split(' ')]
    prices.sort()
    count = 0

    for i in prices:

        if budget - i < 0:
            break
        budget -= i
        count += 1
    return 'Case #{}: {}'.format(cases, count)

t = int(input())

for i in range(1, t+1):
    print(calculate(i))
