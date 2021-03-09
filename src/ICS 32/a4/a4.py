"""
Homework a4 for I&C SCI 32: PROG SOFTWARE LIBR
at University of California, Irvine

Student info:
Name: Shaoxuan Yuan
ID: 89832399

    For developers:

    Test mode example:

        "[Test mode]The command list after process: "

    common interfaces:

        all_items, dirs, files = command_L_get_items(path)

    Color coded messages:

        print_ok is for ok messages like upload done or action complete.

        print_warning is for warning user's illegal input.

        print_error is for system's error which needs to be handled by developer
        or test_mode will also be displayed in error red color.




"""
from pathlib import Path
from helper import print_ok
from helper import print_warning
from helper import print_error
from NaClProfile import NaClProfile
from NaClProfile import DsuFileError, DsuProfileError
import Profile
import ds_client as client
import OpenWeather
import LastFM
import ExtraCreditAPI
import nacl

quitted = False
test_mode = False
PORT = 2021
HOST = "168.235.86.101"


def command_Q():
    """
    Quit functionality that changes global quitted variable
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
        print_warning('There needs to be at least 1 input for COMMAND L')
    else:
        p = Path(commands[1])
        try:
            all_items, dirs, files = command_L_get_items(p)
        except WindowsError:
            print_error("ERROR")

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
                print_warning('Option here should be either -r or -f')

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
    profile = NaClProfile(dsuserver, username, password)
    profile.generate_keypair()
    profile.bio = bio
    # encrypt the bio
    profile.bio = profile.encrypt_entry(profile.bio)
    profile.add_post(post)

    profile = posts_transclude(profile)
    display_profile(profile)
    profile.save_profile(path)
    print('DSU file storing...')
    print_ok("Local file stored at: " + str(path))

    # ask if the user wants to upload
    upload_option(profile)


def upload_option(profile: NaClProfile):
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
    message = profile.get_posts()
    bio = profile.bio
    # decrypt the bio from the local DSU file / current profile
    bio = profile.nacl_profile_decrypt(bio)

    if option == 'Y':
        print("Send post (p)")
        print("Update bio (b)")
        print("Send post and update bio (pb)")
        option = input()
        client.send(profile, option, server, PORT, username, password,
                    message, bio)

    elif option == 'N':
        print_ok("Done.")

    else:
        print_warning('please enter either y or n\n')
        upload_option(profile)


def posts_transclude(profile: NaClProfile):
    """
    Transclude every single post in the posts list of a profile object.
    Use it before saving the DSU file in order to change the posts list
    of the profile object before uploading or saving to local.
    :param profile: current working Profile object
    :return: modified Profile object
    """
    # posts here is not the actual _posts private list from the NaClProfile object
    # they are the decrypted copy of the _posts
    posts = profile.get_posts()
    print('Transcluding...')
    for i in range(len(posts)):
        if '@weather' in posts[i]['entry']:
            a = OpenWeather.OpenWeather('92697', 'US')
            entry = a.transclude(posts[i].get_entry())
            # entry = profile.encrypt_entry(entry)
            posts[i].set_entry(entry)
        if '@lastfm' in posts[i]['entry']:
            a = LastFM.LastFM('United States')
            entry = a.transclude(posts[i].get_entry())
            # entry = profile.encrypt_entry(entry)
            posts[i].set_entry(entry)
        if '@extracredit' in posts[i]['entry']:
            a = ExtraCreditAPI.Joke()
            entry = a.transclude(posts[i].get_entry())
            # entry = profile.encrypt_entry(entry)
            posts[i].set_entry(entry)

    # empty the actual _posts private list from the NaClProfile object
    profile._posts = []
    # move each post in the posts temporary holder back to the actual _posts
    for post in posts:
        profile.add_post(post)

    print_ok('Transcluded!')
    return profile


def modify_profile():
    """
    Load up the profile DSU file for modification.
    :return: None
    """
    path = input('Input the DSU file\'s path which you want to modify.\n'
                 'For example: C:\\Users\\ThinkPad\\Desktop\\test\\mark.dsu\n')
    profile = NaClProfile()
    try:
        profile.load_profile(path)
    except DsuFileError:
        print_warning('This might not be a valid path.')
    else:
        prompt = """\nWhich part you want to modify?
        server (se)
        username (u)
        password (pwd)
        bio (b)
        posts (p)
        save modification(s)"""

        print_ok(path + " is ready for modification.\n")

        # keep prompting the user to choose an option for modification
        while True:
            display_profile(profile)
            print(prompt)

            option = input().lower()
            if option == "u":
                mod = input("Enter the new username: \n")
                profile.username = mod

            elif option == "se":
                mod = input("Enter the new server address: \n")
                profile.dsuserver = mod

            elif option == "pwd":
                mod = input("Enter the new password: \n")
                profile.password = mod

            elif option == "b":
                mod = input("Enter the new bio: \n")
                profile.bio = profile.nacl_profile_encrypt(mod)

            elif option == "p":
                # get users option
                option = input("Add (a) or delete (d) a post?\n").lower()

                if option == "a":
                    entry = input("Write your entry below:\n")
                    post = Profile.Post()
                    post.set_entry(entry)
                    profile.add_post(post)
                    print_ok("Entry added.")

                elif option == 'd':
                    entry = int(input("Which entry you want to delete?\n"))
                    profile.del_post(entry)
                    print_ok('Entry deleted.')

                else:
                    print_warning("Please enter either a or d.")

            elif option == "s":
                profile = posts_transclude(profile)
                profile.save_profile(path)
                display_profile(profile)
                print_ok("All saved.")
                break
            else:
                print_warning("Please enter a valid option. Or "
                            "input 's' to save (quit).")


def command_C(commands):
    """
    Functionalities within command C,
    will read the input and create a new file.
    :param commands: the input command
    :return: None
    """

    if len(commands) != 4:
        print_warning('There needs to be exactly 3 inputs for COMMAND C')
    else:

        p = commands[1] + '\\'
        name = commands[3]
        extention = '.dsu'
        path = p + name + extention

        if test_mode:
            print_error("[Test mode]COMMAND C's path: " + path)

        if commands[2] == '-n':
            try:
                path = Path(path)
                # create the dsu file
                path.touch()
                # for Profile creation (after the dsu file is created)
                create_profile(str(path))
            except FileNotFoundError:
                print_warning('This is a invalid directory')
        else:
            print_warning("This option is invalid for COMMAND C")


def command_D(commands):
    """
    Functionalities within command D, allow the user to delete a DSU file.
    :param commands: the input command
    :return: None
    """
    if len(commands) < 2:
        print_warning('There needs to be at least 1 input for COMMAND D')
    else:
        path = Path(commands[1])

        if not str(path).endswith('.dsu'):
            print_warning('It needs to be a DSU file with .dsu suffix')
        else:
            try:
                path.unlink()
                print_ok(str(path) + ' DELETED')
            except FileNotFoundError:
                print_warning("File not found!")


def command_R(commands):
    """
    Functionalities within command R, print the content of a DSU file.
    :param commands: the input command
    :return: None
    """
    if len(commands) < 2:
        print_warning('There needs to be at least 1 input for COMMAND R')
    elif len(commands) == 2:
        path = Path(commands[1])

        if not str(path).endswith('.dsu'):
            print_warning('It needs to be a DSU file with .dsu suffix')
        else:
            try:
                with open(str(path), 'r') as f:
                    if path.stat().st_size == 0:
                        print_warning('EMPTY')
                    else:
                        output = f.readlines()
                        for i in range(len(output)):
                            if i == len(output) - 1:
                                # should not print a newline at the end
                                print(output[i], end='')
                            else:
                                print(output[i])
            except FileNotFoundError:
                print_warning('This file or directory does not exist: \'{}\''.format(str(path)))
    # -l option to load
    elif len(commands) == 3 and commands[2] == '-l':
        profile = NaClProfile()
        profile.load_profile(commands[1])
        display_profile(profile)
        upload_option(profile)
    else:
        print_warning("The format for COMMAND R seems not right")


def display_profile(profile: NaClProfile):
    """
    Load the profile up and print out the data in the DSU file.
    :param profile: current working profile object
    :return: None
    """
    print("server: " + profile.dsuserver)
    print("username: " + profile.username)
    print("password: " + profile.password)
    # decrypt the bio for human read
    print("bio: " + profile.nacl_profile_decrypt(profile.bio))
    list_posts(profile)


def list_posts(profile: NaClProfile):
    """
    Print out the posts in a profile object.
    :param profile: current working profile object
    :return: None
    """
    print("Here are your posts:")
    posts = profile.get_posts()
    for i in range(len(posts)):
        print("Entry {}:".format(str(i)), posts[i].get_entry())


def input_analyzer(in_commands):
    """
    Analyze the input string and turn it into
    readable list format.
    :param in_commands: the user input string
    :return: a list that contains the processed user input (commands)
    """
    out_commands = []
    command_list = ['L', 'Q', 'C', 'D', 'R', 'M']
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
            print_error("[Test mode]real_path in input_analyzer:" + real_path)

        if 0 < i < length - 1:

            if commands[i] not in built_ins:

                # i is not the last digit
                if i < length - 1:
                    # this is a path with whitespaces
                    if (commands[i + 1] not in built_ins) \
                            or (commands[i - 1] not in built_ins):
                        real_path += commands[i] + ' '
                    # this is a path without whitespaces
                    else:
                        real_path = commands[i]

                # i is the last digit
                else:

                    # this is a path with whitespaces
                    if commands[i - 1] not in built_ins:
                        real_path += commands[i] + ' '

                    # there are only two elements, and command[i] is a
                    # valid path without whitespace
                    elif commands[i - 1] in command_list:
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
    print("\nThis color represents an input prompt or normal system information.")
    print_ok("This color represents successful or approved operations.")
    print_warning("This color represents user's illegal inputs or unexpected operations.")
    print_error("This color represents systematic error or test mode message "
                "that should be handled by developers.\n")

    print("""Usage format: [COMMAND] [INPUT] [[-]OPTION] [INPUT]
    
    Some tips:
    If you want to CREATE a file, go to COMMAND: C
    If you want to MODIFY a file, go to COMMAND: M
    If you want to UPLOAD a file, go to COMMAND: R
    
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

    COMMAND: M - Modify a saved DSU file and the profile relates to it.
                 After the command is typed in, the system will load up
                 a DSU file to a Profile object to modify the data.
                 It will prompt you how to modify and save the data.

                Example usage:
                M (just put in 'M' and wait for the prompt)

    COMMAND: D - Delete the file.

                Example usage:
                D c:\\users\\mark\\a1\\mark.dsu

    COMMAND: R - Read the contents of a file and upload it to the server.


                OPTIONs:
                -l load the specified file from the path, If you want to 
                upload a file directly, use this.

                After the loading of DSU file and profile, the
                program will ask you if you want to upload things
                to the DSU server.

                Example usage:
                R c:\\users\\mark\\a1\\mark.dsu
                R c:\\users\\mark\\a1\\mark.dsu -l
                
    API Supports:
    
                When you are writing posts, you have some API add-ins support
                available for better writing! All the keywords will be transcluded
                before the DSU file is saved. You will see "Transcluding..." when
                the file is being transcluded.
                
                OpenWeather API:
                You can simply add '@weather' in your post at anywhere, and the
                '@weather' script will translate to the current weather in Irvine.
                Supports for your current location will be added later.
                               
                LastFM API:
                You can simply add '@lastfm' in your post at anywhere, and the
                '@lastfm' script will translate to the United Stats' top hit 
                song on LastFM in current time period.
                Supports for other countries will be added later.
                
                Joke API:
                You can simply add '@extracredit' in your post at anywhere, and the
                '@extracredit' script will translate to a random joke.
                
                !CAUTION!: this api may not be accessible in some regions since
                the IP address of the api's server is blocked in some area, if
                you encounter a trancluding problem or connection issue, please
                connect to UCI's VPN when you are using this feature. 
              """)


def main_func():
    """
    The function wrapper.
    :return: None
    """
    in_commands = input()
    commands = input_analyzer(in_commands)
    commands[0] = commands[0].upper()

    # for test purpose

    if test_mode:
        print_error("[Test mode]The command list after process: " + str(commands))
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
    elif commands[0] == 'M':
        modify_profile()
    else:
        print_warning("Incorrect COMMAND")


if __name__ == '__main__':
    print("Welcome to DSU file management system!")
    print("It helps you to create posts, modify bios, upload DSU files")
    print("to the server and chat with people there!\n")
    print("If you need any help, input 'H' for help.")
    while not quitted:
        main_func()
