from pathlib import Path
quitted = False
# common interface: all_items, dirs, files = command_L_get_items(path)


def command_Q(commands):
    global quitted
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


def command_L_r_f(path):
    recursive_items = command_L_r(path, [])
    for i in recursive_items:
        if Path(i).is_file():
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
        raise Exception("ERROR")
    else:
        p = Path(commands[1])
        try:
            all_items, dirs, files = command_L_get_items(p)
        except WindowsError:
            raise WindowsError("Path not valid")

        if len(commands) == 2:
            for i in files:
                print(i)
            for i in dirs:
                print(i)

        elif len(commands) == 3:
            # options -r -f

            if commands[2] == '-r':
                r = command_L_r(p, [])
                for i in r:
                    print(i)
            elif commands[2] == '-f':
                command_L_f(p)
            else:
                print('ERROR')

        elif len(commands) == 4:
            # options -s -e -r-f

            if commands[2] == '-s':
                command_L_s(p, commands[3])
            elif commands[2] == '-e':
                command_L_e(p, commands[3])
            elif commands[2] == '-r' and commands[3] == '-f':
                command_L_r_f(p)

        elif len(commands) == 5:
            # options -r-s -r-e
            if commands[2] == '-r' and commands[3] == '-s':

                command_L_r_s(p, commands[4])

            elif commands[2] == '-r' and commands[3] == '-e':

                command_L_r_e(p, commands[4])


def command_C(commands):
    if len(commands) < 4:
        print("ERROR")
    else:
        p = commands[1] + '\\'
        name = commands[3]
        extention = '.dsu'
        path = p + name + extention
        path = Path(path)
        if commands[2] == '-n':
            path.touch()
            print(str(path))


def command_D(commands):
    if len(commands) < 2:
        print('ERROR')
    else:
        path = Path(commands[1])

        if not str(path).endswith('.dsu'):
            print('ERROR')
        else:
            try:
                path.unlink()
                print(str(path) + ' DELETED')
            except FileNotFoundError:
                print("File not found!")


def command_R(commands):
    if len(commands) < 2:
        print('ERROR')
    else:
        path = Path(commands[1])

        if not str(path).endswith('.dsu'):
            print('ERROR')
        else:
            with open(str(path), 'r') as f:
                if path.stat().st_size == 0:
                    print('EMPTY')
                else:
                    output = f.readlines()
                    for i in range(len(output)):
                        if i == len(output) - 1:
                            # should not print a newline at the end
                            print(output[i], end='')
                        else:
                            print(output[i])


def main_func():

    in_commands = input()
    commands = [x for x in in_commands.split(' ')]

    if commands[0] == 'L':
        command_L(commands)
    elif commands[0] == 'C':
        command_C(commands)
    elif commands[0] == 'D':
        command_D(commands)
    elif commands[0] == 'R':
        command_R(commands)
    elif commands[0] == 'Q':
        command_Q(commands)
    else:
        raise Exception("Incorrect COMMAND")


if __name__ == '__main__':
    while not quitted:
        try:
            main_func()
        except Exception as e:
            print(e)
