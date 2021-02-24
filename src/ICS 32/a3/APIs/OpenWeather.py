import API_Interface


class OpenWeather(API_Interface.API):
    """
    Weather plugin.

    API website: https://openweathermap.org/current
    API sample url (JSON): https://api.openweathermap.org/data/2.5/weather?zip=94040,us&appid={API key}
    """
    def __init__(self, zipcode, ccode):
        super().__init__()
        self.zipcode = zipcode
        self.ccode = ccode
        apikey = "ed6bc62b2f33de9c3042039ce8b14d62"
        self.set_apikey(apikey)
        self.set_url(f"https://api.openweathermap.org/data/2.5/weather?"
                     f"zip={self.zipcode},{self.ccode}&appid={self.apikey}")
        self.set_response()

        # attributes
        self.description = self.response['weather'][0]['description']

    def transclude(self, message: str) -> str:
        if '@weather' in message:
            return message.replace('@weather', self.description)
