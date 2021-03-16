class DirectMessage:
    def __init__(self):
        self.recipient = None
        self.message = None
        self.timestamp = None


class DirectMessenger:
    def __init__(self, dsuserver=None, username=None, password=None):
        self.token = None

    def send(self, message: str, recipient: str) -> bool:
        # returns true if message successfully sent, false if send failed.
        pass

    def retrieve_new(self) -> list:
        # returns a list of DirectMessage objects containing all new messages
        pass

    def retrieve_all(self) -> list:
        # returns a list of DirectMessage objects containing all messages
        pass