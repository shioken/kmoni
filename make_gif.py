#!/usr/bin/env python3

from PIL import Image
import glob
import re
import os
import sys

def make_gif(path):
    ring_files = sorted(glob.glob('ring/*.png'), key=os.path.getmtime)
    print(f"ring files: {ring_files}")
    ring_images = list(map(lambda file: Image.open(file).crop((0, 108, 365, 605)), ring_files))

    files = sorted(glob.glob(f'capture/{path}/*.png'), key=os.path.getctime)
    images = list(map(lambda file: Image.open(file).crop((0, 108, 365, 605)), files))

    ring_images.extend(images)
    ring_images[0].save(f"capture/{path}/{path}.gif", save_all=True, append_images=ring_images[1:], duration=200, loop=1, optimize=True)

    print("save gif: done")

if __name__ == '__main__':
    if len(sys.argv) > 1:
        make_gif(sys.argv[1])
    else:
        print("You'll have to specify the directory.")