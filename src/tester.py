# matrix = [[1,2,8,9],
#           [2,4,9,12],
#           [4,7,10,13],
#           [6,8,11,15]]
#
#
# def find_num_in_matrix(matrix, find):
#     bug_guy = []
#     for x in matrix:
#         bug_guy += x
#     return find in bug_guy

def add_space(in_str):
    out_str = list(in_str + in_str.count(' ') * 2 * ' ')
    point_1 = len(in_str) - 1
    point_2 = len(out_str) - 1
    while point_1 != point_2:
        if out_str[point_1] != ' ':
            out_str[point_2] = out_str[point_1]
            point_1 -= 1
            point_2 -= 1
        else:
            point_1 -= 1
            point_2 -= 3
            out_str[point_2+1:point_2+4] = '%20'
    return str(out_str)

if __name__ == '__main__':
    add_space('w e e')
    print(add_space('  '))
