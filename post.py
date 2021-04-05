#!/usr/bin/env python3

import json
import tweepy
import sys
import os


def post(path, area, mag, sindo):
    print(f"{path}, {area}, {mag}, {sindo}")
    filename = f"output/{path}.gif"
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


    # Twitterオブジェクトの生成
    auth = tweepy.OAuthHandler(api_key, api_key_secret)
    auth.set_access_token(access_token, access_token_secret)

    api = tweepy.API(auth)

    media_ids = []
    res = api.media_upload(filename)
    media_ids.append(res.media_id)
    
    api.update_status(
        status=f"{y}年{m}月{d}日 {h}:{min}:{s} に{area}で発生した地震(マグニチュード{mag}, 震度{sindo})です。 強震モニタ: http://www.kmoni.bosai.go.jp/", media_ids=media_ids)

if __name__ == '__main__':
    if len(sys.argv) > 3:
        post(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4])
    else:
        print("You'll have to specify the directory.")
