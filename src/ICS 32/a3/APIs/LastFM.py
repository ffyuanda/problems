import API_Interface
# /2.0/?method=album.search&album=believe&api_key=YOUR_API_KEY&format=json
# API intro: https://www.last.fm/api/show/album.search
# Search method documentation: https://www.last.fm/api/show/album.search
# API root url: http://ws.audioscrobbler.com/2.0/
# Search example url (JSON): /2.0/?method=album.search&album=believe&api_key=YOUR_API_KEY&format=json


class LastFM(API_Interface.API):

    def __init__(self, album: str, apikey: str, limit: int = 30, page: int = 1):
        self.album = album
        self.set_apikey(apikey)
        self.limit = limit
        self.page = page
        self.root_url = "http://ws.audioscrobbler.com/2.0/"
        self.url = "?method=album.search&" \
                   "album={}&api_key={}&limit={}&page={}&format=json".format(
                    self.album, self.apikey, self.limit, self.page)
        self.url = self.root_url + self.url
        super(LastFM, self).__init__(self.apikey, self.url)
        self.artist = self.response['results']['albummatches']['album'][0]['artist']
        self.album_name = self.response['results']['albummatches']['album'][0]['name']
        self.album_url = self.response['results']['albummatches']['album'][0]['url']
        self.album_img = self.response['results']['albummatches']\
                                      ['album'][0]['image'][3]['#text']

    def transclude(self, message: str) -> str:
        if '@lastfm' in message:
            return message.replace('@lastfm', self.response['results']
            ['albummatches']['album'][0]['name'])