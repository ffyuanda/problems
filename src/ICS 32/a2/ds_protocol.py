import socket
import json
import color
from collections import namedtuple
color_mod = color.bcolors()


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
        print("Json cannot be decoded.")
    except KeyError:
        print("Non-standard response received.")
    except ValueError as e:
        print(e)
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
        print(resp)
    # DataTuple conversion
    resp = extract_json(resp)
    if resp.type == 'ok':

        if resp.message.startswith('Welcome back'):
            msg = color_mod.color_code("Successfully logged in.\n", 'ok')
            print('{}'
                  'Server says: {}'.format(msg, resp.message))

        elif resp.message.startswith('Welcome to'):
            msg = color_mod.color_code("Successfully registered in.\n", 'ok')
            print('{}'
                  'Server says: {}'.format(msg, resp.message))

        elif 'Bio' in resp.message:
            msg = color_mod.color_code("Bio successfully updated.\n", 'ok')
            print('{}'
                  'Server says: {}'.format(msg, resp.message))

        elif 'Post' in resp.message:
            msg = color_mod.color_code("Post successfully sent.\n", 'ok')
            print('{}'
                  'Server says: {}'.format(msg, resp.message))

    elif resp.type == 'error':
        msg = color_mod.color_code("An error occurs.\n", 'error')
        print('{}'
              'Error message: {}'.format(msg, resp.message))

    return resp


if __name__ == '__main__':

    jsonData = '''{"response": {"type": "ok", "message": "Welcome back, ffyuanda"}}'''

    print(extract_json(jsonData))