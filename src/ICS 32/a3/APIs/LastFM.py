import API_Interface
# /2.0/?method=geo.gettoptracks&country=spain&api_key=YOUR_API_KEY&format=json
# API intro: https://www.last.fm/api/show/geo.getTopTracks
# API root url: http://ws.audioscrobbler.com/2.0/
# Search example url (JSON): http://ws.audioscrobbler.com/2.0/?method=geo.gettoptracks&country=spain&api_key=YOUR_API_KEY&format=json


class LastFM(API_Interface.API):
    """
    It gives the top hit track of music in a specific country.
    """

    def __init__(self, country: str):
        super().__init__()
        # deal with the countries that have whitespace in the name:
        # e.g. United States
        self.country = country.replace(' ', '%20')
        apikey = 'a1fd9ccdee9190487ed8eb7d41c693eb'
        self.set_apikey(apikey)
        self.root_url = "http://ws.audioscrobbler.com/2.0/"
        self.url = "?method=geo.gettoptracks&country={}&api_key={}&" \
                   "&limit=1&format=json"\
                   .format(self.country, self.apikey)
        self.url = self.root_url + self.url
        self.set_url(self.url)
        self.set_response()

    def transclude(self, message: str) -> str:
        if '@lastfm' in message:
            return message.replace('@lastfm', self.response['tracks']['track'][0]['name'])
