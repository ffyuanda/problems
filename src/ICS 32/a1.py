from pathlib import Path
quitted = False
def commands_input_check(commands):

    assert len(commands) == 4


def command_Q(commands):
    global quitted
    if commands[0] == 'Q':
        quitted = True


def command_L_r(path:list):
    """
    For -r option of command L.
    :param path: current path
    :return:
    """
    all_items, dirs, files = command_L_get_items(path)
    for i in files:
        print(i)
    for i in dirs:
        print(i)
        command_L_r(i)


def command_L_get_items(path):
    files = [x for x in path.iterdir() if x.is_file()]
    dirs = [x for x in path.iterdir() if x.is_dir()]
    all_items = [x for x in path.iterdir()]
    return all_items, dirs, files


def command_L(commands):
    if len(commands) < 2:
        print('needs at least one more input')
    elif commands[0] == 'L':
        p = Path(commands[1])
        all_items, dirs, files = command_L_get_items(p)

        if len(commands) == 2:
            for i in files:
                print(i)
            for i in dirs:
                print(i)
        if len(commands) == 3:
            if commands[2] == '-r':

                command_L_r(p)

            pass



print('Usage: [COMMAND] [INPUT] [[-]OPTION] [INPUT]')
while not quitted:
    in_commands = input()
    commands = [x for x in in_commands.split(' ')]

    command_Q(commands)
    command_L(commands)


    print(commands)


