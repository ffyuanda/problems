import copy
def combination(in_list, n):
    answer = []
    one = n * [0]
    length = len(in_list)

    def step_forward(list_index=0, n_num=0):
        if n_num == n:
            answer.append(copy.copy(one))
            return
        for i in range(list_index, length):
            one[n_num] = in_list[i]
            step_forward(i+1, n_num+1)
    step_forward()
    return answer


def intersection(lst1, lst2):
    return list(set(lst1) & set(lst2))


def decimal_to_binary(num):
    if num > 0:
        decimal_to_binary(num // 2)
        print(num % 2, end='')
decimal_to_binary(18)