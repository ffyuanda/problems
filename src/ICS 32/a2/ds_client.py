import socket
from ds_protocol import response, send_post_processor,\
  send_bio_processor, send_join_processor

test_mode = False
PORT = 2021
HOST = "168.235.86.101"
token = ''

def join(sock: socket, join_msg: str):
    global token
    send = sock.makefile('w')
    send.write(join_msg + '\r\n')  # bio
    send.flush()
    token = response(sock).token


def post(sock: socket, post_msg: str):
    send = sock.makefile('w')
    send.write(post_msg + '\r\n')  # bio
    send.flush()
    response(sock)


def _bio(sock: socket, bio_msg: str):
    send = sock.makefile('w')
    send.write(bio_msg + '\r\n')  # bio
    send.flush()
    response(sock)


def send(send_type, server: str, port: int, username: str, password: str,
         message: str, bio: str = None):
    '''
    The send function joins a ds server and sends a message, bio, or both
    :param send_type the sending type of this send (post / bio / post and bio)
    :param server: The ip address for the ICS 32 DS server.
    :param port: The port where the ICS 32 DS server is accepting connections.
    :param username: The user name to be assigned to the message.
    :param password: The password associated with the username.
    :param message: The message to be sent to the server.
    :param bio: Optional, a bio for the user.
    '''
    global token
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((str(server), port))

    # join the server
    join_msg = send_join_processor(username, password)
    join(sock, join_msg)

    # TODO timestamp get()
    test_timestamp = 1612701039.1189523
    post_msg = send_post_processor(token, message, test_timestamp)
    bio_msg = send_bio_processor(token, bio, test_timestamp)

    if send_type == 'p':
        post(sock, post_msg)
    elif send_type == 'b':
        _bio(sock, bio_msg)
    elif send_type == 'pb':
        post(sock, post_msg)
        _bio(sock, bio_msg)
    else:
        print("Please provide a valid send type.")


if __name__ == '__main__':
    """
    
    {"dsuserver": "123", "username": "456", "password": "789", "bio": "123", 
    "_posts": [{"entry": "222", "timestamp": 1612701039.1189523}]}
    
    """
    test_token = '551db8b5-7adb-4f9c-b610-a8aecd5793b0'
    send_mode = 'pb'

    send(send_mode, HOST, PORT, 'ffyuanda', 'ffyuanda123', "post1", "bio3")
