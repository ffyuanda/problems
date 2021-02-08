"""
Homework a2 for I&C SCI 32: PROG SOFTWARE LIBR
at University of California, Irvine

Student info:
Name: Shaoxuan Yuan
ID: 89832399
"""

from pathlib import Path
import Profile
import ds_client as client
quitted = False
test_mode = False
PORT = 2021
HOST = "168.235.86.101"
# common interface: all_items, dirs, files = command_L_get_items(path)


def command_Q():
    """
    Quit functionality that changes global quitted variable
    :param commands:
    :return:
    """
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


def command_L_r(path, output):
    """
    For -r option of command L. Recursively go through the current path.
    Usage:
    command_L_r(path, [])

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
    """
    Search by extension
    :param path: current working path
    :param extension: the extension type that you need to search
    :return: None
    """
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
    :return: None
    """
    recursive_items = command_L_r(path, [])
    for i in recursive_items:
        if input_search in str(i):
            print(i)
            pass


def command_L_r_e(path, extension):
    """
    Recursively search by extension
    :param path: current working path
    :param extension: the extension type that you need to search
    :return: None
    """
    recursive_items = command_L_r(path, [])
    for i in recursive_items:
        if str(i).endswith('.' + extension):
            print(i)


def command_L_r_f(path):
    """
    Recursively print out all the files.
    :param path: current working path
    :return: None
    """
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
    """
    Functionalities within command L.
    List the contents of the user specified directory.
    :param commands: the input command
    :return: None
    """
    if len(commands) < 2:
        raise Exception("ERROR")
    else:
        p = Path(commands[1])
        try:
            all_items, dirs, files = command_L_get_items(p)
        except WindowsError:
            raise WindowsError("ERROR")

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


def create_profile(path: str):
    """
    TODO: Update the function to be able to add, delete and edit each term
    :param path:
    :return:
    """
    assert type(path) is str, 'path needs to be str'

    # get the users data
    dsuserver = input('DSU server (type it directly without quotation marks): ')
    username = input('username: ')
    password = input('password: ')
    post = Profile.Post()
    entry = input('post (optional, skip by pressing enter): ')
    post.set_entry(entry)
    bio = input('bio (optional, skip by pressing enter): ')

    # create the profile and pass data in
    profile = Profile.Profile(dsuserver, username, password)
    profile.bio = bio
    profile.add_post(post)
    profile.save_profile(path)
    print('DSU file storing...')
    print("Local file stored at: " + str(path))
    # ask if the user wants to upload
    upload_option(profile)


def upload_option(profile: Profile):
    """
    The interface to upload profile to server,
    working with ds_client module's send().
    :param profile: current working profile object
    :return: None
    """
    option = input("Do you want to also upload it to the server? (y/n)\n").upper()
    server = profile.dsuserver
    username = profile.username
    password = profile.password
    message = profile.get_posts()[0].get_entry()
    # TODO send a list of posts up
    bio = profile.bio

    if option == 'Y':
        print("Send post (p)")
        print("Update bio (b)")
        print("Send post and update bio (pb)")
        option = input()
        client.send(option, server, PORT, username, password,
                    message, bio)
        print("Upload done.")

    elif option == 'N':
        print("Done.")

    else:
        print('please enter either y or n\n')
        upload_option(profile)


def modify_profile(profile: Profile, path):

    while True:
        print("""Which part you want to modify?\n
    username (u)
    password (pwd)
    bio (b)
    posts (p)
    save modification(s)""")

        option = input().lower()
        if option == "u":
            mod = input("Enter the new username: \n")
            profile.username = mod

        elif option == "pwd":
            mod = input("Enter the new password: \n")
            profile.password = mod

        elif option == "b":
            mod = input("Enter the new bio: \n")
            profile.bio = mod

        elif option == "p":


            mod = input("Enter the new password: \n")
            profile.password = mod

        elif option == "s":
            profile.save_profile(path)
            break


def command_C(commands):
    """
    Functionalities within command C,
    will read the input and create a new file.
    :param commands: the input command
    :return: None
    """
    if len(commands) < 4:
        print("ERROR")
    else:

        p = commands[1] + '\\'
        name = commands[3]
        extention = '.dsu'
        path = p + name + extention

        if test_mode:
            print(path)

        if commands[2] == '-n':
            path = Path(path)
            # create the dsu file
            path.touch()
            # for Profile creation (after the dsu file is created)
            create_profile(str(path))


def command_D(commands):
    """
    Functionalities within command D, allow the user to delete a DSU file.
    :param commands: the input command
    :return: None
    """
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
    """
    Functionalities within command R, print the content of a DSU file.
    :param commands: the input command
    :return: None
    """
    if len(commands) < 2:
        print('ERROR')
    elif len(commands) == 2:
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
    # -l option to load
    elif len(commands) == 3 and commands[2] == '-l':
        # TODO It should allow adding post or change bio to the loaded file
        profile = Profile.Profile()
        profile.load_profile(commands[1])
        print(profile.dsuserver,
              profile.password,
              profile.username,
              profile.bio,
              profile.get_posts())
        upload_option(profile)
    else:
        raise Exception('ERROR')


def input_analyzer(in_commands):
    """
    Analyze the input string and turn it into
    readable list format.
    :param in_commands: the user input string
    :return: a list that contains the processed user input (commands)
    """
    out_commands = []
    command_list = ['L', 'Q', 'C', 'D', 'R']
    option_list = ['-s', '-r', '-f', '-e', '-n', '-l']
    built_ins = command_list + option_list
    real_path = ''

    # raw split by space
    commands = [x for x in in_commands.split(' ')]
    length = len(commands)

    # try to find out the real path that may contain whitespace, which
    # 1. has to not in the built_ins keywords
    # 2. its left and right elements are not both built-ins keywords
    for i in range(length):
        # does not check first and last element
        if test_mode:
            print(real_path)

        if 0 < i < length-1:

            if commands[i] not in built_ins:

                # i is not the last digit
                if i < length-1:
                    # this is a path with whitespaces
                    if (commands[i+1] not in built_ins) \
                            or (commands[i-1] not in built_ins):
                        real_path += commands[i] + ' '
                    # this is a path without whitespaces
                    else:
                        real_path = commands[i]

                # i is the last digit
                else:

                    # this is a path with whitespaces
                    if commands[i-1] not in built_ins:
                        real_path += commands[i] + ' '

                    # there are only two elements, and command[i] is a
                    # valid path without whitespace
                    elif commands[i-1] in command_list:
                        real_path = commands[i]

                    # the last element (extension/filename etc.)
                    else:
                        out_commands.append(commands[i])
            else:
                # built-ins keywords
                out_commands.append(commands[i])
        else:
            # first and last element
            out_commands.append(commands[i])

    # remove trailing whitespaces
    if len(real_path) > 0:
        real_path = real_path.strip()
        out_commands.insert(1, real_path)
    return out_commands


def helper():
    print("""Usage format: [COMMAND] [INPUT] [[-]OPTION] [INPUT]
    
    COMMAND: L - List the contents of the user specified directory.
    
                OPTIONs:
                -r Output directory content recursively.
                -f Output only files, excluding directories in the results.
                -s Output only files that match a given file name.
                -e Output only files that match a give file extension.
                
                Example usage:
                L c:\\users\\mark\\a1
                L c:\\users\\mark\\a1 -r
                L c:\\users\\mark\\a1 -f
                L c:\\users\\mark\\a1 -r -s readme.txt
                L c:\\users\\mark\\a1 -s readme.txt
                L c:\\users\\mark\\a1 -r -e jpg
                
    COMMAND: Q - Quit the program.
    
                Example usage:
                Simply press Q.
    
    COMMAND: C - Create a new file in the specified directory.
                 And you need to enter DSU server, username, and
                 password by the following prompt.
                 
                 After the creation of DSU file and profile, the
                 program will ask you if you want to upload things
                 to the DSU server.
                
                OPTIONs:
                -n Specify the name to be used for a new file.
                
                Example usage:
                C c:\\users\\mark\\a1 -n mark
                
                
    COMMAND: D - Delete the file.
    
                Example usage:
                D c:\\users\\mark\\a1\\mark.dsu
    
    COMMAND: R - Read the contents of a file.
    
                OPTIONs:
                -l load the specified file from the path
                
                After the loading of DSU file and profile, the
                program will ask you if you want to upload things
                to the DSU server.
    
                Example usage:
                R c:\\users\\mark\\a1\\mark.dsu
                R c:\\users\\mark\\a1\\mark.dsu -l
              """)
    pass


def main_func():
    """
    The function wrapper.
    :return: None
    """
    in_commands = input()
    commands = input_analyzer(in_commands)

    # for test purpose

    if test_mode:
        print(commands)

    if commands[0] == 'L':
        command_L(commands)
    elif commands[0] == 'C':
        command_C(commands)
    elif commands[0] == 'D':
        command_D(commands)
    elif commands[0] == 'R':
        command_R(commands)
    elif commands[0] == 'Q':
        command_Q()
    elif commands[0] == 'H':
        helper()
    else:
        raise Exception("Incorrect COMMAND")


if __name__ == '__main__':
    # print("If you need any help, input 'H' for help.")
    # while not quitted:
    #     try:
    #         main_func()
    #     except Exception as e:
    #         print(e)

    profile = Profile.Profile('server', 'name', 'pwd')
    modify_profile(profile, "C:\Users\ThinkPad\Desktop\test\mark.dsu")