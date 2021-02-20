#!/usr/bin/env python3

import json
from twitter import Twitter, OAuth
import sys


def post(path):
    keys = json.load(open('twitterapi.json', 'r'))
    api_key = keys["API_key"]
    api_key_secret = keys["API_key_secret"]
    bearer_token = keys["Bearer_token"]
    access_token = keys["Access_token"]
    access_token_secret = keys["Access_token_secret"]

    t = Twitter(auth=OAuth(access_token, access_token_secret, api_key, api_key_secret))
    # statusUpdate = t.statuses.update(status="Test from API")
    with open(path, "rb") as imagefile:
        imagedata = imagefile.read()
    params = {"media[]": imagedata, "status": "PTT ★"}
    t.statuses.update_with_media(**params)

if __name__ == '__main__':
    if len(sys.argv) > 1:
        post(sys.argv[1])
    else:
        print("You'll have to specify the directory.")
