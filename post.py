#!/usr/bin/env python3

import json
from twitter import Twitter, OAuth
import sys
import os


def post(path):
    filename = f"{path}.mp4"
    keys = json.load(open('twitterapi.json', 'r'))
    api_key = keys["API_key"]
    api_key_secret = keys["API_key_secret"]
    bearer_token = keys["Bearer_token"]
    access_token = keys["Access_token"]
    access_token_secret = keys["Access_token_secret"]

    fd = os.path.basename(filename).split('.')[0]
    y = fd[0:4]
    m = fd[4:6]
    d = fd[6:8]
    h = fd[8:10]
    min = fd[10:12]
    s = fd[12:14]
    print(f"{y}年{m}月{d}日 {h}:{min}:{s}")

    t = Twitter(auth=OAuth(access_token, access_token_secret, api_key, api_key_secret))
    # statusUpdate = t.statuses.update(status="Test from API")
    with open(filename, "rb") as imagefile:
        imagedata = imagefile.read()
    params = {"media[]": imagedata, "status": f"{y}年{m}月{d}日 {h}:{min}:{s} に発生した地震です。 データ: http://www.kmoni.bosai.go.jp/"}
    t.statuses.update_with_media(**params)

if __name__ == '__main__':
    if len(sys.argv) > 1:
        post(sys.argv[1])
    else:
        print("You'll have to specify the directory.")
