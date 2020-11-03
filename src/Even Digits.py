def calculate(cases):

    num_original = int(input())
    num_original_string = str(num_original)
    length = len(num_original_string)
    count = 0

    if length < 2 and num_original % 2 == 1:  # one digit case
        count = 1

    else:

        for i in range(length):

            if int(num_original_string[i]) % 2 == 0:
                continue

            else:  # first digit not even

                go_up = num_original_string[:i] + str(int(num_original_string[i]) + 1) + \
                                          (length - i - 1) * '0'
                go_down = num_original_string[:i] + str(int(num_original_string[i]) - 1) + \
                                          (length - i - 1) * '8'

                if int(num_original_string[i]) == 9:  # handle 9s
                    num_original_string = go_down

                else:

                    num_original_string = go_up if abs(int(go_up) - num_original) <= abs(int(go_down) - num_original) \
                                            else go_down
                break

        count = abs(num_original - int(num_original_string))
    return 'Case #{}: {}'.format(cases, count)

# main
t = int(input())
for i in range(1, t+1):
    print(calculate(i))
