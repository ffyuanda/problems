import copy
board = [[2, 2, 2, 2],
         [4, 1, 1, 4],
         [1, 8, 8, 1],
         [1, 32, 16, 1]]
checker = copy.deepcopy(board)
print(checker == board)
