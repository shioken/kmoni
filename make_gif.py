#!/usr/bin/env python3

from PIL import Image
import glob
import re
import os
import sys

def make_gif(path):
    files = sorted(glob.glob(f'capture/{path}/*.png'), key=os.path.getctime)

    # print(files)
    images = list(map(lambda file: Image.open(file).crop((0, 108, 365, 605)), files))
    images[0].save(f"capture/{path}/{path}.gif", save_all=True, append_images=images[1:], duration=100, loop=0)

if __name__ == '__main__':
    if len(sys.argv) > 1:
        make_gif(sys.argv[1])
    else:
        print("You'll have to specify the directory.")