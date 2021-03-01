#!/usr/bin/env python3

import sys
import cv2
import glob
import os

def make_mp4(path):
    img_array = []
    for filename in sorted(glob.glob('ring/*.png'), key=os.path.getmtime):
        img = cv2.imread(filename)
        crop_image = img[135:605, 0:365]
        height, width, layers = crop_image.shape
        size = (width, height)
        img_array.append(crop_image)

    for filename in sorted(glob.glob(f'capture/{path}/*.png'), key=os.path.getctime):
        img = cv2.imread(filename)
        crop_image = img[135:605, 0:365]
        height, width, layers = crop_image.shape
        size = (width, height)
        img_array.append(crop_image)

    outfile = f"{path}.mp4" # パス指定はできない
    video = cv2.VideoWriter(outfile, cv2.VideoWriter_fourcc(*'mp4v'), 10.0, size)

    for img in img_array:
        video.write(img)
    video.release()

if __name__ == "__main__":
    if len(sys.argv) > 1:
        make_mp4(sys.argv[1])
    else:
        print("You'll have to specify the directory.")
