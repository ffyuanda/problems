# import time
# start = time.clock()
# remain = 1
# output = {'Dollar': 0, 'Quarter': 0, 'Dime': 0, 'Nickle': 0, 'Penny': 0}
#
# while remain >= 0:
#     if remain >= 100:
#         remain -= 100
#         output['Dollar'] += 1
#     elif remain >= 25:
#         remain -= 25
#         output['Quarter'] += 1
#     elif remain >= 10:
#         remain -= 10
#         output['Dime'] += 1
#     elif remain >= 5:
#         remain -= 5
#         output['Nickle'] += 1
#     elif remain >= 1:
#         remain -= 1
#         output['Penny'] += 1
#     else:
#         break
#
# for i in output:
#     if output[i] != 0:
#         print(i, output[i])
#
# print(output)
# end = time.clock()
# print("final is in {:.10f}".format(end-start))

# i = abs(int(input()))
# if i // 10 >= 1:
#     print('Error: You entered two or more digits!')
# letter = "q"
# print("Upper Case") if 65 <= ord(letter) <= 90 else print("Non Upper")
#
# answers = [input() for i in range (5)]
# answers_modified = list(map(lambda x: x == 'Yes', answers))
# print('The recorded answers were ', answers, answers_modified)
tu = (0, 1)
print(tu[1])