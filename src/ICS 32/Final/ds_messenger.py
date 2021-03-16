import socket
import json, time

address = '168.235.86.101'

class DirectMessage:
    def __init__(self):
        self.recipient = None
        self.message = None
        self.timestamp = None


    def extract_json(self, json_msg:str, key:str, value:str) -> str:
        """
        Call the json.loads function on a json string and convert it to a DataTuple object.
        """
        try:
            json_obj = json.loads(json_msg)
            return_obj = json_obj[key][value]
            return return_obj
        except json.JSONDecodeError:
            print("Json cannot be decoded.")


    def convert(self, msg:str, rec:str, timestamp:str):
        self.message = msg
        self.recipient = rec
        self.timestamp = timestamp
        


class DirectMessenger:
    def __init__(self, dsuserver=None, username=None, password=None) -> None:
        self.token = None
        self.dsuserver = dsuserver
        self.username = username
        self.password = password
        self.connect()

            
    def connect(self):
        """
        Connects to DS server.
        """
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client:
            try:
                client.connect((self.dsuserver, 3021))
                join_value = '{}"username": "{}", "password": "{}", "token": ""{}'.format('{', self.username, self.password, '}')
                join_msg = '{}"join": {}{}'.format('{', join_value, '}')
                
                self.send_msg = client.makefile('w')
                self.recv = client.makefile('r')

                self.send_msg.write(join_msg + '\r\n')
                self.send_msg.flush()

                resp = self.recv.readline()
                self.dm = DirectMessage()
                assert 'Invalid password or username already taken' not in resp, 'Invalid password or username already taken.'
                self.token = dm.extract_json(resp, 'response', 'token')
                print('Logged in!')
            except AssertionError as error:
                print('ERROR.', error)

		
    def send(self, message:str, recipient:str) -> bool:
        """
        Send a directmessage to another DS user.
        {"token":"user_token", "directmessage": {"entry": "Hello World!","recipient":"ohhimark", "timestamp": "1603167689.3928561"}}
        """
        try:
            msg_info = DirectMessage()
            msg_info.message = message
            msg_info.recipient = recipient
            msg_info.timestamp = time.time()
            
            msg_format = '{}"entry": "{}", "recipient": "{}", "timestamp": "{}"{}'.format('{', msg_info.message, msg_info.recipient, msg_info.timestamp, '}')
            send_server = '{}"token": "{}", "directmessage": {}{}'.format('{', self.token, msg_format, '}')

            self.send_msg.write(send_server + '\r\n')
            self.send_msg.flush()

            resp = self.recv.readline()
            
            if "ok" in resp:
                return True
            else:
                return False
        except:
            print('ERROR.')

	
    def retrieve_new(self) -> list:
        """
        Retrieves unread messages sent to the user from DS server.
        {"token":"user_token", "directmessage": "new"}
        """
        try:
            send_server = '{}"token": "{}", "directmessage": {}{}'.format('{', self.token, '"new"', '}')

            self.send_msg.write(send_server + '\r\n')
            self.send_msg.flush()

            resp = self.recv.readline()

            unread = self.dm.extract_json(resp, 'response', 'messages')
            return unread
        except:
            print('ERROR.')

 
    def retrieve_all(self) -> list:
        """
        Retrieves all messages sent to the user from DS server.
        {"token":"user_token", "directmessage": "all"}
        """
        try:
            send_server = '{}"token": "{}", "directmessage": {}{}'.format('{', self.token, '"all"', '}')

            self.send_msg.write(send_server + '\r\n')
            self.send_msg.flush()

            resp = self.recv.readline()

            all_msg = self.dm.extract_json(resp, 'response', 'messages')
            return all_msg
        except:
            print('ERROR.')

