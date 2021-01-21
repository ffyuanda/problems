#################################################
# 15-112-n19 hw4-2
# Your Name:Shaoxuan Yuan
# Your Andrew ID:Shaoxuan
# Your Section:B
#################################################
import math, random


###################
# helper functions
def flattenHelper(lst, output=[]):
    for item in lst:
        if type(item) == list:
            flattenHelper(item, output)

        else:
            output.append(item)

    return output


def getCourseHelper(courseCatalog, courseNumber, name=[]):
    for item in courseCatalog:
        if type(item) == list:
            name.append(courseCatalog[0])
            name.append(".")
            solution = getCourseHelper(item, courseNumber, name)
            if solution == None:
                name.pop()
                name.pop()
                continue
            return solution
        if item == courseNumber:
            name.append(courseCatalog[0])
            name.append(".")
            name.append(item)
            return name
        if item != courseCatalog[0] and \
                item == courseCatalog[len(courseCatalog) - 1]:
            return None


# taken from hw 2-2
def almostEqual(d1, d2, epsilon=10 ** -7):
    return (abs(d2 - d1) < epsilon)


# taken from hw 2-2
def areLegalValues(values):
    length = len(values)
    intLength = int(math.sqrt(length))
    floatLength = math.sqrt(length)
    if (length == 0): return False
    if (not almostEqual(intLength, floatLength)): return False

    numRange = list(range(0, length + 1))

    for i in values:
        if (values.count(i) > 1 and i != 0):
            return False
        elif (numRange.count(i) < 1):
            return False

    return True


# taken from hw 2-2
def isLegalRow(board, row):
    rowContainer = []
    rowContainer = board[row]
    return areLegalValues(rowContainer)


# taken from hw 2-2
def isLegalCol(board, col):
    colContainer = []

    for i in board:
        colContainer.append(i[col])

    return areLegalValues(colContainer)


# taken from hw 2-2
def isLegalBlock(board, block):
    blockContainer = []
    length = len(board)
    colRow = math.sqrt(length)  # the length of the side of the block
    colRow = int(colRow)

    topLeftX = block // colRow * colRow  # calculate each block's coordinators
    topLeftY = block % colRow * colRow
    bottomRightX = topLeftX + colRow - 1
    bottomRightY = topLeftY + colRow - 1

    for i in range(topLeftX, bottomRightX + 1):  # get the block into a list

        for j in range(topLeftY, bottomRightY + 1):
            blockContainer.append(board[i][j])

    return areLegalValues(blockContainer)


# taken from hw 2-2
def isLegalSudoku(board):
    for i in range(len(board)):
        if (isLegalRow(board, i) == False): return False
        if (isLegalCol(board, i) == False): return False
        if (isLegalBlock(board, i) == False): return False

    return True


#######################


def flatten(lst):
    return flattenHelper(lst, [])


def getCourse(courseCatalog, courseNumber):
    name = getCourseHelper(courseCatalog, courseNumber, [])
    output = ""
    if name == None:
        return None
    for item in name:
        output += item

    return output


def solveSudoku(board, row=0, col=0):
    length = len(board)
    if row == length:
        return board  # base case
    else:  # recursion case
        if col < length and row < length and board[row][col] == 0:
            # the same row and the slot is 0
            for num in range(1, length + 1):
                board[row][col] = num
                if isLegalSudoku(board):
                    solution = solveSudoku(board, row, col + 1)
                    if solution != None: return solution
                if num == length:
                    board[row][col] = 0
                    return None
        elif col < length and row < length and board[row][col] != 0:
            # the same row but the slot is not 0 (skip it)
            return solveSudoku(board, row, col + 1)
        if col >= length:
            # next row
            return solveSudoku(board, row + 1, col=0)


# ignore_rest
# test functions
def testflatten():
    print('Testing flatten()...', end='\n')
    assert (flatten([1, [2]]) == [1, 2])
    assert (flatten([1, 2, [3, [4, 5], 6], 7]) == [1, 2, 3, 4, 5, 6, 7])
    assert (flatten(['wow', [2, [[]]], [True]]) == ['wow', 2, True])
    assert (flatten([]) == [])
    assert (flatten([[]]) == [])


def testgetCourse():
    print('Testing getCourse()...', end='\n')
    courseCatalog = \
        ["CMU",
         ["CIT",
          ["ECE", "18-100", "18-202", "18-213"],
          ["BME", "42-101", "42-201"],
          ],
         ["SCS",
          ["CS",
           ["Intro", "15-110", "15-112"],
           "15-122", "15-150", "15-213"
           ],
          ],
         "99-307", "99-308"
         ]
    assert (getCourse(courseCatalog, "18-100") == "CMU.CIT.ECE.18-100")
    assert (getCourse(courseCatalog, "15-112") == "CMU.SCS.CS.Intro.15-112")
    assert (getCourse(courseCatalog, "15-213") == "CMU.SCS.CS.15-213")
    assert (getCourse(courseCatalog, "99-307") == "CMU.99-307")
    assert (getCourse(courseCatalog, "15-251") == None)


def testSolveSudoku():
    print('Testing solveSudoku()...', end='\n')
    board = [
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [5, 7, 0, 0, 6, 0, 0, 0, 0],
        [0, 0, 8, 0, 0, 2, 0, 4, 9],
        [0, 3, 0, 0, 0, 0, 5, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 4, 0, 0, 9, 0, 0, 8],
        [0, 0, 0, 3, 5, 0, 6, 0, 0],
        [0, 0, 9, 0, 0, 0, 0, 0, 1],
        [0, 0, 0, 0, 0, 0, 0, 0, 0]
    ]
    solved = solveSudoku(board)
    for i in solved:
        print(i)

    # solution = [
    #     [5, 3, 4, 6, 7, 8, 9, 1, 2],
    #     [6, 7, 2, 1, 9, 5, 3, 4, 8],
    #     [1, 9, 8, 3, 4, 2, 5, 6, 7],
    #     [8, 5, 9, 7, 6, 1, 4, 2, 3],
    #     [4, 2, 6, 8, 5, 3, 7, 9, 1],
    #     [7, 1, 3, 9, 2, 4, 8, 5, 6],
    #     [9, 6, 1, 5, 3, 7, 2, 8, 4],
    #     [2, 8, 7, 4, 1, 9, 6, 3, 5],
    #     [3, 4, 5, 2, 8, 6, 1, 7, 9]
    # ]
    # assert (solved == solution)
    print('Passed!')




def testAll():
    testflatten()
    testgetCourse()
    testSolveSudoku()

def main():
    testAll()


if __name__ == '__main__':
    main()