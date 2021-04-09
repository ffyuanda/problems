import urllib, json
from urllib import request, error


def send_data(data: str):
    # the url and port of the ICSHTTP Simple Server:
    url = 'http://localhost:8000'

    # create some data to send, we'll use json format
    json = {'data': data}

    # properly encode the data for the request object
    data = urllib.parse.urlencode(json)
    data = data.encode('utf-8')

    # set a header, with content type. We don't need to specify user agent here
    # since we are just sending to a custom server
    headers = {'content-type': 'application/json'}
    req = urllib.request.Request(url, data, headers)

    # make the call, and print the response
    with urllib.request.urlopen(req) as response:
        resp = response.read()
        print(resp)


if __name__ == '__main__':
    while True:
        send_data(input("What would you like to send? "))