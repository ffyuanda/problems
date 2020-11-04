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