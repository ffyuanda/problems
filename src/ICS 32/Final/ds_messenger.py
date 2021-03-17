import socket
import json
import time
from collections import namedtuple

test_mode = False
PORT = 3021
HOST = "168.235.86.101"
DataTuple = namedtuple('DataTuple', ['type', 'message', 'token'])


class DirectMessengerError(Exception):
    pass


class DirectMessageError(Exception):
    pass


class DirectMessage:
    """

    """
    def __init__(self):
        self.recipient = None
        self.message = None
        self.timestamp = time.time()

    def get_recipient(self):
        """
        Get self.recipient
        :return: self.recipient
        """
        return self.recipient

    def get_message(self):
        """
        Get self.message
        :return: self.message
        """
        return self.message

    def get_timestamp(self):
        """
        Get self.timestamp
        :return: self.timestamp
        """
        return self.timestamp

    def set_recipient(self, name) -> None:
        """
        Set self.recipient
        :return: None
        """
        self.recipient = name

    def set_message(self, msg) -> None:
        """
        Set self.message
        :return: None
        """
        self.message = msg

    def set_timestamp(self, time) -> None:
        """
        Set self.timestamp
        :return: None
        """
        self.timestamp = time


class DirectMessenger:
    def __init__(self, dsuserver=None, username=None, password=None):
        self.token = None
        self.dsuserver = dsuserver
        self.username = username
        self.password = password
        self.protocol = DMProtocol()

        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self.sock.connect((str(self.dsuserver), PORT))
        except socket.gaierror as e:
            msg = 'The address or port seems incorrect'
            raise DirectMessengerError(msg) from e

    def send(self, message: str, recipient: str) -> bool:
        # returns true if message successfully sent, false if send failed.

        self.join(self.sock, self.username, self.password)
        self.send_dm(self.sock, message, recipient)

    def join(self, sock: socket, username, password) -> None:
        """
        Joins the server and feed the retrieved token back to self.token
        Uses send_join_processor() from DMProtocol
        :param sock:
        :param username:
        :param password:
        :return: None
        """
        join_msg = self.protocol.send_join_processor(username, password)
        self.protocol.sender(sock, join_msg)
        self.token = self.protocol.response(sock).token

    def send_dm(self, sock: socket, message: str, recipient: str) -> None:
        """
        Wraps up message and recipient into a DirectMessage and send it
        :param sock:
        :param message:
        :param recipient:
        :return: None
        """

        dm = DirectMessage()
        dm.set_message(message)
        dm.set_recipient(recipient)

        message = self.protocol.send_directmessage_processor(self.token, dm)

        self.protocol.sender(sock, message)
        self.protocol.response(sock)

    def retrieve_new(self) -> list:
        # returns a list of DirectMessage objects containing all new messages
        self.join(self.sock, self.username, self.password)
        msg = self.protocol.request_unread_processor(self.token)

        self.protocol.sender(self.sock, msg)
        self.protocol.response(self.sock)

    def retrieve_all(self) -> list:
        # returns a list of DirectMessage objects containing all messages

        # make sure self.token is filled with the correct data
        self.join(self.sock, self.username, self.password)
        msg = self.protocol.request_all_processor(self.token)

        self.protocol.sender(self.sock, msg)
        self.protocol.response(self.sock)


class DMProtocol:
    def __init__(self):
        pass

    def sender(self, sock: socket, msg: str):
        send = sock.makefile('w')
        send.write(msg + '\r\n')
        send.flush()

    def extract_json(self, json_msg: str) -> DataTuple:
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
            # either 'message' or 'messages' will be returned from the server
            if 'message' in json_obj['response']:
                # message here is a str
                message = json_obj['response']['message']
            elif 'messages' in json_obj['response']:
                # message here is a list
                message = json_obj['response']['messages']
                # print(json_obj['response'])

            # when token is present for ok response
            if 'token' in json_obj['response']:
                token = json_obj['response']['token']
            # when token is not present for error response
            else:
                token = ''

        except json.JSONDecodeError:
            print("Json cannot be decoded.")
        except KeyError as e:
            print("Non-standard response received.")
        except ValueError as e:
            print(e)
        else:
            return DataTuple(type_, message, token)

    def response(self, sock: socket) -> DataTuple:
        """

        :param sock: current connecting socket
        :return: a DataTuple that contains the info from the server
        response JSON
        """
        recv = sock.makefile('r')
        resp = recv.readline()
        # print(resp)
        resp = self.extract_json(resp)

        # DataTuple conversion
        if resp.type == 'ok':
            if type(resp.message) is str:

                if resp.message.startswith('Welcome back'):
                    print("Successfully logged in.")
                    print('Server says: {}\n'.format(resp.message))

                elif resp.message.startswith('Welcome to'):
                    print("Successfully registered in.")
                    print('Server says: {}\n'.format(resp.message))

                elif 'Direct message sent' in resp.message:
                    print("Direct message successfully sent.")
                    print('Server says: {}\n'.format(resp.message))

                elif 'Post' in resp.message:
                    print("Post successfully sent.")
                    print('Server says: {}\n'.format(resp.message))

            elif type(resp.message) is list:
                print('Messages successfully retrieved!')
                print('Messages listed here:')
                for m in resp.message:
                    print(m)

        elif resp.type == 'error':
            print("An error occurs.")
            print('Error message: {}\n'.format(resp.message))
        return resp

    def send_join_processor(self, username, password, token='') -> str:
        """
        Process the inputs username password and token, and make them
        into a JSON string.

        Send format:
        {"join": {"username": "ohhimark", "password": "password123", "token": "user_token"}}

        Example usage:
        JSON_send = send_join_processor('0001', 'I am happy', '120000')

        :param username: the username of the user
        :param password: the password of the user
        :param token: the token that you want to verify with the server
        :return: JSON string
        """
        output = '{{"join": {{"username": "{0}", "password": "{1}", "token": "{2}"}}}}'. \
            format(username, password, token)
        return output

    def send_directmessage_processor(self, token, dm: DirectMessage) -> str:
        """
        Send format:
        {"token":"user_token", "directmessage": {"entry": "Hello World!","recipient":"ohhimark", "timestamp": "1603167689.3928561"}}
        :return: the formatted JSON string to server
        """
        entry = dm.get_message()
        recipient = dm.get_recipient()

        # set the timestamp when sending the message, it shows when the message was originally sent
        timestamp = time.time()
        dm.set_timestamp(timestamp)
        timestamp = dm.get_timestamp()

        output = '{{"token": "{0}", "directmessage": {{"entry": "{1}", "recipient": "{2}", "timestamp": "{3}"}}}}'.\
            format(token, entry, recipient, timestamp)
        return output

    def request_unread_processor(self, token):
        """
        Request format:
        {"token":"user_token", "directmessage": "new"}
        :return: the formatted JSON string to server
        """
        output = '{{"token": "{0}", "directmessage": "new"}}'.format(token)
        return output

    def request_all_processor(self, token):
        """
        Request format:
        {"token":"user_token", "directmessage": "all"}
        :return:
        """
        output = '{{"token": "{0}", "directmessage": "all"}}'.format(token)
        return output


if __name__ == '__main__':

    sender_dsuserver = HOST
    sender_username = 'The_Group_Sender'
    sender_password = 'The_Group_Sender_password'
    sender = DirectMessenger(sender_dsuserver, sender_username, sender_password)
    sender.send('something nice', 'The_Group_Receiver')

    receiver_username = 'The_Group_Receiver'
    receiver_password = 'The_Group_Receiver_password'
    receiver_dsuserver = HOST
    receiver = DirectMessenger(receiver_dsuserver, receiver_username, receiver_password)
    receiver.retrieve_new()
    receiver.retrieve_all()
