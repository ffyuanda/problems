import socket
import json
import time
from collections import namedtuple

test_mode = False
PORT = 3021
HOST = "168.235.86.101"
DataTuple = namedtuple('DataTuple', ['type', 'message', 'token'])


class DMProtocolError(Exception):
    """
    Custom error class for DMProtocolError
    """
    pass


class DirectMessengerError(Exception):
    """
    Custom error class for DirectMessenger
    """
    pass


class DirectMessage:
    """
    The DirectMessage object using in sending messages.
    """
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
    """
    The class responsible for sending and receiving messages to and from another
    user.
    """
    def __init__(self, dsuserver: str = None, username: str = None, password: str = None):
        self.token = None
        self.dsuserver = dsuserver
        self.username = username
        self.password = password
        # DMProtocol for usage
        self.protocol = DMProtocol()
        # Initialize the sock along with the DirectMessenger object
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self.sock.connect((str(self.dsuserver), PORT))
        except socket.gaierror as e:
            msg = 'The address or port seems incorrect'
            raise DirectMessengerError(msg) from e

    def send(self, message: str, recipient: str) -> bool:
        """
        Send the message to the specified recipient.
        Returns true if message successfully sent, false if send failed.
        :param message: the input string that needs to be sent to another user
        :param recipient: the user's name
        :return: success, which indicates if the sending is successful
        """
        # join first to set self.token
        self.join(self.sock, self.username, self.password)
        success = self.send_dm(self.sock, message, recipient)
        return success

    def join(self, sock: socket, username, password) -> None:
        """
        Joins the server and feed the retrieved token back to self.token
        :param sock: currently working socket
        :param username: username of current user
        :param password: password of current user
        :return: None
        """
        join_msg = self.protocol.send_join_processor(username, password)
        self.protocol.sender(sock, join_msg)
        self.token = self.protocol.response(sock).token

    def send_dm(self, sock: socket, message: str, recipient: str) -> bool:
        """
        Wraps up message and recipient into a DirectMessage and send it
        :param sock: currently working socket
        :param message: the input string that needs to be sent to another user
        :param recipient: the user's name
        :return: a bool indicates if the sending is successful
        """

        dm = DirectMessage()
        dm.set_message(message)
        dm.set_recipient(recipient)

        message = self.protocol.send_directmessage_processor(self.token, dm)
        self.protocol.sender(sock, message)

        response = self.protocol.response(sock)
        if response.type == 'ok':
            return True
        else:
            return False

    def retrieve_new(self) -> list:
        """
        Returns a list of DirectMessage objects containing all new messages
        :return: a list of DirectMessage objects containing all new messages
        """

        # make sure self.token is filled with the correct data
        self.join(self.sock, self.username, self.password)

        msg = self.protocol.request_unread_processor(self.token)
        self.protocol.sender(self.sock, msg)

        dm_list = self.protocol.response(self.sock).message

        return dm_list

    def retrieve_all(self) -> list:
        """
        Returns a list of DirectMessage objects containing all messages
        :return: a list of DirectMessage objects containing all messages
        """

        # make sure self.token is filled with the correct data
        self.join(self.sock, self.username, self.password)

        msg = self.protocol.request_all_processor(self.token)
        self.protocol.sender(self.sock, msg)

        dm_list = self.protocol.response(self.sock).message

        return dm_list


class DMProtocol:
    """
    A protocol class works collaboratively with DirectMessenger class.
    It can also be modified to support other uses of server communication.
    """
    def __init__(self):
        pass

    def sender(self, sock: socket, msg: str) -> None:
        """
        A wrapper method to simplify the sending process.
        :param sock: currently working socket
        :param msg: the message needs to be sent
        :return: None
        """
        send = sock.makefile('w')
        send.write(msg + '\r\n')
        send.flush()

    def extract_json(self, json_msg: str) -> DataTuple:
        """
        Call the json.loads function on a JSON string and convert it to a DataTuple object
        :param json_msg: the input JSON str
        :return: the DataTuple object contains json_msg's information
        """
        try:
            type_list = ['error', 'ok']

            json_obj = json.loads(json_msg)

            # make sure the type is either ok or error
            if json_obj['response']['type'] not in type_list:
                raise ValueError('Type is not ok or error.')

            type_ = json_obj['response']['type']

            # either 'message' or 'messages' will be returned from the server
            if 'message' in json_obj['response']:
                # message here is a str from server
                message = json_obj['response']['message']
            elif 'messages' in json_obj['response']:
                # message here is a list of DirectMessage
                message = json_obj['response']['messages']

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
        It listens the raw response from the server at sock and convert them
        to user friendly messages.
        :param sock: current working socket
        :return: a DataTuple that contains the info from the server
        response JSON
        """
        recv = sock.makefile('r')
        resp = recv.readline()
        resp = self.extract_json(resp)

        # DataTuple conversion
        if resp.type == 'ok':
            # when sending DirectMessage
            if type(resp.message) is str:

                if 'Direct message sent' in resp.message:
                    print("Direct message successfully sent.")
                    print('Server says: {}\n'.format(resp.message))

            # when retrieving DirectMessage
            elif type(resp.message) is list:
                print('Messages successfully retrieved!')

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

        :param username: the username of the user
        :param password: the password of the user
        :param token: the token that you want to verify with the server
        :return: the formatted JSON string to server
        """
        output = '{{"join": {{"username": "{0}", "password": "{1}", "token": "{2}"}}}}'. \
            format(username, password, token)
        return output

    def send_directmessage_processor(self, token, dm: DirectMessage) -> str:
        """
        Process the inputs token and dm, and make them
        into a JSON string.

        Send format:
        {"token":"user_token", "directmessage": {"entry": "Hello World!","recipient":"ohhimark", "timestamp": "1603167689.3928561"}}

        :param token: the token of this message's sender
        :param dm: the DirectMessage object that needs to be sent
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

    def request_unread_processor(self, token) -> str:
        """
        Process the inputs token, and make it into a JSON string.

        Request format:
        {"token":"user_token", "directmessage": "new"}

        :param token: the token of this message's sender
        :return: the formatted JSON string to server
        """
        output = '{{"token": "{0}", "directmessage": "new"}}'.format(token)
        return output

    def request_all_processor(self, token) -> str:
        """
        Process the inputs token, and make it into a JSON string.

        Request format:
        {"token":"user_token", "directmessage": "all"}

        :param token: the token of this message's sender
        :return: the formatted JSON string to server
        """
        output = '{{"token": "{0}", "directmessage": "all"}}'.format(token)
        return output


if __name__ == '__main__':

    # for test usage, run and see what happens!

    sender_dsuserver = HOST
    sender_username = 'The_Group_Sender'
    sender_password = 'The_Group_Sender_passworssd'
    sender = DirectMessenger(sender_dsuserver, sender_username, sender_password)
    print(sender.send('something nice', 'The_Group_Receiver'))

    print()

    receiver_username = 'The_Group_Receiver'
    receiver_password = 'The_Group_Receiver_password'
    receiver_dsuserver = HOST
    receiver = DirectMessenger(receiver_dsuserver, receiver_username, receiver_password)

    print("receiver's new messages:")
    print(receiver.retrieve_new())

    print()

    print("receiver's all messages:")
    print(receiver.retrieve_all())

