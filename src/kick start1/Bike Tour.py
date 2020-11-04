def calculate(cases):

    num_checks = int(input())
    peaks = [int(j) for j in input().split(' ')]
    count = 0

    for i in range(1, num_checks - 1):

        if peaks[i - 1] < peaks[i] and peaks[i] > peaks[i + 1]:
            count += 1

    return 'Case #{}: {}'.format(cases, count)

# read test cases
t = int(input())

# execution
for i in range(1, t+1):
    print(calculate(i))
