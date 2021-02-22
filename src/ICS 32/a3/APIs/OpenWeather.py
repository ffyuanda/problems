import API_Interface


class OpenWeather(API_Interface.API):
    def __init__(self, zipcode, ccode, apikey):
        self.zipcode = zipcode
        self.ccode = ccode
        self.set_apikey(apikey)
        self.url = f"https://api.openweathermap.org/data/2.5/weather?" \
                   f"zip={self.zipcode},{self.ccode}&appid={self.apikey}"
        super().__init__(apikey, self.url)
        self.description = self.response['weather'][0]['description']
        self.weather_obj = self._download_url(self.url)
        self.temperature = self.weather_obj['main']['temp']
        self.high_temperature = self.weather_obj['main']['temp_max']
        self.low_temperature = self.weather_obj['main']['temp_min']
        self.longitude = self.weather_obj['coord']['lon']
        self.latitude = self.weather_obj['coord']['lat']
        self.description = self.weather_obj['weather'][0]['description']
        self.humidity = self.weather_obj['main']['humidity']
        self.city = self.weather_obj['name']
        self.sunset = self.weather_obj['sys']['sunset']

    def transclude(self, message: str) -> str:
        if '@weather' in message:
            return message.replace('@weather', self.response['weather'][0]['description'])
