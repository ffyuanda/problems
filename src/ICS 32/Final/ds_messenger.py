import socket
import json
from collections import namedtuple

test_mode = False
PORT = 2021
HOST = "168.235.86.101"
DataTuple = namedtuple('DataTuple', ['type', 'message', 'token'])


class DirectMessengerError(Exception):
    pass


class DirectMessageError(Exception):
    pass


class DirectMessage:
    def __init__(self):
        self.recipient = None
        self.message = None
        self.timestamp = None

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

    def send(self, message: str, recipient: str) -> bool:
        # returns true if message successfully sent, false if send failed.
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            sock.connect((str(HOST), PORT))
        except socket.gaierror as e:
            msg = 'The address or port seems incorrect'
            raise DirectMessengerError(msg) from e

    def join(self, sock: socket, username, password):
        join_msg = self.protocol.send_join_processor(username, password)
        send = sock.makefile('w')
        send.write(join_msg + '\r\n')
        send.flush()
        self.token = self.protocol.response(sock).token

    def retrieve_new(self) -> list:
        # returns a list of DirectMessage objects containing all new messages
        pass

    def retrieve_all(self) -> list:
        # returns a list of DirectMessage objects containing all messages
        pass


class DMProtocol:
    def __init__(self):
        pass

    def extract_json(json_msg: str) -> DataTuple:
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

    def response(self, sock: socket) -> DataTuple:
        """

        :param sock: current connecting socket
        :return: a DataTuple that contains the info from the server
        response JSON
        """
        recv = sock.makefile('r')
        resp = recv.readline()
        resp = self.extract_json(resp)
        print(resp)
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

    def send_directmessage_processor(self, token, dm: DirectMessage):
        """
        Send format:
        {"token":"user_token", "directmessage": {"entry": "Hello World!","recipient":"ohhimark", "timestamp": "1603167689.3928561"}}
        :return:
        """
        entry = dm.get_message()
        recipient = dm.get_recipient()
        timestamp = dm.get_timestamp()
        output = '{{"token": "{0}", "directmessage": {{"entry": "{1}", "recipient": "{2}", "timestamp": "{3}"}}}}'.\
            format(token, entry, recipient, timestamp)
        return output

    def request_unread_processor(self, token, dm):
        """
        Request format:
        {"token":"user_token", "directmessage": "new"}
        :return:
        """
        pass

    def request_all_processor(self, token, dm):
        """
        Request format:
        {"token":"user_token", "directmessage": "all"}
        :return:
        """
        pass

    def response_processor(self):
        """
        Processes the response from the server.
        :return:
        """
        pass


if __name__ == '__main__':

    sender = DirectMessenger()
    sender.dsuserver = HOST
    sender.username = 'The_Group_Sender'
    sender.password = 'The_Group_Sender_password'

    receiver = DirectMessenger()
    receiver.dsuserver = HOST
    receiver.username = 'The_Group_Receiver'
    receiver.password = 'The_Group_Receiver_password'

    message = DirectMessage()
    message.set_message("test")
    message.set_recipient("test")
    message.set_timestamp("test")
    test_token = "test"

    protocol = DMProtocol()
    test_output = protocol.send_directmessage_processor(test_token, message)
    print(test_output)
