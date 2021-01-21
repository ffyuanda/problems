from pathlib import Path
quitted = False
# common interface: all_items, dirs, files = command_L_get_items(path)


def command_Q(commands):
    global quitted
    if commands[0] == 'Q':
        quitted = True


def command_L_get_items(path):
    """
    Trying to gather all the files, directories, and the whole path content
    and store them separately.
    :param path: current path user want to explore
    :return: a three-units tuple from larger scope to smaller scope:
    all_items, dirs, and files.
    """
    files = [x for x in path.iterdir() if x.is_file()]
    dirs = [x for x in path.iterdir() if x.is_dir()]
    all_items = [x for x in path.iterdir()]
    return all_items, dirs, files


def command_L_r(path, output: list):
    """
    For -r option of command L. Recursively go through the current path. Usage:
    print(command_L_r(path)); with loop if you want a nice layout.
    :param path: current working path
    :param output: an empty list (initially) that collects the info
    after each recursion.
    :return: the final output that contains files and directories after all
    recursions
    """

    all_items, dirs, files = command_L_get_items(path)
    for i in files:
        output.append(str(i))
    for i in dirs:
        output.append(str(i))
        command_L_r(i, output)

    return output


def command_L_s(path, input_search):
    """
    Search by name.
    :param path: current working path
    :param input_search: the filename
    :return: None
    """
    all_items, dirs, files = command_L_get_items(path)
    for i in all_items:
        if input_search in str(i):
            print(i)


def command_L_e(path, extension):
    all_items, dirs, files = command_L_get_items(path)
    for i in all_items:
        if str(i).endswith('.' + extension):
            print(i)


def command_L_r_s(path, input_search):
    """
    For -r option of command L. Recursively go through the current path and
    search the required file.
    :param path: current path
    :param input_search: the filename
    :return:
    """
    recursive_items = command_L_r(path, [])
    for i in recursive_items:
        if input_search in str(i):
            print(i)
            pass


def command_L_r_e(path, extension):
    recursive_items = command_L_r(path, [])
    for i in recursive_items:
        if str(i).endswith('.' + extension):
            print(i)


def command_L_f(path):
    """
    Output only files (non-directories)
    :param path: current working path
    :return: None
    """
    all_items, dirs, files = command_L_get_items(path)
    for i in files:
        print(i)


def command_L(commands):

    if len(commands) < 2:
        print('needs at least one more input')
    elif commands[0] == 'L':
        p = Path(commands[1])
        try:
            all_items, dirs, files = command_L_get_items(p)
        except WindowsError:
            print("Path not valid.")

        if len(commands) == 2:
            for i in files:
                print(i)
            for i in dirs:
                print(i)

        elif len(commands) == 3:
            # options -r -f

            if commands[2] == '-r':
                r = command_L_r(p)
                for i in r:
                    print(i)
            elif commands[2] == '-f':
                command_L_f(p)
            else:
                print('ERROR')

        elif len(commands) == 4:
            # options -s -e

            if commands[2] == '-s':
                command_L_s(p, commands[3])
            elif commands[2] == '-e':
                command_L_e(p, commands[3])

        elif len(commands) == 5:
            # options -r-s -r-e
            if commands[2] == '-r' and commands[3] == '-s':

                command_L_r_s(p, commands[4])

            elif commands[2] == '-r' and commands[3] == '-e':

                command_L_r_e(p, commands[4])


def main_func():

    print('Usage: [COMMAND] [INPUT] [[-]OPTION] [INPUT]')

    in_commands = input()
    commands = [x for x in in_commands.split(' ')]

    command_Q(commands)

    if commands[0] == 'L':
        command_L(commands)
    else:
        raise Exception("Error occur")


if __name__ == '__main__':
    while not quitted:
        try:
            main_func()
        except Exception as e:
            print(e)

