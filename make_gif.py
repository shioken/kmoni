#!/usr/bin/env python3

from PIL import Image
import glob
import re
import os

def cmp_seq(a, b):
    ax = re.split('[_.]', a)
    bx = re.split('[_.]', b)
    print(ax)
    print(bx)
    return 0

files = sorted(glob.glob('capture/eq_1_*.png'), key=os.path.getctime)
# files = glob.glob('capture/eq_1_*.png')

print(files)
# images = list(map(lambda file: Image.open(file), files))
# images[0].save('eq1.gif', save_all=True, append_images=images[1:], duration=500, loop=0)