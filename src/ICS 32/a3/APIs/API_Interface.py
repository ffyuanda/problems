import urllib.error
import urllib.request
import json


class API:
    def __init__(self, apikey, url):
        # specified in child classes
        self.url = url
        # specified in child classes
        self.apikey = None
        self.set_apikey(apikey)
        self.response = self._download_url(self.url)

    def _download_url(self, url_to_download: str):
        response = None
        r_obj = None
        # print(self.url)

        try:
            response = urllib.request.urlopen(url_to_download)
            json_results = response.read()
            r_obj = json.loads(json_results)

        except urllib.error.HTTPError as e:
            print('Failed to download contents of URL')
            print('Status code: {}'.format(e.code))

        except Exception as e:
            print('An error has occurred:\n', e)

        finally:
            if response is not None:
                response.close()

        return r_obj

    def set_apikey(self, apikey: str) -> None:
        '''
        Sets the apikey required to make requests to a web API.
        :param apikey: The apikey supplied by the API service
        '''
        self.apikey = apikey

    def transclude(self, message: str) -> str:
        '''
        Replaces keywords in a message with associated API data.
        :param message: The message to transclude

        :returns: The transcluded message
        '''
        if '@weather' in message:
            return message.replace('@weather', self.response['weather'][0]['description'])
        if '@lastfm' in message:
            return message.replace('@lastfm', self.response['results']['albummatches']['album'][0]['name'])
