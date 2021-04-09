import socket
import json
from collections import namedtuple
from helper import print_error
from helper import print_ok
from helper import print_warning


def send_join_processor(username, password, token='') -> str:
    # join as existing or new user
    # {"join": {"username": "ohhimark", "password": "password123", "token": "user_token"}}
    """
    Process the inputs username password and token, and make them
    into a JSON string.

    Example usage:
    JSON_send = send_join_processor('0001', 'I am happy', '120000')

    :param username: the username of the user
    :param password: the password of the user
    :param token: the token that you want to verify with the server
    :return: JSON string
    """
    output = '{{"join": {{"username": "{0}", "password": "{1}", "token": "{2}"}}}}'.\
        format(username, password, token)
    return output


def send_post_processor(token, post, timestamp='') -> str:
    # timestamp is generate automatically in the Profile module using Python's
    # time.time() function
    # {"token": "user_token", "post": {"entry": "Hello World!", "timestamp": "1603167689.3928561"}}
    """
    Process the inputs token post and timestamp, and make them
    into a JSON string.

    Example usage:
    JSON_send = send_post_processor(0001, 'I am happy', 120000)

    :param token: the token retrieved from the server response
    :param post: the post that the user wants to upload
    :param timestamp: the timestamp that comes with a post
    :return: JSON string
    """

    output = '{{"token": "{0}", "post": {{"entry": "{1}", ' \
             '"timestamp": "{2}"}}}}'. \
        format(token, post, timestamp)
    return output


def send_bio_processor(token, bio, timestamp='') -> str:
    # for bio, you will have to generate the timestamp yourself or leave it empty.
    # {"token": "user_token", "bio": {"entry": "Hello World!", "timestamp": "1603167689.3928561"}}
    """
    Process the inputs token bio and timestamp, and make them
    into a JSON string.

    Example usage:
    JSON_send = send_bio_processor(0001, 'I am happy', 120000)

    :param token: the token retrieved from the server response
    :param bio: the post that the user wants to upload
    :param timestamp: the timestamp that comes with a post
    :return: JSON string
    """

    output = '{{"token": "{0}", "bio": {{"entry": "{1}", ' \
             '"timestamp": "{2}"}}}}'. \
        format(token, bio, timestamp)
    return output


# Create a namedtuple to hold the values we expect to retrieve from json messages.
DataTuple = namedtuple('DataTuple', ['type', 'message', 'token'])


def extract_json(json_msg:str) -> DataTuple:
    '''
    Call the json.loads function on a json string and convert it to a DataTuple object
    '''
    try:
        type_list = ['error', 'ok']

        json_obj = json.loads(json_msg)

        # make sure the type is either ok or error
        if json_obj['response']['type'] not in type_list:
            raise ValueError('Type is not ok or error.')

        type_ = json_obj['response']['type']
        message = json_obj['response']['message']

        # when token is present for ok response
        if 'token' in json_obj['response']:
            token = json_obj['response']['token']
        # when token is not present for error response
        else:
            token = ''

    except json.JSONDecodeError:
        print_error("Json cannot be decoded.")
    except KeyError:
        print_error("Non-standard response received.")
    except ValueError as e:
        print_error(e)
    else:
        return DataTuple(type_, message, token)


def response(sock: socket) -> DataTuple:
    """
    Respond to the user about detailed message retrieved from
    the server response JSON

    Sample server JSON response:

    {"response": {"type": "ok", "message": "Welcome back, ffyuanda",
    "token": "551db8b5-7adb-4f9c-b610-a8aecd5793b0"}}

    {"response": {"type": "error",
    "message": "Post rejected: invalid timestamp"}}

    :param sock: current connecting socket
    :return: a DataTuple that contains the info from the server
    response JSON.
    """
    recv = sock.makefile('r')
    resp = recv.readline()

    # resolve the conflict of two modules importing each other
    from ds_client import test_mode

    if test_mode:
        print_error('[Test mode]resp\'s value: ' + resp)
    # DataTuple conversion
    resp = extract_json(resp)
    if resp.type == 'ok':

        if resp.message.startswith('Welcome back'):
            print_ok("Successfully logged in.")
            print_ok('Server says: {}\n'.format(resp.message))

        elif resp.message.startswith('Welcome to'):
            print_ok("Successfully registered in.")
            print_ok('Server says: {}\n'.format(resp.message))

        elif 'Bio' in resp.message:
            print_ok("Bio successfully updated.")
            print_ok('Server says: {}\n'.format(resp.message))

        elif 'Post' in resp.message:
            print_ok("Post successfully sent.")
            print_ok('Server says: {}\n'.format(resp.message))

    elif resp.type == 'error':
        print_error("An error occurs.")
        print_error('Error message: {}\n'.format(resp.message))

    return resp


if __name__ == '__main__':

    jsonData = '''{"response": {"type": "ok", "message": "Welcome back, ffyuanda"}}'''

    print(extract_json(jsonData))