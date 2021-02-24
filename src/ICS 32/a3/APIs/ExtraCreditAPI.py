import API_Interface


class Joke(API_Interface.API):
    """
    Random jokes generator.

    API website: https://github.com/15Dkatz/official_joke_api
    API sample url (JSON): https://official-joke-api.appspot.com/random_joke
    """
    def __init__(self):
        super().__init__()
        self.set_url("https://official-joke-api.appspot.com/random_joke")
        self.set_response()

        # attributes
        self.type = self.response['type']
        self.setup = self.response['setup']
        self.punchline = self.response['punchline']

    def transclude(self, message: str) -> str:
        if '@extracredit' in message:
            return message.replace('@extracredit', "-{} -{}".
                                   format(self.setup,
                                          self.punchline))
