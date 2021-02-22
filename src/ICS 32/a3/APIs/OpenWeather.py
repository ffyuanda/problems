import API_Interface


class OpenWeather(API_Interface.API):
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
        self.temperature = self.response['main']['temp']
        self.high_temperature = self.response['main']['temp_max']
        self.low_temperature = self.response['main']['temp_min']
        self.longitude = self.response['coord']['lon']
        self.latitude = self.response['coord']['lat']
        self.description = self.response['weather'][0]['description']
        self.humidity = self.response['main']['humidity']
        self.city = self.response['name']
        self.sunset = self.response['sys']['sunset']
        # attributes

    def transclude(self, message: str) -> str:
        if '@weather' in message:
            return message.replace('@weather', self.response['weather'][0]['description'])
