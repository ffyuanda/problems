def calculate(cases):

    N, P = [int(i) for i in input().split(' ')]
    in_list = [int(j) for j in input().split(' ')]
    in_list.sort()
    min_num = 0
    curr = 0
    for i in range(P - 1):

        curr += in_list[P-1] - in_list[i]
    min_num = curr
    j = P
    while j < N:
        dmax = in_list[j-1] - in_list[j-P]
        dmin = in_list[j] - in_list[j-1]
        curr += (P - 1) * dmin - dmax
        min_num = min(min_num, curr)
        j += 1
    # for i in range(N-P+1):
    #     total = sum(in_list[i:i+P])
    #     curr = max(in_list[i:i+P]) * P - total
    #     if curr <= min_num:
    #         min_num = curr
    return 'Case #{}: {}'.format(cases, min_num)

t = int(input())

for i in range(1, t+1):
    print(calculate(i))
