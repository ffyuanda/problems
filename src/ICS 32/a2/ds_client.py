import socket
import color
import time
from ds_protocol import response, send_post_processor,\
  send_bio_processor, send_join_processor

test_mode = False
PORT = 2021
HOST = "168.235.86.101"
token = ''
color_mod = color.bcolors()


def join(sock: socket, username, password):
    global token
    join_msg = send_join_processor(username, password)
    send = sock.makefile('w')
    send.write(join_msg + '\r\n')  # bio
    send.flush()
    token = response(sock).token


def post(sock: socket, message):
    send = sock.makefile('w')
    for single_post in message:
        entry = single_post.get_entry()
        if test_mode:
            print(entry)
        timestamp = single_post.get_time()
        post_msg = send_post_processor(token, entry, timestamp)
        send.write(post_msg + '\r\n')  # bio
        send.flush()
        # the server's message reception time interval must be long enough
        # and I set 1 for convenience, or it will print an error cause I'm
        # sending message to it too frequently.
        time.sleep(1)
    response(sock)


def _bio(sock: socket, bio):
    timestamp = ''
    bio_msg = send_bio_processor(token, bio, timestamp)
    send = sock.makefile('w')
    send.write(bio_msg + '\r\n')  # bio
    send.flush()
    response(sock)


def send(send_type, server: str, port: int, username: str, password: str,
         message: list, bio: str = None):
    '''
    The send function joins a ds server and sends a message, bio, or both
    :param send_type the sending type of this send (post / bio / post and bio)
    :param server: The ip address for the ICS 32 DS server.
    :param port: The port where the ICS 32 DS server is accepting connections.
    :param username: The user name to be assigned to the message.
    :param password: The password associated with the username.
    :param message: The list of posts to be sent to the server.
    :param bio: Optional, a bio for the user.
    '''
    global token
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((str(server), port))
    done = color_mod.color_code("Upload done.", 'ok')

    send_types = ['p', 'b', 'pb']
    # make sure the send type is a valid one
    if send_type in send_types:
        # join the server
        join(sock, username, password)
        # if connected successfully, the token will be given a value
        # otherwise it's an empty string.
        if token != '':

            if send_type == 'p':
                post(sock, message)
                print(done)
            elif send_type == 'b':
                _bio(sock, bio)
                print(done)
            elif send_type == 'pb':
                post(sock, message)
                _bio(sock, bio)
                print(done)
    else:
        msg = color_mod.color_code("Please provide a valid send type.\n"
              "Upload failed.", 'error')
        print(msg)
