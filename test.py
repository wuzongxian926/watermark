import os

__author__ = 'zhangxulong'
def combine_video(dir="temp"):
    for parent, dirname, filename in os.walk(dir):
        for file in filename:
            print file

    return 0
combine_video('out')