import urllib.error
import urllib.request
import json


class API:
    """
    To create a new child class,
    the usages of functions should be something like the following example:

    self.set_apikey(apikey)
    self.set_url(f"https://api.openweathermap.org/data/2.5/weather?"
                 f"zip={self.zipcode},{self.ccode}&appid={self.apikey}")
    self.set_response()

    First set the api, then set the url, finally set the response (order is
    important!!!).
    """
    def __init__(self):
        self.apikey = None
        self.url = None
        self.response = None

    def _download_url(self, url_to_download: str) -> dict:
        """
        Gets the info from the url and returns a dict JSON file.
        :param url_to_download: the url that needs to be accessed
        :return: a dict JSON file
        """
        response = None
        r_obj = None

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

    def set_response(self) -> None:
        """
        Sets the response (JSON response from the server)
        """
        self.response = self._download_url(self.url)

    def get_response(self) -> dict:
        """
        Get response.
        :return: response JSON dict
        """
        return self.response

    def set_url(self, url: str) -> None:
        """
        Sets the url required to make requests to a web API.
        :param url: The url supplied by the API service
        """
        self.url = url

    def get_url(self) -> str:
        """
        Get url.
        :return: the url string
        """
        return self.url

    def set_apikey(self, apikey: str) -> None:
        """
        Sets the apikey required to make requests to a web API.
        :param apikey: The apikey supplied by the API service
        """
        self.apikey = apikey

    def get_apikey(self) -> str:
        """
        Get apikey.
        :return: the apikey string.
        """
        return self.apikey

    def transclude(self, message: str) -> None:
        """
        Replaces keywords in a message with associated API data. For
        child-classes usage.
        :param message: The message to transclude
        """
        pass


