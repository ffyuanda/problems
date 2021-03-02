import socket
import time
import NaClProfile
from helper import print_error
from helper import print_ok
from helper import print_warning
from ds_protocol import response, send_post_processor,\
  send_bio_processor, send_join_processor

test_mode = False
PORT = 2021
HOST = "168.235.86.101"
token = ''


def join(sock: socket, username, password, public_key):
    global token
    join_msg = send_join_processor(username, password, public_key)
    send = sock.makefile('w')
    send.write(join_msg + '\r\n')  # bio
    send.flush()
    token = response(sock).token


def post(sock: socket, message, nprofile):
    send = sock.makefile('w')
    for single_post in message:
        entry = single_post.get_entry()
        # encryption
        entry = nprofile.encrypt_entry(entry, token)

        if test_mode:
            print(entry)

        timestamp = single_post.get_time()
        # and send back my public key to the server
        post_msg = send_post_processor(nprofile.public_key, entry, timestamp)
        send.write(post_msg + '\r\n')  # bio
        send.flush()
        # the server's message reception time interval must be long enough
        # and I set 1 for convenience, or it will print an error cause I'm
        # sending message to it too frequently.
        response(sock)
        time.sleep(1)


def _bio(sock: socket, bio, nprofile):
    # TODO decrypt the bio before send to the server
    timestamp = ''
    # encryption and send back my public key to the server
    bio = nprofile.encrypt_entry(bio, token)
    bio_msg = send_bio_processor(nprofile.public_key, bio, timestamp)
    send = sock.makefile('w')
    send.write(bio_msg + '\r\n')  # bio
    send.flush()
    response(sock)


def send(np: NaClProfile, send_type, server: str, port: int, username: str, password: str,
         message: list, bio: str = None):
    '''
    The send function joins a ds server and sends a message, bio, or both
    :param np: it is the NaClProfile object passed in from the main program
    :param send_type: the sending type of this send (post / bio / post and bio)
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
    done = "Upload done."

    send_types = ['p', 'b', 'pb']
    # make sure the send type is a valid one
    if send_type in send_types:
        # join the server
        join(sock, username, password, np.public_key)
        # if connected successfully, the token will be given a value
        # otherwise it's an empty string.
        if token != '':

            if send_type == 'p':
                post(sock, message, np)
                print_ok(done)
            elif send_type == 'b':
                _bio(sock, bio, np)
                print_ok(done)
            elif send_type == 'pb':
                post(sock, message, np)
                _bio(sock, bio, np)
                print_ok(done)
    else:
        print_error("Please provide a valid send type.\n"
                    "Upload failed.")

if __name__ == '__main__':
    np = NaClProfile.NaClProfile()
    kp = np.generate_keypair()
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((str(HOST), PORT))
    username = 'ffyuanda'
    pwd = 'ffyuanda123'
    join(sock, username, pwd, np.public_key)
    from Profile import Post
    test_post = Post()
    test_post.set_entry('a4 test')
    post(sock, [test_post], np)
    _bio(sock, 'a4 test bio', np)
