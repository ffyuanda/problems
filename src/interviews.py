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


def solution(A):
    l = list(filter(lambda x: x > 0, sorted(A)))
    if len(l) == 0 or l[-1] < 0 or l[0] > 1:
        return 1
    prev = None
    for i in l:
        curr = i
        if prev is not None:
            if curr - prev > 1:
                return prev + 1
        prev = curr
    return l[-1] + 1


class Tree(object):
    def __init__(self, node=None):

        if node is None:
            self.root_node = Node()
        else:
            self.root_node = node

    def preorder_display(self, node):
        print(node.self_value)
        if node.left_value is not None:
            self.preorder_display(node.left_value)
        if node.right_value is not None:
            self.preorder_display(node.right_value)


class Node(object):
    def __init__(self, value=None):
        self.self_value = value
        self.left_value = None
        self.right_value = None

    def set_left(self, node):
        self.left_value = node

    def set_right(self, node):
        self.right_value = node


if __name__ == '__main__':
    node1 = Node(1)
    node2 = Node(2)
    node3 = Node(3)
    node4 = Node(4)
    node5 = Node(5)
    node1.set_left(node2)
    node1.set_right(node3)
    node2.set_left(node4)
    node2.set_right(node5)
    test_tree = Tree(node1)

    test_tree.preorder_display(test_tree.root_node)
