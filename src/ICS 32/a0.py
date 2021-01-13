a = "+-+-+"
b = "| |"
c = "+-+"
num = int(input())
num = num * 2 + 1
curr = -1

for i in range(num):
    if num == 1:
        break
    if i == 0:
        print(c)
    elif i == num - 1:
        print(curr * 2 * ' ', end='')
        print(c)
    elif i > 0 and i % 2 == 1:
        curr += 1
        print(curr * 2 * ' ', end='')
        print(b)
    elif i > 0 and i % 2 == 0:
        print(curr * 2 * ' ', end='')
        print(a)
