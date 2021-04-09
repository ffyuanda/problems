# import urllib, json
# from urllib import request, error
#
#
# def _download_url(url_to_download: str) -> dict:
#     response = None
#     r_obj = None
#
#     try:
#         response = urllib.request.urlopen(url_to_download)
#         json_results = response.read()
#         r_obj = json.loads(json_results)
#
#     except urllib.error.HTTPError as e:
#         print('Failed to download contents of URL')
#         print('Status code: {}'.format(e.code))
#
#     finally:
#         if response != None:
#             response.close()
#
#     return r_obj
#
#
# def main() -> None:
#     zip = "92697"
#     city_id = "1809858"
#     ccode = "US"
#     apikey = "ed6bc62b2f33de9c3042039ce8b14d62"
#     url = f"https://api.openweathermap.org/data/2.5/weather?zip={zip},{ccode}&appid={apikey}"
#     url_by_city = f"https://api.openweathermap.org/data/2.5/weather?id={city_id}&appid={apikey}"
#     weather_obj = _download_url(url_by_city)
#     if weather_obj is not None:
#         print(weather_obj['name'], weather_obj['weather'][0]['description'])
#
#
if __name__ == '__main__':

    # OpenWeather test
    # from OpenWeather import OpenWeather
    # zipcode = "92697"
    # ccode = "US"
    # open_weather = OpenWeather(zipcode,ccode)
    # print(open_weather.transclude('@weather'))

    # LastFM test
    # from LastFM import LastFM
    # country = 'United States'
    # last_FM = LastFM(country)
    # print(last_FM.transclude('@lastfm'))

    # Joke test
    from ExtraCreditAPI import Joke
    joke = Joke()
    print(joke.transclude('@extracredit'))
